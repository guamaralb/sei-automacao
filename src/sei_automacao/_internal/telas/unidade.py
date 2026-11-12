from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO, xpath_literal


def acessar_pagina_trocar_unidade(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    a_trocar_unidade: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'lnkInfraUnidade'))
    )
    driver.execute_script('arguments[0].click();', a_trocar_unidade)


def item_esta_marcado(
    driver: webdriver.Remote,
    unidade: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> bool:
    """Diz se a unidade já está marcada na lista de troca de unidade."""
    xpath_linha = f'//tr[td[normalize-space()={xpath_literal(unidade)}]]'

    try:
        linha: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath_linha))
        )
    except TimeoutException:
        return False  # linha não encontrada

    checkbox = linha.find_element(
        By.XPATH, ".//input[@type='radio' or @type='checkbox']"
    )
    return checkbox.is_selected()


def selecionar_unidade(
    driver: webdriver.Remote,
    unidade: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    if item_esta_marcado(driver, unidade, timeout=timeout):
        return

    td_unid: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f'//td[contains(text(), {xpath_literal(unidade)})]',
        ))
    )
    td_unid.click()
    esperar_pagina_carregada(driver, timeout=timeout)


def esperar_pagina_carregada(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    """Espera a página atual terminar de carregar e mostrar a pesquisa
    rápida."""
    espera = WebDriverWait(driver, timeout, poll_frequency=0.1)
    espera.until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    espera.until(EC.element_to_be_clickable((By.ID, 'txtPesquisaRapida')))
