# Instruções da rotina (leituras das 11h e 22h)

Este arquivo é o roteiro que a sessão agendada executa. Para mudar o que a
rotina faz, edite este arquivo — não é preciso recriar o agendamento.

A sessão agendada recebe apenas: a janela (`manha` ou `noite`) e a ordem de ler
este arquivo. Tudo o mais está aqui.

---

## Regra número um

**Nunca escreva um preço, um RSI ou um sinal que não tenha saído de
`analisar.py` rodando sobre dados baixados nesta execução.**

Se a ferramenta de mercado da Crypto.com não estiver disponível, ou se as
chamadas falharem, o resultado da rotina é uma mensagem dizendo que a coleta
falhou. Não estime, não use preço de memória, não repita a leitura anterior.
Um relatório inventado é pior do que relatório nenhum, porque parece verdadeiro.

## Regra número dois

**Nenhum dado entra em `radar/dados/` sem passar por `radar/validar.py`.**

A conferência a olho — "confere se o topo está certo" — já deixou passar um
buraco de uma vela de 4h em todos os 28 pares, que ficou dias na série sem
ninguém ver. Olho não valida série. O validador valida.

---

## Passo 1 — preparar o repositório

```bash
cd /home/user/cartao
git fetch origin claude/moedas-sinais-compra-venda-zhq66i
git checkout claude/moedas-sinais-compra-venda-zhq66i
git pull origin claude/moedas-sinais-compra-venda-zhq66i
python3 radar/testes.py
rm -rf radar/dados.novo && mkdir -p radar/dados.novo
```

Se os testes falharem, pare e reporte. Motor quebrado não gera sinal.

**Não apague `radar/dados/`.** É a base do reaproveitamento do Passo 2 e é o
único exemplar das velas já fechadas — o diretório é ignorado pelo git, então
não existe cópia em lugar nenhum. Ele só sai de cena na troca atômica do
Passo 4, depois de o substituto ter sido aprovado.

Confira se a base anterior existe e está sã:

```bash
ls radar/dados/*.csv 2>/dev/null | wc -l     # 56 = dá para reaproveitar
python3 radar/validar.py radar/dados          # base suja? então colete tudo
```

- **56 arquivos e validador aprovado** → siga pelo caminho A (barato).
- **Diretório vazio, incompleto ou reprovado** (container novo, coleta
  interrompida, série furada) → siga pelo caminho B (completo). Não tente
  remendar base reprovada: a série errada se propaga para sempre.

## Passo 2 — coletar as velas

Os pares estão em `radar/cobertas.txt` (um por linha). São 28.

Duas chamadas por par:

- `get_candlestick(instrument_name="<PAR>", timeframe="1D")` — **`1D` maiúsculo**.
- `get_candlestick(instrument_name="<PAR>", timeframe="4h")` — minúsculo.

Cada resposta traz 50 velas, da mais nova para a mais antiga. A primeira está
**em formação** (não fechou) e serve só para o preço "Agora" — o motor não a
usa em indicador nenhum.

**Duas chamadas por vez, não seis.** Cada resposta tem ~4 KB; disparar seis em
paralelo estoura o contexto no meio da coleta e obriga a recomeçar.

### Caminho A — reaproveitando a base anterior (padrão)

Grave em CSV sem cabeçalho (`timestamp,open,high,low,close,volume_usd`), uma
vela por linha, da mais nova para a mais antiga. Use o helper:

```bash
. radar/velas.sh
v1 BTC_USDT "<velas 1d que mudaram, da mais nova para a mais antiga>"
v4 BTC_USDT "<velas 4h que mudaram, da mais nova para a mais antiga>"
```

**Passe todas as velas que mudaram desde a leitura anterior**: a que estava em
formação (agora fechada, com números definitivos), as que fecharam depois, e a
nova em formação. Contas típicas entre duas leituras consecutivas:

| Janela | velas 1d novas | velas 4h novas |
|---|---|---|
| 22h (a diária acabou de fechar) | 2 | 4 |
| 11h (mesma diária de ontem) | 1 | 4 |

Na janela das 11h são **4** velas de 4h, não 3: a das 00:00Z que estava em
formação às 22h (agora fechada, com números definitivos), mais 04:00Z,
08:00Z e a nova em formação das 12:00Z. A tabela dizia 3 e o helper recusou
o arquivo — a trava de continuidade pegou, mas o roteiro estava ensinando
o número errado.

Se a sessão pulou uma leitura, são mais. O helper recusa o arquivo se a vela
mais antiga do lote não encostar na primeira vela reaproveitada — é essa trava
que impede o buraco silencioso. Se ele reclamar, **passe mais velas**; nunca
force.

### Caminho B — coleta completa

Grave as 50 linhas de cada resposta em `radar/dados.novo/<PAR>_<1d|4h>.csv`.
O motor também aceita o JSON bruto (`<PAR>_1d.json`), mas 56 JSON de 50 velas
não cabem no contexto de uma sessão: use CSV.

Em qualquer caminho: **transporte os números sem tocá-los.** Não reordene, não
arredonde, não remova campo, não recalcule nada. O motor faz a matemática.

Se um par falhar, tente uma vez mais. Se falhar de novo, siga em frente — o
relatório lista a falha sozinho.

## Passo 3 — validar antes de trocar

