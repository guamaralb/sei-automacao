from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def selecionar_inserir_bloco_ass(driver: webdriver.Remote) -> None:
    img_bloco_ass: WebElement = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//img[@alt='Incluir em Bloco de Assinatura']",
        ))
    )
    img_bloco_ass.click()


def seleciona_bloco_ass(driver: webdriver.Remote, num_bloco: str) -> None:
    select_bloco_ass: Select = Select(driver.find_element(By.ID, 'selBloco'))
    select_bloco_ass.select_by_value(num_bloco)
