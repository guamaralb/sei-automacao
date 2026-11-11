import logging
from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import (
    TIMEOUT_PADRAO,
    TIMEOUT_SONDAGEM,
    xpath_literal,
)
from sei_automacao.exceptions import ElementoNaoEncontrado, IframeNaoEncontrado

logger = logging.getLogger(__name__)

TipoBusca = Literal['id', 'name', 'xpath']


def localizar_xpath_elemento_com_fallback_iframe(
    driver: webdriver.Remote,
    nome_iframe: str,
    xpath_elemento: str,
    tipo_busca: TipoBusca | None = None,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> WebElement:
    """
    Tenta localizar `xpath_elemento` dentro do iframe chamado `nome_iframe`.
    Se o iframe nomeado não existir ou o elemento não aparecer nele,
    varre todos os iframes da página procurando o elemento.

    Ao final, o driver fica posicionado no iframe onde o elemento foi
    encontrado (não retorna para o default_content automaticamente).
    """
    try:
        trocar_iframe(driver, nome_iframe, tipo_busca, timeout=timeout)
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath_elemento))
        )
    except (TimeoutException, NoSuchElementException, IframeNaoEncontrado):
        logger.warning(
            "Iframe '%s' não encontrado ou elemento ausente nele; buscando "
            "'%s' em todos os iframes da página.",
            nome_iframe,
            xpath_elemento,
        )

    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    for iframe in iframes:
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(iframe)
        except WebDriverException:
            continue

        try:
            element = WebDriverWait(driver, TIMEOUT_SONDAGEM).until(
                EC.presence_of_element_located((By.XPATH, xpath_elemento))
            )
            logger.debug(
                "Elemento encontrado no iframe '%s'",
                iframe.get_attribute('name') or iframe.get_attribute('id'),
            )
            return element
        except TimeoutException:
            continue

    driver.switch_to.default_content()
    raise ElementoNaoEncontrado(
        f"Elemento '{xpath_elemento}' não encontrado em nenhum iframe "
        f"(nem no nomeado '{nome_iframe}', nem na busca em todos os iframes)."
    )


def trocar_iframe(
    driver: webdriver.Remote,
    iframe: str,
    tipo_busca: TipoBusca | None = None,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    """Entra no iframe procurando por id, name e title ao mesmo tempo (ou só
    por ``tipo_busca``). Espera até ``timeout`` pelo primeiro que aparecer."""
    estrategias: dict[TipoBusca, tuple[str, str]] = {
        'id': (By.ID, iframe),
        'name': (By.NAME, iframe),
        'xpath': (By.XPATH, f'//iframe[@title={xpath_literal(iframe)}]'),
    }

    ordem = [tipo_busca] if tipo_busca else list(estrategias)

    try:
        WebDriverWait(driver, timeout).until(
            EC.any_of(
                *(
                    EC.frame_to_be_available_and_switch_to_it(
                        estrategias[tipo]
                    )
                    for tipo in ordem
                )
            )
        )
    except TimeoutException:
        raise IframeNaoEncontrado(
            f'iFrame "{iframe}" não encontrado por: {", ".join(ordem)}'
        ) from None
