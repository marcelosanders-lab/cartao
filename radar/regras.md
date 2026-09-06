# Regras de sinal

Tudo aqui é mecânico. O motor (`analisar.py`) não interpreta, não opina e não
tem espaço para "achismo": ele lê velas, calcula e aplica os pontos abaixo.
Mudar o comportamento do radar significa mudar as constantes no topo de
`analisar.py` — não significa argumentar com o relatório.

## O que entra na conta

| Prazo | Papel | Indicadores |
|---|---|---|
| Diário (1D, 50 velas) | define a tendência | EMA9, EMA21, RSI14, histograma MACD(12,26,9), ATR14 |
| 4 horas (4h, 50 velas) | define o gatilho de entrada | cruzamento EMA9 × EMA21 |

**Velas em formação nunca entram no cálculo.** A vela mais recente devolvida
pela corretora ainda está aberta; um sinal calculado sobre ela muda sozinho até
o fechamento e não é reproduzível. O fechamento dessa vela aberta aparece no
relatório só como coluna "Agora", para referência de preço.

Consequência prática: às 22h a vela diária acabou de fechar (21h de Brasília).
Às 11h da manhã a última vela diária fechada **é a mesma** — só o gráfico de 4h
mudou. Por isso um sinal novo pela manhã é rotulado `COMPRA (gatilho 4h)`: ele
nasce só do prazo curto e vale menos que o sinal da noite.

## Pontuação

Cada par recebe um score de compra e um de venda:

| Condição | Compra | Venda |
|---|---|---|
| Fechamento diário acima da EMA21 | +2 | — |
| Fechamento diário abaixo da EMA21 | — | +2 |
| EMA9 diária acima da EMA21 | +2 | — |
| EMA9 diária abaixo da EMA21 | — | +2 |
| Histograma MACD diário positivo / negativo | +1 | +1 |
| MACD acelerando / perdendo força | +1 | +1 |
| Cruzamento de alta no 4h nas últimas 3 velas | +2 | — |
| Cruzamento de baixa no 4h nas últimas 3 velas | — | +2 |
| RSI diário entre 45 e 68 (zona de tendência) | +1 | — |
| RSI diário acima de 78 (sobrecomprado) | — | +2 |
| Preço mais de 15% acima da EMA21 (esticado) | — | +1 |
| BTC em regime de alta (não se aplica ao próprio BTC) | +1 | — |
| BTC em regime de baixa (não se aplica ao próprio BTC) | — | +2 |

Regime do BTC: **alta** quando o fechamento diário e a EMA9 estão acima da
EMA21; **baixa** quando o fechamento está abaixo da EMA21; neutro no resto.

## Decisão

| Sinal | Condição |
|---|---|
| `REALIZAR PARCIAL` | RSI diário ≥ 85, qualquer que seja o score |
| `COMPRA` | score de compra ≥ 6, maior que o de venda, e RSI diário < 78 |
| `VENDA` | score de venda ≥ 5 e maior que o de compra |
| `NEUTRO` | resto |

O RSI alto derruba a compra de propósito: o sistema segue tendência, mas se
recusa a comprar depois que o movimento já aconteceu.

## Gestão da posição

Toda `COMPRA` sai com stop e alvo calculados, não sugeridos:

- **Stop** = fechamento diário − 1,5 × ATR14 diário
- **Alvo** = fechamento + 2 × (fechamento − stop), ou seja, risco/retorno 2:1
- **Invalidação** = fechamento diário abaixo do stop (fechamento, não pavio)

Toda `VENDA` sai com o critério de reentrada: fechamento diário de volta acima
da EMA21. Sem isso, "vendi" vira "fiquei de fora para sempre".

Tamanho da posição não é calculado aqui porque o radar não conhece seu capital.
A regra que fecha o sistema é sua: arrisque um percentual fixo do capital por
operação (1% é o padrão de mercado) e derive a quantidade de
`capital × 1% ÷ (preço − stop)`. Um sinal sem tamanho de posição definido não é
um sistema, é um palpite com número.

## Filtro de confiabilidade da fonte

Pares com volume médio abaixo de US$ 50.000/dia na Crypto.com saem marcados. O
sinal continua sendo calculado, mas o preço da fonte é ruim: pavios largos e
buracos no gráfico geram cruzamentos que não existem na corretora onde você
opera de fato. Confira esses no seu gráfico antes de agir.

## O que este sistema não é

- **Não tem backtest.** Os limiares (6 pontos, 1,5 ATR, 15%) são convenções de
  seguimento de tendência, não parâmetros otimizados sobre o histórico dessas
  moedas. Ninguém sabe qual é o acerto histórico dele.
- **Não conhece notícia, desbloqueio de tokens, listagem, hack ou liquidez do
  livro.** Só preço e volume.
- **Perde dinheiro em mercado lateral.** Todo sistema de seguimento de
  tendência perde: ele entra no rompimento e sai no repique. O retorno vem de
  poucas operações grandes, e só se você respeitar o stop nas outras.
- **Não é recomendação de investimento.**

## Diagnóstico de seletividade

Quando 60% ou mais dos pares avaliados disparam COMPRA na mesma leitura, o
relatório abre com um aviso. O motivo é direto: um sistema que compra quase tudo
não está escolhendo moeda, está apenas informando que o mercado inteiro está
acima da média móvel. Isso é leitura de regime, não seleção.

Foi o que aconteceu na primeira leitura completa (06/09/2026): **23 de 28 pares
deram COMPRA**. O sinal ali não distingue nada — todas as 28 moedas subiram
junto desde a virada de 19/08. Agir sobre a lista inteira é comprar o mercado
pagando 23 taxas de corretagem e assumindo 23 stops.

Isso é uma limitação estrutural de qualquer sistema de seguimento de tendência
aplicado a uma cesta correlacionada, não um defeito de implementação. A correção
não é mexer nos pesos até a lista encurtar — isso seria ajustar a régua ao
resultado. A correção é sua: escolher entre os sinais por critério que o radar
não tem (liquidez real na sua corretora, convicção na tese, tamanho de posição)
e aceitar que em mercado de alta generalizada o radar não agrega seleção.
