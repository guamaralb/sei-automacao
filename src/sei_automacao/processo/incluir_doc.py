import time
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.utils.selecionar_nivel_acesso import selecionar_nivel_acesso


def clicar_incluir_doc(driver: webdriver.Chrome):
    img_incluir_doc = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='Incluir Documento']"))
    )
    img_incluir_doc.click()


def selecionar_tipo_doc(driver: webdriver.Chrome, tipo: str):
    try:
        a_exibir_menos_tipos_doc = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Exibir apenas os tipos já utilizados pela unidade']"))   
        )
    
    except:
        a_exibir_todos_tipos_doc = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Exibir todos os tipos']"))   
        )
        a_exibir_todos_tipos_doc.click()
    
    xpath_tipo_doc = ""
    
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
            elemento = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_tipo_doc))
            )
            elemento.click()
            return  # sucesso
        except StaleElementReferenceException:
            print("Elemento ficou stale ao escolher o tipo de documento. Recarregando e tentando novamente...")

    # 4. Se falhar todas as tentativas:
    raise Exception("Não foi possível clicar no tipo de documento após várias tentativas (stale repetido).")


def preencher_metadados_doc_externo(
    driver: webdriver.Chrome,
    tipo_doc: str,
    num: str,
    formato: str,
    data: str,
    caminho_anexo: str,
    nivel_acesso: str,
    hipotese_legal: str = ""
):
    try:
        for _ in range(5):
            try:
                input_data = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'txtDataElaboracao'))
                )
                input_data.send_keys(data)
                
                break

            except StaleElementReferenceException:
                print("Elemento ficou stale ao preencher a data do documento. Recarregando e tentando novamente...")

    except:
        raise Exception("Não foi possível preencher a data do documento após várias tentativas (stale repetido).")

    # Seleciona tipo de documento
    try:
        for _ in range(5):
            try:
                select_tipo_doc = Select(driver.find_element(By.ID, 'selSerie'))
                select_tipo_doc.select_by_visible_text(tipo_doc)
                
                break

            except StaleElementReferenceException:
                print("Elemento ficou stale ao selecionar o tipo de documento. Recarregando e tentando novamente...")

    except:
        raise Exception("Não foi possível selecionar o tipo de documento após várias tentativas (stale repetido).")

    # Preenche número
    try:
        for _ in range(5):
            try:
                time.sleep(2)
                input_num = driver.find_element(By.ID, 'txtNumero')
                input_num.send_keys(num)
                time.sleep(2)
                
                break

            except StaleElementReferenceException:
                print("Elemento ficou stale ao preencher o numero do documento. Recarregando e tentando novamente...")

    except:
        raise Exception("Não foi possível preencher o numero do documento após várias tentativas (stale repetido).")

    # Seleciona formato
    formato_XPATH = ''
    if formato == 'Nato-digital':
        formato_XPATH = '//*[@id="divOptNato"]/div/label'
    else:
        raise Exception(f'Opção de formato ainda não implementada: {formato}')
    
    try:
        for _ in range(5):
            try:
                input_formato = driver.find_element(By.XPATH, formato_XPATH)
                input_formato.click()
                
                break

            except StaleElementReferenceException:
                print("Elemento ficou stale ao selecionar o formato do documento. Recarregando e tentando novamente...")

    except:
        raise Exception("Não foi possível selecionar o formato do documento após várias tentativas (stale repetido).")

    # Seleciona nivel de acesso
    selecionar_nivel_acesso(driver, nivel_acesso, hipotese_legal)
        
    # Anexa arquivo
    try:
        for _ in range(5):
            try:
                input_arq = driver.find_element(By.ID, 'filArquivo')
                input_arq.send_keys(caminho_anexo)
                
                break

            except StaleElementReferenceException:
                print("Elemento ficou stale ao anexar o arquivo. Recarregando e tentando novamente...")

    # 4. Se falhar todas as tentativas:
    except:
        raise Exception("Não foi possível anexar o arquivo após várias tentativas (stale repetido).")

    # Espera o arquivo anexo carregar
    nome_arq = os.path.basename(caminho_anexo)
    
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//td/div[contains(text(), '{nome_arq}')]"))
    )
    

def preencher_metadados_doc_sei(driver: webdriver.Chrome, nivel_acesso: str, hipotese_legal: str, nome: str = ""):
    if not nome == "":
        # Preenche nome na arvore
        input_nome = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "txtNomeArvore"))
        )
        input_nome.send_keys(nome)
        
    selecionar_nivel_acesso(driver, nivel_acesso, hipotese_legal)
    

