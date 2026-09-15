import time
from typing import Literal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from sei_automacao.core.buttons import (
    clicar_incluir_sbmIncluir,
    clicar_salvar_sbmSalvar,
)
from sei_automacao.core.iframes import trocar_iframe
from sei_automacao.documento.assinatura import (
    seleciona_bloco_ass,
    selecionar_inserir_bloco_ass,
)
from sei_automacao.documento.gestao import (
    confirmar_exclusao_doc,
    preencher_motivo_cancelamento,
    selecionar_cancelar_doc,
    selecionar_excluir_doc,
)
from sei_automacao.utils.acesso import (
    selecionar_nivel_acesso as selecionar_nivel_acesso,
)


def cancelar_doc(driver: webdriver.Remote, motivo: str) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_cancelar_doc(driver)
    preencher_motivo_cancelamento(driver, motivo)
    clicar_salvar_sbmSalvar(driver)
    driver.switch_to.default_content()


def excluir_doc(driver: webdriver.Remote) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_excluir_doc(driver)
    confirmar_exclusao_doc(driver)
    driver.switch_to.default_content()


def inserir_bloco_ass(driver: webdriver.Remote, num_bloco: str) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    selecionar_inserir_bloco_ass(driver)
    trocar_iframe(driver, 'ifrVisualizacao')
    seleciona_bloco_ass(driver, num_bloco)
    clicar_incluir_sbmIncluir(driver)
    time.sleep(2)
    driver.switch_to.default_content()


def obter_conteudo_doc(
    driver: webdriver.Remote,
    formato: Literal['web_element', 'texto'] = 'texto',
) -> str | WebElement:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    trocar_iframe(driver, 'ifrVisualizacao')

    body = driver.find_element(By.TAG_NAME, 'body')

    texto = body.text

    if formato == 'web_element':
        return body
    elif formato == 'texto':
        return texto
