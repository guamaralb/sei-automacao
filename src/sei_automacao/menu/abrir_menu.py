from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def abrir_menu(driver: webdriver.Remote) -> None:
    menu_lateral: WebElement = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "divInfraAreaTelaE"))
    )
    classes: str = menu_lateral.get_attribute("class")

    if "infraAreaTelaEEscondeGrande" in classes:
        element: WebElement | None = driver.execute_script("""
            return document.querySelector("a#lnkInfraMenuSistema");
        """)

        if element:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.execute_script("arguments[0].click();", element)
            return

        else:
            raise Exception("Não conseguiu abrir o menu")
