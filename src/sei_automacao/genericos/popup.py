from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def fechar_popup_basico(driver, msg_contains: str) -> None:
    try:
        alert: Alert = WebDriverWait(driver, 5).until(
            EC.alert_is_present()
        )

        if msg_contains in alert.text:
            alert.accept()

    except TimeoutException:
        pass