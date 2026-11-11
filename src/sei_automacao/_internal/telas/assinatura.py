from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO
from sei_automacao.exceptions import OpcaoNaoSuportada


def selecionar_inserir_bloco_ass(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    a_bloco_ass: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//img[@alt='Incluir em Bloco de Assinatura']/ancestor::a[1]",
        ))
    )
    a_bloco_ass.click()

    driver.switch_to.frame('ifrVisualizacao')

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div/h1[contains(text(), 'Incluir em Bloco de Assinatura')]",
        ))
    )

    driver.switch_to.default_content()


def seleciona_bloco_ass(driver: webdriver.Remote, num_bloco: str) -> None:
    num_bloco = str(num_bloco)
    try:
        select_bloco_ass: Select = Select(
            driver.find_element(By.ID, 'selBloco')
        )
        select_bloco_ass.select_by_value(num_bloco)
    except WebDriverException as e:
        raise OpcaoNaoSuportada(
            f'Bloco de Assinatura "{num_bloco}" não encontrado'
        ) from e
