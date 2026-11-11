"""Troca da unidade em que o usuário trabalha no SEI."""

import time

from selenium import webdriver

from sei_automacao._internal.espera import TIMEOUT_PADRAO as _TIMEOUT_PADRAO
from sei_automacao._internal.telas import busca as _busca
from sei_automacao._internal.telas import unidade as _tela_unidade

__all__ = ['trocar_unidade']

# TODO(0.1.0): remover processo fixo antes de publicar. Hoje trocar_unidade
# abre este processo antes de clicar em "trocar unidade" (solução
# temporária, a ser resolvida pelo mantenedor).
_PROCESSO_TROCA_UNIDADE = '2010.01.0100691/2026-32'


def trocar_unidade(
    driver: webdriver.Remote,
    unidade: str,
    *,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Troca a unidade atual do usuário no SEI.

    Args:
        driver: navegador com sessão do SEI aberta.
        unidade: sigla da unidade, como aparece na lista de unidades (ex.:
            ``'IPSEMG/GEACS - Utilização'``).
        timeout: tempo máximo (s) de espera por cada elemento.
    """
    driver.switch_to.default_content()
    _busca.pesquisar_processo(driver, _PROCESSO_TROCA_UNIDADE, timeout=timeout)
    _tela_unidade.acessar_pagina_trocar_unidade(driver, timeout=timeout)
    _tela_unidade.selecionar_unidade(driver, unidade, timeout=timeout)
    driver.refresh()
    time.sleep(2)
