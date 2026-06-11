from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
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
