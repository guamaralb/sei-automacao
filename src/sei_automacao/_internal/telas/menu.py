import logging
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO, xpath_literal
from sei_automacao.exceptions import AcaoNaoConcluida, ElementoNaoEncontrado

logger = logging.getLogger(__name__)


def abrir_menu(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    menu_lateral: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'divInfraAreaTelaE'))
    )
    classes: str = menu_lateral.get_attribute('class') or ''

    if 'infraAreaTelaEEscondeGrande' not in classes:
        return

    element: WebElement | None = driver.execute_script(
        'return document.querySelector("a#lnkInfraMenuSistema");'
    )
    if not element:
        raise ElementoNaoEncontrado('Não conseguiu abrir o menu')

    driver.execute_script('arguments[0].scrollIntoView();', element)
    driver.execute_script('arguments[0].click();', element)


def clicar_iniciar_processo(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    for index in range(3):
        try:
            span_iniciar_processo: WebElement = WebDriverWait(
                driver, timeout
            ).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(text(), 'Iniciar Processo')]",
                ))
            )
            span_iniciar_processo.click()

            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//label[contains(text(), 'Escolha o Tipo do Processo:')]",
                ))
            )
            return

        except WebDriverException as e:
            logger.warning(
                'Falha na tentativa %d/3 de iniciar processo: %s -> %s',
                index + 1,
                type(e).__name__,
                e,
            )
            time.sleep(2)

    raise AcaoNaoConcluida(
        "Falha ao clicar em 'Iniciar Processo' após várias tentativas"
    )


def selecionar_tipo_processo(
    driver: webdriver.Remote,
    tipo_processo: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    a_exibir_todos_tipos_processo: WebElement = WebDriverWait(
        driver, timeout
    ).until(EC.element_to_be_clickable((By.ID, 'ancExibirTiposProcedimento')))
    a_exibir_todos_tipos_processo.click()

    ultimo_erro: WebDriverException | None = None
    for _ in range(3):
        try:
            a_tipo_processo: WebElement = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//a[normalize-space(text())='
                    f'{xpath_literal(tipo_processo)}]',
                ))
            )
            a_tipo_processo.click()
            return

        except WebDriverException as e:
            ultimo_erro = e
            time.sleep(1)

    raise AcaoNaoConcluida(
        f"Não foi possível selecionar o tipo de processo '{tipo_processo}'"
    ) from ultimo_erro


def preencher_especificacao_processo(
    driver: webdriver.Remote,
    especificacao: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    input_espec: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'txtDescricao'))
    )
    input_espec.send_keys(especificacao)
