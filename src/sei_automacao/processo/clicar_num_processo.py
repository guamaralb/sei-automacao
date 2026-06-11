from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clicar_num_processo(driver: webdriver.Remote, num_processo: str) -> None:
    span_num_processo: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{num_processo}')]"))
    )
    span_num_processo.click()
