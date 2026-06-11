from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def clicar_salvar_btnSalvar(driver: webdriver.Remote) -> None:
    button_salvar: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "btnSalvar"))
    )
    button_salvar.click()


def clicar_salvar_sbmSalvar(driver: webdriver.Remote) -> None:
    button_salvar: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "sbmSalvar"))
    )
    button_salvar.click()


def clicar_incluir_sbmIncluir(driver: webdriver.Remote) -> None:
    button_salvar: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "sbmIncluir"))
    )
    button_salvar.click()


def clicar_adicionar_btnAdicionar(driver: webdriver.Remote) -> None:
    button_adicionar: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "btnAdicionar"))
    )
    button_adicionar.click()


def clicar_enviar_sbmEnviar(driver: webdriver.Remote) -> None:
    button_adicionar: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "sbmEnviar"))
    )
    button_adicionar.click()


def clicar_enviar_btnEnviar(driver: webdriver.Remote) -> None:
    button_adicionar: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@name='btnEnviar']"))
    )
    button_adicionar.click()
