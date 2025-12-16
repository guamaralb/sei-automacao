from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By



def selecionar_excluir_doc(driver: webdriver.Chrome):
    img_excluir_doc = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Excluir']"))
    )
    img_excluir_doc.click()
    

def confirmar_exclusao_doc(driver: webdriver.Chrome):
    alerta = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alerta.accept()