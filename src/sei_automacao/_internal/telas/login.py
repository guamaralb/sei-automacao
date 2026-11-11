from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO, TIMEOUT_SONDAGEM


def preencher_e_enviar_login(
    driver: webdriver.Remote,
    usuario: str,
    senha: str,
    orgao: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    input_usuario: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, 'txtUsuario'))
    )
    input_usuario.clear()
    input_usuario.send_keys(usuario)

    input_senha: WebElement = driver.find_element(By.ID, 'pwdSenha')
    input_senha.clear()
    input_senha.send_keys(senha)

    select_orgao: Select = Select(driver.find_element(By.ID, 'selOrgao'))
    select_orgao.select_by_visible_text(orgao)

    botao_acessar: WebElement = driver.find_element(By.ID, 'sbmAcessar')
    botao_acessar.click()


def esperar_tela_inicial(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, 'tblProcessosRecebidos'))
    )


def fechar_popup_novidades(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_SONDAGEM
) -> None:
    """Fecha o modal de novidades, se aparecer. Por padrão é uma sondagem
    curta: na maioria dos logins o modal não aparece."""
    try:
        botao_fechar: WebElement = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//a[normalize-space(text())='Fechar' and "
                "contains(@href, 'infraModalFechar')]",
            ))
        )
        botao_fechar.click()
    except TimeoutException:
        pass
