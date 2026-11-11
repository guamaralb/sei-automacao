import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from sei_automacao.core.buttons import clicar_enviar_btnEnviar
from sei_automacao.core.popups import fechar_popup_basico
from sei_automacao.core.windows import identifica_abertura_nova_janela
from sei_automacao.utils.acesso import selecionar_nivel_acesso


def clicar_img_enviar_email(driver: webdriver.Remote) -> None:
    for i in range(3):
        try:
            img_enviar_email: WebElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//img[@alt='Enviar Correspondência Eletrônica' or "
                    "@alt='Enviar Documento por Correio Eletrônico']",
                ))
            )
            img_enviar_email.click()
            return

        except StaleElementReferenceException:
            print(
                f'Elemento img_enviar_email ficou stale. '
                f'Tentando novamente {i + 1}/3'
            )

    raise Exception(
        'Elemento img_enviar_email ficou stale mesmo após 3 tentativas.'
    )


def preenche_dados_email_envia(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    email_de: str,
    emails_para: list[str],
    assunto: str,
    corpo_email: str,
    nivel_acesso: str,
    hipotese_legal: str = '',
) -> None:
    janela_principal: str = driver.current_window_handle

    identifica_abertura_nova_janela(driver)

    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(lambda d: d.current_url != 'about:blank')
    time.sleep(1)

    select_de: Select = Select(
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'selDe'))
        )
    )
    select_de.select_by_value(email_de)

    input_para: WebElement = driver.find_element(By.ID, 's2id_autogen1')

    ultimo_email: str = ''
    for email_bruto in emails_para:
        ultimo_email = email_bruto.strip()

        input_para.send_keys(ultimo_email)
        time.sleep(1)

    span_para: WebElement = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//span[@class='select2-match' and "
            f"normalize-space(text())='{ultimo_email}']",
        ))
    )

    if span_para.text.strip() == ultimo_email:
        span_para.click()

    input_assunto: WebElement = driver.find_element(By.ID, 'txtAssunto')
    input_assunto.send_keys(assunto)

    input_mensagem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'txaMensagem'))
    )

    driver.execute_script(
        'arguments[0].value = arguments[1];', input_mensagem, corpo_email
    )

    fechar_popup_basico(driver, msg_contains='Informe a Mensagem.')

    selecionar_nivel_acesso(driver=driver, nivel_acesso=nivel_acesso)

    clicar_enviar_btnEnviar(driver)

    fechar_popup_basico(driver, msg_contains='E-mail enviado.')

    driver.switch_to.window(janela_principal)
