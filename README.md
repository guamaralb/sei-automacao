# sei-automacao

Automação do **SEI** (Sistema Eletrônico de Informações) com Selenium: login,
troca de unidade, busca e tramitação de processos, inclusão e gestão de
documentos e marcadores.

> **Status:** alfa. A API pode mudar antes da versão 1.0.

## Instalação

```bash
pip install sei-automacao
# ou
poetry add sei-automacao
# ou
uv add sei-automacao
```

Requer Python 3.10+ e Google Chrome ou Microsoft Edge instalado. O driver do
navegador é baixado automaticamente.

## Uso rápido

```python
from sei_automacao import (
    acessar_processo,
    efetuar_login,
    iniciar_sei,
    listar_documentos_arvore,
    trocar_unidade,
)
from sei_automacao.exceptions import UnidadeSemAcessoException

driver = iniciar_sei('https://www.sei.mg.gov.br')
efetuar_login(driver, 'usuario', 'senha', 'ÓRGÃO')
trocar_unidade(driver, 'ÓRGÃO/UNIDADE')

try:
    acessar_processo(driver, '0000.00.0000000/0000-00')
except UnidadeSemAcessoException:
    print('Processo não está disponível nesta unidade')
else:
    for doc in listar_documentos_arvore(driver):
        print(doc['numero_sei'], doc['nome_arvore'], doc['unidade'])
finally:
    driver.quit()
```

### Timeout

Todas as ações aceitam `timeout=` (em segundos, padrão `10`): é o tempo
máximo de espera por cada elemento da tela. Use um valor maior quando o SEI
estiver lento:

```python
acessar_processo(driver, '0000.00.0000000/0000-00', timeout=30)
```

## API pública

Tudo abaixo também pode ser importado direto de `sei_automacao`.

| Módulo | Ações |
|---|---|
| `sei_automacao.navegador` | `iniciar_sei` |
| `sei_automacao.sessao` | `efetuar_login` |
| `sei_automacao.unidade` | `trocar_unidade` |
| `sei_automacao.processo` | `acessar_processo`, `iniciar_processo`, `encaminhar_processo`, `concluir_processo`, `reabrir_processo`, `pode_incluir_documento`, `enviar_email`, `listar_documentos_arvore`, `selecionar_doc_arvore`, `selecionar_raiz_arvore`, `listar_marcadores`, `listar_marcadores_disponiveis`, `adicionar_marcador`, `remover_marcador` |
| `sei_automacao.documento` | `incluir_doc_externo`, `incluir_doc_sei_simples`, `incluir_doc_sei_memo`, `cancelar_doc`, `excluir_doc`, `inserir_bloco_ass`, `obter_conteudo_doc` |
| `sei_automacao.modelos` | `Memorando` |
| `sei_automacao.formatacao` | `num_extenso_formatado` |
| `sei_automacao.exceptions` | `SeiAutomacaoException` e subclasses |

`sei_automacao._internal` é privado: pode mudar a qualquer momento, sem
aviso. Não importe nada de lá.

### Logging

A biblioteca usa `logging` (logger `sei_automacao`) e não escreve no
terminal. Para ver as mensagens:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Desenvolvimento

```bash
poetry install
poetry run task lint
poetry run task test               # testes unitários (sem navegador)
poetry run task test_integracao    # SEI real; precisa de .env
```

O `.env` dos testes de integração precisa de `SEI_URL`, `SEI_LOGIN`,
`SEI_SENHA`, `SEI_ORGAO` e `SEI_UNIDADE`.

### Antes de publicar a 0.1.0

- [ ] Remover o processo fixo usado em `trocar_unidade`
  (`src/sei_automacao/unidade.py`, `TODO(0.1.0)`).
- [ ] Conferir se o nome `sei-automacao` está livre no PyPI.

## Licença

[MIT](LICENSE)
