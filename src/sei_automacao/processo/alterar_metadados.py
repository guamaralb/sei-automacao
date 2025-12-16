from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def abrir_metadados_processo(driver: webdriver.Chrome):
    img_metadados_processo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Consultar/Alterar Processo']"))
    )
    img_metadados_processo.click()


def alterar_especificacao_processo(driver: webdriver.Chrome, novo_nome: str):
    input_espec = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "txtDescricao"))
    )
    input_espec.clear()
    input_espec.send_keys(novo_nome)



