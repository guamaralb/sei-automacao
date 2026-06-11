from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def capturar_num_processo(driver: webdriver.Remote) -> str:
    span_num_processo: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='infraArvoreNoSelecionado']"))
    )
    num_processo: str = span_num_processo.text

    return num_processo
