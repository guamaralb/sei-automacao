from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def trocar_iframe(driver: webdriver.Remote, iframe: str) -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, iframe))
        )
    except:
        try:
            WebDriverWait(driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, iframe))
            )
        except:
            raise Exception(f"Iframe '{iframe}' não encontrado por ID nem por NAME")
