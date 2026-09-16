from typing import Literal

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TipoBusca = Literal['id', 'name', 'xpath']


def trocar_iframe(
    driver: webdriver.Remote,
    iframe: str,
    tipo_busca: TipoBusca | None = None,
    timeout: float = 1,
) -> None:
    estrategias: dict[TipoBusca, tuple[str, str]] = {
        'id': (By.ID, iframe),
        'name': (By.NAME, iframe),
        'xpath': (By.XPATH, f'//iframe[@title="{iframe}"]'),
    }

    ordem = [tipo_busca] if tipo_busca else ['id', 'name', 'xpath']

    for tipo in ordem:
        try:
            WebDriverWait(driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(estrategias[tipo])
            )
            return
        except TimeoutException:
            continue

    tentativas = tipo_busca or ', '.join(estrategias)
    raise ValueError(f'iFrame "{iframe}" não encontrado por: {tentativas}')
