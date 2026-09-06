# Radar de cripto — leituras das 11h e 22h

Sistema mecânico de sinais de compra e venda sobre a sua lista de moedas, com
duas leituras por dia (11h e 22h, horário de Brasília).

## Antes de usar: quatro limitações que mudam o que dá para esperar disto

**1. Nem todas as suas moedas entram.** A única fonte de preços acessível neste
ambiente é a Crypto.com Exchange (as APIs da Binance e da CoinGecko estão
bloqueadas pela política de rede). 28 dos seus pares existem lá. **14 não
existem** — entre eles ANKR e TOSHI, que estão na sua lista de selecionadas.
Para essas moedas o radar não emite sinal nenhum, e vai dizer isso em todo
relatório em vez de fingir cobertura. A lista completa está em `moedas.json`.

**2. Suas listas do TradingView misturam moedas com índices.** `BTC.D`,
`OTHERS.D`, `TOTAL3`, `SPX`, `NDAQ` e `RUSSELL` não são pares negociáveis — são
índices de dominância e de bolsa. `AEROUSDT.P`, `PENGUUSDT.P` e `RENDERUSDC.P`
são contratos perpétuos, não spot. Nenhum recebe sinal.

**3. Os preços são da Crypto.com, não da Binance.** Nos pares grandes a
diferença é irrelevante. Em pares magros é grave: SUPER movimenta ~US$ 129/dia
lá, LMWR ~US$ 10/dia. Um gráfico desses tem buracos e pavios que geram
cruzamentos inexistentes. O relatório marca todo par abaixo de US$ 50 mil/dia
como preço pouco confiável. Nesses, confira no seu gráfico antes de agir.

**4. O sistema não tem backtest.** Os limiares são convenções de seguimento de
tendência, não parâmetros otimizados. Ninguém sabe qual é o acerto histórico
deles nessas moedas. Isso não é um detalhe: significa que o valor real do radar
é obrigar você a olhar as mesmas regras todo dia, não prever o mercado.

## Como funciona

Tendência pelo gráfico diário (EMA9/EMA21, RSI14, MACD, ATR14), gatilho pelo
gráfico de 4h (cruzamento EMA9×EMA21), filtro de regime pelo BTC. Pontuação
fixa, decisão por limiar, stop e alvo calculados. Regras completas e a
justificativa de cada peso: **`regras.md`**.

Velas em formação nunca entram na conta. Por isso a leitura das 22h é a que
importa — é logo depois do fechamento da vela diária (21h de Brasília). Às 11h
a vela diária fechada ainda é a mesma da véspera; só o 4h mudou, e o relatório
avisa isso na primeira linha.

## Arquivos

| Arquivo | O quê |
|---|---|
| `analisar.py` | motor: indicadores, regras, relatório. Nenhum número é estimado |
| `testes.py` | testes do motor (RSI conferido contra a série clássica de Wilder) |
| `regras.md` | as regras e os pesos, por extenso |
| `moedas.json` | universo: cobertas, sem cobertura e não negociáveis |
| `cobertas.txt` | os 28 pares que a rotina coleta |
| `prompt-rotina.md` | o roteiro que a sessão agendada executa |
| `dados/` | velas brutas da rodada (descartável, não versionado) |
| `relatorios/` | relatórios gerados, um por leitura |

## Rodar na mão

```bash
python3 radar/testes.py                                  # sempre antes
# baixe as velas para radar/dados/<PAR>_1d.json e <PAR>_4h.json
python3 radar/analisar.py --dir radar/dados --janela noite
python3 radar/analisar.py --dir radar/dados --janela noite --json   # saída bruta
```

O motor recusa-se a rodar sem dados em disco. Ele nunca inventa preço.

## Mudar o comportamento

As constantes ficam no topo de `analisar.py` (`SCORE_COMPRA`, `STOP_ATR`,
`RSI_SOBRECOMPRA`, `LIQUIDEZ_MINIMA_USD`...). Mude lá, rode `testes.py`, e
atualize `regras.md` para o documento continuar sendo verdade.

## Aviso

Sinais mecânicos, sem backtest, sobre uma fonte de preços parcial. Não são
recomendação de investimento. O radar não sabe o tamanho da sua posição, não
conhece seu capital e não conhece nenhuma notícia.
