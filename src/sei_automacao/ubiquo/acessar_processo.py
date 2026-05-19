from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def acessar_processo(driver: webdriver.Chrome, num_processo: str):
    input_pesquisa = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'txtPesquisaRapida'))
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        input_pesquisa,
        num_processo
    )
    input_pesquisa.submit()    
