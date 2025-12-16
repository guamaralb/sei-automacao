from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clicar_num_processo(driver: webdriver.Chrome, num_processo: str):
    span_num_processo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{num_processo}')]"))
    )
    span_num_processo.click()
