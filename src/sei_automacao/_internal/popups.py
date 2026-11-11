from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO


def fechar_popup_basico(
    driver: webdriver.Remote,
    msg_contains: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    try:
        alert: Alert = WebDriverWait(driver, timeout).until(
            EC.alert_is_present()
        )

        if msg_contains in alert.text:
            alert.accept()

    except TimeoutException:
        pass
