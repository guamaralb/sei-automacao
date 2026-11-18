"""Barra de ações do documento selecionado (no iframe
``ifrConteudoVisualizacao``): cancelar e excluir."""

import logging

from selenium import webdriver
from selenium.common.exceptions import (
    NoAlertPresentException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sei_automacao._internal.espera import TIMEOUT_PADRAO, xpath_literal
from sei_automacao.exceptions import AcaoIndisponivel, AcaoNaoConcluida

logger = logging.getLogger(__name__)

ACAO_CANCELAR = 'Cancelar Documento'
ACAO_EXCLUIR = 'Excluir'

_XPATH_ACOES = '//a/img[@alt]'


def _xpath_acao(acao: str) -> str:
    return f'//img[@alt={xpath_literal(acao)}]/ancestor::a[1]'


def listar_acoes(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> set[str]:
    """Ações (``alt`` dos ícones) da barra do documento. Deve ser chamada com
    o driver no iframe ``ifrConteudoVisualizacao``."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, _XPATH_ACOES))
    )
    return {
        alt
        for img in driver.find_elements(By.XPATH, _XPATH_ACOES)
        if (alt := (img.get_attribute('alt') or '').strip())
    }


def clicar_acao(
    driver: webdriver.Remote, acao: str, *, timeout: float = TIMEOUT_PADRAO
) -> WebElement:
    """Clica na ação da barra do documento, sem esperar a ação aparecer:
    ausente, levanta :class:`AcaoIndisponivel` na hora (ex.: "Excluir" em
    documento assinado). Devolve o link clicado."""
    disponiveis = listar_acoes(driver, timeout=timeout)
    if acao not in disponiveis:
        raise AcaoIndisponivel(acao, disponiveis)
    link: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, _xpath_acao(acao)))
    )
    link.click()
    return link


def preencher_motivo_cancelamento(
    driver: webdriver.Remote,
    motivo: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> WebElement:
    """Deve ser chamada com o driver no iframe ``ifrVisualizacao``, onde
    abre o formulário "Cancelar Documento". Devolve o campo do motivo."""
    input_motivo: WebElement = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, 'txaMotivo'))
    )
    input_motivo.send_keys(motivo)
    return input_motivo


def confirmar_exclusao_doc(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    alerta: Alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
    alerta.accept()


def _alerta_ou_sumiu(elemento: WebElement):
    """Condição de espera: o alerta, se o SEI abrir um, ou ``True`` quando o
    ``elemento`` sai da página (a tela foi recarregada)."""

    def condicao(driver: webdriver.Remote) -> Alert | bool:
        try:
            return driver.switch_to.alert
        except NoAlertPresentException:
            pass
        try:
            elemento.is_enabled()
        except StaleElementReferenceException:
            return True
        return False

    return condicao


def esperar_tela_sair(
    driver: webdriver.Remote,
    elemento: WebElement,
    acao: str,
    *,
    exigir: bool = True,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    """Espera a tela da ação ser substituída (``elemento`` some). Se o SEI
    abrir um alerta no lugar (erro da ação), aceita e levanta
    :class:`AcaoNaoConcluida` com o texto dele. A tela que não sai no prazo
    também é :class:`AcaoNaoConcluida` com ``exigir``; sem ele, só vai para o
    log (quem chamou confere o resultado)."""
    try:
        resultado = WebDriverWait(driver, timeout).until(
            _alerta_ou_sumiu(elemento)
        )
    except TimeoutException:
        if exigir:
            raise AcaoNaoConcluida(
                f'{acao}: a tela não foi concluída no prazo'
            ) from None
        logger.debug('%s: a tela não saiu no prazo', acao)
        return
    if isinstance(resultado, Alert):
        texto = resultado.text
        resultado.accept()
        raise AcaoNaoConcluida(f'{acao}: o SEI recusou a ação ({texto})')
