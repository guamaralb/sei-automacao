from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def fechar_popup_basico(driver, msg: str) -> None:
    print("FECHANDO")
    try:
        alert: Alert = WebDriverWait(driver, 5).until(
            EC.alert_is_present()
        )
        print("Texto alerta: ", alert.text)
        if msg in alert.text:
            alert.accept()

    except TimeoutException:
        pass