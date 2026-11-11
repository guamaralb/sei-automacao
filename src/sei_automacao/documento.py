"""Ações sobre documentos do processo: incluir, cancelar, excluir, assinar
e ler.

As funções esperam o navegador com um processo aberto (ver
:func:`sei_automacao.processo.acessar_processo`). As de cancelar, excluir,
assinar e ler agem sobre o documento selecionado na árvore (ver
:func:`sei_automacao.processo.selecionar_doc_arvore`).
"""

import time
from pathlib import Path
from typing import Literal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from sei_automacao._internal import botoes as _botoes
from sei_automacao._internal import iframes as _iframes
from sei_automacao._internal import popups as _popups
from sei_automacao._internal.espera import TIMEOUT_PADRAO as _TIMEOUT_PADRAO
from sei_automacao._internal.nivel_acesso import NivelAcesso
from sei_automacao._internal.telas import assinatura as _assinatura
from sei_automacao._internal.telas import documentos as _documentos
from sei_automacao._internal.telas import gestao_doc as _gestao_doc

__all__ = [
    'cancelar_doc',
    'excluir_doc',
    'incluir_doc_externo',
    'incluir_doc_sei_memo',
    'incluir_doc_sei_simples',
    'inserir_bloco_ass',
    'obter_conteudo_doc',
]

_MSG_DOC_JA_EXISTE = 'Já existe um documento'


def _esperar_doc_na_arvore(
    driver: webdriver.Remote,
    tipo_doc: str,
    num: str | None,
    timeout: float,
) -> None:
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrArvore', timeout=timeout)
    _documentos.espera_documento_aparecer_arvore(
        driver, tipo_doc, num, timeout=timeout
    )
    driver.switch_to.default_content()
    time.sleep(1)


# --- Inclusão ---------------------------------------------------------------


def incluir_doc_externo(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    tipo_doc: str,
    num: str,
    formato: str,
    data: str,
    path_anexo: Path,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Inclui um documento externo (arquivo anexo) no processo e espera ele
    aparecer na árvore.

    Args:
        tipo_doc: tipo do documento, como aparece na lista (ex.: ``'PDF'``).
        num: número/nome do documento.
        formato: ``'Nato-digital'`` (único suportado por enquanto).
        data: data de elaboração (``dd/mm/aaaa``).
        path_anexo: arquivo a anexar.
        nivel_acesso: ``'Público'``, ``'Restrito'`` ou ``'Sigiloso'``.
        hipotese_legal: obrigatória se o nível não for público.
        fecha_alerta_doc_ja_existe: aceita o alerta "Já existe um
            documento..." se aparecer.
    """
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _documentos.clicar_incluir_doc(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)
    _documentos.selecionar_tipo_doc(driver, 'Externo', timeout=timeout)

    _documentos.preencher_metadados_doc_externo(
        driver,
        tipo_doc=tipo_doc,
        num=num,
        formato=formato,
        data=data,
        path_anexo=path_anexo,
        nivel_acesso=nivel_acesso,
        hipotese_legal=hipotese_legal,
        timeout=timeout,
    )
    time.sleep(1)
    _botoes.clicar_salvar_btnSalvar(driver, timeout=timeout)

    if fecha_alerta_doc_ja_existe:
        _popups.fechar_popup_basico(
            driver, msg_contains=_MSG_DOC_JA_EXISTE, timeout=timeout
        )

    _esperar_doc_na_arvore(driver, tipo_doc, num, timeout)


def incluir_doc_sei_simples(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    tipo_doc: str,
    texto: str,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str = '',
    nome: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Inclui um documento gerado no SEI com o ``texto`` (HTML) no corpo e
    espera ele aparecer na árvore."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _documentos.clicar_incluir_doc(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)
    _documentos.selecionar_tipo_doc(driver, tipo_doc, timeout=timeout)
    _documentos.preencher_metadados_doc_sei(
        driver, nivel_acesso, hipotese_legal, nome, timeout=timeout
    )
    _botoes.clicar_salvar_btnSalvar(driver, timeout=timeout)
    if fecha_alerta_doc_ja_existe:
        _popups.fechar_popup_basico(
            driver, msg_contains=_MSG_DOC_JA_EXISTE, timeout=timeout
        )
    _documentos.inserir_conteudo_doc_sei_simples(
        driver, texto, timeout=timeout
    )
    _esperar_doc_na_arvore(driver, tipo_doc, None, timeout)


def incluir_doc_sei_memo(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    vocativo: str,
    destinatario_nome: str,
    assunto: str,
    texto_principal: str,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str | None = None,
    nome: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Inclui um Memorando, preenchendo o modelo da unidade, e espera ele
    aparecer na árvore.

    Os argumentos podem vir de
    :meth:`sei_automacao.modelos.Memorando.para_kwargs_inserir_doc`.
    """
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _documentos.clicar_incluir_doc(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)
    _documentos.selecionar_tipo_doc(driver, 'Memorando', timeout=timeout)
    _documentos.preencher_metadados_doc_sei(
        driver, nivel_acesso, hipotese_legal, nome, timeout=timeout
    )
    _botoes.clicar_salvar_btnSalvar(driver, timeout=timeout)
    if fecha_alerta_doc_ja_existe:
        _popups.fechar_popup_basico(
            driver, msg_contains=_MSG_DOC_JA_EXISTE, timeout=timeout
        )
    _documentos.inserir_conteudo_doc_sei_memo(
        driver,
        vocativo,
        destinatario_nome,
        assunto,
        texto_principal,
        timeout=timeout,
    )
    _esperar_doc_na_arvore(driver, 'Memorando', None, timeout)


# --- Documento selecionado --------------------------------------------------


def cancelar_doc(
    driver: webdriver.Remote,
    motivo: str,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Cancela o documento selecionado na árvore."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _gestao_doc.selecionar_cancelar_doc(driver, timeout=timeout)
    _gestao_doc.preencher_motivo_cancelamento(driver, motivo, timeout=timeout)
    _botoes.clicar_salvar_sbmSalvar(driver, timeout=timeout)
    driver.switch_to.default_content()


def excluir_doc(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> None:
    """Exclui o documento selecionado na árvore."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _gestao_doc.selecionar_excluir_doc(driver, timeout=timeout)
    _gestao_doc.confirmar_exclusao_doc(driver, timeout=timeout)
    driver.switch_to.default_content()


def inserir_bloco_ass(
    driver: webdriver.Remote,
    num_bloco: str,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Inclui o documento selecionado no bloco de assinatura ``num_bloco``."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _assinatura.selecionar_inserir_bloco_ass(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    driver.switch_to.frame('ifrVisualizacao')
    _assinatura.seleciona_bloco_ass(driver, num_bloco)
    _botoes.clicar_incluir_sbmIncluir(driver, timeout=timeout)
    time.sleep(2)
    driver.switch_to.default_content()


def obter_conteudo_doc(
    driver: webdriver.Remote,
    formato: Literal['web_element', 'texto'] = 'texto',
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> str | WebElement:
    """Conteúdo do documento selecionado: o texto (padrão) ou o ``<body>``
    como ``WebElement`` (o driver fica no iframe do documento nesse caso)."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)

    body = driver.find_element(By.TAG_NAME, 'body')

    if formato == 'web_element':
        return body
    return body.text
