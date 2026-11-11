import importlib
import inspect

import pytest

import sei_automacao

API_PUBLICA: dict[str, set[str]] = {
    'sei_automacao.navegador': {'DOWNLOAD_DIR_PADRAO', 'iniciar_sei'},
    'sei_automacao.sessao': {'efetuar_login'},
    'sei_automacao.unidade': {'trocar_unidade'},
    'sei_automacao.processo': {
        'acessar_processo',
        'iniciar_processo',
        'encaminhar_processo',
        'concluir_processo',
        'reabrir_processo',
        'pode_incluir_documento',
        'enviar_email',
        'listar_documentos_arvore',
        'selecionar_doc_arvore',
        'selecionar_raiz_arvore',
        'listar_marcadores',
        'listar_marcadores_disponiveis',
        'adicionar_marcador',
        'remover_marcador',
    },
    'sei_automacao.documento': {
        'incluir_doc_externo',
        'incluir_doc_sei_simples',
        'incluir_doc_sei_memo',
        'cancelar_doc',
        'excluir_doc',
        'inserir_bloco_ass',
        'obter_conteudo_doc',
    },
    'sei_automacao.modelos': {'Memorando'},
    'sei_automacao.formatacao': {'num_extenso_formatado'},
}

# Passos internos que não podem ser acessíveis pelos módulos públicos
NOMES_INTERNOS = [
    'selecionar_unidade',
    'acessar_pagina_trocar_unidade',
    'trocar_iframe',
    'encontrar_elemento',
    'selecionar_nivel_acesso',
    'clicar_salvar_btnSalvar',
    'clicar_gerenciar_marcadores',
    'procurar_sbmSalvar',
    'fechar_popup_basico',
    'fechar_popup_novidades',
    'pesquisar_processo',
    'abrir_menu',
    'clicar_num_processo',
    'WebDriverWait',
]

ACOES = sorted(
    (modulo, nome)
    for modulo, nomes in API_PUBLICA.items()
    for nome in nomes
    if modulo not in {'sei_automacao.modelos', 'sei_automacao.formatacao'}
    and nome != 'DOWNLOAD_DIR_PADRAO'
)


@pytest.mark.parametrize('modulo', sorted(API_PUBLICA))
def test_all_de_cada_modulo(modulo):
    mod = importlib.import_module(modulo)
    assert set(mod.__all__) == API_PUBLICA[modulo]
    for nome in mod.__all__:
        assert hasattr(mod, nome)


@pytest.mark.parametrize('modulo', sorted(API_PUBLICA))
@pytest.mark.parametrize('nome', NOMES_INTERNOS)
def test_passos_internos_nao_sao_acessiveis(modulo, nome):
    mod = importlib.import_module(modulo)
    assert not hasattr(mod, nome)
    with pytest.raises(ImportError):
        exec(f'from {modulo} import {nome}', {})  # noqa: S102


def test_topo_reexporta_as_acoes():
    for modulo, nomes in API_PUBLICA.items():
        for nome in nomes - {'DOWNLOAD_DIR_PADRAO'}:
            assert getattr(sei_automacao, nome) is getattr(
                importlib.import_module(modulo), nome
            )
    for nome in sei_automacao.__all__:
        assert hasattr(sei_automacao, nome)
    for nome in NOMES_INTERNOS:
        assert not hasattr(sei_automacao, nome)


@pytest.mark.parametrize(('modulo', 'nome'), ACOES)
def test_toda_acao_tem_timeout_so_por_nome(modulo, nome):
    funcao = getattr(importlib.import_module(modulo), nome)
    parametro = inspect.signature(funcao).parameters['timeout']
    assert parametro.kind is inspect.Parameter.KEYWORD_ONLY
    assert parametro.default == 10  # noqa: PLR2004


def test_versao():
    assert isinstance(sei_automacao.__version__, str)
