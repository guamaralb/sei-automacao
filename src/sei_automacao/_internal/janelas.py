from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO


def identifica_abertura_nova_janela(
    driver: webdriver.Remote,
    num_janelas_esperadas: int = 2,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> bool:
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.window_handles) == num_janelas_esperadas
    )
    return True
