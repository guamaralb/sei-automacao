from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException


def clicar_img_concluir_processo(driver: webdriver.Remote) -> None:
    for i in range(3):
        try:
            img_concluir_processo: WebElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Concluir Processo']"))
            )
            img_concluir_processo.click()
            return

        except StaleElementReferenceException:
            print(f"Clique na img_concluir_processo ficou stale na tentativa {i}. Tentando novamente...")

    raise Exception("Elemento img_concluir_processo ficou stale após 3 tentativas")
