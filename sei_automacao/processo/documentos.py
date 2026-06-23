import time
import os

from pathlib import Path

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.utils.acesso import selecionar_nivel_acesso


def clicar_incluir_doc(driver: webdriver.Remote) -> None:
    img_incluir_doc: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='Incluir Documento']"))
    )
    img_incluir_doc.click()


def selecionar_tipo_doc(driver: webdriver.Remote, tipo: str) -> None:
    try:
        a_exibir_menos_tipos_doc: WebElement = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Exibir apenas os tipos já utilizados pela unidade']"))
        )

    except:
        a_exibir_todos_tipos_doc: WebElement = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Exibir todos os tipos']"))
        )
        a_exibir_todos_tipos_doc.click()

    xpath_tipo_doc: str = ""

    if tipo == "Externo":
        xpath_tipo_doc = "//tr[@data-desc=' externo']"
    elif tipo == "Memorando":
        xpath_tipo_doc = "//tr[@data-desc='memorando']"
    elif tipo == "Nota Técnica":
        xpath_tipo_doc = "//tr[@data-desc='nota tecnica']"
    else:
        raise Exception(f"Tipo de documento '{tipo}' não implementada")

    for _ in range(5):
        try:
            elemento: WebElement = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_tipo_doc))
            )
            elemento.click()
            return
        except StaleElementReferenceException:
            print("Elemento ficou stale ao escolher o tipo de documento. Recarregando e tentando novamente...")

    raise Exception("Não foi possível clicar no tipo de documento após várias tentativas (stale repetido).")


def preencher_metadados_doc_externo(
    driver: webdriver.Remote,
    tipo_doc: str,
    num: str,
    formato: str,
    data: str,
    path_anexo: Path,
    nivel_acesso: str,
    hipotese_legal: str = ""
) -> None:
    for _ in range(5):
        try:
            input_data: WebElement = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'txtDataElaboracao'))
            )
            input_data.send_keys(data)
            break
        except StaleElementReferenceException:
            print("Elemento ficou stale ao preencher a data do documento. Recarregando e tentando novamente...")
    else:
        raise Exception("Não foi possível preencher a data do documento após várias tentativas (stale repetido).")

    for _ in range(5):
        try:
            select_tipo_doc: Select = Select(driver.find_element(By.ID, 'selSerie'))
            select_tipo_doc.select_by_visible_text(tipo_doc)
            break
        except StaleElementReferenceException:
            print("Elemento ficou stale ao selecionar o tipo de documento. Recarregando e tentando novamente...")
    else:
        raise Exception("Não foi possível selecionar o tipo de documento após várias tentativas (stale repetido).")

    for _ in range(5):
        try:
            time.sleep(2)
            input_num: WebElement = driver.find_element(By.ID, 'txtNumero')
            input_num.send_keys(num)
            time.sleep(2)
            break
        except StaleElementReferenceException:
            print("Elemento ficou stale ao preencher o numero do documento. Recarregando e tentando novamente...")
    else:
        raise Exception("Não foi possível preencher o numero do documento após várias tentativas (stale repetido).")

    formato_XPATH: str = ''
    if formato == 'Nato-digital':
        formato_XPATH = '//*[@id="divOptNato"]/div/label'
    else:
        raise Exception(f'Opção de formato ainda não implementada: {formato}')

    for _ in range(5):
        try:
            label_formato: WebElement = driver.find_element(By.XPATH, formato_XPATH)
            label_formato.click()
            break
        except StaleElementReferenceException:
            print("Elemento ficou stale ao selecionar o formato do documento. Recarregando e tentando novamente...")
    else:
        raise Exception("Não foi possível selecionar o formato do documento após várias tentativas (stale repetido).")

    selecionar_nivel_acesso(driver, nivel_acesso, hipotese_legal)

    for _ in range(5):
        try:
            input_arq: WebElement = driver.find_element(By.ID, 'filArquivo')
            input_arq.send_keys(str(path_anexo))
            break
        except StaleElementReferenceException:
            print("Elemento ficou stale ao anexar o arquivo. Recarregando e tentando novamente...")
    else:
        raise Exception("Não foi possível anexar o arquivo após várias tentativas (stale repetido).")

    nome_arq: str = path_anexo.name

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//td/div[contains(text(), '{nome_arq}')]"))
    )


