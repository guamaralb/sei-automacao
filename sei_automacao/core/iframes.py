import logging
from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TipoBusca = Literal['id', 'name', 'xpath']


def localizar_xpath_elemento_com_fallback_iframe(
    driver: webdriver.Remote,
    nome_iframe: str,
    xpath_elemento: str,
    tipo_busca: TipoBusca | None = None,
    timeout_nomeado: int = 10,
    timeout_fallback: int = 3,
) -> WebElement:
    """
    Tenta localizar `xpath_elemento` dentro do iframe chamado `nome_iframe`.
    Se o iframe nomeado não existir ou o elemento não aparecer nele,
    varre todos os iframes da página procurando o elemento.

    Ao final, o driver fica posicionado no iframe onde o elemento foi
    encontrado (não retorna para o default_content automaticamente).
    """
    try:
        trocar_iframe(driver, nome_iframe, tipo_busca)
        return WebDriverWait(driver, timeout_nomeado).until(
            EC.presence_of_element_located((By.XPATH, xpath_elemento))
        )
    except (TimeoutException, NoSuchElementException):
        print("Não conseguiu achar o ifram, tentando achar o elemento em todos os iframes")
        logging.warning(
            f"Iframe nomeado '{nome_iframe}' não encontrado ou elemento "
            f"ausente nele; buscando '{xpath_elemento}' em todos os "
            'iframes da página.'
        )

    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    print('PROCURANDO:', xpath_elemento)
    for iframe in iframes:
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(iframe)
            print(
                'Alterado para iframe:',
                iframe.get_attribute('name') or iframe.get_attribute('id'),
            )
        except Exception:
            continue

        try:
            element = WebDriverWait(driver, timeout_fallback).until(
                EC.presence_of_element_located((By.XPATH, xpath_elemento))
            )
            print('ACHOU')
            return element
        except TimeoutException:
            print('NÃO ACHOU')
            continue

    driver.switch_to.default_content()
    raise NoSuchElementException(
        f"Elemento '{xpath_elemento}' não encontrado em nenhum iframe "
        f"(nem no nomeado '{nome_iframe}', nem na busca em todos os iframes)."
    )


def trocar_iframe(
    driver: webdriver.Remote,
    iframe: str,
    tipo_busca: TipoBusca | None = None,
    timeout: float = 1,
) -> None:
    estrategias: dict[TipoBusca, tuple[str, str]] = {
        'id': (By.ID, iframe),
        'name': (By.NAME, iframe),
        'xpath': (By.XPATH, f'//iframe[@title="{iframe}"]'),
    }

    ordem = [tipo_busca] if tipo_busca else ['id', 'name', 'xpath']

    for tipo in ordem:
        try:
            WebDriverWait(driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(estrategias[tipo])
            )
            return
        except TimeoutException:
            continue

    tentativas = tipo_busca or ', '.join(estrategias)
    raise ValueError(f'iFrame "{iframe}" não encontrado por: {tentativas}')
