from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def identifica_abertura_nova_janela(driver: webdriver.Remote, num_janelas_esperadas: int = 2) -> bool:
    WebDriverWait(driver, 20).until(
        lambda d: len(d.window_handles) == num_janelas_esperadas
    )
    return True
