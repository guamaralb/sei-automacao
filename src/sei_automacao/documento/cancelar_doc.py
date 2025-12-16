from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def selecionar_cancelar_doc(driver: webdriver.Chrome):
    img_cancelar_doc = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Cancelar Documento']"))
    )
    img_cancelar_doc.click()
    

def preencher_motivo_cancelamento(driver: webdriver.Chrome, motivo: str):
    input_motivo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "txaMotivo"))
    )
    input_motivo.send_keys(motivo)