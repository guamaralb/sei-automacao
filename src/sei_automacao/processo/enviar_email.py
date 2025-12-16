import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.genericos.botoes import clicar_enviar_btnEnviar

def clicar_img_enviar_email(driver):
    for i in range(3):
        try:
            img_enviar_email = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Enviar Correspondência Eletrônica']"))
            )
            img_enviar_email.click()
            return
        
        except StaleElementReferenceException:
            print(f"Elemento img_enviar_email ficou stale. Tentando novamente {i + 1}/3")
    
    raise Exception("Elemento img_enviar_email ficou stale mesmo após 3 tentativas.")


def fecha_alerta(driver: webdriver.Chrome):
    alert = WebDriverWait(driver, 12).until(
        EC.alert_is_present()
    )
    alert.accept()


def preenche_dados_email_envia_fecha_alerta(
    driver:webdriver.Chrome,
    email_de: str,
    emails_para: list,
    assunto: str,
    msg: str
):
    janela_principal = driver.current_window_handle

    # Espera abrir a nova janela
    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) == 2)

    # Troca para a nova janela
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break

    driver.switch_to.default_content()

    # 🔥 AGUARDA CARREGAR (antes era about:blank)
    WebDriverWait(driver, 20).until(
        lambda d: d.current_url != "about:blank"
    )
    time.sleep(1)  # dá tempo do JS montar o DOM

    # Preenche DE
    select_de = Select(
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "selDe"))
        )
    )
    select_de.select_by_value(email_de)
    
    # Preenche PARA
    input_para = driver.find_element(By.ID, "s2id_autogen1")
        
    for email in emails_para:
        input_para.send_keys(email)
        
        time.sleep(1)
        
        span_para = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[@class='select2-match' and text()='{email}']"))
        )
        span_para.click()
            
        
    #Preenche ASSUNTO
    input_para = driver.find_element(By.ID, "txtAssunto")
    input_para.send_keys(assunto)
        
    # Preenche MENSAGEM
    txt_mensagem = msg
    input_para = driver.find_element(By.ID, "txaMensagem")
    input_para.send_keys(txt_mensagem)
        
    # Envia email
    clicar_enviar_btnEnviar(driver)
    fecha_alerta(driver)
        
    driver.switch_to.window(janela_principal)