def preencher_metadados_doc_sei(driver: webdriver.Remote, nivel_acesso: str, hipotese_legal: str, nome: str = "") -> None:
    if not nome == "":
        input_nome: WebElement = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "txtNomeArvore"))
        )
        input_nome.send_keys(nome)

    selecionar_nivel_acesso(driver, nivel_acesso, hipotese_legal)


def inserir_conteudo_doc_sei_simples(driver: webdriver.Remote, texto: str) -> None:
    janela_principal: str = driver.current_window_handle

    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) == 2)
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break

    driver.switch_to.default_content()

    iframe_corpo: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@aria-describedby='cke_250']"))
    )
    driver.switch_to.frame(iframe_corpo)

    seletores: list[str] = [
        "p.Texto_Justificado_Recuo_Primeira_Linha",
        "p.Corpo_do_Texto",
        "p.Texto_Justificado",
        "body p"
    ]
    paragrafo: WebElement | None = None
    for seletor in seletores:
        try:
            paragrafo = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, seletor))
            )
            break
        except:
            continue

    if not paragrafo:
        driver.execute_script("""
            let p = document.createElement('p');
            document.body.appendChild(p);
        """)
        paragrafo = driver.find_element(By.CSS_SELECTOR, "body p:last-of-type")

    paragrafo.click()

    driver.execute_script(
        "arguments[0].innerHTML = arguments[1];",
        paragrafo,
        texto
    )

    driver.switch_to.default_content()
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(5)

    button_salvar_doc: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "cke_207"))
    )
    driver.execute_script("arguments[0].click();", button_salvar_doc)
    WebDriverWait(driver, 30).until(
        lambda d: "cke_button_off" in d.find_element(By.ID, "cke_207").get_attribute("class")
    )
    driver.close()
    driver.switch_to.window(janela_principal)


def inserir_conteudo_doc_sei_memo(driver: webdriver.Remote, vocativo: str, destinatario_nome: str, assunto: str, texto_principal: str) -> None:
    janela_principal: str = driver.current_window_handle
    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) == 2)
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break

    iframe_enderecamento: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Endereçamento']"))
    )
    driver.switch_to.frame(iframe_enderecamento)

    p_cargo: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '@cargo_destinatario@')]"))
    )
    p_cargo.clear()

    p_nome: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '@nome_destinatario@')]"))
    )
    driver.execute_script(
        f"arguments[0].innerHTML = arguments[0].innerHTML.replace('@nome_destinatario@', '{destinatario_nome}');", p_nome
    )

    driver.switch_to.default_content()

    iframe_assunto: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Assunto']"))
    )
    driver.switch_to.frame(iframe_assunto)

    strong_assunto: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[strong[contains(text(), 'Assunto:')]]"))
    )
    strong_assunto.send_keys(assunto)

    driver.switch_to.default_content()

    iframe_corpo: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Corpo do Texto']"))
    )
    driver.switch_to.frame(iframe_corpo)

    p_vocativo: WebElement = driver.find_element(By.XPATH, "//p[contains(text(), '@vocativo_destinatario@')]")
    driver.execute_script(
        f"arguments[0].innerHTML = arguments[0].innerHTML.replace('@vocativo_destinatario@', '{vocativo}');", p_vocativo
    )

    p_inserir_txt: WebElement = driver.find_element(
        By.XPATH, "//p[contains(text(), '[ Inserir Texto ]')]"
    )
    driver.execute_script(
        """
        arguments[0].innerHTML = arguments[1];
        """,
        p_inserir_txt,
        texto_principal
    )

    driver.switch_to.default_content()
    body: WebElement = driver.find_element(By.TAG_NAME, "body")
    body.click()
    time.sleep(5)

    button_salvar_doc: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[@id='cke_331' and @title='Salvar (Ctrl+Alt+S)']")
        )
    )

    driver.execute_script("arguments[0].click();", button_salvar_doc)

    WebDriverWait(driver, 30).until(
        lambda d: "cke_button_off" in d.find_element(By.ID, "cke_331").get_attribute("class")
    )

    driver.close()
    driver.switch_to.window(janela_principal)


def espera_documento_aparecer_arvore(driver: webdriver.Remote, tipo_doc: str, num: str = None) -> None:
    nome_arvore: str = None

    if num:
        nome_arvore = f'{tipo_doc} {num}'
    else:
        nome_arvore = tipo_doc

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{nome_arvore}')]"))
    )
