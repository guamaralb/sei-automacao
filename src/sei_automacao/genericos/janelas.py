import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

from sei_automacao.genericos.botoes import clicar_enviar_btnEnviar
from sei_automacao.genericos.popup import fechar_popup_basico

def identifica_abertura_nova_janela(driver: webdriver.Remote, num_janelas_esperadas: int = 2) -> bool:

	WebDriverWait(driver, 20).until(
		lambda d: len(d.window_handles) == num_janelas_esperadas
	)

	return True
