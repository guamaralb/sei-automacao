"""O ``timeout`` de cada ação pública chega a todas as esperas internas.

Roda as ações com um driver falso e um ``WebDriverWait`` falso que só
registra o tempo pedido. Nenhuma espera pode usar o padrão (10s) quando a
ação recebe outro valor; só as sondagens curtas e os mínimos das esperas
longas têm valores próprios.
"""

import importlib
import inspect
import pkgutil
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import sei_automacao._internal
from sei_automacao import documento, processo, sessao, unidade
from sei_automacao._internal.espera import TIMEOUT_PADRAO, TIMEOUT_SONDAGEM

TIMEOUT_TESTE = 3.5
# Sondagens e mínimos de esperas longas (ver _internal)
PERMITIDOS = {TIMEOUT_TESTE, TIMEOUT_SONDAGEM, 0, 2, 15, 30}


class EsperaFalsa:
    registros: list[float] = []

    def __init__(self, driver, timeout, *args, **kwargs):
        EsperaFalsa.registros.append(timeout)

    def until(self, condicao, mensagem=''):
        return _elemento()


def _elemento() -> MagicMock:
    elemento = MagicMock(name='elemento')
    elemento.get_attribute.side_effect = lambda nome: (
        'ifrConteudoVisualizacao' if nome == 'id' else ''
    )
    span = MagicMock(text='2010.01.0100691/2026-32')
    elemento.__iter__.side_effect = lambda: iter([span])
    return elemento


@pytest.fixture
def sem_navegador(monkeypatch):
    EsperaFalsa.registros = []
    for info in pkgutil.walk_packages(
        sei_automacao._internal.__path__, 'sei_automacao._internal.'
    ):
        modulo = importlib.import_module(info.name)
        if hasattr(modulo, 'WebDriverWait'):
            monkeypatch.setattr(modulo, 'WebDriverWait', EsperaFalsa)
        if hasattr(modulo, 'Select'):
            monkeypatch.setattr(modulo, 'Select', MagicMock())
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    return MagicMock(name='driver')


CHAMADAS = {
    'efetuar_login': lambda d, t: sessao.efetuar_login(
        d, 'u', 's', 'o', timeout=t
    ),
    'trocar_unidade': lambda d, t: unidade.trocar_unidade(d, 'X', timeout=t),
    'acessar_processo': lambda d, t: processo.acessar_processo(
        d, '1', timeout=t
    ),
    'iniciar_processo': lambda d, t: processo.iniciar_processo(
        d, 'Tipo', 'Espec', 'Público', timeout=t
    ),
    'encaminhar_processo': lambda d, t: processo.encaminhar_processo(
        d, 'UNID', timeout=t
    ),
    'concluir_processo': lambda d, t: processo.concluir_processo(d, timeout=t),
    'reabrir_processo': lambda d, t: processo.reabrir_processo(d, timeout=t),
    'pode_incluir_documento': lambda d, t: processo.pode_incluir_documento(
        d, timeout=t
    ),
    'enviar_email': lambda d, t: processo.enviar_email(
        d, 'de', ['para'], 'assunto', 'corpo', 'Público', timeout=t
    ),
    'listar_documentos_arvore': lambda d, t: processo.listar_documentos_arvore(
        d, timeout=t
    ),
    'selecionar_doc_arvore': lambda d, t: processo.selecionar_doc_arvore(
        d, numero_sei='1', timeout=t
    ),
    'selecionar_raiz_arvore': lambda d, t: processo.selecionar_raiz_arvore(
        d, timeout=t
    ),
    'listar_marcadores': lambda d, t: processo.listar_marcadores(d, timeout=t),
    'listar_marcadores_disponiveis': lambda d, t: (
        processo.listar_marcadores_disponiveis(d, timeout=t)
    ),
    'adicionar_marcador': lambda d, t: processo.adicionar_marcador(
        d, 'M', timeout=t
    ),
    'remover_marcador': lambda d, t: processo.remover_marcador(
        d, ['M'], timeout=t
    ),
    'incluir_doc_externo': lambda d, t: documento.incluir_doc_externo(
        d,
        'PDF',
        '1',
        'Nato-digital',
        '01/01/2026',
        Path('a.pdf'),
        'Público',
        timeout=t,
    ),
    'incluir_doc_sei_simples': lambda d, t: documento.incluir_doc_sei_simples(
        d, 'Nota Técnica', '<p>x</p>', 'Público', timeout=t
    ),
    'incluir_doc_sei_memo': lambda d, t: documento.incluir_doc_sei_memo(
        d, 'Senhor', 'Fulano', 'Assunto', '<p>x</p>', 'Público', timeout=t
    ),
    'cancelar_doc': lambda d, t: documento.cancelar_doc(
        d, 'motivo', timeout=t
    ),
    'excluir_doc': lambda d, t: documento.excluir_doc(d, timeout=t),
    'inserir_bloco_ass': lambda d, t: documento.inserir_bloco_ass(
        d, '1', timeout=t
    ),
    'obter_conteudo_doc': lambda d, t: documento.obter_conteudo_doc(
        d, timeout=t
    ),
}


def test_todas_as_acoes_estao_cobertas():
    acoes = {
        nome
        for modulo in (sessao, unidade, processo, documento)
        for nome in modulo.__all__
    }
    assert acoes == set(CHAMADAS)


@pytest.mark.parametrize('acao', sorted(CHAMADAS))
def test_timeout_chega_nas_esperas(sem_navegador, acao):
    CHAMADAS[acao](sem_navegador, TIMEOUT_TESTE)

    registros = EsperaFalsa.registros
    assert TIMEOUT_TESTE in registros or acao == 'efetuar_login' and registros
    assert TIMEOUT_PADRAO not in registros
    assert set(registros) <= PERMITIDOS


def test_assinaturas_das_chamadas_batem():
    """Evita que um lambda acima passe argumentos que a ação não aceita."""
    for nome in CHAMADAS:
        for modulo in (sessao, unidade, processo, documento):
            if nome in modulo.__all__:
                assert (
                    'timeout'
                    in inspect.signature(getattr(modulo, nome)).parameters
                )
