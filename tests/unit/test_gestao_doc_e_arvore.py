"""Cancelar/excluir documento e árvore, com um driver falso: ação
indisponível, alerta de erro do SEI, documento sem conteúdo e pastas que
demoram a abrir."""

import time
from unittest.mock import MagicMock, PropertyMock

import pytest
from selenium.common.exceptions import (
    NoAlertPresentException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.alert import Alert

from sei_automacao._internal.telas import arvore, gestao_doc
from sei_automacao.exceptions import (
    AcaoIndisponivel,
    AcaoNaoConcluida,
    DocumentoSemConteudo,
    IframeNaoEncontrado,
)


def _img(alt: str) -> MagicMock:
    return MagicMock(get_attribute=MagicMock(return_value=alt))


def _sem_alerta(driver: MagicMock) -> None:
    type(driver.switch_to).alert = PropertyMock(
        side_effect=NoAlertPresentException
    )


def test_acao_indisponivel_sem_esperar():
    driver = MagicMock()
    driver.find_elements.return_value = [
        _img('Cancelar Documento'),
        _img('Assinar'),
    ]

    with pytest.raises(AcaoIndisponivel) as erro:
        gestao_doc.clicar_acao(driver, 'Excluir', timeout=0.1)

    assert erro.value.acao == 'Excluir'
    assert erro.value.disponiveis == {'Cancelar Documento', 'Assinar'}
    assert 'Cancelar Documento' in str(erro.value)


def test_acao_disponivel_e_clicada():
    driver = MagicMock()
    driver.find_elements.return_value = [_img('Excluir')]
    driver.find_element.return_value.is_displayed.return_value = True

    link = gestao_doc.clicar_acao(driver, 'Excluir', timeout=0.1)

    link.click.assert_called_once()


def test_tela_saiu():
    driver = MagicMock()
    _sem_alerta(driver)
    elemento = MagicMock()
    elemento.is_enabled.side_effect = StaleElementReferenceException

    gestao_doc.esperar_tela_sair(driver, elemento, 'Cancelar', timeout=0.1)


def test_alerta_do_sei_e_acao_nao_concluida():
    driver = MagicMock()
    alerta = MagicMock(spec=Alert)
    alerta.text = 'Documento não pode ser cancelado'
    type(driver.switch_to).alert = PropertyMock(return_value=alerta)

    with pytest.raises(AcaoNaoConcluida, match='não pode ser cancelado'):
        gestao_doc.esperar_tela_sair(
            driver, MagicMock(), 'Cancelar', timeout=0.1
        )
    alerta.accept.assert_called_once()


@pytest.mark.parametrize('exigir', [True, False])
def test_tela_que_nao_sai(exigir):
    driver = MagicMock()
    _sem_alerta(driver)

    def esperar():
        gestao_doc.esperar_tela_sair(
            driver, MagicMock(), 'Excluir', exigir=exigir, timeout=0.1
        )

    if exigir:
        with pytest.raises(AcaoNaoConcluida, match='no prazo'):
            esperar()
    else:
        esperar()


@pytest.fixture
def arvore_falsa(monkeypatch):
    monkeypatch.setattr(arvore, 'trocar_iframe', lambda *a, **k: None)
    monkeypatch.setattr(arvore, 'html_do_iframe', lambda *a, **k: None)
    driver = MagicMock()
    driver.execute_script.return_value = 'complete'
    return driver


def test_documento_sem_conteudo(arvore_falsa):
    arvore_falsa.find_elements.return_value = []

    with pytest.raises(DocumentoSemConteudo) as erro:
        arvore.selecionar_doc_arvore(arvore_falsa, numero_sei='123')

    # Quem já tratava o iframe ausente continua tratando
    assert isinstance(erro.value, IframeNaoEncontrado)


def test_documento_com_conteudo(arvore_falsa):
    arvore_falsa.find_elements.return_value = [MagicMock()]

    arvore.selecionar_doc_arvore(arvore_falsa, numero_sei='123', timeout=0.1)


class _ArvoreLenta:
    """Uma pasta fechada que só abre algumas leituras depois do clique."""

    def __init__(self, leituras_ate_abrir: int):
        self.leituras_ate_abrir = leituras_ate_abrir
        self.clicada = False
        self.pasta = MagicMock()
        self.pasta.click.side_effect = lambda: setattr(self, 'clicada', True)

    def aberta(self) -> bool:
        if self.clicada and self.leituras_ate_abrir > 0:
            self.leituras_ate_abrir -= 1
        return self.clicada and self.leituras_ate_abrir == 0

    def find_elements(self, _by, xpath):
        if 'processo_fechado' in xpath:
            return [] if self.aberta() else [self.pasta]
        if 'processo_aberto' in xpath:
            return [self.pasta] if self.aberta() else []
        return []  # itens da árvore: sem "Aguarde..."


def test_pastas_que_demoram_a_abrir_sao_clicadas_uma_vez(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    falsa = _ArvoreLenta(leituras_ate_abrir=3)
    driver = MagicMock(find_elements=falsa.find_elements)

    assert arvore.abrir_todas_pastas_arvore(driver, timeout=1) == 1
    falsa.pasta.click.assert_called_once()


def test_pasta_que_nao_abre(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    monkeypatch.setattr(arvore, '_TIMEOUT_MIN_PASTAS', 0)
    falsa = _ArvoreLenta(leituras_ate_abrir=10**9)
    driver = MagicMock(find_elements=falsa.find_elements)

    with pytest.raises(AcaoNaoConcluida, match='inconsistente'):
        arvore.abrir_todas_pastas_arvore(driver, timeout=0.05)
