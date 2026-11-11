import logging
import time
from collections.abc import Callable
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from sei_automacao._internal.espera import (
    TIMEOUT_PADRAO,
    TIMEOUT_SONDAGEM,
    xpath_literal,
)
from sei_automacao._internal.iframes import (
    localizar_xpath_elemento_com_fallback_iframe,
)
from sei_automacao._internal.nivel_acesso import (
    NivelAcesso,
    selecionar_nivel_acesso,
)
from sei_automacao.exceptions import AcaoNaoConcluida, OpcaoNaoSuportada

logger = logging.getLogger(__name__)

NUM_JANELAS_COM_POPUP = 2

# Upload do anexo e gravação do editor podem demorar
_TIMEOUT_MIN_SALVAR: float = 30
# A tela de tipos mostra o link "exibir apenas..." logo que carrega
_TIMEOUT_SONDAGEM_TIPOS: float = 2

_XPATH_TIPOS_DOC: dict[str, str] = {
    'Externo': "//tr[@data-desc=' externo']",
    'Memorando': "//tr[@data-desc='memorando']",
    'Nota Técnica': "//tr[@data-desc='nota tecnica']",
}

_XPATH_FORMATOS: dict[str, str] = {
    'Nato-digital': '//*[@id="divOptNato"]/div/label',
}

# Substitui o marcador pelo texto sem interpretar "$&" e afins do replace
_JS_SUBSTITUIR = (
    'arguments[0].innerHTML = arguments[0].innerHTML'
    '.replace(arguments[1], () => arguments[2]);'
)


def _com_retentativa_stale(descricao: str, acao: Callable[[], None]) -> None:
    for _ in range(5):
        try:
            acao()
            return
        except StaleElementReferenceException:
            logger.debug(
                'Elemento ficou stale ao %s; tentando novamente', descricao
            )
    raise AcaoNaoConcluida(
        f'Não foi possível {descricao} após várias tentativas '
        '(stale repetido).'
    )


def clicar_incluir_doc(
    driver: webdriver.Remote, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    img_incluir_doc: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//img[@alt='Incluir Documento']",
        ))
    )
    img_incluir_doc.click()


def selecionar_tipo_doc(
    driver: webdriver.Remote, tipo: str, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    try:
        xpath_tipo_doc = _XPATH_TIPOS_DOC[tipo]
    except KeyError:
        raise OpcaoNaoSuportada(
            f"Tipo de documento '{tipo}' não implementado"
        ) from None

    try:
        WebDriverWait(driver, _TIMEOUT_SONDAGEM_TIPOS).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//img[@alt='Exibir apenas os tipos já "
                "utilizados pela unidade']",
            ))
        )

    except TimeoutException:
        a_exibir_todos_tipos_doc: WebElement = WebDriverWait(
            driver, timeout
        ).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//img[@alt='Exibir todos os tipos']",
            ))
        )
        a_exibir_todos_tipos_doc.click()

    def clicar() -> None:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath_tipo_doc))
        ).click()

    _com_retentativa_stale('escolher o tipo de documento', clicar)


def preencher_metadados_doc_externo(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    tipo_doc: str,
    num: str,
    formato: str,
    data: str,
    path_anexo: Path,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str | None = '',
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    try:
        xpath_formato = _XPATH_FORMATOS[formato]
    except KeyError:
        raise OpcaoNaoSuportada(
            f'Opção de formato ainda não implementada: {formato}'
        ) from None

    def preencher_data() -> None:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, 'txtDataElaboracao'))
        ).send_keys(data)

    def selecionar_tipo() -> None:
        Select(driver.find_element(By.ID, 'selSerie')).select_by_visible_text(
            tipo_doc
        )

    def preencher_numero() -> None:
        time.sleep(2)
        driver.find_element(By.ID, 'txtNumero').send_keys(num)
        time.sleep(2)

    def selecionar_formato() -> None:
        driver.find_element(By.XPATH, xpath_formato).click()

    def anexar_arquivo() -> None:
        driver.find_element(By.ID, 'filArquivo').send_keys(str(path_anexo))

    _com_retentativa_stale('preencher a data do documento', preencher_data)
    _com_retentativa_stale('selecionar o tipo de documento', selecionar_tipo)
    _com_retentativa_stale('preencher o numero do documento', preencher_numero)
    _com_retentativa_stale(
        'selecionar o formato do documento', selecionar_formato
    )

    selecionar_nivel_acesso(
        driver, nivel_acesso, hipotese_legal, timeout=timeout
    )

    _com_retentativa_stale('anexar o arquivo', anexar_arquivo)

    WebDriverWait(driver, max(timeout, _TIMEOUT_MIN_SALVAR)).until(
        EC.presence_of_element_located((
            By.XPATH,
            f'//td/div[contains(text(), {xpath_literal(path_anexo.name)})]',
        ))
    )


def preencher_metadados_doc_sei(
    driver: webdriver.Remote,
    nivel_acesso: NivelAcesso,
    hipotese_legal: str | None,
    nome: str = '',
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    if nome:
        input_nome: WebElement = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, 'txtNomeArvore'))
        )
        input_nome.send_keys(nome)

    selecionar_nivel_acesso(
        driver, nivel_acesso, hipotese_legal, timeout=timeout
    )


def _ir_para_janela_editor(
    driver: webdriver.Remote, janela_principal: str, timeout: float
) -> None:
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.window_handles) == NUM_JANELAS_COM_POPUP
    )
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            break


