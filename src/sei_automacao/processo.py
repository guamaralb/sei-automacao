"""Ações sobre o processo: busca, criação, tramitação, árvore e marcadores.

Salvo indicação contrária, as funções esperam o navegador com um processo
aberto (ver :func:`acessar_processo`) e terminam no ``default_content``.
"""

import time

from selenium import webdriver

from sei_automacao._internal import botoes as _botoes
from sei_automacao._internal import elementos as _elementos
from sei_automacao._internal import iframes as _iframes
from sei_automacao._internal import nivel_acesso as _nivel_acesso
from sei_automacao._internal import popups as _popups
from sei_automacao._internal.espera import TIMEOUT_PADRAO as _TIMEOUT_PADRAO
from sei_automacao._internal.nivel_acesso import NivelAcesso
from sei_automacao._internal.telas import arvore as _arvore
from sei_automacao._internal.telas import busca as _busca
from sei_automacao._internal.telas import ciclo_de_vida as _ciclo_de_vida
from sei_automacao._internal.telas import documentos as _documentos
from sei_automacao._internal.telas import email as _email
from sei_automacao._internal.telas import encaminhamento as _encaminhamento
from sei_automacao._internal.telas import marcadores as _marcadores
from sei_automacao._internal.telas import menu as _menu
from sei_automacao.exceptions import ProcessoNaoReabrivel

__all__ = [
    'acessar_processo',
    'adicionar_marcador',
    'concluir_processo',
    'encaminhar_processo',
    'enviar_email',
    'iniciar_processo',
    'listar_documentos_arvore',
    'listar_marcadores',
    'listar_marcadores_disponiveis',
    'pode_incluir_documento',
    'reabrir_processo',
    'remover_marcador',
    'selecionar_doc_arvore',
    'selecionar_raiz_arvore',
]

_XPATH_INCLUIR_DOCUMENTO = "//img[@alt='Incluir Documento']"


# --- Busca e criação --------------------------------------------------------


