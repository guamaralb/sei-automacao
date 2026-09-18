import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def acessar_processo(driver: webdriver.Remote, num_processo: str) -> None:
    driver.switch_to.default_content()

    try:
        input_pesquisa: WebElement = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'txtPesquisaRapida'))
        )
    except TimeoutException:
        logging.error(f'[{num_processo}] URL atual: {driver.current_url}')
        logging.error(f'[{num_processo}] Título: {driver.title}')
        logging.error(
            f'[{num_processo}] Janelas abertas: {driver.window_handles}'
        )
        driver.save_screenshot(f'debug_{num_processo.replace("/", "_")}.png')
        raise

    driver.execute_script(
        'arguments[0].value = arguments[1];', input_pesquisa, num_processo
    )
    input_pesquisa.submit()

    iframe_opcoes_processo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ifrConteudoVisualizacao'))
    )
    iframe_opcoes_processo.is_displayed()
