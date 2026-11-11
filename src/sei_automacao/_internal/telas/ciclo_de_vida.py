import logging

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO
from sei_automacao.exceptions import AcaoNaoConcluida

logger = logging.getLogger(__name__)


def _clicar_img_com_retentativa(
    driver: webdriver.Remote, alt: str, timeout: float
) -> None:
    for i in range(3):
        try:
            img: WebElement = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//img[@alt='{alt}']",
                ))
            )
            img.click()
            return
        except StaleElementReferenceException:
            logger.debug(
                "Clique em '%s' ficou stale na tentativa %d; tentando "
                'novamente',
                alt,
                i + 1,
            )

    raise AcaoNaoConcluida(f"Elemento '{alt}' ficou stale após 3 tentativas")


def clicar_img_reabrir_processo(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar_img_com_retentativa(driver, 'Reabrir Processo', timeout)


def clicar_img_concluir_processo(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    _clicar_img_com_retentativa(driver, 'Concluir Processo', timeout)
