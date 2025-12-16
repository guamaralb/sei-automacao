from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def selecionar_unidade(driver: webdriver.Chrome, unidade: str):
    # Seleciona o campo de trocar de unidade
    a_trocar_unidade = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "lnkInfraUnidade"))
    )
    driver.execute_script("arguments[0].click();", a_trocar_unidade)
    
    # Seleciona a unidade
    td_unid = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{unidade}')]"))
    )
    td_unid.click()
