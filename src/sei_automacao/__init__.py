"""Automação do SEI (Sistema Eletrônico de Informações) com Selenium.

Exemplo::

    from sei_automacao import (
        acessar_processo,
        efetuar_login,
        iniciar_sei,
        trocar_unidade,
    )

    driver = iniciar_sei('https://www.sei.mg.gov.br')
    efetuar_login(driver, 'usuario', 'senha', 'ÓRGÃO')
    trocar_unidade(driver, 'ÓRGÃO/UNIDADE')
    acessar_processo(driver, '0000.00.0000000/0000-00')

As ações também estão nos módulos por assunto: :mod:`sei_automacao.processo`,
:mod:`sei_automacao.documento`, :mod:`sei_automacao.unidade` etc.
"""

import logging
from importlib.metadata import PackageNotFoundError, version

from sei_automacao import exceptions as exceptions
from sei_automacao.documento import (
    cancelar_doc,
    excluir_doc,
    incluir_doc_externo,
    incluir_doc_sei_memo,
    incluir_doc_sei_simples,
    inserir_bloco_ass,
    obter_conteudo_doc,
)
from sei_automacao.exceptions import (
    SeiAutomacaoException,
    UnidadeSemAcessoException,
)
from sei_automacao.formatacao import num_extenso_formatado
from sei_automacao.modelos import Memorando
from sei_automacao.navegador import iniciar_sei
from sei_automacao.processo import (
    acessar_processo,
    adicionar_marcador,
    concluir_processo,
    encaminhar_processo,
    enviar_email,
    iniciar_processo,
    listar_documentos_arvore,
    listar_marcadores,
    listar_marcadores_disponiveis,
    pode_incluir_documento,
    reabrir_processo,
    remover_marcador,
    selecionar_doc_arvore,
    selecionar_raiz_arvore,
)
from sei_automacao.sessao import efetuar_login
from sei_automacao.unidade import trocar_unidade

try:
    __version__ = version('sei-automacao')
except PackageNotFoundError:  # pragma: no cover - código fora de instalação
    __version__ = '0.0.0'

# Biblioteca não configura logging: quem usa decide se e onde exibir
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    'Memorando',
    'SeiAutomacaoException',
    'UnidadeSemAcessoException',
    '__version__',
    'acessar_processo',
    'adicionar_marcador',
    'cancelar_doc',
    'concluir_processo',
    'efetuar_login',
    'encaminhar_processo',
    'enviar_email',
    'excluir_doc',
    'exceptions',
    'incluir_doc_externo',
    'incluir_doc_sei_memo',
    'incluir_doc_sei_simples',
    'iniciar_processo',
    'iniciar_sei',
    'inserir_bloco_ass',
    'listar_documentos_arvore',
    'listar_marcadores',
    'listar_marcadores_disponiveis',
    'num_extenso_formatado',
    'obter_conteudo_doc',
    'pode_incluir_documento',
    'reabrir_processo',
    'remover_marcador',
    'selecionar_doc_arvore',
    'selecionar_raiz_arvore',
    'trocar_unidade',
]
