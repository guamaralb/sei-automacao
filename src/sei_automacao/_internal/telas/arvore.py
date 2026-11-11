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

from sei_automacao._internal.espera import TIMEOUT_PADRAO, xpath_literal
from sei_automacao._internal.iframes import trocar_iframe
from sei_automacao.exceptions import (
    AcaoNaoConcluida,
    DocumentoNaoEncontrado,
    ElementoNaoEncontrado,
)

# Árvores grandes demoram para abrir todas as pastas
_TIMEOUT_MIN_PASTAS: float = 30

_XPATH_ITENS_ARVORE = '//div[@class="infraArvore"]/a/span'
_PADRAO_NUM_PROCESSO = r'\d{4}\.\d{2}\.\d{7}/\d{4}-\d{2}'


def _xpath_pasta(img: str) -> str:
    return (
        f'//img[contains(@src, "{img}")]'
        '/parent::a/following-sibling::a[1]/span'
    )


def abrir_todas_pastas_arvore(driver: webdriver.Remote) -> int:
    """Deve ser chamada com o driver já no iframe da árvore."""
    pastas_fechadas_antes: list[WebElement] = driver.find_elements(
        By.XPATH, _xpath_pasta(img='processo_fechado.svg')
    )
    pastas_abertas_antes: list[WebElement] = driver.find_elements(
        By.XPATH, _xpath_pasta(img='processo_aberto.svg')
    )

    qnt_pastas_antes = len(pastas_fechadas_antes) + len(pastas_abertas_antes)

    for pasta in pastas_fechadas_antes:
        pasta.click()
        time.sleep(0.5)

    pastas_abertas_depois: list[WebElement] = driver.find_elements(
        By.XPATH, _xpath_pasta(img='processo_aberto.svg')
    )

    qnt_pastas_depois = len(pastas_abertas_depois)

    if qnt_pastas_antes != qnt_pastas_depois:
        raise AcaoNaoConcluida(
            'Identificado um número inconsistente de pastas na arvore'
        )

    return qnt_pastas_depois


def _esta_aguardando(arvore_elements: list[WebElement]) -> bool:
    return any(element.text == 'Aguarde...' for element in arvore_elements)


def espera_pastas_abrirem_e_retorna_elementos(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> list[WebElement]:
    limite = time.monotonic() + max(timeout, _TIMEOUT_MIN_PASTAS)
    while time.monotonic() < limite:
        try:
            arvore_elements = driver.find_elements(
                By.XPATH, _XPATH_ITENS_ARVORE
            )
            if not _esta_aguardando(arvore_elements):
                return arvore_elements
        except StaleElementReferenceException:
            pass  # a árvore recarregou no meio da leitura; tenta de novo
        time.sleep(0.5)

    raise TimeoutError('Pastas da árvore não terminaram de carregar.')


def listar_documentos_arvore(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> list[dict]:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore', timeout=timeout)

    abrir_todas_pastas_arvore(driver)

    # Só para esperar o "Aguarde..." sumir
    espera_pastas_abrirem_e_retorna_elementos(driver, timeout=timeout)

    xpath = f'{_XPATH_ITENS_ARVORE}[not(starts-with(@id, "spanPASTA"))]'

    # Busca de novo, agora sem as pastas
    itens = driver.find_elements(By.XPATH, xpath)

    # Remove o número do processo (primeiro item)
    itens = itens[1:]

    textos = [item.text for item in itens]

    if len(textos) % 2 != 0:
        raise AcaoNaoConcluida(
            f'Número ímpar de itens na árvore ({len(textos)}); '
            'esperado apenas duplas documento/unidade'
        )

    arvore_list: list[dict] = []

    for item_text_and_num, item_unidade in zip(textos[::2], textos[1::2]):
        try:
            item_text, item_num_com_parenteses = item_text_and_num.rsplit(
                ' ', 1
            )
            item_num = item_num_com_parenteses.strip('()')
        except ValueError:
            item_text = item_text_and_num.strip()
            item_num = 'Sem Numero'

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
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    if numero_sei is None and nome is None:
        raise ValueError('Informe numero_sei ou nome para a busca')

    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore', timeout=timeout)

    doc_element: WebElement | None = None
    for termo in (numero_sei, nome):
        if termo is None:
            continue
        try:
            doc_element = driver.find_element(
                By.XPATH,
                f'//a[span[contains(text(), {xpath_literal(termo)})]]',
            )
            break
        except NoSuchElementException:
            continue

    if doc_element is None:
        driver.switch_to.default_content()
        raise DocumentoNaoEncontrado(
            f'Documento não encontrado (numero_sei={numero_sei!r}, '
            f'nome={nome!r})'
        )

    doc_element.click()

    # Espera o iFrame do documento em si carregar
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrConteudoVisualizacao', timeout=timeout)
    trocar_iframe(driver, 'ifrVisualizacao', timeout=timeout)

    driver.switch_to.default_content()


def clicar_num_processo(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    driver.switch_to.default_content()

    trocar_iframe(driver, 'ifrArvore', timeout=timeout)

    spans: list[WebElement] = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, _XPATH_ITENS_ARVORE))
    )

    span_num_processo = next(
        (span for span in spans if re.search(_PADRAO_NUM_PROCESSO, span.text)),
        None,
    )

    if span_num_processo is None:
        driver.switch_to.default_content()
        raise ElementoNaoEncontrado(
            'Nenhum número de processo encontrado na árvore.'
        )

    span_num_processo.click()

    driver.switch_to.default_content()
