import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO
from sei_automacao.exceptions import UnidadeSemAcessoException

logger = logging.getLogger(__name__)

_XPATH_SEM_ACESSO = (
    '//label[contains(text(), "Unidade atual não possui acesso ao processo")]'
)
_ID_IFRAME_PROCESSO = 'ifrConteudoVisualizacao'


def pesquisar_processo(
    driver: webdriver.Remote,
    num_processo: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    """Pesquisa o processo e espera a tela dele (ou a mensagem de sem
    acesso) carregar."""
    driver.switch_to.default_content()

    try:
        input_pesquisa: WebElement = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, 'txtPesquisaRapida'))
        )
    except TimeoutException:
        logger.error(
            '[%s] Pesquisa rápida não encontrada. URL: %s | Título: %s | '
            'Janelas: %s',
            num_processo,
            driver.current_url,
            driver.title,
            driver.window_handles,
        )
        raise

    driver.execute_script(
        'arguments[0].value = arguments[1];', input_pesquisa, num_processo
    )
    pagina_anterior: WebElement = driver.find_element(By.TAG_NAME, 'html')
    input_pesquisa.submit()

    espera = WebDriverWait(driver, timeout, poll_frequency=0.1)

    # Garante que a página da pesquisa carregou, para não encontrar o
    # iframe da página anterior (ex.: já estava em um processo).
    espera.until(EC.staleness_of(pagina_anterior))

    elemento: WebElement = espera.until(
        EC.any_of(
            EC.presence_of_element_located((By.XPATH, _XPATH_SEM_ACESSO)),
            EC.presence_of_element_located((By.ID, _ID_IFRAME_PROCESSO)),
        )
    )

    if elemento.get_attribute('id') != _ID_IFRAME_PROCESSO:
        raise UnidadeSemAcessoException(num_processo)

    elemento.is_displayed()
