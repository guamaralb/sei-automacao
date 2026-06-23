from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def efetuar_login(driver: webdriver.Remote, usuario: str, senha: str, orgao: str) -> None:
    input_usuario: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(driver.find_element(By.ID, 'txtUsuario'))
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
