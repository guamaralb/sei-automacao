"""Fluxo básico no SEI real. Rode com ``pytest -m integracao``.

Precisa de um .env com SEI_URL, SEI_LOGIN, SEI_SENHA, SEI_ORGAO e
SEI_UNIDADE.
"""

import os

import pytest

from sei_automacao import efetuar_login, iniciar_sei, trocar_unidade

pytestmark = pytest.mark.integracao

_VARIAVEIS = ('SEI_URL', 'SEI_LOGIN', 'SEI_SENHA', 'SEI_ORGAO', 'SEI_UNIDADE')


@pytest.fixture
def driver():
    dotenv = pytest.importorskip('dotenv')
    dotenv.load_dotenv()
    faltando = [v for v in _VARIAVEIS if not os.getenv(v)]
    if faltando:
        pytest.skip(f'Variáveis ausentes no .env: {faltando}')

    driver = iniciar_sei(os.environ['SEI_URL'])
    yield driver
    driver.quit()


def test_login_e_troca_de_unidade(driver):
    efetuar_login(
        driver,
        os.environ['SEI_LOGIN'],
        os.environ['SEI_SENHA'],
        os.environ['SEI_ORGAO'],
    )
    trocar_unidade(driver, os.environ['SEI_UNIDADE'])
