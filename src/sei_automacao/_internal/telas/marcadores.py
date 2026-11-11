from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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
from sei_automacao.exceptions import MarcadorNaoEncontrado


def _xpath_linha_marcador(marcador: str) -> str:
    return (
        '//tbody/tr/td[contains(normalize-space(.), '
        f'{xpath_literal(marcador)})]'
    )


def normalizar_espacos(texto: str) -> str:
    """Equivalente ao ``normalize-space()`` do XPath."""
    return ' '.join(texto.split())


def clicar_gerenciar_marcadores(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    driver.switch_to.default_content()
    trocar_iframe(
        driver, 'ifrConteudoVisualizacao', tipo_busca='id', timeout=timeout
    )

    a_gerenciar_marcadores: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//img[@alt='Gerenciar Marcador']/ancestor::a[1]",
        ))
    )
    a_gerenciar_marcadores.click()


def listar_marcadores_arvore(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> list[str]:
    driver.switch_to.default_content()
    trocar_iframe(driver, 'ifrArvore', timeout=timeout)

    lista_marcadores: list[str] = []

    imgs = driver.find_elements(
        By.XPATH, '//a/img[contains(@title, "Marcador")]'
    )
    for img in imgs:
        title = img.get_attribute('title') or ''
        nome_marcador = title.split('\n', 1)[-1].strip()
        lista_marcadores.append(nome_marcador)

    driver.switch_to.default_content()

    return lista_marcadores


def procurar_sbmSalvar(driver: webdriver.Remote) -> bool:
    return bool(driver.find_elements(By.ID, 'sbmSalvar'))


def ler_opcoes_marcador(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> set[str]:
    """Nomes da lista suspensa de marcadores (tela de adicionar marcador)."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#selMarcador'))
    )
    opcoes = driver.find_elements(
        By.CSS_SELECTOR, '#selMarcador label.dd-option-text'
    )
    return {
        normalizar_espacos(o.get_attribute('textContent') or '')
        for o in opcoes
    } - {''}


def selecionar_marcador_lista_suspensa(
    driver: webdriver.Remote,
    marcador: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    dropdown: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#selMarcador .dd-select',
        ))
    )
    dropdown.click()

    opcao: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//label[@class='dd-option-text' and "
            f'normalize-space(text())={xpath_literal(marcador)}]',
        ))
    )
    opcao.click()

    # Esperar o selecionado aparecer
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//label[@class='dd-selected-text' and "
            f'normalize-space(text())={xpath_literal(marcador)}]',
        ))
    )


def esperar_marcador_aparecer_apos_salvar(
    driver: webdriver.Remote,
    marcador: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                _xpath_linha_marcador(marcador),
            ))
        )
    except TimeoutException:
        raise MarcadorNaoEncontrado(
            f'Marcador "{marcador}" não encontrado após salvar'
        ) from None


def selecionar_marcador_checkbox(
    driver: webdriver.Remote,
    marcador: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    xpath = (
        f'//tr[td[2]//img[@title={xpath_literal(marcador)}]]'
        "//input[@type='checkbox']"
    )

    checkbox: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    if not checkbox.is_selected():
        driver.execute_script('arguments[0].click();', checkbox)


def esperar_marcador_sumir_apos_salvar(
    driver: webdriver.Remote, marcador: str
) -> None:
    """Levanta :class:`MarcadorNaoEncontrado` se o marcador ainda estiver
    na tabela depois de :data:`TIMEOUT_SONDAGEM` segundos."""
    try:
        WebDriverWait(driver, TIMEOUT_SONDAGEM).until(
            EC.invisibility_of_element_located((
                By.XPATH,
                # Mesma linha usada para marcar o checkbox (título exato do
                # marcador), para não confundir com marcadores de nome
                # parecido
                f'//tr[td[2]//img[@title={xpath_literal(marcador)}]]',
            ))
        )
    except TimeoutException:
        raise MarcadorNaoEncontrado(
            f'Marcador "{marcador}" continua no processo após remover'
        ) from None
