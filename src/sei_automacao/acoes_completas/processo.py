import time
from selenium import webdriver
from sei_automacao.processo.incluir_doc import clicar_incluir_doc, selecionar_tipo_doc, preencher_metadados_doc_externo, preencher_metadados_doc_sei, inserir_conteudo_doc_sei_simples, inserir_conteudo_doc_sei_memo
from sei_automacao.genericos.botoes import clicar_salvar_btnSalvar, clicar_salvar_sbmSalvar, clicar_adicionar_btnAdicionar, clicar_enviar_sbmEnviar
from sei_automacao.processo.adicionar_marcador import clicar_img_gerenciar_marcadores, selecionar_marcador, procurar_sbmSalvar
from sei_automacao.processo.encaminhar_processo import clicar_enviar_processo, preencher_unidade, selecionar_manter_aberto
from sei_automacao.processo.enviar_email import clicar_img_enviar_email, preenche_dados_email_envia_fecha_alerta
from sei_automacao.processo.concluir_processo import clicar_img_concluir_processo

def incluir_doc_externo(
    driver: webdriver.Chrome,
    tipo_doc: str,
    num: str,
    formato: str,
    data: str,
    caminho_anexo: str,
    nivel_acesso: str,
    hipotese_legal: str = ""
):
    clicar_incluir_doc(driver)
    selecionar_tipo_doc(driver, "Externo")
    preencher_metadados_doc_externo(
        driver,
        tipo_doc=tipo_doc,
        num=num,
        formato=formato,
        data=data,
        caminho_anexo=caminho_anexo,
        nivel_acesso=nivel_acesso,
        hipotese_legal=hipotese_legal
    )
    time.sleep(1)
    clicar_salvar_btnSalvar(driver)
    

def incluir_doc_sei_simples(
    driver: webdriver.Chrome,
    tipo_doc: str,
    texto: str,
    nivel_acesso: str,
    hipotese_legal: str = "",
    nome: str = ""
):
    clicar_incluir_doc(driver)
    selecionar_tipo_doc(driver, tipo_doc)
    preencher_metadados_doc_sei(driver, nivel_acesso, hipotese_legal, nome)
    clicar_salvar_btnSalvar(driver)
    inserir_conteudo_doc_sei_simples(driver, texto)
    

def incluir_doc_sei_memo(
    driver: webdriver.Chrome,
    tipo_doc: str,
    vocativo: str,
    destinatario: str,
    assunto: str,
    texto_principal: str,
    nivel_acesso: str,
    hipotese_legal: str = "",
    nome: str = ""
):
    clicar_incluir_doc(driver)
    selecionar_tipo_doc(driver, tipo_doc)
    preencher_metadados_doc_sei(driver, nivel_acesso, hipotese_legal, nome)
    clicar_salvar_btnSalvar(driver)
    inserir_conteudo_doc_sei_memo(driver, vocativo, destinatario, assunto, texto_principal)
    

def adicionar_marcador(
    driver: webdriver.Chrome,
    marcador
):
    clicar_img_gerenciar_marcadores(driver)
    
    if not procurar_sbmSalvar(driver):
        clicar_adicionar_btnAdicionar(driver)
        
    selecionar_marcador(driver, marcador)
    time.sleep(2)
    clicar_salvar_sbmSalvar(driver)


def encaminhar_processo(
    driver: webdriver.Chrome,
    unidade: str,
    desce_lista: int = 1,
    manter_aberto: bool = True
):
    clicar_enviar_processo(driver)
    preencher_unidade(driver, unidade, desce_lista)
    
    if manter_aberto:
        selecionar_manter_aberto(driver)
    
    clicar_enviar_sbmEnviar(driver)
    

def enviar_email(
    driver: webdriver.Chrome,
    email_de: str,
    emails_para: list,
    assunto: str,
    msg: str
):
    clicar_img_enviar_email(driver)
    preenche_dados_email_envia_fecha_alerta(
        driver,
        email_de,
        emails_para,
        assunto,
        msg
    )

def concluir_processo(driver: webdriver.Chrome):
    clicar_img_concluir_processo(driver)