import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clicar_enviar_processo(driver: webdriver.Chrome):
    img_enviar_processo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Enviar Processo']"))
    )
    img_enviar_processo.click()
    

def preencher_unidade(driver: webdriver.Chrome, unidade: str, desce_lista: int = 1):
    input_unidade = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "txtUnidade"))
    )
    input_unidade.send_keys(unidade)
    time.sleep(1)
    
    for i in range(desce_lista):
        input_unidade.send_keys(Keys.DOWN)
    
    input_unidade.send_keys(Keys.ENTER)


def selecionar_manter_aberto(driver: webdriver.Chrome):
    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='chkSinManterAberto']"))
    )
    label.click()
