import os

from dotenv import load_dotenv
from selenium import webdriver

from sei_automacao.auth.login import efetuar_login
from sei_automacao.driver import iniciar_driver
from sei_automacao.processo import (
    clicar_gerenciar_marcadores,
    remover_marcador,
)
from sei_automacao.processo.marcadores import listar_marcadores
from sei_automacao.ubiquo.busca import acessar_processo


def test_new_function():
    load_dotenv()

    driver: webdriver.Remote = iniciar_driver()
    driver.get('https://www.sei.mg.gov.br/')
    efetuar_login(
        driver,
        os.getenv('SEI_LOGIN'),
        os.getenv('SEI_SENHA'),
        os.getenv('SEI_ORGAO'),
    )

    acessar_processo(driver, '2010.01.0096589/2026-12')
    clicar_gerenciar_marcadores(driver)

    marcadores = listar_marcadores(driver)

    print('REMOVENDO:', marcadores)
    remover_marcador(driver, marcadores)
