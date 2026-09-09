# cartao

Páginas estáticas, sem dependência de build ou servidor.

| Arquivo | O que é |
| --- | --- |
| `index.html` | Cartão de visita digital com atalho para WhatsApp. |
| `indices.html` | Painel de índices e projeções: IPCA, IGP-M, INPC, Selic e dólar. |

## indices.html

Consulta **em tempo real, pelo navegador**, as APIs públicas do Banco Central. Nenhum valor
fica gravado no arquivo — abrir a página é o que dispara a busca, então não há dado velho
para conferir antes de usar.

Fontes:

- **BCB/SGS** (`api.bcb.gov.br`) — séries realizadas: IPCA (433), INPC (188), IGP-M (189),
  Selic meta (432), Selic acumulada no mês (4390), CDI (12) e dólar PTAX venda (1).
- **BCB/Expectativas — Focus** (`olinda.bcb.gov.br`) — medianas de mercado anuais, mensais
  e por reunião do Copom.

Abas:

- **Anual** — último dado divulgado, acumulado no ano e em 12 meses; medianas Focus para o
  ano corrente e os três seguintes.
- **Mensal** — 13 meses realizados e 12 meses de projeção Focus, com acumulado encadeado.
- **Semanal** — evolução das últimas oito coletas do Focus, Selic por reunião do Copom,
  PTAX dos últimos pregões e equivalentes semanais derivados.
- **Correção monetária** — encadeia as variações mensais divulgadas entre dois meses e
  devolve fator, percentual e valor corrigido.

### Limitações que importam

- **Não existe projeção semanal de IPCA, IGP-M ou INPC.** O que é semanal é a *coleta* do
  Focus. Os "equivalentes semanais" da aba Semanal são conversão da taxa mensal/anual feita
  no próprio script — não servem como índice oficial em cálculo judicial, contrato ou reajuste.
- Projeção Focus é expectativa de mercado, revisada toda semana. Para correção monetária
  vale o índice **efetivamente divulgado**, nunca a projeção.
- A janela de série carregada é de 20 anos (`JANELA_MESES` no script). Para períodos
  anteriores, aumentar a constante.
- A página depende de o navegador alcançar `api.bcb.gov.br` e `olinda.bcb.gov.br`. Em rede
  corporativa que bloqueia esses domínios, o painel exibe as URLs que falharam em vez de
  mostrar número errado.
