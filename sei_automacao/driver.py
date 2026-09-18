import logging
import os
from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


logger = logging.getLogger(__name__)


def iniciar_driver(
    driver_type: Literal['chrome', 'edge'] = 'chrome',
) -> webdriver.Remote:
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
    os.environ['no_proxy'] = 'localhost,127.0.0.1'

    try:
        if driver_type == 'edge':
            logger.info('Iniciando Microsoft Edge...')

            options = EdgeOptions()
            options.add_argument('--no-proxy-server')

            logger.info('Obtendo EdgeDriver...')
            service = EdgeService(
                EdgeChromiumDriverManager().install()
            )

            logger.info('Inicializando WebDriver do Edge...')
            driver = webdriver.Edge(
                service=service,
                options=options,
            )

            logger.info('Microsoft Edge iniciado com sucesso.')
            return driver

        logger.info('Iniciando Google Chrome...')

        options = ChromeOptions()
        options.add_argument('--no-proxy-server')

        logger.info('Obtendo ChromeDriver...')
        service = ChromeService(
            ChromeDriverManager().install()
        )

        logger.info('Inicializando WebDriver do Chrome...')
        driver = webdriver.Chrome(
            service=service,
            options=options,
        )

        logger.info('Google Chrome iniciado com sucesso.')
        return driver

    except WebDriverException as e:
        logger.exception(
            'Erro ao inicializar o WebDriver (%s): %s',
            driver_type,
            e,
        )
        raise

    except Exception as e:
        logger.exception(
            'Erro inesperado ao inicializar o WebDriver (%s): %s',
            driver_type,
            e,
        )
        raise