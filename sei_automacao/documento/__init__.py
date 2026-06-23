from selenium import webdriver

from sei_automacao.documento.gestao import (
    selecionar_cancelar_doc,
    preencher_motivo_cancelamento,
    selecionar_excluir_doc,
    confirmar_exclusao_doc,
)
from sei_automacao.documento.assinatura import selecionar_inserir_bloco_ass, seleciona_bloco_ass
from sei_automacao.core.buttons import clicar_salvar_sbmSalvar, clicar_incluir_sbmIncluir
from sei_automacao.core.iframes import trocar_iframe


def cancelar_doc(
    driver: webdriver.Remote,
    motivo: str
) -> None:
    selecionar_cancelar_doc(driver)
    preencher_motivo_cancelamento(driver, motivo)
    clicar_salvar_sbmSalvar(driver)


def excluir_doc(
    driver: webdriver.Remote
) -> None:
    selecionar_excluir_doc(driver)
    confirmar_exclusao_doc(driver)


def inserir_bloco_ass(
    driver: webdriver.Remote,
    num_bloco: str
) -> None:
    selecionar_inserir_bloco_ass(driver)
    trocar_iframe(driver, "ifrVisualizacao")
    seleciona_bloco_ass(driver, num_bloco)
    clicar_incluir_sbmIncluir(driver)
