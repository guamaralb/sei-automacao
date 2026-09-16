from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Memorando:
    """Representa os dados necessários para montar um memorando no SEI."""

    vocativo: str
    destinatario_nome: str
    assunto: str
    texto_principal: str
    nivel_acesso: Literal['Restrito', 'Público', 'Sigiloso'] = 'Público'
    hipotese_legal: str | None = None

    def __post_init__(self) -> None:
        if self.nivel_acesso.lower() != 'público' and not self.hipotese_legal:
            raise ValueError(
                'hipotese_legal é obrigatória quando nivel_acesso não é'
                ' "Público".'
            )

    def para_kwargs_inserir_doc(self) -> dict:
        """Retorna os kwargs prontos para incluir_doc_sei_memo."""
        return {
            'vocativo': self.vocativo,
            'destinatario_nome': self.destinatario_nome,
            'assunto': self.assunto,
            'texto_principal': self.texto_principal(),
            'nivel_acesso': self.nivel_acesso,
            'hipotese_legal': self.hipotese_legal,
        }