from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def clicar_img_gerenciar_marcadores(driver):
    img_gerenciar_marcadores = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='Gerenciar Marcador']"))
    )
    img_gerenciar_marcadores.click()


def procurar_sbmSalvar(driver: webdriver.Chrome):
    button_smbSalvar = driver.find_elements(By.ID, "sbmSalvar")
    
    if button_smbSalvar:
        return True
    else:
        return False


def selecionar_marcador(driver, marcador):
    dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#selMarcador .dd-select"))
    )
    dropdown.click()  

    opcao_planilhado = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//label[@class='dd-option-text' and normalize-space(text())='{marcador}']"))
    )
    opcao_planilhado.click()

