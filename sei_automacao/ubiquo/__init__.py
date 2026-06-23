from selenium import webdriver

from sei_automacao.navigation.menu import abrir_menu, clicar_iniciar_processo, selecionar_tipo_processo, preencher_especificacao_processo
from sei_automacao.utils.acesso import selecionar_nivel_acesso
from sei_automacao.core.buttons import clicar_salvar_btnSalvar
from sei_automacao.ubiquo.unidade import acessar_pagina_trocar_unidade, selecionar_unidade


def iniciar_processo(
    driver: webdriver.Remote,
    tipo_processo: str,
    especificacao: str,
    nivel_acesso: str,
    hipotese_legal: str = ""
) -> None:
    abrir_menu(driver)
    clicar_iniciar_processo(driver)
    selecionar_tipo_processo(driver, tipo_processo)
    preencher_especificacao_processo(driver, especificacao)
    selecionar_nivel_acesso(driver, nivel_acesso, hipotese_legal)
    clicar_salvar_btnSalvar(driver)


def trocar_unidade(
    driver: webdriver.Remote,
    unidade: str
) -> None:
    acessar_pagina_trocar_unidade(driver)
    selecionar_unidade(driver, unidade)
