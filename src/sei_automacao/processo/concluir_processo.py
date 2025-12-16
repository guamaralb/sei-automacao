from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By


def clicar_img_concluir_processo(driver):
    for i in range(3):
        try:        
            img_concluir_processo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Concluir Processo']"))
            )
            img_concluir_processo.click()
            return
            
        except:
            print(f"Clique na img_concluir_processo ficou stale na tentativa {i}. Tentando novamente...")
            continue
    
    raise Exception("Elemento img_concluir_processo ficou stale após 3 tentativas")