import logging
import re
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import (
    TIMEOUT_PADRAO,
    TIMEOUT_SONDAGEM,
    xpath_literal,
)
from sei_automacao._internal.iframes import trocar_iframe
from sei_automacao.exceptions import (
    AcaoNaoConcluida,
    DocumentoNaoEncontrado,
    DocumentoSemConteudo,
    ElementoNaoEncontrado,
    IframeNaoEncontrado,
)

logger = logging.getLogger(__name__)

# Árvores grandes demoram para abrir todas as pastas
_TIMEOUT_MIN_PASTAS: float = 30

_XPATH_ITENS_ARVORE = '//div[@class="infraArvore"]/a/span'
_PADRAO_NUM_PROCESSO = r'\d{4}\.\d{2}\.\d{7}/\d{4}-\d{2}'


def _xpath_pasta(img: str) -> str:
    return (
        f'//img[contains(@src, "{img}")]'
        '/parent::a/following-sibling::a[1]/span'
    )


def _pastas(driver: webdriver.Remote, img: str) -> list[WebElement]:
    return driver.find_elements(By.XPATH, _xpath_pasta(img=img))


def abrir_todas_pastas_arvore(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> int:
    """Abre as pastas fechadas da árvore e espera todas ficarem abertas.
    Deve ser chamada com o driver já no iframe da árvore.

    A árvore pode estar recarregando (ex.: logo depois de cancelar ou
    excluir um documento): espera o "Aguarde..." sumir antes de contar e,
    se ela recarregar no meio, recomeça. Levanta :class:`AcaoNaoConcluida`
    se sobrar pasta fechada depois do prazo."""
    limite = time.monotonic() + max(timeout, _TIMEOUT_MIN_PASTAS)
    clicadas = False
    while True:
        try:
            espera_pastas_abrirem_e_retorna_elementos(driver, timeout=timeout)
            fechadas = _pastas(driver, 'processo_fechado.svg')
            if len(fechadas) == 0:  # lista (também no driver falso dos testes)
                return len(_pastas(driver, 'processo_aberto.svg'))
            # Clica uma vez; nas voltas seguintes só espera as pastas
            # abrirem (clicar de novo fecharia a pasta que está abrindo)
            if not clicadas:
                for pasta in fechadas:
                    pasta.click()
                    time.sleep(0.5)
                clicadas = True
        except StaleElementReferenceException:
            # A árvore recarregou: as pastas voltam fechadas
            clicadas = False
        if time.monotonic() >= limite:
            raise AcaoNaoConcluida(
                'Identificado um número inconsistente de pastas na arvore: '
                'pasta(s) que não abriu(ram) no prazo'
            )
        time.sleep(0.5)


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

    abrir_todas_pastas_arvore(driver, timeout=timeout)

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


def html_do_iframe(driver: webdriver.Remote, iframe: str) -> WebElement | None:
    """O ``<html>`` atual do iframe, para esperar ele recarregar
    (:func:`esperar_iframe_recarregar`). ``None`` se o iframe não existe.
    Termina no ``default_content``."""
    driver.switch_to.default_content()
    try:
        trocar_iframe(driver, iframe, timeout=TIMEOUT_SONDAGEM)
    except IframeNaoEncontrado:
        return None
    html = driver.find_element(By.TAG_NAME, 'html')
    driver.switch_to.default_content()
    return html


def esperar_iframe_recarregar(
    driver: webdriver.Remote,
    iframe: str,
    html_antigo: WebElement | None,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> bool:
    """Entra no ``iframe`` e espera a página antiga (``html_antigo``, de
    :func:`html_do_iframe`) sair e a nova terminar de carregar. ``False`` se
    a página não mudou no prazo (o driver fica no iframe do mesmo jeito)."""
    driver.switch_to.default_content()
    trocar_iframe(driver, iframe, timeout=timeout)
    if html_antigo is not None:
        try:
            WebDriverWait(driver, timeout).until(EC.staleness_of(html_antigo))
        except TimeoutException:
            logger.debug('iFrame "%s" não recarregou no prazo', iframe)
            return False
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    return True


def esperar_arvore_recarregar(
    driver: webdriver.Remote,
    html_antigo: WebElement | None,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    """Depois de uma ação que recarrega a árvore (cancelar, excluir): espera
    a árvore nova e o "Aguarde..." sumir. Termina no ``default_content``."""
    if not esperar_iframe_recarregar(
        driver, 'ifrArvore', html_antigo, timeout=timeout
    ):
        logger.debug('A árvore não recarregou depois da ação')
    espera_pastas_abrirem_e_retorna_elementos(driver, timeout=timeout)
    driver.switch_to.default_content()


def _tem_ifr_visualizacao(driver: webdriver.Remote) -> bool:
    return bool(
        driver.find_elements(
            By.XPATH,
            '//iframe[@id="ifrVisualizacao" or @name="ifrVisualizacao"]',
        )
    )


def selecionar_doc_arvore(
    driver: webdriver.Remote,
    numero_sei: str | None = None,
    nome: str | None = None,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    if numero_sei is None and nome is None:
        raise ValueError('Informe numero_sei ou nome para a busca')

    # Página que está aberta: depois do clique, espera ela ser substituída
    # (senão o iframe do documento anterior passaria pelo do clicado)
    conteudo_antigo = html_do_iframe(driver, 'ifrConteudoVisualizacao')

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

    # Espera a página do documento clicado carregar e o iFrame do documento
    # em si. Sem ele (ex.: documento cancelado), DocumentoSemConteudo
    esperar_iframe_recarregar(
        driver, 'ifrConteudoVisualizacao', conteudo_antigo, timeout=timeout
    )
    if not _tem_ifr_visualizacao(driver):
        driver.switch_to.default_content()
        raise DocumentoSemConteudo(
            f'Documento sem conteúdo para exibir (numero_sei={numero_sei!r}, '
            f'nome={nome!r}): cancelado?'
        )
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
