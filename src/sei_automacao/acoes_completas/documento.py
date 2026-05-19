from sei_automacao.documento.cancelar_doc import selecionar_cancelar_doc, preencher_motivo_cancelamento
from sei_automacao.documento.excluir_doc import selecionar_excluir_doc, confirmar_exclusao_doc
from sei_automacao.documento.inserir_bloco_ass import selecionar_inserir_bloco_ass, seleciona_bloco_ass
from sei_automacao.genericos.botoes import clicar_salvar_sbmSalvar, clicar_incluir_sbmIncluir
from selenium import webdriver
from sei_automacao.utils.trocar_iframe import trocar_iframe



def cancelar_doc(
    driver: webdriver.Chrome,
    motivo: str
):
    selecionar_cancelar_doc(driver)
    preencher_motivo_cancelamento(driver, motivo)
    clicar_salvar_sbmSalvar(driver)
    

def excluir_doc(
    driver: webdriver.Chrome
):
    selecionar_excluir_doc(driver)
    confirmar_exclusao_doc(driver)


def inserir_bloco_ass(
    driver: webdriver.Chrome,
    num_bloco: str
):
    selecionar_inserir_bloco_ass(driver)
    trocar_iframe(driver, "ifrVisualizacao")
    seleciona_bloco_ass(driver, num_bloco)
    clicar_incluir_sbmIncluir(driver)