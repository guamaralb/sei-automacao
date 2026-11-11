from unittest.mock import MagicMock

import pytest
from selenium.common.exceptions import WebDriverException

from sei_automacao import navegador
from sei_automacao._internal.espera import xpath_literal


@pytest.fixture
def driver_falso(monkeypatch, tmp_path):
    driver = MagicMock(name='driver')
    driver.execute_script.return_value = 'complete'
    monkeypatch.setattr(navegador, '_criar_driver', lambda tipo, prefs: driver)
    return driver


def test_iniciar_sei_abre_a_url(driver_falso, tmp_path):
    resultado = navegador.iniciar_sei(
        'https://sei.exemplo.gov.br', download_dir=tmp_path / 'downloads'
    )
    assert resultado is driver_falso
    driver_falso.get.assert_called_once_with('https://sei.exemplo.gov.br')
    driver_falso.quit.assert_not_called()
    assert (tmp_path / 'downloads').is_dir()


def test_iniciar_sei_fecha_o_navegador_se_falhar(driver_falso, tmp_path):
    driver_falso.get.side_effect = WebDriverException('sem rede')
    with pytest.raises(WebDriverException):
        navegador.iniciar_sei(
            'https://sei.exemplo.gov.br', download_dir=tmp_path
        )
    driver_falso.quit.assert_called_once()


def test_driver_type_invalido():
    with pytest.raises(ValueError, match='driver_type'):
        navegador._criar_driver('firefox', {})


@pytest.mark.parametrize(
    ('texto', 'esperado'),
    [
        ('simples', "'simples'"),
        ("d'água", '"d\'água"'),
        ('a"b\'c', "concat('a\"b', \"'\", 'c')"),
    ],
)
def test_xpath_literal(texto, esperado):
    assert xpath_literal(texto) == esperado
