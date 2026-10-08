# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 07/10 22h.

1. **(56a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (07/10 22h): 1 barrado por "preco ja
    correu" (JUP, +0,43 ATR, R:R 1,33:1); nenhum por "risco ja
    consumido". Os 14 barrados das 11h por "risco ja consumido" fizeram
    +2,28% ate as 22h, contra +1,70% do painel e +1,34% das COMPRA: o
    portao recusou o grupo que mais rendeu. Mas quem carrega o grupo e
    JUP (+16,46%); sem ele, os 13 fizeram +1,18%, abaixo do painel.
    Placar do portao: nove contra, oito a favor.
2. **(53a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: o regime virou BAIXA, a primeira vez
   desde 18/09 11h. Nenhuma COMPRA depende do bonus (6→6 sem ele); as 6
   COMPRA levam o -2 do regime e passam mesmo assim. A favor da pergunta
   nesta janela: o REGIME das 11h fez +1,25% contra +1,85% da unica outra
   COMPRA (SUI). Contra, em 24h: o das 22h de ontem fez -3,63% contra
   -4,05%. Placar na janela curta: nove a favor do bonus, seis contra.
3. **(50a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 4 de 6 COMPRA (IMX, RENDER, SUPER, AIOZ).
   Contra a pergunta nesta janela: o LIQ das 11h (ONDO, AIOZ) fez +2,42%
   contra +0,91% do resto. A favor, em 24h: o das 22h de ontem fez -4,39%
   contra -2,92%.
4. **(52a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (22h): das 7 COMPRA das 11h, 2 continuam COMPRA (NEAR, AIOZ), 3 viraram
   NEUTRO (SUI, LTC, AVAX) e 2 VENDA (LINK, ONDO). Dos 18 que a vela em
   formacao tirou de COMPRA as 11h, 4 voltaram (AAVE, RENDER, SUPER, IMX).
5. **(51a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhum.
6. **(50a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (07/10 22h): 2 COMPRA com
    marca MORTA (IMX, SUPER). Nas duas, o fechamento diario saiu da vela
    de 4h das 16:00 (US$ 133,55 em IMX, US$ 146,06 em SUPER); as velas das
    20:00 e de 08/10 nao tem negocio. Contra a pergunta nesta janela: o
    MORTA das 11h (AIOZ) fez +3,31% contra +1,01%. A favor, em 24h: o das
    22h de ontem fez -5,35% contra -3,31%.
7. **(47a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z) com a base das 11h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(44a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (07/10 22h): nenhuma COMPRA com X4H-. Contra a pergunta nas
   duas medidas: o X4H- das 11h (AIOZ) fez +3,31% contra +1,01%; o das 22h
   de ontem, -3,51% contra -3,89% em 24h.
9. **(42a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (07/10 22h): nenhuma DER-BORDA. As 3 DER-BORDA das 11h
    (LTC, LINK, ONDO) fizeram +0,17% contra +2,22% das outras COMPRA; LINK
    e ONDO viraram VENDA.
10. **(41a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 67 (NEAR).
11. **(38a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 1
    "preco ja correu" (JUP, 0,37028); o alvo dele e 0,43835. Nenhum chegou
    ao alvo.
12. **(37a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(33a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, **0**. Hoje: com teto 85, nada muda (6 COMPRA nas duas versoes).
14. **(32a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(32a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    11h: SOL 4h de 05/10 08:00 voltou a 120,81 (base 120,83) e a de 02/10
    16:00 veio 118,00 (base 117,99); BTC diaria de 06/09 fecha 80344,16
    (base 80344,15). A base nao foi alterada.
16. **(31a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 6 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(30a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 2 das 6 COMPRA ja eram COMPRA as 11h (NEAR, AIOZ);
    AAVE, RENDER e SUPER vieram de "risco ja consumido" e IMX de "abaixo
    do stop".
18. **(30a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(26a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. Nenhuma COMPRA por gatilho 4h.
20. **(25a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (07/10
    22h): IMX fechou 0,17293, abaixo do stop das 22h de ontem (0,17497), e
    voltou a COMPRA com stop 0,15589, 10,90% mais baixo. Em 24h, 4 de 6
    stops desceram (IMX -10,90%, RENDER -7,92%, SUPER -7,38%, AAVE
    -3,46%). Dos 4 "abaixo do stop" das 11h, so IMX e LPT fecharam abaixo;
    ETH (2574,02 contra 2571,95) e ASTR (0,0069861 contra 0,0069681)
    fecharam acima.
21. **(25a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(25a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (07/10 22h): indisponivel, 403 da rede do ambiente, vigesima quinta
    coleta seguida.
23. **(17a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h (so SUI) fez +1,85% contra +1,70% do painel (+0,15
    pp); a das 22h de ontem (so BTC) fez -2,34% em 24h contra -3,75%
    (+1,41 pp). No total, 16 vitorias em 35; quatro seguidas. A lista de
    agora tem 2 pares (AAVE, NEAR) de 6 COMPRA.
