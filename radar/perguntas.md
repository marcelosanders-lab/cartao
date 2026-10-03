# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 02/10 22h.

1. **(45a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (02/10 22h): das 11h as 22h os 16 barrados
    das 11h fizeram -3,44%, contra -2,58% das COMPRA: ponto a favor do
    portao. Placar do portao: seis leituras contra, quatro a favor. Em 24h,
    o unico barrado de ontem (LTC) fez +2,29%, contra -0,49% das COMPRA. As
    22h, 2 barrados: SUI (+0,38 ATR) e PYTH (+0,32 ATR).
2. **(42a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 20→9 sem o bonus; 11 COMPRA so existem
   por ele, e o proprio BTC esta NEUTRO. A favor da pergunta: em 24h, o
   grupo REGIME de ontem as 22h fez -1,61% contra -0,03% das outras COMPRA;
   na janela, o das 11h fez -3,58% contra -2,34%. Contra: o regime "alta"
   segue a regra (`analisar.py:409`) e as COMPRA bateram o painel na
   janela.
3. **(39a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 12 de 20 COMPRA. A favor da pergunta: o
   grupo LIQ das 11h fez -3,33% ate as 22h, contra -2,09% do resto; em 24h,
   -1,59% contra +0,60%.
4. **(41a)** A leitura das 11h deve considerar a vela em formacao? Hoje: 11
   dos 16 barrados das 11h voltaram a COMPRA as 22h, quase todos depois de
   cair. Os 13 que eram COMPRA ontem as 22h fizeram -3,71% das 11h as 22h;
   as 10 COMPRA das 11h, -2,58%.
5. **(40a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje (22h): nenhuma COMPRA
   rotulada por gatilho 4h.
6. **(39a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (02/10 22h): 6 COMPRA com
    marca MORTA (IMX, DYDX, AR, LPT, AIOZ, ASTR). O dia inteiro de AR foram
    dois negocios, US$ 134,02. A favor da pergunta: o grupo MORTA das 11h
    (DYDX, AR) fez -5,78% ate as 22h, contra -1,78% do resto.
7. **(36a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(33a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (02/10 22h): 4 COMPRA com X4H- (AVAX, SHIB, AR, ASTR). O
   grupo X4H- de ontem as 22h (NEAR, SHIB) fez -1,97% em 24h, contra -0,36%
   do resto.
9. **(31a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (02/10 22h): 2 COMPRA com DER-BORDA, LTC (+0,26 ATR) e
    ASTR (+0,27 ATR). O limite e +0,30.
10. **(30a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA; AAVE com RSI 73 e a mais alta.
11. **(27a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 2
    barrados por preco ja corrido (SUI, PYTH). Nenhum chegou ao alvo. Nas
    11h eram 15, e nao 16 como escrevi.
12. **(26a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo. LMWR, barrado assim as 11h,
    virou VENDA.
13. **(23a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, **0**. Hoje: SUPER, com
    RSI 86, segue como REALIZAR PARCIAL.
14. **(21a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 27 dos 28 pares vieram iguais. No BTC, 84674,03 na diaria e
    84665,14 no 4h.
15. **(21a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a ETH diaria de 07/09
    veio 2490,08 (base 2490,49) e a SUI diaria de 30/08 veio 0,71114 (base
    0,71134). A alternancia continua.
16. **(20a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "20 de 28" e "Comprar os 20"; bate por coincidencia.
17. **(19a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 9 das 20 COMPRA ja eram COMPRA as 11h; 11 voltaram
    do bloqueio das 11h.
18. **(19a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(15a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21; LMWR, que tinha, virou VENDA.
20. **(14a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (02/10
    22h): das 11h para ca, 8 de 9 stops desceram (AR -6,06%, LINK -5,03%,
    DYDX -5,00%). Em 24h, 14 de 19; LPT -5,59%.
21. **(14a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(14a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (02/10 22h): indisponivel, 403 da rede do ambiente, decima quarta
    coleta seguida.
23. **(6a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h fez -2,46% ate as 22h contra -2,85% do painel (+0,39
    pp); a das 22h de ontem fez +1,56% em 24h contra -0,26% (+1,82 pp).
    Sete vitorias nas ultimas dez medicoes, depois de cinco derrotas.
