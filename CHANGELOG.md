# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
o projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado
- API pública por assunto: `navegador`, `sessao`, `unidade`, `processo`,
  `documento`, `modelos`, `formatacao` e `exceptions`, reexportada em
  `sei_automacao`.
- Parâmetro `timeout` (só por nome) em todas as funções.
- `iniciar_sei(url_sei, ...)`: abre o navegador já na página do SEI
  (substitui `iniciar_driver`).
- `processo.pode_incluir_documento` e `processo.listar_marcadores_disponiveis`.
- `processo.selecionar_raiz_arvore` (antigo `clicar_num_processo`).
- Exceções específicas: `ElementoNaoEncontrado`, `IframeNaoEncontrado`,
  `DocumentoNaoEncontrado`, `MarcadorNaoEncontrado`, `OpcaoNaoSuportada`,
  `ProcessoNaoReabrivel`, `AcaoNaoConcluida`.
- `py.typed`, licença MIT, metadados PEP 621.

### Alterado
- Layout `src/`. Passos internos movidos para `sei_automacao._internal`
  (privado).
- Ações de marcador movidas para `sei_automacao.processo`; inclusão de
  documentos movida para `sei_automacao.documento`.
- `efetuar_login` fecha o aviso de novidades (`fechar_novidades=True`).
- `acessar_processo` espera a página nova carregar e detecta "Unidade atual
  não possui acesso ao processo" assim que a mensagem aparece.
- `trocar_iframe` procura o iframe por id, name e title ao mesmo tempo.
- Mensagens via `logging` em vez de `print`.

### Corrigido
- `Memorando.hipotese_legal` tinha `(None,)` (tupla) como padrão.
- `clicar_img_reabrir_processo` sempre lançava exceção depois de clicar.
- `remover_marcador` parava no primeiro marcador ausente e nunca acusava
  marcador que continuava no processo.
- `selecionar_tipo_processo` falhava em silêncio.
- `enviar_email` com nível de acesso não público não repassava a hipótese
  legal.
- Nomes com aspas quebravam XPaths e scripts do editor.

### Pendente para a 0.1.0
- `trocar_unidade` ainda abre um processo fixo antes de trocar a unidade.
