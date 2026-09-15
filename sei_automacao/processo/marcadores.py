from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep

def clicar_img_gerenciar_marcadores(driver: webdriver.Remote) -> None:
    a_gerenciar_marcadores: WebElement = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Gerenciar Marcador']/ancestor::a[1]"))
    )
    a_gerenciar_marcadores.click()

    # Esperar mudar para a página de "Adicionar Marcador"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h1[contains(normalize-space(), 'Adicionar Marcador')]"))
    )


def procurar_sbmSalvar(driver: webdriver.Remote) -> bool:
    button_smbSalvar: list[WebElement] = driver.find_elements(By.ID, "sbmSalvar")
    return bool(button_smbSalvar)


def selecionar_marcador(driver: webdriver.Remote, marcador: str) -> None:
    dropdown: WebElement = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#selMarcador .dd-select"))
    )
    dropdown.click()

    opcao_planilhado: WebElement = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//label[@class='dd-option-text' and normalize-space(text())='{marcador}']"))
    )
    opcao_planilhado.click()

    # Esperar o selecionado aparecer
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//label[@class='dd-selected-text' and normalize-space(text())='{marcador}']"))
    )


def esperar_marcador_aparecer_apos_salvar(driver: webdriver.Remote, marcador: str) -> None:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//tbody/tr/td[contains(normalize-space(.), "{marcador}")]'))
        )
    except Exception:
        raise ValueError(
            f'Marcador "{marcador}" não encontrado após salvar'
        )