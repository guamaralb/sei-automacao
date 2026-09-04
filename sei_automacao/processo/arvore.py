import time
import os

from pathlib import Path

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.utils.acesso import selecionar_nivel_acesso
from sei_automacao.core.iframes import trocar_iframe


def listar_documentos_arvore(driver: webdriver.Remote) -> list[dict]:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')

    arvore_itens_elements = driver.find_elements(
        By.XPATH, '//div[@class="infraArvore"]/a/span'
    )

    if len(arvore_itens_elements) % 2 != 1:
        raise Exception(
            'Identificado um número inconsistente de itens na arvore'
        )

    arvore_list: list[dict] = []

    # O find_elements encontra também o numero do processo, por isso deve ser
    # pulado o primeiro item da lista
    for i in range(1, len(arvore_itens_elements), 2):
        item_text_and_num = arvore_itens_elements[i].text

        item_num_com_parenteses = item_text_and_num.split(' ')[-1]
        item_num = item_num_com_parenteses.strip('()')

        item_text = item_text_and_num.removesuffix(f' {item_num_com_parenteses}')

        item_unidade = arvore_itens_elements[i + 1].text

        item = {
            'num': item_num,
            'text': item_text,
            'unidade': item_unidade
        }

        arvore_list.append(item)

    return arvore_list