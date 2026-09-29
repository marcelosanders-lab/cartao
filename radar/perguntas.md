# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 28/09 22h.

1. **(37a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (28/09 22h): as 22h a deriva e medida contra
    a vela que acabou de fechar, entao todo mundo passa (25 de 28). Na
    janela 11h→22h os 10 bloqueados das 11h fizeram +0,66%, as 8 COMPRA
    -0,03%. LINK, bloqueado as 11h por "preco ja correu", subiu +7,52% -
    quinta leitura seguida em que esse bloqueio cai sobre quem sobe.
2. **(34a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 25→17 sem o bonus. O proprio BTC e NEUTRO
   (5/2) e continua dando o ponto de "regime de alta" aos outros 27. O grupo
   REGIME das 11h (ETH, SOL, AR, AIOZ) fez -0,81%, o painel -0,12%.
3. **(31a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 13 de 25 COMPRA.
4. **(33a)** A leitura das 11h deve considerar a vela em formacao?
5. **(32a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(31a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (28/09 22h): 8 COMPRA com
    marca MORTA (PENDLE, IMX, DYDX, AR, SUPER, LPT, PENGU, AIOZ). DYDX teve
    as velas 4h das 16:00 e 20:00 sem negocio e fechou o dia no preco do
    ultimo negocio das 12:00.
7. **(28a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: a rotina das 22h rodou no horario (disparo 22:03).
8. **(25a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (28/09 22h): 4 das 25 COMPRA com cruzamento de baixa no 4h
   (SOL, AAVE, LPT, AIOZ).
9. **(23a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (28/09 22h): nenhuma; a mais proxima e SEI em -0,31 ATR.
10. **(22a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SUPER com RSI 78 (no teto exato), SEI 77, PYTH 76.
11. **(19a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(18a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: os 9 "risco ja consumido" das 11h fizeram -0,10% ate as
    22h, as COMPRA -0,03% - empate.
13. **(15a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, **0**. Na janela 11h→22h os 3 barrados das 11h que
    entrariam com teto 85 (LTC, PYTH, SEI) fizeram -0,59% contra -0,03% das
    COMPRA: o teto evitou 0,56 pp.
14. **(13a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(13a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente", e de novo isso nao prova nada. Nesta
    coleta a fonte trouxe BTC 4h 24/09 16:00 com fechamento 84406,44 (base
    84418,23), BTC 4h 22/09 00:00 com outro volume, ETH 4h 24/09 16:00 com
    2696,50 (base 2695,89); e SOL 4h 22/09 16:00 voltou a 118,21 depois de
    vir 118,26 as 11h. Duas versoes alternando.
16. **(12a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "25 de 28 pares deram COMPRA" e na frase seguinte "Comprar os 20" - o
    numero errado esta impresso no relatorio.
17. **(11a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: leitura das 22h, nao se aplica.
18. **(11a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(7a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(6a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (28/09
    22h): 4 das 21 COMPRA das 22h de ontem fecharam o dia abaixo da propria
    invalidacao (DYDX, JUP, ONDO, PENDLE) e as 4 voltaram a ser COMPRA, com
    stop 9,5% a 14,9% mais baixo. Em 24h, 17 de 19 stops rebaixados.
21. **(6a)** Outra fonte de velas. Todos os sites de preço testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa acessivel.
22. **(6a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (28/09 22h): indisponivel, 403 da rede do ambiente, sexta coleta
    seguida.
