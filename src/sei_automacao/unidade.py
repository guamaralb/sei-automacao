"""Troca da unidade em que o usuário trabalha no SEI."""

from selenium import webdriver

from sei_automacao._internal.espera import TIMEOUT_PADRAO as _TIMEOUT_PADRAO
from sei_automacao._internal.telas import unidade as _tela_unidade

__all__ = ['trocar_unidade']


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
    _tela_unidade.acessar_pagina_trocar_unidade(driver, timeout=timeout)
    _tela_unidade.selecionar_unidade(driver, unidade, timeout=timeout)
    _tela_unidade.esperar_pagina_carregada(driver, timeout=timeout)
