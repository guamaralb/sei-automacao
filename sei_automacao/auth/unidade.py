from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def selecionar_unidade(driver: webdriver.Remote, unidade: str) -> None:
    a_trocar_unidade: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "lnkInfraUnidade"))
    )
    driver.execute_script("arguments[0].click();", a_trocar_unidade)

    td_unid: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{unidade}')]"))
    )
    td_unid.click()
