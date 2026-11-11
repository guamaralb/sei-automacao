import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO


def clicar_enviar_processo(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    img_enviar_processo: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Enviar Processo']"))
    )
    img_enviar_processo.click()


def preencher_unidade(
    driver: webdriver.Remote,
    unidade: str,
    desce_lista: int = 1,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    input_unidade: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, 'txtUnidade'))
    )
    input_unidade.send_keys(unidade)
    time.sleep(1)

    for _ in range(desce_lista):
        input_unidade.send_keys(Keys.DOWN)

    input_unidade.send_keys(Keys.ENTER)


def selecionar_manter_aberto(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    label: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "label[for='chkSinManterAberto']",
        ))
    )
    label.click()
