# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 05/10 11h.

1. **(50a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (05/10 11h): 5 barrados: PENDLE (+0,63 ATR),
    AAVE (+0,57), AIOZ (+0,55), LPT (+0,46) e ICP (+0,31). AIOZ foi barrado
    por um unico bloco de US$ 124,27 que subiu o preco 4,54%. Na janela
    22h → 11h nao havia barrado as 22h: sem medida; o placar do portao segue
    sete contra, sete a favor. Os 3 que o portao barrou ontem as 11h (ASTR,
    SOL, SEI) e que a vela diaria nova readmitiu as 22h fizeram -1,68% desde
    as 22h, contra +0,89% das outras 20 COMPRA das 22h. Em 24h, os
    mesmos 3 fizeram -0,88% contra +1,74% das COMPRA.
2. **(47a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 20→14 sem o bonus; 6 COMPRA so existem
   por ele (AR, AVAX, IMX, JUP, SUPER, UNI) e 3 barrados virariam NEUTRO.
   Contra a pergunta, nas duas medidas: na janela, o REGIME das 22h fez
   +0,83% contra -0,03% das outras COMPRA; em 24h, o das 11h de ontem fez
   +2,61% contra +1,21% (sem PENGU, +2,14%). Placar na janela curta: seis a
   favor do bonus, quatro contra.
3. **(44a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 12 de 20 COMPRA. Nesta janela, empate: o
   LIQ das 22h fez +0,35% contra +0,34% do resto. Em 24h, +1,63% contra
   +1,89% (sem PENGU, +1,25%).
4. **(46a)** A leitura das 11h deve considerar a vela em formacao? Hoje: 5
   das 25 COMPRA das 22h viraram SEM ENTRADA sem vela diaria nova (AAVE,
   AIOZ, ICP, LPT, PENDLE). Fizeram +2,94% em media desde as 22h; as outras
   20, -0,30%. Os 5 pares que entraram em COMPRA as 22h (SEI, SOL, ASTR,
   BTC, SUPER) fizeram -1,81%.
5. **(45a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: 6, LINK, DYDX, PYTH,
   NEAR, ONDO e PENGU. DYDX negociou US$ 142,99 no dia. Contra a pergunta
   em 24h: as 3 das 11h de ontem (PENDLE, ETH, JUP) fizeram +2,26% contra
   +1,66% das outras COMPRA.
6. **(44a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (05/10 11h): 2 COMPRA com
    marca MORTA (IMX, DYDX). Fora da marca: AR negociou um unico bloco no
    dia (US$ 506,89), que baixou o preco 1,13%; SUPER caiu 3,79% com
    US$ 1.019 no dia e ficou com o melhor R:R da lista (4,41:1). Contra a
    pergunta nesta janela: o MORTA das 22h fez +0,77% contra +0,21% das
    outras COMPRA, puxado por AIOZ (+4,54% num bloco de US$ 124).
7. **(41a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(38a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (05/10 11h): 1 COMPRA com X4H- (DYDX). O X4H- das 22h (LPT,
   PYTH) fez +1,88% contra +0,21% do resto: contra a pergunta.
9. **(36a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (05/10 11h): 2 COMPRA com DER-BORDA, PENGU (+0,30 ATR,
    exatamente no limite) e NEAR (+0,27). As duas sao COMPRA por gatilho 4h.
10. **(35a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SUPER segue com RSI 77,976 e marca RSI-BORDA. Desde as 22h fez
    -3,79%.
11. **(32a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 5
    barrados por preco ja corrido (PENDLE, AAVE, AIOZ, LPT, ICP). Nenhum
    chegou ao alvo.
12. **(31a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(28a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, **0**. Hoje:
    com teto 85, nada muda (20 COMPRA nas duas versoes).
14. **(26a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(26a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a AAVE diaria de 01/10
    voltou para 171,454 (as 22h veio 171,387, igual a base e ao proprio 4h).
    A BTC diaria de 06/09 voltou para 80344,15 (as 22h, 80344,16). A SOL
    diaria de 30/08 veio 101,75 (base 101,78). A AVAX 4h de 29/09 16:00 veio
    de novo com volume diferente da base. A fonte segue alternando.
16. **(25a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "20 de 28" e "Comprar os 20". Bate por coincidencia; o numero continua
    fixo no codigo.
17. **(24a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 20 das 20 COMPRA ja eram COMPRA as 22h; nenhuma e nova.
    6 delas mudaram para "gatilho 4h".
18. **(24a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(20a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. 6 COMPRA por gatilho 4h, 2 delas no
    limite de deriva.
20. **(19a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (05/10
    11h): das 22h para ca, nenhum dos 20 stops mudou (mesma vela diaria). Em
    24h, 3 de 15 desceram: AR -5,05%, DYDX -0,81%, ONDO -0,17%.
21. **(19a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(19a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (05/10 11h): indisponivel, 403 da rede do ambiente, decima nona coleta
    seguida.
23. **(11a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (BTC, ETH, SOL, SUI, LINK, SHIB) fez -0,38% ate as 11h
    contra +0,36% do painel (-0,74 pp); a das 11h de ontem (ETH, AAVE, SUI,
    LINK, PYTH) fez +1,64% em 24h contra +1,09% (+0,55 pp). No total, 12
    vitorias em 25.
