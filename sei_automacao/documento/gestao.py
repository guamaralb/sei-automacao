from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement


def selecionar_cancelar_doc(driver: webdriver.Remote) -> None:
    img_cancelar_doc: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Cancelar Documento']"))
    )
    img_cancelar_doc.click()


def preencher_motivo_cancelamento(driver: webdriver.Remote, motivo: str) -> None:
    input_motivo: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "txaMotivo"))
    )
    input_motivo.send_keys(motivo)


def selecionar_excluir_doc(driver: webdriver.Remote) -> None:
    img_excluir_doc: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Excluir']"))
    )
    img_excluir_doc.click()


def confirmar_exclusao_doc(driver: webdriver.Remote) -> None:
    alerta: Alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alerta.accept()
