from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def selecionar_nivel_acesso(driver: webdriver.Chrome, nivel_acesso: str, hipotese_legal: str = ""):
    id_nivel_acesso = ""
    
    if nivel_acesso == "Restrito":
        id_nivel_acesso = "divOptRestrito"
    elif nivel_acesso == "Público":
        id_nivel_acesso = "divOptPublico"
    elif nivel_acesso == "Sigiloso":
        id_nivel_acesso == "divOptSigiloso"
    else:
        raise Exception(f"Nivel de acesso '{nivel_acesso}' inexistente ou não implementado")
        
    try:
        for _ in range(5):
            try:
                input_nivel_acesso = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@id='{id_nivel_acesso}']/div/label"))
                )
                input_nivel_acesso.click()
                
                break
            except StaleElementReferenceException:
                print("Elemento ficou stale ao selecionar o nivel de acesso. Recarregando e tentando novamente...")
                
    # 4. Se falhar todas as tentativas:
    except:
        raise Exception("Não foi possível selecionar o nivel de acesso após várias tentativas (stale repetido).")

    if not nivel_acesso == "Público":
        if hipotese_legal == "":
            raise Exception("Hipotese Legal não informada")
        
        # Espera carregar mais opções dentro do select
        WebDriverWait(driver, 15).until(
            lambda d: len(Select(d.find_element(By.ID, "selHipoteseLegal")).options) > 1
        )
        
        select_hip_legal = Select(driver.find_element(By.ID, "selHipoteseLegal"))
        select_hip_legal.select_by_visible_text(hipotese_legal)
        
        try:
            for _ in range(5):
                try:
                    select_hip_legal = Select(driver.find_element(By.ID, "selHipoteseLegal"))
                    select_hip_legal.select_by_visible_text(hipotese_legal)
                    
                    break

                except StaleElementReferenceException:
                    print("Elemento ficou stale ao selecionar a hipotese legal. Recarregando e tentando novamente...")

        # 4. Se falhar todas as tentativas:
        except:
            raise Exception("Não foi possível selecionar a hipotese legal após várias tentativas (stale repetido).")

