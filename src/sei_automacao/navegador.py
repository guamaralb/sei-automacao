"""Abertura do navegador já na página do SEI."""

import logging
import os
from pathlib import Path
from typing import Literal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait as _WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from sei_automacao._internal.espera import TIMEOUT_PADRAO as _TIMEOUT_PADRAO

__all__ = ['DOWNLOAD_DIR_PADRAO', 'iniciar_sei']

logger = logging.getLogger(__name__)

DOWNLOAD_DIR_PADRAO = os.path.join(os.path.expanduser('~'), 'Downloads', 'SEI')


def _criar_driver(
    driver_type: Literal['chrome', 'edge'], prefs: dict
) -> webdriver.Remote:
    if driver_type == 'edge':
        logger.info('Iniciando Microsoft Edge...')
        options = EdgeOptions()
        options.add_argument('--no-proxy-server')
        options.add_experimental_option('prefs', prefs)
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    if driver_type == 'chrome':
        logger.info('Iniciando Google Chrome...')
        options = ChromeOptions()
        options.add_argument('--no-proxy-server')
        options.add_experimental_option('prefs', prefs)
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    raise ValueError(
        f"driver_type inválido: {driver_type!r}. Use 'chrome' ou 'edge'."
    )


def iniciar_sei(
    url_sei: str,
    driver_type: Literal['chrome', 'edge'] = 'chrome',
    download_dir: str | Path = DOWNLOAD_DIR_PADRAO,
    *,
    desativar_proxy_local: bool = True,
    timeout: float = _TIMEOUT_PADRAO,
) -> webdriver.Remote:
    """Abre o navegador e carrega a página do SEI (tela de login).

    Args:
        url_sei: endereço do SEI (ex.: ``'https://www.sei.mg.gov.br'``).
        driver_type: ``'chrome'`` ou ``'edge'``.
        download_dir: pasta onde o navegador salva os downloads (é criada
            se não existir).
        desativar_proxy_local: define ``NO_PROXY`` para ``localhost`` no
            ambiente do processo, para o Selenium falar com o driver local
            mesmo atrás de proxy.
        timeout: tempo máximo (s) para a página terminar de carregar.

    Returns:
        O ``WebDriver`` já na página do SEI. Se o carregamento falhar, o
        navegador é fechado antes de a exceção ser relançada.
    """
    if desativar_proxy_local:
        os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
        os.environ['no_proxy'] = 'localhost,127.0.0.1'

    download_dir = os.path.abspath(download_dir)
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
    }

    driver = _criar_driver(driver_type, prefs)

    try:
        driver.execute_cdp_cmd(
            'Page.setDownloadBehavior',
            {'behavior': 'allow', 'downloadPath': download_dir},
        )
        logger.info('Navegador iniciado. Downloads em: %s', download_dir)

        driver.get(url_sei)
        _WebDriverWait(driver, timeout).until(
            lambda d: (
                d.execute_script('return document.readyState') == 'complete'
            )
        )
    except BaseException:
        logger.exception('Erro ao abrir o SEI em %s', url_sei)
        driver.quit()
        raise

    return driver