def _fechar_janelas_extras(
    driver: webdriver.Remote, janela_principal: str
) -> None:
    for handle in driver.window_handles:
        if handle != janela_principal:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(janela_principal)


def inserir_conteudo_doc_sei_simples(
    driver: webdriver.Remote, texto: str, *, timeout: float = TIMEOUT_PADRAO
) -> None:
    janela_principal: str = driver.current_window_handle

    _ir_para_janela_editor(driver, janela_principal, timeout)

    driver.switch_to.default_content()

    iframe_corpo: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//iframe[@aria-describedby='cke_250']",
        ))
    )
    driver.switch_to.frame(iframe_corpo)

    seletores: list[str] = [
        'p.Texto_Justificado_Recuo_Primeira_Linha',
        'p.Corpo_do_Texto',
        'p.Texto_Justificado',
        'body p',
    ]
    paragrafo: WebElement | None = None
    for seletor in seletores:
        try:
            paragrafo = WebDriverWait(driver, TIMEOUT_SONDAGEM).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, seletor))
            )
            break
        except TimeoutException:
            continue

    if not paragrafo:
        driver.execute_script("""
            let p = document.createElement('p');
            document.body.appendChild(p);
        """)
        paragrafo = driver.find_element(By.CSS_SELECTOR, 'body p:last-of-type')

    paragrafo.click()

    driver.execute_script(
        'arguments[0].innerHTML = arguments[1];', paragrafo, texto
    )

    driver.switch_to.default_content()
    driver.find_element(By.TAG_NAME, 'body').click()
    time.sleep(5)

    button_salvar_doc: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'cke_207'))
    )
    driver.execute_script('arguments[0].click();', button_salvar_doc)
    WebDriverWait(driver, max(timeout, _TIMEOUT_MIN_SALVAR)).until(
        lambda d: (
            'cke_button_off'
            in (d.find_element(By.ID, 'cke_207').get_attribute('class') or '')
        )
    )
    driver.close()
    driver.switch_to.window(janela_principal)


def inserir_conteudo_doc_sei_memo(  # noqa: PLR0913, PLR0917
    driver: webdriver.Remote,
    vocativo: str,
    destinatario_nome: str,
    assunto: str,
    texto_principal: str,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    janela_principal: str = driver.current_window_handle

    try:
        _ir_para_janela_editor(driver, janela_principal, timeout)

        p_cargo = localizar_xpath_elemento_com_fallback_iframe(
            driver,
            'Endereçamento',
            "//p[contains(text(), '@cargo_destinatario@')]",
            timeout=timeout,
        )
        p_cargo.clear()

        # Já estamos no iframe correto (nomeado ou achado por fallback)
        p_nome: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(text(), '@nome_destinatario@')]",
            ))
        )
        driver.execute_script(
            _JS_SUBSTITUIR, p_nome, '@nome_destinatario@', destinatario_nome
        )

        driver.switch_to.default_content()

        strong_assunto = localizar_xpath_elemento_com_fallback_iframe(
            driver,
            'Assunto',
            "//p[strong[contains(text(), 'Assunto:')]]",
            timeout=timeout,
        )
        driver.execute_script(
            _JS_SUBSTITUIR, strong_assunto, 'Assunto:', f'Assunto: {assunto}'
        )

        driver.switch_to.default_content()

        p_vocativo = localizar_xpath_elemento_com_fallback_iframe(
            driver,
            'Corpo do Texto',
            "//p[contains(text(), '@vocativo_destinatario@')]",
            timeout=timeout,
        )
        driver.execute_script(
            _JS_SUBSTITUIR, p_vocativo, '@vocativo_destinatario@', vocativo
        )

        # Já estamos no iframe correto de "Corpo do Texto"
        p_att: WebElement = driver.find_element(
            By.XPATH, "//p[contains(text(), 'Atenciosamente,')]"
        )
        driver.execute_script(
            'arguments[0].innerHTML = arguments[1];', p_att, ''
        )

        p_inserir_txt: WebElement = driver.find_element(
            By.XPATH, "//p[contains(text(), '[ Inserir Texto ]')]"
        )
        driver.execute_script(
            'arguments[0].innerHTML = arguments[1];',
            p_inserir_txt,
            texto_principal,
        )

        # Espera a atualização
        time.sleep(3)

        driver.switch_to.default_content()
        driver.find_element(By.TAG_NAME, 'body').click()

        button_salvar_doc: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[contains(@class, 'cke_button__save')]",
            ))
        )

        driver.execute_script('arguments[0].click();', button_salvar_doc)

        WebDriverWait(driver, max(timeout, _TIMEOUT_MIN_SALVAR)).until(
            lambda d: (
                'cke_button_disabled'
                in (
                    d.find_element(
                        By.CSS_SELECTOR, 'a.cke_button__save'
                    ).get_attribute('class')
                    or ''
                )
            )
        )

        driver.close()
        driver.switch_to.window(janela_principal)

    except Exception:
        _fechar_janelas_extras(driver, janela_principal)
        raise


def espera_documento_aparecer_arvore(
    driver: webdriver.Remote,
    tipo_doc: str,
    num: str | None = None,
    *,
    timeout: float = TIMEOUT_PADRAO,
) -> None:
    nome_arvore = f'{tipo_doc} {num}' if num else tipo_doc

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            By.XPATH,
            f'//span[contains(text(), {xpath_literal(nome_arvore)})]',
        ))
    )
