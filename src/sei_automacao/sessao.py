"""Login no SEI."""

from selenium import webdriver

from sei_automacao._internal.espera import TIMEOUT_PADRAO as _TIMEOUT_PADRAO
from sei_automacao._internal.telas import login as _login

__all__ = ['efetuar_login']


def efetuar_login(  # noqa: PLR0913
    driver: webdriver.Remote,
    usuario: str,
    senha: str,
    orgao: str,
    *,
    fechar_novidades: bool = True,
    timeout: float = _TIMEOUT_PADRAO,
) -> None:
    """Faz login no SEI e espera a tela de "Controle de Processos".

    Args:
        driver: navegador na tela de login (ver :func:`iniciar_sei`).
        usuario: login do usuário.
        senha: senha do usuário.
        orgao: órgão, como aparece na lista da tela de login.
        fechar_novidades: fecha o aviso de novidades do SEI, se aparecer.
        timeout: tempo máximo (s) de espera por cada elemento.
    """
    _login.preencher_e_enviar_login(
        driver, usuario, senha, orgao, timeout=timeout
    )
    _login.esperar_tela_inicial(driver, timeout=timeout)

    if fechar_novidades:
        _login.fechar_popup_novidades(driver)
