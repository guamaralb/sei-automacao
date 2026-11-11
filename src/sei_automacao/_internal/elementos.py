from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TipoBusca = Literal[
    'ID',
    'XPATH',
    'NAME',
    'CSS_SELECTOR',
    'CLASS_NAME',
    'TAG_NAME',
    'LINK_TEXT',
    'PARTIAL_LINK_TEXT',
]

_MAPA_BY: dict[str, str] = {
    'ID': By.ID,
    'XPATH': By.XPATH,
    'NAME': By.NAME,
    'CSS_SELECTOR': By.CSS_SELECTOR,
    'CLASS_NAME': By.CLASS_NAME,
    'TAG_NAME': By.TAG_NAME,
    'LINK_TEXT': By.LINK_TEXT,
    'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
}


def encontrar_elemento(
    driver: webdriver.Remote,
    tipo_busca: TipoBusca,
    termo_busca: str,
    timeout: float = 10,
) -> WebElement | None:
    try:
        by = _MAPA_BY[tipo_busca]
    except KeyError:
        raise ValueError(
            f'Tipo de busca inválido: {tipo_busca!r}. '
            f'Use um de: {", ".join(_MAPA_BY)}'
        ) from None

    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, termo_busca))
        )
    except TimeoutException:
        return None
