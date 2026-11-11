import pytest

from sei_automacao.formatacao import num_extenso_formatado
from sei_automacao.modelos import Memorando


def _memo(**kwargs) -> Memorando:
    dados = {
        'destinatario_nome': 'Fulano',
        'assunto': 'Assunto',
        'vocativo': 'Senhor',
        'nome_signatario': 'Beltrano',
        'cargo_signatario': 'Gerente',
    }
    return Memorando(**(dados | kwargs))


def test_memorando_publico_sem_hipotese_legal():
    memo = _memo()
    assert memo.hipotese_legal is None
    assert memo.para_kwargs_inserir_doc()['hipotese_legal'] is None


def test_memorando_restrito_exige_hipotese_legal():
    with pytest.raises(ValueError, match='hipotese_legal'):
        _memo(nivel_acesso='Restrito')


def test_memorando_monta_texto():
    memo = _memo()
    memo.adicionar_paragrafo('Primeiro')
    texto = memo.texto_principal()
    assert 'Primeiro</p>' in texto
    assert 'Beltrano' in texto
    assert 'Gerente' in texto


def test_num_extenso_formatado():
    assert num_extenso_formatado(1234.5) == (
        '1.234,50',
        'mil, duzentos e trinta e quatro',
        'cinquenta',
    )
