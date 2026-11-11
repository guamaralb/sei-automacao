"""Tempos de espera e helpers comuns."""

TIMEOUT_PADRAO: float = 10
"""Tempo máximo (s) de espera por um elemento, usado quando o chamador não
informa ``timeout``."""

TIMEOUT_SONDAGEM: float = 3
"""Tempo (s) das verificações rápidas de "o elemento existe?". Não segue o
``timeout`` do chamador: usá-lo deixaria toda ação lenta quando o elemento
não existe, que é um resultado esperado nessas verificações."""


def xpath_literal(texto: str) -> str:
    """Devolve ``texto`` como literal XPath, com as aspas necessárias.

    XPath 1.0 não tem escape de aspas: com os dois tipos de aspas no texto,
    monta um ``concat()``.
    """
    if "'" not in texto:
        return f"'{texto}'"
    if '"' not in texto:
        return f'"{texto}"'
    partes = texto.split("'")
    return 'concat(' + ', "\'", '.join(f"'{parte}'" for parte in partes) + ')'