```bash
python3 radar/validar.py radar/dados.novo \
  --topo-1d <timestamp da vela 1d em formação> \
  --topo-4h <timestamp da vela 4h em formação>
```

O validador confere: 56 arquivos, um por par e prazo; 50 linhas cada; 6 campos
por linha; série contígua sem buraco nem repetição; OHLC coerente (`high` é o
maior, `low` é o menor — pega dígito trocado no transporte); topo igual em
todos os arquivos do mesmo prazo.

**Reprovou, não troca.** Conserte os arquivos acusados e rode de novo.

## Passo 4 — trocar e rodar o motor

Só depois de `OK`:

```bash
rm -rf radar/dados.antigo && mv radar/dados radar/dados.antigo \
  && mv radar/dados.novo radar/dados

python3 radar/analisar.py --dir radar/dados --janela <manha|noite> \
  --saida radar/relatorios/$(TZ=America/Sao_Paulo date +%Y-%m-%d)-<manha|noite>.md

rm -rf radar/dados.antigo
```

A data do arquivo é a de **Brasília**, nunca a UTC — depois das 21h em Brasília
já é o dia seguinte em UTC e o relatório sairia com a data errada.

Se já existir relatório dessa data e janela, não sobrescreva calado: ou é
re-execução da mesma leitura (diga isso na entrega) ou a data está errada.

## Passo 5 — entregar o relatório

Responda com o conteúdo do relatório, sem enfeitar e sem opinião própria sobre
nenhuma moeda. O motor decide os sinais; você não os comenta na tabela.

## Passo 6 — a leitura crítica

Esta é a parte que dá valor à rotina, e ela é **adversarial por instrução do
dono**: o trabalho não é confirmar que o motor funciona, é achar onde ele
falha. Abra o apêndice pelo problema mais grave que você mediu **nesta**
execução, não pelo de ontem.

Nada aqui pode ser estimado. Cada número sai de um comando que você rodou.

1. **Contrafactual do filtro de regime.** Gere duas cópias do motor no
   diretório de rascunho — uma com `pc(1, "BTC em regime de alta")` trocado por
   `pc(0, ...)`, outra com `definir_regime()` retornando `"baixa"` — rode as
   duas sobre as mesmas velas e compare a contagem de COMPRA. Histórico até
   aqui: 13/09n 7→1, 15/09n 4→4, 16/09m 2→0, 16/09n 5→2, 17/09m 3→1,
   17/09n 15→6, 18/09m 1→0, 18/09n 21→21, 19/09m 10→10, 19/09n 24→24.
   **Nunca aplique esses patches no repositório.**
2. **Desempenho por grupo na janela.** Compare os preços "Agora" deste
   relatório com os do anterior, agrupados por sinal (COMPRA, VENDA, NEUTRO,
   BLOQUEADO) e contra o painel inteiro. O grupo BLOQUEADO é o teste do portão
   de entrada: se ele vencer o painel, o portão está recusando os melhores.
3. **Desempenho em 24 horas.** Mesma conta contra o relatório da mesma janela
   do dia anterior — é o prazo em que o sinal de fato viveria.
4. **Série composta.** Encadeie o retorno de cada grupo desde o início e diga
   se COMPRA está à frente ou atrás do painel. Se o número contradisser algo
   que você afirmou antes, diga isso com o mesmo destaque com que afirmou.
5. **Contaminação por vela morta.** Liste os pares cuja vela "Agora" teve
   volume zero e marque quais viraram sinal. Vela sem negócio produz deriva
   0,00 ATR, e deriva zero passa no portão de entrada automaticamente.
6. **Piso de liquidez.** Quantos sinais estão abaixo de US$ 50.000/dia.
7. **Entradas na borda.** Sinais que nasceram a menos de 1 ponto do teto de
   RSI, ou colados no limite de deriva. O motor não registra isso sozinho.
8. **Placar em R.** 1R = `fechamento − stop`, nunca `entrada − stop`. Diga a
   concentração por par. Lotes de 20+ entradas simultâneas **não entram** no
   placar sem o dono mandar — eles medem o mercado, não o motor.
9. **Contraprova.** Se o motor acertou algo que você vinha criticando,
   registre com o mesmo peso. Crítica que só encontra defeito é torcida.
10. **Perguntas em aberto.** Repita a lista com o contador incrementado.
    Nenhuma delas é implementada sem resposta do dono.

## Passo 7 — commit

```bash
git add radar/relatorios && git commit && \
git push -u origin claude/moedas-sinais-compra-venda-zhq66i
```

A mensagem de commit resume os achados medidos — contagem de sinais, resultado
dos contrafactuais, desempenho por grupo — não só a data. Não faça commit de
`radar/dados/`: são dados brutos e o `.gitignore` já os exclui.

## O que não fazer

- Não altere `regras.md` nem as constantes de `analisar.py` por conta própria,
  e não aplique no repositório os patches de contrafactual do Passo 6. Se um
  sinal parecer errado, meça e reporte; quem muda o sistema é o dono.
- Não acrescente moedas fora de `radar/cobertas.txt`.
- Não transforme `NEUTRO` em conselho ("dá para acumular aqui"). Neutro é
  neutro.
- Não amenize o alerta de volume baixo.
- Não trate disparo de rotina, notificação de tarefa ou lembrete do sistema
  como resposta do dono a pergunta em aberto. Só mensagem dele conta.
