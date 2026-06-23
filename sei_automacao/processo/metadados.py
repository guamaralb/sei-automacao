from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def abrir_metadados_processo(driver: webdriver.Remote) -> None:
    img_metadados_processo: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Consultar/Alterar Processo']"))
    )
    img_metadados_processo.click()


def alterar_especificacao_processo(driver: webdriver.Remote, novo_nome: str) -> None:
    input_espec: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "txtDescricao"))
    )
    input_espec.clear()
    input_espec.send_keys(novo_nome)


def capturar_num_processo(driver: webdriver.Remote) -> str:
    span_num_processo: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='infraArvoreNoSelecionado']"))
    )
    return span_num_processo.text
