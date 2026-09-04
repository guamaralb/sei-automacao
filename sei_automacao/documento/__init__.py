from selenium import webdriver
import time

from sei_automacao.documento.gestao import (
    selecionar_cancelar_doc,
    preencher_motivo_cancelamento,
    selecionar_excluir_doc,
    confirmar_exclusao_doc,
)
from sei_automacao.documento.assinatura import (
    selecionar_inserir_bloco_ass,
    seleciona_bloco_ass,
)
from sei_automacao.core.buttons import clicar_salvar_sbmSalvar, clicar_incluir_sbmIncluir
from sei_automacao.core.iframes import trocar_iframe


def cancelar_doc(
    driver: webdriver.Remote,
    motivo: str
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_cancelar_doc(driver)
    preencher_motivo_cancelamento(driver, motivo)
    clicar_salvar_sbmSalvar(driver)
    driver.switch_to.default_content()


def excluir_doc(
    driver: webdriver.Remote
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_excluir_doc(driver)
    confirmar_exclusao_doc(driver)
    driver.switch_to.default_content()


def inserir_bloco_ass(
    driver: webdriver.Remote,
    num_bloco: str
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    selecionar_inserir_bloco_ass(driver)
    trocar_iframe(driver, 'ifrVisualizacao')
    seleciona_bloco_ass(driver, num_bloco)
    clicar_incluir_sbmIncluir(driver)
    time.sleep(2)
    driver.switch_to.default_content()

import time
import os

from pathlib import Path
from typing import Literal

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.utils.acesso import selecionar_nivel_acesso
from sei_automacao.core.iframes import trocar_iframe


def obter_conteudo_doc(driver: webdriver.Remote, formato: Literal['web_element', 'texto'] = 'texto') -> str | WebElement:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    trocar_iframe(driver, 'ifrVisualizacao')

    body = driver.find_element(By.TAG_NAME, 'body')

    texto = body.text

    if formato == 'html':
        return body
    elif formato == 'texto':
        return texto




