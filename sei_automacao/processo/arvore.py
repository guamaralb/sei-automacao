import time
import os
import re
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

    arvore_elements = driver.find_elements(
        By.XPATH, '//div[@class="infraArvore"]/a/span'
    )

    if len(arvore_elements) % 2 != 1:
        raise Exception(
            'Identificado um número inconsistente de itens na arvore'
        )

    arvore_list: list[dict] = []

    # O find_elements encontra também o numero do processo, por isso deve ser
    # pulado o primeiro item da lista
    for i in range(1, len(arvore_elements), 2):
        item_text_and_num = arvore_elements[i].text

        item_num_com_parenteses = item_text_and_num.split(' ')[-1]
        item_num = item_num_com_parenteses.strip('()')

        item_text = item_text_and_num.removesuffix(f' {item_num_com_parenteses}')

        item_unidade = arvore_elements[i + 1].text

        item = {
            'numero_sei': item_num,
            'nome_arvore': item_text,
            'unidade': item_unidade
        }

        arvore_list.append(item)

    return arvore_list


def selecionar_doc_arvore(
    driver: webdriver.Remote,
    numero_sei: str | None = None,
    nome: str | None = None
) -> None:
    if numero_sei is None and nome is None:
        raise Exception('Nenhum termo inserido para busca')

    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')

    doc_element: WebElement = None

    try:
        doc_element = driver.find_element(
            By.XPATH,
            f'//a[span[contains(text(), "{numero_sei}")]]'
        )

    except:
        try:
            doc_element = driver.find_element(
                By.XPATH,
                f'//a[span[contains(text(), "{nome}")]]'
            )

        except:
            raise Exception('Documento não encontrado')

    doc_element.click()

    # Espera o iFrame do documento em si carregar
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    trocar_iframe(driver, 'ifrVisualizacao')

    driver.switch_to.default_content()


def clicar_num_processo(driver: webdriver.Remote) -> None:
    driver.switch_to.default_content()

    trocar_iframe(driver=driver, iframe='ifrArvore')

    padrao_processo = r"\d{4}\.\d{2}\.\d{7}/\d{4}-\d{2}"

    spans: list[WebElement] = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="infraArvore"]/a/span')
        )
    )

    span_num_processo = next(
        (
            span
            for span in spans
            if re.search(padrao_processo, span.text)
        ),
        None
    )

    if span_num_processo is None:
        raise ValueError(
            "Nenhum número de processo encontrado no padrão informado."
        )

    span_num_processo.click()

    driver.switch_to.default_content()