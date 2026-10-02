# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 01/10 22h.

1. **(43a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (01/10 22h): das 11h as 22h os 3 bloqueados
    (AAVE, AR, NEAR) fizeram +0,40%, as 21 COMPRA +0,39%, o painel +0,98%.
    Empate (0,01 pp); nao conto como voto. Placar do portao: seis leituras
    contra, duas a favor. As 22h, 1 bloqueado: LTC, a +0,32 ATR, 0,02 acima
    do limite.
2. **(40a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 24→17 sem o bonus; 7 COMPRA so existem
   por ele (ETH, SOL, UNI, AR, AIOZ, ASTR, LMWR). A favor da pergunta: o
   grupo REGIME das 11h fez -1,65% ate as 22h, contra +1,21% das outras
   COMPRA; em 24h, o grupo das 22h de ontem fez -1,14% contra +0,67%.
   Contra: o BTC virou COMPRA (8/1) nesta leitura.
3. **(37a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 12 de 24 COMPRA. Contra a pergunta: o grupo
   LIQ das 11h fez +0,33% ate as 22h; o resto das COMPRA, +0,46%.
4. **(39a)** A leitura das 11h deve considerar a vela em formacao? Hoje: as
   21 COMPRA das 11h fizeram +0,39% ate as 22h, 0,59 pp abaixo do painel.
   AAVE, AR e NEAR, barrados as 11h, voltaram a COMPRA; LTC fez o caminho
   contrario.
5. **(38a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje (22h): nenhuma COMPRA
   rotulada por gatilho 4h. Contra a pergunta: as 3 das 11h (IMX, ETH,
   SHIB) fizeram +1,54% ate as 22h, contra +0,20% das outras COMPRA.
6. **(37a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (01/10 22h): 7 COMPRA com
    marca MORTA (IMX, DYDX, RENDER, AR, LPT, AIOZ, LMWR). LMWR nao negocia
    desde 30/09 04:00 UTC; AR, desde 01/10 08:00 UTC; o "Agora" de IMX e
    um negocio de US$ 66,75.
7. **(34a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(31a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (01/10 22h): 2 das 24 COMPRA (NEAR, SHIB). O grupo X4H-
   das 11h fez -0,52% ate as 22h, contra +0,98% do painel.
9. **(29a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (01/10 22h): nenhuma marca DER-BORDA. Do outro lado do
    limite, LTC foi barrado a +0,32 ATR, 0,02 acima.
10. **(28a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA; AAVE com RSI 70 e a mais alta.
11. **(25a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: LTC
    barrado por preco ja corrido (+0,32 ATR).
12. **(24a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(21a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, **0**. Hoje: SUPER, com RSI 86,
    esta acima ate do teto 85 e saiu como REALIZAR PARCIAL.
14. **(19a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: nos 28 pares, o fechamento da diaria em formacao e o da ultima
    vela de 4h vieram iguais.
15. **(19a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a ETH diaria de 07/09
    veio 2490,08 (base 2490,49) e a ETH de 4h de 24/09 16:00 veio 2696,50
    (base 2695,89). A alternancia continua.
16. **(18a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "24 de 28" e, na frase seguinte, "Comprar os 20".
17. **(17a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 20 das 24 COMPRA ja eram COMPRA as 11h; novas:
    BTC, AAVE, AR e NEAR.
18. **(17a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(13a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: LMWR segue
    COMPRA com a EMA9 diaria abaixo da EMA21.
20. **(12a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (01/10
    22h): das 11h para ca, 8 de 20 stops desceram (PYTH -5,03%, LPT
    -4,47%, SEI -4,40%). Em 24h, 9 de 23; NEAR -12,26%.
21. **(12a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(12a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (01/10 22h): indisponivel, 403 da rede do ambiente, decima segunda
    coleta seguida.
23. **(4a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h fez +0,83% ate as 22h contra +0,98% do painel (-0,15
    pp); a das 22h de ontem fez +1,25% em 24h contra +0,72% (+0,53 pp).
    Quatro vitorias nas ultimas seis medicoes, depois de cinco derrotas.
