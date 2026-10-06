# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 05/10 22h.

1. **(52a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (05/10 22h): os 5 barrados das 11h (AAVE,
    AIOZ, ICP, LPT, PENDLE) viraram todos COMPRA com a vela diaria nova.
    Tres deles (AIOZ, LPT, PENDLE) estao em vela morta; AIOZ voltou com
    deriva +0,00 sobre um fechamento feito por um bloco de US$ 124,27. Das
    11h ate as 22h o grupo barrado fez +0,10% contra +0,57% das COMPRA: o
    portao acertou. Placar do portao: sete contra, oito a favor.
2. **(49a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 25→16 sem o bonus; 9 COMPRA so existem
   por ele (AAVE, AR, ETH, IMX, LINK, NEAR, ONDO, SOL, SUPER); com regime
   em baixa ONDO vira VENDA. Contra a pergunta, nas duas medidas: o REGIME
   das 11h fez +1,67% contra +0,09% das outras COMPRA; o das 22h de ontem,
   +1,94% contra -0,05% em 24h (sem NEAR, +1,32%). Placar na janela curta:
   sete a favor do bonus, quatro contra.
3. **(46a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 16 de 25 COMPRA. Contra a pergunta nas duas
   medidas: o LIQ das 11h fez +0,60% contra +0,51% do resto; o das 22h de
   ontem, +0,84% contra +0,78% em 24h.
4. **(48a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (22h): a vela diaria nova desfez os 5 bloqueios das 11h e apagou os 6
   "gatilho 4h". Na leitura extra das 12h08, uma hora de vela em formacao
   ja tinha posto PENDLE em COMPRA.
5. **(47a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhum "gatilho 4h".
   Os 6 das 11h (LINK, DYDX, PYTH, NEAR, ONDO, PENGU) fizeram -0,30% ate as
   22h contra +0,94% das outras COMPRA (sem NEAR, -1,37%). A favor da
   pergunta. AIOZ e LPT ganharam +2 por "cruzamento de alta no 4h" em velas
   sem negocio.
6. **(46a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (05/10 22h): 9 COMPRA com
    marca MORTA (PENDLE, IMX, ONDO, DYDX, AR, SUPER, LPT, AIOZ, ASTR), o
    maior numero registrado. Fechamentos de negocio isolado: AIOZ (US$
    124,27), IMX (US$ 240,49, +4,64%), AR (US$ 25,00, +2,22%). Na janela
    curta, o MORTA das 11h fez -0,35% contra +0,67%; em 24h, o das 22h de
    ontem fez +1,05% contra +0,75%.
7. **(43a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(40a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (05/10 22h): 5 COMPRA com X4H- (UNI, AVAX, ONDO, DYDX,
   PYTH). O X4H- das 11h (DYDX) fez -1,82% contra +0,69%; o das 22h de
   ontem (LPT, PYTH), +1,07% contra +0,80% em 24h.
9. **(38a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (05/10 22h): nenhuma DER-BORDA. Com a vela diaria recem
    fechada, todas as derivas ficaram entre -0,23 e +0,16 ATR.
10. **(37a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 73 (AAVE, ICP,
    SUPER).
11. **(34a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje:
    nenhum barrado por preco ja corrido.
12. **(33a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(30a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, **0**.
    Hoje: com teto 85, nada muda (25 COMPRA nas duas versoes).
14. **(28a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(28a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a SOL 4h de 05/10
    08:00 veio 120,81 pela segunda vez (base 120,83). A ETH diaria de 07/09
    voltou a bater com a base; a ETH 4h de 02/10 16:00 veio 2668,73 (base
    2668,68). A SUI diaria de 30/08 veio 0,71114 (base 0,71134). A AAVE
    voltou a 171,387 nos dois prazos. A fonte segue alternando.
16. **(27a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "25 de 28" e "Comprar os 20". O numero fixo erra pela segunda leitura
    seguida.
17. **(26a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 20 das 25 COMPRA ja eram COMPRA as 11h; 5 sao
    novas (AAVE, AIOZ, ICP, LPT, PENDLE), todas barradas as 11h.
18. **(26a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(22a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. Nenhuma COMPRA por gatilho 4h.
20. **(21a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (05/10
    22h): das 11h para ca, 8 de 20 stops desceram: SUPER -3,87%, LINK
    -3,09%, BTC -0,90%, ETH -0,56%, SOL -0,56%, SHIB -0,34%, DYDX -0,29%,
    ASTR -0,13%. Em 24h, os mesmos 8 de 25.
21. **(21a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(21a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (05/10 22h): indisponivel, 403 da rede do ambiente, vigesima primeira
    coleta seguida.
23. **(13a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h fez -0,53% ate as 22h contra +0,32% do painel (-0,85
    pp); a das 22h de ontem fez -0,90% em 24h contra +0,68% (-1,58 pp). No
    total, 12 vitorias em 27. Hoje sobram 3 de 25 (BTC, SUI, SHIB).
