import logging
from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO
from sei_automacao.exceptions import AcaoNaoConcluida, OpcaoNaoSuportada

logger = logging.getLogger(__name__)

NivelAcesso = Literal['Restrito', 'Público', 'Sigiloso']

# A lista de hipóteses legais carrega depois de escolher o nível de acesso
_TIMEOUT_MIN_HIPOTESE_LEGAL: float = 15

_IDS_NIVEL_ACESSO: dict[str, str] = {
    'Restrito': 'divOptRestrito',
    'Público': 'divOptPublico',
    'Sigiloso': 'divOptSigiloso',
}


def selecionar_nivel_acesso(
    driver: webdriver.Remote,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str | None = '',
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    try:
        id_nivel_acesso = _IDS_NIVEL_ACESSO[nivel_acesso]
    except KeyError:
        raise OpcaoNaoSuportada(
            f"Nivel de acesso '{nivel_acesso}' inexistente ou não implementado"
        ) from None

    for _ in range(5):
        try:
            input_nivel_acesso: WebElement = WebDriverWait(
                driver, timeout
            ).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//*[@id='{id_nivel_acesso}']/div/label",
                ))
            )
            input_nivel_acesso.click()
            break
        except StaleElementReferenceException:
            logger.debug(
                'Elemento ficou stale ao selecionar o nivel de acesso; '
                'tentando novamente'
            )
    else:
        raise AcaoNaoConcluida(
            'Não foi possível selecionar o nivel de acesso após '
            'várias tentativas (stale repetido).'
        )

    if nivel_acesso == 'Público':
        return

    if not hipotese_legal:
        raise OpcaoNaoSuportada(
            f'Hipotese Legal obrigatória para nível de acesso {nivel_acesso}'
        )

    WebDriverWait(driver, max(timeout, _TIMEOUT_MIN_HIPOTESE_LEGAL)).until(
        lambda d: (
            len(Select(d.find_element(By.ID, 'selHipoteseLegal')).options) > 1
        )
    )

    for _ in range(5):
        try:
            select_hip_legal = Select(
                driver.find_element(By.ID, 'selHipoteseLegal')
            )
            select_hip_legal.select_by_visible_text(hipotese_legal)
            break
        except StaleElementReferenceException:
            logger.debug(
                'Elemento ficou stale ao selecionar a hipotese legal; '
                'tentando novamente'
            )
    else:
        raise AcaoNaoConcluida(
            'Não foi possível selecionar a hipotese legal após '
            'várias tentativas (stale repetido).'
        )
