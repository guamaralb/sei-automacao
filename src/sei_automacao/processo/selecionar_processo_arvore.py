from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def selecionar_processo_arvore(driver: webdriver.Chrome, num_processo: str):
    span_processo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{num_processo}')]"))
    )
    span_processo.click()
