# Instruções da rotina (leituras das 11h e 22h)

Este arquivo é o roteiro que a sessão agendada executa. Para mudar o que a
rotina faz, edite este arquivo — não é preciso recriar o agendamento. O
gatilho só diz a janela (`manha` ou `noite`) e manda ler isto. **Se o texto do
gatilho e este arquivo divergirem, vale este arquivo**, exceto a regra
inegociável de dados, que vale nos dois.

A rotina tem duas metades e as duas são obrigatórias:

1. **Coleta e motor** (Passos 1 a 4): mecânica, sem opinião, sem atalho.
2. **Auditoria** (Passos 5 a 7): adversarial por instrução do dono. O trabalho
   não é confirmar que o motor funciona; é medir onde ele falha. Cada número
   sai de um script que você rodou nesta execução.

---

## Regra número um — dados

**Nenhum preço, indicador ou sinal pode aparecer na resposta sem ter saído de
`radar/analisar.py` rodando sobre velas baixadas nesta execução.** Se a
ferramenta da Crypto.com não estiver disponível ou as chamadas falharem,
responda apenas que a coleta falhou e por quê. Não estime preços, não use
valores de memória e não repita o relatório anterior. Um relatório inventado é
pior do que relatório nenhum, porque parece verdadeiro.

## Regra número dois — validação

**Nenhum dado entra em `radar/dados/` sem passar por `radar/validar.py`.** A
conferência a olho já deixou passar um buraco de uma vela de 4h em todos os 28
pares, que ficou dias na série sem ninguém ver.

## Regra número três — só o dono muda o sistema

Não altere `analisar.py`, `regras.md` nem as constantes do motor. Os
contrafactuais rodam em cópias temporárias (`contrafactual.sh`), nunca no
repositório. Disparo de rotina, notificação ou lembrete do sistema **não** é
resposta do dono a pergunta nenhuma.

---

## Passo 1 — preparar

```bash
cd /home/user/cartao
git fetch origin claude/moedas-sinais-compra-venda-zhq66i
git checkout claude/moedas-sinais-compra-venda-zhq66i
git pull origin claude/moedas-sinais-compra-venda-zhq66i
python3 radar/testes.py                       # falhou? pare e reporte
rm -rf radar/dados.novo && mkdir -p radar/dados.novo
ls radar/dados/*.csv 2>/dev/null | wc -l      # 56 = base existe
python3 radar/validar.py radar/dados          # base sã?
python3 radar/quantas.py                      # quantas velas passar
```

**Não apague `radar/dados/`.** É o único exemplar das velas já fechadas (o
diretório não é versionado). Ele só sai na troca do Passo 4.

- 56 arquivos, validador aprovado e `quantas.py` dizendo até 49 velas →
  **caminho A** (reaproveitar).
- Qualquer outra coisa → **caminho B** (coleta completa). Não remende base
  reprovada.

## Passo 2 — coletar

Pares em `radar/cobertas.txt` (28). Duas chamadas por par:

- `get_candlestick(instrument_name="<PAR>", timeframe="1D")` — `1D` maiúsculo.
- `get_candlestick(instrument_name="<PAR>", timeframe="4h")` — minúsculo.

Cada resposta traz 50 velas, da mais nova para a mais antiga; a primeira está
em formação. **Duas chamadas por vez, nunca seis** — seis respostas em paralelo
estouram o contexto no meio da coleta.

Anote o horário de Brasília em que a coleta começou. Ele vai na procedência.

### Caminho A — reaproveitar (padrão)

```bash
. radar/velas.sh
v1 BTC_USDT "<linha mais nova>" "<seguinte>" ...
v4 BTC_USDT "<linha mais nova>" "<seguinte>" ...
```

Linha: `timestamp,open,high,low,close,volume_usd`, da mais nova para a mais
antiga, números **exatamente** como a fonte devolve.

