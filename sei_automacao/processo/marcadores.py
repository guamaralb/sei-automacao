from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def clicar_img_gerenciar_marcadores(driver: webdriver.Remote) -> None:
    img_gerenciar_marcadores: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='Gerenciar Marcador']"))
    )
    img_gerenciar_marcadores.click()


def procurar_sbmSalvar(driver: webdriver.Remote) -> bool:
    button_smbSalvar: list[WebElement] = driver.find_elements(By.ID, "sbmSalvar")
    return bool(button_smbSalvar)


def selecionar_marcador(driver: webdriver.Remote, marcador: str) -> None:
    dropdown: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#selMarcador .dd-select"))
    )
    dropdown.click()

    opcao_planilhado: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//label[@class='dd-option-text' and normalize-space(text())='{marcador}']"))
    )
    opcao_planilhado.click()
