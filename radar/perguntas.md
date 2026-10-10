# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 10/10 11h.

1. **(61a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (10/10 11h): 4 barrados por "preco ja
    correu": ONDO (+0,38 ATR, R:R 1,39:1), AIOZ (+0,44, 1,32:1), NEAR
    (+0,93, 0,86:1) e LPT (+0,95, 0,83:1). Nenhum por "risco ja
    consumido". O barrado das 22h (IMX) fez -4,89% ate as 11h, contra
    +1,08% do painel e +0,12% das COMPRA: o portao acertou. Em 24h, os 3
    barrados das 11h de ontem fizeram -3,68% contra +4,57% das COMPRA.
    Placar do portao: dez contra, onze a favor.
2. **(58a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: regime em BAIXA pela sexta leitura;
   4→4 sem o bonus, nenhuma COMPRA depende dele. Nao havia REGIME as 22h
   nem as 11h de ontem: sem medida. Placar na janela curta: nove a favor
   do bonus, seis contra.
3. **(55a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 4 de 4 COMPRA (PYTH, JUP, IMX, DYDX). Na
   janela, as 5 COMPRA das 22h eram todas LIQ: +0,12% contra +1,08% do
   painel, sem grupo limpo para comparar. Contra a pergunta em 24h: o LIQ
   das 11h de ontem (LPT) fez +6,35% contra +2,79% de AAVE, saido de uma
   unica vela de 4h (US$ 1.351,12).
4. **(57a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (11h): das 5 COMPRA das 22h, 2 continuam COMPRA (JUP, PYTH); ONDO e
   AIOZ viraram "preco ja correu" e WLFI, NEUTRO. A barrada das 22h (IMX)
   virou COMPRA depois de cair 4,89%.
5. **(56a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: DYDX e COMPRA por
   gatilho 4h; o cruzamento fechou na vela das 04:00 (US$ 177,37) e se
   manteve na das 08:00 (US$ 17,62). Sem os +2 seria 5/4. Contra a
   pergunta em 24h: LPT, gatilho 4h das 11h de ontem, fez +6,35%.
6. **(55a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (10/10 11h): 2 COMPRA com
    MORTA (IMX, DYDX). O "Agora" de IMX (0,19684) e um negocio de US$
    403,84 na vela das 08:00; o de DYDX (0,1393), US$ 17,62 na mesma
    vela. Nenhuma das duas tem negocio na vela das 12:00. Contra a
    pergunta na janela: o MORTA das 22h (AIOZ) fez +3,61% contra -0,76%
    do resto, com o preco final num negocio de US$ 65,95. Nao havia MORTA
    entre as COMPRA das 11h de ontem: sem medida em 24h.
7. **(52a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z) com a base das 22h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(49a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (10/10 11h): nenhuma COMPRA com X4H-. Nao havia X4H- as 22h
   nem as 11h de ontem: sem medida.
9. **(47a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (10/10 11h): nenhuma DER-BORDA. Sem medida.
10. **(46a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 68 (IMX).
11. **(43a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 4
    "preco ja correu": ONDO (0,49746, alvo 0,59763215), AIOZ (0,1199, alvo
    0,14401014), NEAR (5,3772, alvo 6,4834971) e LPT (1,825, alvo
    2,0592061). Nenhum chegou ao alvo.
12. **(42a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(38a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, **0**. Hoje: com teto 85, nada muda (4 COMPRA nas
    duas versoes).
14. **(37a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(37a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    22h: ETH diaria de 07/09 (2490,49 contra 2490,08), 30/08 (2416,87
    contra 2417,19) e 29/08 (2457,69 contra 2457,70), como as 22h. SOL
    diaria de 30/08 voltou a bater com a base (101,75). A diaria de PENDLE
    em formacao abre em 2,1364 enquanto as velas de 4h do dia abrem em
    2,0984 sem negocio. A base nao foi alterada.
16. **(36a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 4 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(35a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (11h): 2 das 4 COMPRA eram COMPRA as 22h (JUP, PYTH).
    IMX veio de "preco ja correu" e DYDX de NEUTRO.
18. **(35a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(31a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. DYDX depende do +2 do cruzamento de
    alta no 4h (sem ele, 5/4). Os 4 barrados (ONDO, AIOZ, NEAR, LPT) tem
    cruzamento de alta no 4h e foram recusados pela deriva.
20. **(30a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (10/10
    11h): as 5 COMPRA das 22h estao acima do stop. JUP e PYTH, COMPRA nas
    duas leituras, com stop igual. Em 24h, nenhum par COMPRA nas duas.
21. **(30a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(30a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (10/10 11h): indisponivel, 403 da rede do ambiente, trigesima coleta
    seguida.
23. **(22a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista esta vazia (0 de 4), pela segunda leitura seguida. A das 22h
    estava vazia: sem medida na janela. A das 11h de ontem (so AAVE) fez
    +2,79% em 24h contra +2,75% do painel (+0,04 pp): vitoria por margem
    minima, fim de oito derrotas seguidas. No total, 17 vitorias em 44.