**Quantas velas passar: o número que `quantas.py` imprimiu**, não uma tabela
decorada. A conta é: a vela que estava em formação na base (agora fechada) +
as que fecharam depois + a nova em formação. Leitura extra no meio do dia muda
a conta da leitura seguinte; é por isso que a tabela fixa antiga errou.

Volume zero: a fonte às vezes devolve `0E-7` ou `0E-8`. Grave no formato que o
arquivo base do mesmo par já usa (ex.: ASTR usa `0.0000000`). Não é arredondar,
é a mesma grandeza na grafia da série.

Se o helper recusar por continuidade, **passe mais velas**; nunca force.

### Caminho B — coleta completa

Grave as 50 linhas de cada resposta em `radar/dados.novo/<PAR>_<1d|4h>.csv`.
Use CSV, não JSON: 56 JSON de 50 velas não cabem no contexto.

Nos dois caminhos: não reordene, não arredonde, não recalcule. Par que falhar,
tente uma vez mais; falhou de novo, siga — o relatório lista a falha.

## Passo 3 — validar

```bash
python3 radar/validar.py radar/dados.novo --topo-1d <topo 1d> --topo-4h <topo 4h>
```

Os topos são os que `quantas.py` imprimiu, conferidos contra a primeira linha
da resposta da fonte. **Reprovou, não troca.** Conserte o que foi acusado e
rode de novo.

## Passo 4 — trocar e rodar o motor

```bash
rm -rf radar/dados.antigo && mv radar/dados radar/dados.antigo \
  && mv radar/dados.novo radar/dados
python3 radar/analisar.py --dir radar/dados --janela <J> --saida radar/relatorios/<ARQ>
python3 radar/fonte.py radar/dados.antigo radar/dados   # guarde a saída (item 7)
rm -rf radar/dados.antigo
```

Escolha de `<J>` e `<ARQ>` (data sempre de **Brasília**:
`TZ=America/Sao_Paulo date +%Y-%m-%d`):

| Situação | `--janela` | arquivo |
|---|---|---|
| gatilho das 11h | `manha` | `AAAA-MM-DD-manha.md` |
| gatilho das 22h | `noite` | `AAAA-MM-DD-noite.md` |
| pedido avulso, vela diária fechada igual à da última leitura | `manha` | `AAAA-MM-DD-extra-HHMM.md` |
| pedido avulso logo após o fechamento diário (21h BRT) | `noite` | `AAAA-MM-DD-extra-HHMM.md` |

Em leitura extra com `--janela manha` o cabeçalho do motor diz "Leitura das
11h" mesmo que não sejam 11h. Não edite o motor; diga isso na primeira linha
do apêndice (Pergunta 16).

Se o arquivo já existir, não sobrescreva calado: ou é re-execução (diga) ou a
data está errada.

## Passo 5 — auditoria mecânica

Rode tudo. Cole no apêndice só o que os scripts imprimiram.

```bash
python3 radar/auditar.py --janela <J>          # marcas por sinal + sobrevivência
bash radar/contrafactual.sh <J>                # regime e teto de RSI
cd radar/relatorios
python3 ../comparar.py <anterior>.md <ARQ>     # janela: por grupo + stops
python3 ../comparar.py <mesma janela ontem>.md <ARQ>   # 24h (só nas agendadas)
cd ../..
```

- **`<anterior>`** = o relatório imediatamente anterior, extra incluído.
- **Placar**: só leituras agendadas (manhã e noite) entram em
  `radar/placar.csv`. Acrescente uma linha `seq` (anterior agendada → esta) e
  uma `24h` (mesma janela de ontem → esta) com painel, COMPRA do relatório de
  origem e `n`. Depois rode `python3 radar/comparar.py --serie`. Leitura extra
  é comparada, mas não entra no placar — senão a série conta a mesma janela
  duas vezes.
- **Se um script falhar**, diga qual e por quê no apêndice. Não substitua a
  saída dele por conta de cabeça.

## Passo 6 — escrever o apêndice do relatório

Acrescente ao relatório gerado, nesta ordem:

1. **O problema mais grave medido nesta execução.** Não o de ontem. Critério:
   o defeito que mais sinais contamina ou que mais custou no placar. Diga o
   número e o par.