def inserir_conteudo_doc_sei_simples(driver: webdriver.Chrome, texto: str):
    janela_principal = driver.current_window_handle
    
    # Espera abrir a janela do editor e muda para ela
    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) == 2)
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break
        
    driver.switch_to.default_content()
    
    # Seleciona o iframe CORRETO pelo aria-describedby
    iframe_corpo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@aria-describedby='cke_250']"))
    )
    driver.switch_to.frame(iframe_corpo)
    
    # Tenta localizar o primeiro parágrafo válido
    seletores = [
        "p.Texto_Justificado_Recuo_Primeira_Linha",
        "p.Corpo_do_Texto",
        "p.Texto_Justificado",
        "body p"
    ]
    paragrafo = None
    for seletor in seletores:
        try:
            paragrafo = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, seletor))
            )
            break
        except:
            continue

    # Se não achou nenhum <p>, cria um
    if not paragrafo:
        driver.execute_script("""
            let p = document.createElement('p');
            document.body.appendChild(p);
        """)
        paragrafo = driver.find_element(By.CSS_SELECTOR, "body p:last-of-type")
        
    # Ativa o cursor
    paragrafo.click()
    
    # Substitui apenas o conteúdo do parágrafo
    driver.execute_script(
        "arguments[0].innerHTML = arguments[1];",
        paragrafo,
        texto
    )
    
    # volta ao documento externo
    driver.switch_to.default_content()
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(5)
    
    # Salvar documento
    button_salvar_doc = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "cke_207"))
    )
    driver.execute_script("arguments[0].click();", button_salvar_doc)
    WebDriverWait(driver, 30).until(
        lambda d: "cke_button_off" in d.find_element(By.ID, "cke_207").get_attribute("class")
    )
    driver.close()
    driver.switch_to.window(janela_principal)


def inserir_conteudo_doc_sei_memo(driver: webdriver.Chrome, vocativo: str, destinatario: str, assunto: str, texto_principal: str):
    # Muda para a nova janela
    janela_principal = driver.current_window_handle
    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) == 2)
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break
        
    # Altera a barra de nome e cargo do destinatário
    iframe_enderecamento = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Endereçamento']"))
    )
    driver.switch_to.frame(iframe_enderecamento)
    
    p_cargo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '@cargo_destinatario@')]"))
    )
    p_cargo.clear()
    
    p_nome = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '@nome_destinatario@')]"))
    )
    driver.execute_script(
        f"arguments[0].innerHTML = arguments[0].innerHTML.replace('@nome_destinatario@', '{destinatario}');", p_nome
    )
    
    driver.switch_to.default_content()
    
    # Altera assunto   
    iframe_assunto = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Assunto']"))
    )
    driver.switch_to.frame(iframe_assunto)
    
    strong_assunto = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[strong[contains(text(), 'Assunto:')]]"))
    )
    strong_assunto.send_keys(assunto)
    
    driver.switch_to.default_content()
    
    # Altera o texto do corpo do memorando
    iframe_corpo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='Corpo do Texto']"))
    )
    driver.switch_to.frame(iframe_corpo)
       
    p_vocativo = driver.find_element(By.XPATH, "//p[contains(text(), '@vocativo_destinatario@')]")
    driver.execute_script(
        f"arguments[0].innerHTML = arguments[0].innerHTML.replace('@vocativo_destinatario@', '{vocativo}');", p_vocativo
    )
    
    p_inserir_txt = driver.find_element(
        By.XPATH, "//p[contains(text(), '[ Inserir Texto ]')]"
    )

    driver.execute_script(
        """
        arguments[0].innerHTML = arguments[1];
        """,
        p_inserir_txt,
        texto_principal
    )
    
    # Clica e ativa a barra de ferramentas do editor
    driver.switch_to.default_content()
    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    time.sleep(5)
    
    # Espera o botão salvar aparecer
    button_salvar_doc = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[@id='cke_331' and @title='Salvar (Ctrl+Alt+S)']")
        )
    )
    
    # Clica usando JavaScript para evitar ElementNotInteractable
    driver.execute_script("arguments[0].click();", button_salvar_doc)
    
    # Espera salvar o documento
    WebDriverWait(driver, 30).until(
        lambda d: "cke_button_off" in d.find_element(By.ID, "cke_331").get_attribute("class")
    )
    
    driver.close()
    
    driver.switch_to.window(janela_principal)
