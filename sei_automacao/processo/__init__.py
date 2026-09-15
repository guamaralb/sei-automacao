import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao.core.buttons import (
    clicar_adicionar_btnAdicionar,
    clicar_enviar_sbmEnviar,
    clicar_salvar_btnSalvar,
    clicar_salvar_sbmSalvar,
)
from sei_automacao.core.iframes import trocar_iframe
from sei_automacao.core.popups import fechar_popup_basico
from sei_automacao.processo.arvore import clicar_num_processo
from sei_automacao.processo.ciclo_de_vida import clicar_img_concluir_processo
from sei_automacao.processo.documentos import (
    clicar_incluir_doc,
    espera_documento_aparecer_arvore,
    inserir_conteudo_doc_sei_memo,
    inserir_conteudo_doc_sei_simples,
    preencher_metadados_doc_externo,
    preencher_metadados_doc_sei,
    selecionar_tipo_doc,
)
from sei_automacao.processo.email import (
    clicar_img_enviar_email,
    preenche_dados_email_envia,
)
from sei_automacao.processo.encaminhamento import (
    clicar_enviar_processo,
    preencher_unidade,
    selecionar_manter_aberto,
)
from sei_automacao.processo.marcadores import (
    clicar_gerenciar_marcadores,
    esperar_marcador_aparecer_apos_salvar,
    procurar_sbmSalvar,
    selecionar_marcador,
)


def incluir_doc_externo(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    tipo_doc: str,
    num: str,
    formato: str,
    data: str,
    path_anexo: Path,
    nivel_acesso: str,
    hipotese_legal: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    clicar_incluir_doc(driver)
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_tipo_doc(driver, 'Externo')

    preencher_metadados_doc_externo(
        driver,
        tipo_doc=tipo_doc,
        num=num,
        formato=formato,
        data=data,
        path_anexo=path_anexo,
        nivel_acesso=nivel_acesso,
        hipotese_legal=hipotese_legal,
    )
    time.sleep(1)
    clicar_salvar_btnSalvar(driver)

    if fecha_alerta_doc_ja_existe:
        fechar_popup_basico(driver, msg_contains='Já existe um documento')

    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')
    espera_documento_aparecer_arvore(driver, tipo_doc, num)
    driver.switch_to.default_content()
    time.sleep(1)


def incluir_doc_sei_simples(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    tipo_doc: str,
    texto: str,
    nivel_acesso: str,
    hipotese_legal: str = '',
    nome: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrVisualizacao')
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    clicar_incluir_doc(driver)
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_tipo_doc(driver, tipo_doc)
    preencher_metadados_doc_sei(driver, nivel_acesso, hipotese_legal, nome)
    clicar_salvar_btnSalvar(driver)
    if fecha_alerta_doc_ja_existe:
        fechar_popup_basico(driver, msg_contains='Já existe um documento')
    inserir_conteudo_doc_sei_simples(driver, texto)
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')
    espera_documento_aparecer_arvore(driver, tipo_doc)
    driver.switch_to.default_content()
    time.sleep(1)


def incluir_doc_sei_memo(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    vocativo: str,
    destinatario_nome: str,
    assunto: str,
    texto_principal: str,
    nivel_acesso: str,
    hipotese_legal: str = '',
    nome: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    clicar_incluir_doc(driver)
    trocar_iframe(driver, 'ifrVisualizacao')
    selecionar_tipo_doc(driver, tipo='Memorando')
    preencher_metadados_doc_sei(driver, nivel_acesso, hipotese_legal, nome)
    clicar_salvar_btnSalvar(driver)
    if fecha_alerta_doc_ja_existe:
        fechar_popup_basico(driver, msg_contains='Já existe um documento')
    inserir_conteudo_doc_sei_memo(
        driver, vocativo, destinatario_nome, assunto, texto_principal
    )
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')
    espera_documento_aparecer_arvore(driver, tipo_doc='Memorando')
    driver.switch_to.default_content()
    time.sleep(1)


def adicionar_marcador(driver: webdriver.Remote, marcador: str) -> None:
    clicar_num_processo(driver)
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    clicar_gerenciar_marcadores(driver)

    trocar_iframe(driver, 'ifrVisualizacao')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//h1[contains(normalize-space(), 'Adicionar Marcador')]",
        ))
    )

    if not procurar_sbmSalvar(driver):
        clicar_adicionar_btnAdicionar(driver)

    selecionar_marcador(driver, marcador)
    clicar_salvar_sbmSalvar(driver)
    esperar_marcador_aparecer_apos_salvar(driver, marcador)
    driver.switch_to.default_content()


def encaminhar_processo(
    driver: webdriver.Remote,
    unidade: str,
    desce_lista: int = 1,
    manter_aberto: bool = True,
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    clicar_enviar_processo(driver)
    trocar_iframe(driver, 'ifrVisualizacao')
    preencher_unidade(driver, unidade, desce_lista)

    if manter_aberto:
        selecionar_manter_aberto(driver)

    clicar_enviar_sbmEnviar(driver)
    driver.switch_to.default_content()


def enviar_email(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    email_de: str,
    emails_para: list[str],
    assunto: str,
    corpo_email: str,
    nivel_acesso: str,
    hipotese_legal: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    clicar_img_enviar_email(driver)
    if fecha_alerta_doc_ja_existe:
        fechar_popup_basico(driver, msg_contains='Já existe um documento')
    preenche_dados_email_envia(
        driver=driver,
        email_de=email_de,
        emails_para=emails_para,
        assunto=assunto,
        corpo_email=corpo_email,
        nivel_acesso=nivel_acesso,
        hipotese_legal=hipotese_legal,
    )
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')
    espera_documento_aparecer_arvore(driver, tipo_doc='E-mail')
    driver.switch_to.default_content()
    time.sleep(1)


def concluir_processo(driver: webdriver.Remote) -> None:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrVisualizacao')
    clicar_img_concluir_processo(driver)
    driver.switch_to.default_content()
