"""Exceções levantadas pela sei_automacao.

Todas herdam de :class:`SeiAutomacaoException`. As que substituem um
``ValueError`` de versões anteriores também herdam de ``ValueError``, para
não quebrar quem já as trata assim.
"""

__all__ = [
    'AcaoIndisponivel',
    'AcaoNaoConcluida',
    'DocumentoNaoEncontrado',
    'DocumentoSemConteudo',
    'ElementoNaoEncontrado',
    'IframeNaoEncontrado',
    'MarcadorNaoEncontrado',
    'OpcaoNaoSuportada',
    'ProcessoNaoReabrivel',
    'SeiAutomacaoException',
    'UnidadeSemAcessoException',
]


class SeiAutomacaoException(Exception):
    """Exceção base do pacote sei_automacao."""


class UnidadeSemAcessoException(SeiAutomacaoException):
    """A unidade atual não possui acesso ao processo pesquisado."""

    def __init__(self, num_processo: str) -> None:
        self.num_processo = num_processo
        super().__init__(
            f'Unidade atual não possui acesso ao processo {num_processo}'
        )


class ElementoNaoEncontrado(SeiAutomacaoException):
    """Um elemento esperado não foi encontrado na tela do SEI."""


class IframeNaoEncontrado(ElementoNaoEncontrado, ValueError):
    """O iframe esperado não foi encontrado na página."""


class DocumentoNaoEncontrado(ElementoNaoEncontrado):
    """O documento procurado não está na árvore do processo."""


class DocumentoSemConteudo(IframeNaoEncontrado):
    """O documento foi aberto, mas não mostra conteúdo (sem o iframe
    ``ifrVisualizacao``), como o documento cancelado."""


class MarcadorNaoEncontrado(ElementoNaoEncontrado, ValueError):
    """O marcador não apareceu (ou não sumiu) depois de salvar."""


class OpcaoNaoSuportada(SeiAutomacaoException, ValueError):
    """Valor de opção não implementado (nível de acesso, formato, tipo...)."""


class ProcessoNaoReabrivel(SeiAutomacaoException, ValueError):
    """O processo não pode ser reaberto (nem está aberto) na unidade."""


class AcaoNaoConcluida(SeiAutomacaoException):
    """A ação falhou mesmo depois de várias tentativas."""


class AcaoIndisponivel(SeiAutomacaoException):
    """A ação não está na barra do documento selecionado (ex.: "Excluir" em
    documento assinado, "Cancelar Documento" em documento já cancelado)."""

    def __init__(self, acao: str, disponiveis: set[str]) -> None:
        self.acao = acao
        self.disponiveis = disponiveis
        super().__init__(
            f'Ação "{acao}" indisponível no documento selecionado '
            f'(disponíveis: {", ".join(sorted(disponiveis)) or "nenhuma"})'
        )