def acessar_processo(
    driver: webdriver.Remote,
    num_processo: str,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Abre o processo pela pesquisa rápida.

    Raises:
        UnidadeSemAcessoException: a unidade atual não tem acesso ao
            processo (detectado assim que a mensagem aparece).
    """
    _busca.pesquisar_processo(driver, num_processo, timeout=timeout)


def iniciar_processo(  # noqa: PLR0913
    driver: webdriver.Remote,
    tipo_processo: str,
    especificacao: str,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str = '',
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Cria um processo pelo menu "Iniciar Processo"."""
    driver.switch_to.default_content()
    _menu.abrir_menu(driver, timeout=timeout)
    _menu.clicar_iniciar_processo(driver, timeout=timeout)
    _menu.selecionar_tipo_processo(driver, tipo_processo, timeout=timeout)
    _menu.preencher_especificacao_processo(
        driver, especificacao, timeout=timeout
    )
    _nivel_acesso.selecionar_nivel_acesso(
        driver, nivel_acesso, hipotese_legal, timeout=timeout
    )
    _botoes.clicar_salvar_btnSalvar(driver, timeout=timeout)


# --- Tramitação e ciclo de vida --------------------------------------------


def encaminhar_processo(
    driver: webdriver.Remote,
    unidade: str,
    desce_lista: int = 1,
    manter_aberto: bool = True,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Envia o processo para outra unidade.

    Args:
        unidade: texto digitado no campo de unidade.
        desce_lista: quantas vezes descer na lista de sugestões antes de
            confirmar (1 = primeira sugestão).
        manter_aberto: marca "Manter processo aberto na unidade atual".
    """
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _encaminhamento.clicar_enviar_processo(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)
    _encaminhamento.preencher_unidade(
        driver, unidade, desce_lista, timeout=timeout
    )

    if manter_aberto:
        _encaminhamento.selecionar_manter_aberto(driver, timeout=timeout)

    _botoes.clicar_enviar_sbmEnviar(driver, timeout=timeout)
    driver.switch_to.default_content()


def concluir_processo(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> None:
    """Conclui o processo na unidade atual."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _ciclo_de_vida.clicar_img_concluir_processo(driver, timeout=timeout)
    driver.switch_to.default_content()


def reabrir_processo(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> None:
    """Reabre o processo na unidade atual. Se ele já estiver aberto (botão
    "Concluir Processo" visível), não faz nada.

    Raises:
        ProcessoNaoReabrivel: a tela do processo não carregou ou não há
            como reabrir nem concluir o processo.
    """
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)

    try:
        img_acompanhamento_especial = _elementos.encontrar_elemento(
            driver,
            'XPATH',
            "//img[@alt='Acompanhamento Especial']",
            timeout=timeout,
        )
        if not img_acompanhamento_especial:
            raise ProcessoNaoReabrivel(
                'Processo não foi carregado corretamente'
            )

        img_reabrir_processo = _elementos.encontrar_elemento(
            driver, 'XPATH', "//img[@alt='Reabrir Processo']", timeout=0
        )
        if img_reabrir_processo:
            img_reabrir_processo.click()
            return

        img_concluir_processo = _elementos.encontrar_elemento(
            driver, 'XPATH', "//img[@alt='Concluir Processo']", timeout=0
        )
        if not img_concluir_processo:
            raise ProcessoNaoReabrivel(
                'Não há como concluir nem reabrir o processo'
            )
    finally:
        driver.switch_to.default_content()


def pode_incluir_documento(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> bool:
    """Indica se a tela do processo mostra "Incluir Documento", isto é, se a
    unidade atual pode agir no processo (ele está aberto nela)."""
    driver.switch_to.default_content()
    try:
        _iframes.trocar_iframe(
            driver, 'ifrConteudoVisualizacao', timeout=timeout
        )
        return (
            _elementos.encontrar_elemento(
                driver, 'XPATH', _XPATH_INCLUIR_DOCUMENTO, timeout=timeout
            )
            is not None
        )
    finally:
        driver.switch_to.default_content()


def enviar_email(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    email_de: str,
    emails_para: list[str],
    assunto: str,
    corpo_email: str,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str = '',
    fecha_alerta_doc_ja_existe: bool = False,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Envia um e-mail pelo processo e espera ele aparecer na árvore."""
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    _email.clicar_img_enviar_email(driver, timeout=timeout)
    if fecha_alerta_doc_ja_existe:
        _popups.fechar_popup_basico(
            driver, msg_contains='Já existe um documento', timeout=timeout
        )
    _email.preenche_dados_email_envia(
        driver,
        email_de=email_de,
        emails_para=emails_para,
        assunto=assunto,
        corpo_email=corpo_email,
        nivel_acesso=nivel_acesso,
        hipotese_legal=hipotese_legal,
        timeout=timeout,
    )
    driver.switch_to.default_content()
    _iframes.trocar_iframe(driver, 'ifrArvore', timeout=timeout)
    _documentos.espera_documento_aparecer_arvore(
        driver, tipo_doc='E-mail', timeout=timeout
    )
    driver.switch_to.default_content()
    time.sleep(1)


# --- Árvore -----------------------------------------------------------------


def listar_documentos_arvore(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> list[dict]:
    """Abre todas as pastas da árvore e lista os documentos.

    Returns:
        Uma lista, na ordem da árvore, de dicts com ``numero_sei``,
        ``nome_arvore`` e ``unidade``.
    """
    return _arvore.listar_documentos_arvore(driver, timeout=timeout)


def selecionar_doc_arvore(
    driver: webdriver.Remote,
    numero_sei: str | None = None,
    nome: str | None = None,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Clica no documento da árvore (por número SEI ou, se não achar, por
    nome) e espera ele abrir.

    Raises:
        DocumentoNaoEncontrado: o documento não está na árvore.
    """
    _arvore.selecionar_doc_arvore(
        driver, numero_sei=numero_sei, nome=nome, timeout=timeout
    )


def selecionar_raiz_arvore(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> None:
    """Clica no número do processo (raiz da árvore), voltando para a tela
    do processo."""
    _arvore.clicar_num_processo(driver, timeout=timeout)


# --- Marcadores -------------------------------------------------------------


def listar_marcadores(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> list[str]:
    """Marcadores aplicados ao processo (lidos na árvore)."""
    return _marcadores.listar_marcadores_arvore(driver, timeout=timeout)


def listar_marcadores_disponiveis(
    driver: webdriver.Remote, *, timeout: float = _TIMEOUT_PADRAO
) -> set[str]:
    """Marcadores cadastrados na unidade, lidos na tela "Gerenciar
    Marcador" do processo aberto, sem salvar nada."""
    driver.refresh()
    _abrir_tela_adicionar_marcador(driver, timeout)
    nomes = _marcadores.ler_opcoes_marcador(driver, timeout=timeout)

    # Sai da tela sem salvar
    driver.refresh()
    driver.switch_to.default_content()
    return nomes


def adicionar_marcador(
    driver: webdriver.Remote,
    marcador: str,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Adiciona o marcador ao processo. Se ele já estiver no processo, não
    faz nada.

    Raises:
        MarcadorNaoEncontrado: o marcador não apareceu depois de salvar.
    """
    # Garante que a página retorna no menu do processo
    driver.refresh()

    if marcador in listar_marcadores(driver, timeout=timeout):
        return

    _abrir_tela_adicionar_marcador(driver, timeout)
    _marcadores.selecionar_marcador_lista_suspensa(
        driver, marcador, timeout=timeout
    )
    _botoes.clicar_salvar_sbmSalvar(driver, timeout=timeout)
    _marcadores.esperar_marcador_aparecer_apos_salvar(
        driver, marcador, timeout=timeout
    )

    driver.switch_to.default_content()


def remover_marcador(
    driver: webdriver.Remote,
    marcadores: list[str],
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Remove do processo os marcadores informados que estiverem nele
    (os ausentes são ignorados).

    Raises:
        MarcadorNaoEncontrado: algum marcador continuou no processo.
    """
    # Garante que a página retorna no menu do processo
    driver.refresh()

    no_processo = listar_marcadores(driver, timeout=timeout)
    a_remover = [m for m in marcadores if m in no_processo]
    if not a_remover:
        return

    driver.switch_to.default_content()
    _marcadores.clicar_gerenciar_marcadores(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)

    for marcador in a_remover:
        _marcadores.selecionar_marcador_checkbox(
            driver, marcador, timeout=timeout
        )

    _botoes.clicar_remover_btnRemover(driver, timeout=timeout)
    _popups.fechar_popup_basico(
        driver,
        msg_contains=(
            'Confirma remoção dos Marcadores selecionados do processo?'
        ),
        timeout=timeout,
    )
    for marcador in a_remover:
        _marcadores.esperar_marcador_sumir_apos_salvar(driver, marcador)

    driver.switch_to.default_content()


def _abrir_tela_adicionar_marcador(
    driver: webdriver.Remote, timeout: float
) -> None:
    driver.switch_to.default_content()
    _marcadores.clicar_gerenciar_marcadores(driver, timeout=timeout)
    _iframes.trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)
    if not _marcadores.procurar_sbmSalvar(driver):
        _botoes.clicar_adicionar_btnAdicionar(driver, timeout=timeout)
