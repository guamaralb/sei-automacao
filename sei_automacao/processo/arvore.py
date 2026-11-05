import re
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao.core.iframes import trocar_iframe


def abrir_todas_pastas_arvore(driver: webdriver.Remote) -> None:
    """
    Função deve ser chamada sempre dentro de "listar_documentos_arvore"
    """

    def xpath_pasta(img: str):
        return (
            f'//img[contains(@src, "{img}")]'
            '/parent::a/following-sibling::a[1]/span'
        )

    pastas_fechadas_antes: list[WebElement] = driver.find_elements(
        By.XPATH, xpath_pasta(img='processo_fechado.svg')
    )
    pastas_abertas_antes: list[WebElement] = driver.find_elements(
        By.XPATH, xpath_pasta(img='processo_aberto.svg')
    )

    qnt_pastas_antes = len(pastas_fechadas_antes) + len(pastas_abertas_antes)

    print('len(pastas_fechadas_antes):', len(pastas_fechadas_antes))
    print('len(pastas_abertas_antes):', len(pastas_abertas_antes))
    print('qnt_pastas_antes:', qnt_pastas_antes)

    for pasta in pastas_fechadas_antes:
        pasta.click()
        time.sleep(0.5)

    pastas_abertas_depois: list[WebElement] = driver.find_elements(
        By.XPATH, xpath_pasta(img='processo_aberto.svg')
    )

    qnt_pastas_depois = len(pastas_abertas_depois)

    print('len(pastas_abertas_depois):', len(pastas_abertas_depois))

    if qnt_pastas_antes != qnt_pastas_depois:
        raise Exception(
            'Identificado um número inconsistente de pastas na arvore'
        )

    return qnt_pastas_depois


def verifica_esta_aguardando(arvore_elements: list[WebElement]) -> bool:
    aguardando = False
    for i, element in enumerate(arvore_elements):
        texto = element.text
        print(f'{i}: {texto!r}')
        if texto == 'Aguarde...':
            aguardando = True
    return aguardando


def espera_pastas_abrirem_e_retorna_elementos(
    driver: webdriver.Remote, timeout: float = 30
) -> list[WebElement]:
    limite = time.monotonic() + timeout
    while time.monotonic() < limite:
        try:
            arvore_elements = driver.find_elements(
                By.XPATH, '//div[@class="infraArvore"]/a/span'
            )
            if not verifica_esta_aguardando(arvore_elements):
                return arvore_elements
        except StaleElementReferenceException:
            pass  # a árvore recarregou no meio da leitura; tenta de novo
        time.sleep(0.5)

    raise TimeoutError('Pastas da árvore não terminaram de carregar.')


def listar_documentos_arvore(driver: webdriver.Remote) -> list[dict]:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')

    abrir_todas_pastas_arvore(driver)

    # Só para esperar o "Aguarde..." sumir
    espera_pastas_abrirem_e_retorna_elementos(driver)

    xpath = (
        '//div[@class="infraArvore"]/a/span'
        '[not(starts-with(@id, "spanPASTA"))]'
    )

    # Busca de novo, agora sem as pastas
    itens = driver.find_elements(By.XPATH, xpath)

    # Remove o número do processo (primeiro item)
    itens = itens[1:]

    textos = [item.text for item in itens]

    if len(textos) % 2 != 0:
        raise Exception(
            f'Número ímpar de itens na árvore ({len(textos)}); '
            'esperado apenas duplas documento/unidade'
        )

    arvore_list: list[dict] = []

    for item_text_and_num, item_unidade in zip(textos[::2], textos[1::2]):
        item_text, item_num_com_parenteses = item_text_and_num.rsplit(' ', 1)
        item_num = item_num_com_parenteses.strip('()')

        arvore_list.append({
            'numero_sei': item_num,
            'nome_arvore': item_text,
            'unidade': item_unidade,
        })

    return arvore_list


def selecionar_doc_arvore(
    driver: webdriver.Remote,
    numero_sei: str | None = None,
    nome: str | None = None,
) -> None:
    if numero_sei is None and nome is None:
        raise Exception('Nenhum termo inserido para busca')

    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore')

    doc_element: WebElement = None

    try:
        doc_element = driver.find_element(
            By.XPATH, f'//a[span[contains(text(), "{numero_sei}")]]'
        )

    except NoSuchElementException:
        try:
            doc_element = driver.find_element(
                By.XPATH, f'//a[span[contains(text(), "{nome}")]]'
            )

        except NoSuchElementException:
            raise Exception('Documento não encontrado')

    doc_element.click()

    # Espera o iFrame do documento em si carregar
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao')
    trocar_iframe(driver, 'ifrVisualizacao')

    driver.switch_to.default_content()


def clicar_num_processo(driver: webdriver.Remote) -> None:
    driver.switch_to.default_content()

    trocar_iframe(driver=driver, iframe='ifrArvore')

    padrao_processo = r'\d{4}\.\d{2}\.\d{7}/\d{4}-\d{2}'

    spans: list[WebElement] = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.XPATH,
            '//div[@class="infraArvore"]/a/span',
        ))
    )

    span_num_processo = next(
        (span for span in spans if re.search(padrao_processo, span.text)), None
    )

    if span_num_processo is None:
        raise ValueError(
            'Nenhum número de processo encontrado no padrão informado.'
        )

    span_num_processo.click()

    driver.switch_to.default_content()
