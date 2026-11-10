import os

from dotenv import load_dotenv
from selenium import webdriver

from sei_automacao.auth.login import efetuar_login
from sei_automacao.driver import iniciar_driver
from sei_automacao.ubiquo import trocar_unidade


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

    trocar_unidade(driver, 'IPSEMG/GEACS - Utilização')
