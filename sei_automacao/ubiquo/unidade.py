from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def acessar_pagina_trocar_unidade(driver: webdriver.Remote) -> None:
    a_trocar_unidade: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "lnkInfraUnidade"))
    )
    driver.execute_script("arguments[0].click();", a_trocar_unidade)


def selecionar_unidade(driver: webdriver.Remote, unidade: str) -> None:
    td_unid: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{unidade}')]"))
    )
    td_unid.click()
