from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO


def _clicar(
    driver: webdriver.Remote, localizador: tuple[str, str], timeout: float
) -> None:
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(localizador)
    ).click()


def clicar_salvar_btnSalvar(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.ID, 'btnSalvar'), timeout)


def clicar_salvar_sbmSalvar(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.ID, 'sbmSalvar'), timeout)


def clicar_incluir_sbmIncluir(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.ID, 'sbmIncluir'), timeout)


def clicar_adicionar_btnAdicionar(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.ID, 'btnAdicionar'), timeout)


def clicar_enviar_sbmEnviar(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.ID, 'sbmEnviar'), timeout)


def clicar_enviar_btnEnviar(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.XPATH, "//button[@name='btnEnviar']"), timeout)


def clicar_remover_btnRemover(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar(driver, (By.ID, 'btnRemover'), timeout)
