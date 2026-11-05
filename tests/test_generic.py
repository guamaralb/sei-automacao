import os

from dotenv import load_dotenv
from selenium import webdriver

from sei_automacao.auth.login import efetuar_login
from sei_automacao.driver import iniciar_driver
from sei_automacao.processo.arvore import listar_documentos_arvore
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

    # 0 PASTAS
    # acessar_processo(driver, '2010.01.0082932/2024-60')

    # 2 PASTAS
    acessar_processo(driver, '2010.01.0072062/2024-28')

    # 3 PASTAS
    # acessar_processo(driver, '2010.01.0099303/2026-66')

    docs = listar_documentos_arvore(driver)

    for i, doc in enumerate(docs):
        print(i, doc)
