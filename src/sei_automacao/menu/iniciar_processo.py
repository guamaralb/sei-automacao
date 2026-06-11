import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clicar_iniciar_processo(driver: webdriver.Remote) -> None:
    for index in range(3):
        try:
            span_iniciar_processo: WebElement = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Iniciar Processo')]"))
            )
            span_iniciar_processo.click()

            # Espera a página mudar
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Escolha o Tipo do Processo:')]"))
            )
            return

        except Exception as e:
            print(f"Falha na tentativa {index+1}/3 de iniciar processo: {type(e).__name__} -> {e}")
            time.sleep(2)

    raise Exception("Falha ao clicar em 'Iniciar Processo' após várias tentativas")


def selecionar_tipo_processo(driver: webdriver.Remote, tipo_processo: str) -> None:
    a_exibir_todos_tipos_processo: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "ancExibirTiposProcedimento"))
    )
    a_exibir_todos_tipos_processo.click()

    for _ in range(3):
        try:
            a_tipo_processo: WebElement = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space(text())='{tipo_processo}']"))
            )
            a_tipo_processo.click()
            return

        except Exception:
            time.sleep(1)


def preencher_especificacao_processo(driver: webdriver.Remote, especificacao: str) -> None:
    input_espec: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'txtDescricao'))
    )
    input_espec.send_keys(especificacao)
