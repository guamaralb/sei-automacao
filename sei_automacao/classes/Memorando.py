from dataclasses import dataclass, field
from typing import Literal

_CSS_PADRAO = 'Texto_Justificado_Recuo_Primeira_Linha'


@dataclass
class Memorando:
    """Representa os dados necessários para montar um memorando no SEI."""

    destinatario_nome: str
    assunto: str
    vocativo: str
    nome_signatario: str
    cargo_signatario: str
    nivel_acesso: Literal['Restrito', 'Público', 'Sigiloso'] = 'Público'
    hipotese_legal: (
        None | Literal['Informação Pessoal (Art. 31 da Lei nº 12.527/2011)']
    ) = (None,)
    css_paragrafo: str = _CSS_PADRAO
    paragrafos: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.nivel_acesso.lower() != 'público' and not self.hipotese_legal:
            raise ValueError(
                'hipotese_legal é obrigatória quando nivel_acesso não é'
                ' "Público".'
            )

    def adicionar_paragrafo(self, texto_html: str) -> None:
        """Adiciona um novo parágrafo ao corpo do memorando."""
        self.paragrafos.append(texto_html)

    def texto_principal(self) -> str:
        """Monta o HTML do corpo do memorando a partir dos parágrafos."""
        corpo = ''.join(
            f'<p class="{self.css_paragrafo}">{paragrafo}</p>'
            for paragrafo in self.paragrafos
        )
        assinatura = (
            f'<p class="Nome_Signatário">{self.nome_signatario}</p>'
            f'<p class="Cargo_Signatário">{self.cargo_signatario}</p>'
        )
        return corpo + assinatura

    def para_kwargs_inserir_doc(self) -> dict:
        """Retorna os kwargs prontos para incluir_doc_sei_memo."""
        return {
            'destinatario_nome': self.destinatario_nome,
            'assunto': self.assunto,
            'vocativo': self.vocativo,
            'texto_principal': self.texto_principal(),
            'nivel_acesso': self.nivel_acesso,
            'hipotese_legal': self.hipotese_legal,
        }
