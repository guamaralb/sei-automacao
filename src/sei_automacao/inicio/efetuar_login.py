from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def efetuar_login(driver: webdriver.Chrome, usuario: str, senha: str, orgao: str):
    input_usuario = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(driver.find_element(By.ID, 'txtUsuario'))
    )
    input_usuario.clear()
    input_usuario.send_keys(usuario)

    input_senha = driver.find_element(By.ID, 'pwdSenha')
    input_senha.clear()
    input_senha.send_keys(senha)

    select_orgao = Select(driver.find_element(By.ID, 'selOrgao'))
    select_orgao.select_by_visible_text(orgao)

    botao_acessar = driver.find_element(By.ID, 'sbmAcessar')
    botao_acessar.click()