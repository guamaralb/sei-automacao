from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def acessar_pagina_trocar_unidade(driver: webdriver.Chrome):
    a_trocar_unidade = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "lnkInfraUnidade"))
    )
    driver.execute_script("arguments[0].click();", a_trocar_unidade)


def selecionar_unidade(driver: webdriver.Chrome, unidade: str):
    td_unid = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{unidade}')]"))
    )
    td_unid.click()