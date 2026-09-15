from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def trocar_iframe(driver: webdriver.Remote, iframe: str) -> None:
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, iframe))
        )
    except TimeoutException:
        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, iframe))
            )
        except TimeoutException:
            try:
                WebDriverWait(driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((
                        By.XPATH,
                        f'//iframe[@title="{iframe}"]',
                    ))
                )
            except TimeoutException:
                raise Exception(
                    f"Iframe '{iframe}' não encontrado por ID, NAME nem TITLE"
                )