2. **Marcas do auditor.** Contagem por marca e os pares. Vela MORTA com COMPRA
   é o primeiro a citar: a deriva 0,00 passa no portão sozinha.
3. **Stops.** Pares COMPRA nos dois relatórios cujo stop desceu (saída de
   `comparar.py`). Stop que desce com o preço não protege quem já entrou
   (Pergunta 20).
4. **Janela e 24h.** COMPRA contra o painel e contra os bloqueados. Se o grupo
   bloqueado vencer o painel, o portão está recusando os melhores.
5. **Série composta** (`--serie`): COMPRA à frente ou atrás do painel, e em
   quantas janelas de 24h venceu.
6. **Contrafactual.** Contagens das quatro versões e os pares que mudam.
7. **Fonte.** Saída de `fonte.py` (Passo 4): velas fechadas que a fonte
   devolveu diferentes do que estava na base. Par, campo e os dois valores.
   No caminho B não há base antiga; diga que não foi medido.
8. **Contraprova.** Onde o motor acertou algo que vinha sendo criticado, com o
   mesmo peso. **Autocorreção**: se um número desta execução contradiz algo
   afirmado num relatório anterior, diga qual relatório e o quê, com o mesmo
   destaque com que foi afirmado.
9. **Perguntas.** Atualize `radar/perguntas.md`: some 1 ao contador de cada
   uma, troque o "Hoje:" pelo dado desta execução, e copie a lista para o
   relatório. Pergunta nova entra no fim com "(1a)". Nenhuma é implementada.
10. **Procedência.** Fonte, horário da coleta, base usada, velas passadas por
    par, resultado do validador e dos testes, scripts rodados, e a frase
    "nenhum preço, indicador ou sinal deste relatório foi estimado, lembrado
    ou copiado de leitura anterior".

O que **não** entra: opinião sobre moeda, previsão, "dá para acumular",
lotes de 20+ COMPRA simultâneas no placar em R sem ordem do dono (Pergunta 18).

## Passo 7 — responder ao dono

O dono pediu modo crítico: **nenhuma resposta começa com elogio, concordância
ou validação; toda resposta começa pelo problema mais crítico medido.** Formato:

1. Primeira frase: o problema mais grave desta execução, com número.
2. Os sinais do motor, como o motor emitiu: COMPRA, VENDA, REALIZAR PARCIAL,
   bloqueados. Sem comentário dentro da lista.
3. **Lista de sobrevivência** (saída de `auditar.py`), sempre com este rótulo:
   *"não é sinal do motor; é o que sobra das COMPRA depois de descontar
   liquidez, vela morta, dependência do regime, cruzamento contrário e bordas
   de RSI e deriva."* Se o dono perguntar "quais as melhores para comprar", é
   esta lista, com esse rótulo, e com o stop de cada uma — nada além.
4. Placar em uma linha: janela, 24h e série composta.
5. Autocorreções, se houver.
6. Link do relatório no repositório.

Português simples, frases curtas, lista antes de tabela, sem jargão sem
explicação. Não amenize alerta de liquidez nem de vela morta.

## Passo 8 — commit

```bash
git add radar/relatorios radar/placar.csv radar/perguntas.md
git commit    # mensagem: contagem de sinais, marcas, contrafactual, placar
git push -u origin claude/moedas-sinais-compra-venda-zhq66i
```

Sem nome de modelo na mensagem. Nunca faça commit de `radar/dados/`.

## O que não fazer

- Não altere motor, regras ou constantes; não aplique contrafactual no repo.
- Não acrescente moedas fora de `radar/cobertas.txt`.
- Não transforme NEUTRO em conselho.
- Não chame a lista de sobrevivência de "recomendação" ou "melhores compras".
- Não copie perguntas, contadores ou números do relatório anterior: o que é
  canônico está em `perguntas.md` e `placar.csv`, e o resto é medido agora.
- Não trate disparo de rotina como resposta do dono.
