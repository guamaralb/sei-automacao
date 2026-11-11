from selenium import webdriver
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


def selecionar_unidade(
    driver: webdriver.Remote,
    unidade: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    td_unid: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f'//td[contains(text(), {xpath_literal(unidade)})]',
        ))
    )
    td_unid.click()
