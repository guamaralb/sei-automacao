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
- `documento.acoes_disponiveis_doc`: ações da barra do documento selecionado
  (ex.: `'Excluir'`, `'Cancelar Documento'`).
- Exceções `AcaoIndisponivel` (a ação não está na barra do documento) e
  `DocumentoSemConteudo` (documento sem o iframe do conteúdo, ex.: cancelado;
  subclasse de `IframeNaoEncontrado`).

### Alterado
- Layout `src/`. Passos internos movidos para `sei_automacao._internal`
  (privado).
- Ações de marcador movidas para `sei_automacao.processo`; inclusão de
  documentos movida para `sei_automacao.documento`.
- `efetuar_login` fecha o aviso de novidades (`fechar_novidades=True`).
- `acessar_processo` espera a página nova carregar e detecta "Unidade atual
  não possui acesso ao processo" assim que a mensagem aparece.
- `trocar_iframe` procura o iframe por id, name e title ao mesmo tempo.
- `trocar_unidade` não abre mais um processo fixo antes da troca, não
  clica de novo se a unidade já está selecionada e espera a página
  carregar (em vez de `refresh()` + `sleep(2)`): a primeira pesquisa de
  processo depois da troca não se perde mais.
- Mensagens via `logging` em vez de `print`.

### Corrigido
- `cancelar_doc` procurava o campo do motivo fora do iframe `ifrVisualizacao`,
  onde o formulário abre, e nunca cancelava. Agora também espera o SEI salvar
  e recarregar a árvore, trata o alerta de erro do SEI (`AcaoNaoConcluida`) e
  levanta `AcaoIndisponivel` sem esperar o `timeout` quando não há a opção.
- `excluir_doc` esperava o `timeout` inteiro pelo ícone "Excluir" em
  documento que não pode ser excluído (agora `AcaoIndisponivel` na hora) e
  voltava antes de a árvore recarregar.
- `listar_documentos_arvore` falhava com "número inconsistente de pastas"
  logo depois de cancelar ou excluir um documento: a abertura das pastas
  espera a árvore terminar de carregar, recomeça se ela recarregar e espera as
  pastas abrirem.
- `selecionar_doc_arvore` podia aceitar o iframe do documento anterior (o
  texto lido era o dele, ou vazio): agora espera a página do documento clicado
  substituir a anterior. Documento sem conteúdo levanta
  `DocumentoSemConteudo` na hora.
- `Memorando.hipotese_legal` tinha `(None,)` (tupla) como padrão.
- `clicar_img_reabrir_processo` sempre lançava exceção depois de clicar.
- `remover_marcador` parava no primeiro marcador ausente e nunca acusava
  marcador que continuava no processo.
- `selecionar_tipo_processo` falhava em silêncio.
- `enviar_email` com nível de acesso não público não repassava a hipótese
  legal.
- Nomes com aspas quebravam XPaths e scripts do editor.
