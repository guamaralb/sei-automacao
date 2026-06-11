import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.genericos.botoes import clicar_enviar_btnEnviar
from sei_automacao.genericos.popup import fechar_popup_basico
from sei_automacao.genericos.janelas import identifica_abertura_nova_janela
from sei_automacao.utils.selecionar_nivel_acesso import selecionar_nivel_acesso

def clicar_img_enviar_email(driver: webdriver.Remote) -> None:
    for i in range(3):
        try:
            img_enviar_email: WebElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//img[@alt='Enviar Correspondência Eletrônica' or @alt='Enviar Documento por Correio Eletrônico']"))
            )
            img_enviar_email.click()
            return

        except StaleElementReferenceException:
            print(f"Elemento img_enviar_email ficou stale. Tentando novamente {i + 1}/3")

    raise Exception("Elemento img_enviar_email ficou stale mesmo após 3 tentativas.")


def preenche_dados_email_envia(
    driver: webdriver.Remote,
    email_de: str,
    emails_para: list[str],
    assunto: str,
    corpo_email: str,
    nivel_acesso: str,
    hipotese_legal: str = ""
) -> None:
    janela_principal: str = driver.current_window_handle

    # Espera abrir a nova janela
    identifica_abertura_nova_janela(driver)

    # Troca para a nova janela
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break

    driver.switch_to.default_content()

    WebDriverWait(driver, 20).until(
        lambda d: d.current_url != "about:blank"
    )
    time.sleep(1)

    # Preenche DE
    select_de: Select = Select(
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "selDe"))
        )
    )
    select_de.select_by_value(email_de)

    # Preenche PARA
    input_para: WebElement = driver.find_element(By.ID, "s2id_autogen1")

    for email in emails_para:
        input_para.send_keys(email)
        time.sleep(1)

        span_para: WebElement = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[@class='select2-match' and text()='{email}']"))
        )
        span_para.click()

    # Preenche ASSUNTO
    input_assunto: WebElement = driver.find_element(By.ID, "txtAssunto")
    input_assunto.send_keys(assunto)
    
    # Preenche MENSAGEM
    input_mensagem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "txaMensagem"))
    )

    input_mensagem.clear()
    input_mensagem.send_keys(corpo_email)
    
    # Popup as vezes aparece por não identificar a msg no corpo
    fechar_popup_basico(driver, msg="Informe a Mensagem.")
    time.sleep(5)
    
    selecionar_nivel_acesso(driver=driver, nivel_acesso=nivel_acesso)
    time.sleep(5)
    
    # Envia email
    clicar_enviar_btnEnviar(driver)
    time.sleep(5)

    fechar_popup_basico(driver)
    time.sleep(5)

    driver.switch_to.window(janela_principal)
