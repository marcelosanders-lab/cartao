# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 02/10 11h.

1. **(44a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (02/10 11h): 17 bloqueados, 16 por "preco ja
    correu" e 1 por "risco ja consumido". 14 deles eram COMPRA as 22h. Das
    22h as 11h, o unico bloqueado das 22h (LTC) fez +2,52%, contra +2,71%
    das COMPRA: ponto a favor do portao, com um par so. Placar do portao:
    seis leituras contra, tres a favor. Em 24h, os 3 bloqueados das 11h de
    ontem fizeram +3,52%, contra +3,06% das COMPRA.
2. **(41a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 10→8 sem o bonus; UNI e AR so existem
   por ele. A favor da pergunta: o grupo REGIME das 22h fez +2,14% ate as
   11h, contra +2,95% das outras COMPRA; em 24h, o das 11h de ontem fez
   +1,32% contra +3,75%. Contra: o BTC segue com score 6/1 de compra; so
   foi barrado por preco ja corrido.
3. **(38a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 4 de 10 COMPRA. Contra a pergunta: o grupo
   LIQ das 22h fez +2,78% ate as 11h; o resto das COMPRA, +2,64%.
4. **(40a)** A leitura das 11h deve considerar a vela em formacao? Hoje: a
   vela diaria fechada e a mesma das 22h, e 14 das 24 COMPRA das 22h
   viraram SEM ENTRADA so porque o preco andou. Os 13 barrados por preco
   ja corrido subiram +4,24% desde as 22h; as 10 COMPRA que sobraram,
   +1,52%.
5. **(39a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhuma COMPRA rotulada
   por gatilho 4h. LTC, RENDER, SOL, ASTR e PENDLE tem cruzamento de alta
   no 4h e estao barrados por preco ja corrido.
6. **(38a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (02/10 11h): 2 COMPRA com
    marca MORTA (DYDX, AR). O dia inteiro de AR e um negocio de US$ 24,99.
    Contra a pergunta: o grupo MORTA das 22h fez +2,90% ate as 11h, contra
    +2,64% do resto.
7. **(35a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(32a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (02/10 11h): nenhuma COMPRA com marca X4H-. O grupo X4H-
   das 22h (NEAR, SHIB) fez +1,39% ate as 11h, contra +2,83% do resto.
9. **(30a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (02/10 11h): 2 COMPRA com DER-BORDA, SEI (+0,27 ATR) e
    ONDO (+0,28 ATR). O limite e +0,30.
10. **(29a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA; SUI com RSI 67 e a mais alta.
11. **(26a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 16
    barrados por preco ja corrido; o maior, IMX, a +1,51 ATR. Nenhum chegou
    ao alvo.
12. **(25a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: LMWR, com R:R de 164,69:1, depois de cair 5,24% num
    unico bloco de US$ 1.322.
13. **(22a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, **0**. Hoje: SUPER, com RSI
    86, segue como REALIZAR PARCIAL.
14. **(20a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 27 dos 28 pares vieram iguais. No BTC, 86744,69 na diaria e
    86746,83 no 4h.
15. **(20a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a BTC diaria de 06/09
    veio 80344,16 (base 80344,15), a BTC de 4h de 24/09 16:00 veio 84406,44
    (base 84418,23) e a SUI diaria de 30/08 veio 0,71114 (base 0,71134). A
    alternancia continua.
16. **(19a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 10 COMPRA
    o aviso nao aparece.
17. **(18a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: as 10 COMPRA ja eram COMPRA as 22h; nenhuma nova.
18. **(18a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(14a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21; LMWR, que tinha, saiu da lista por
    risco ja consumido.
20. **(13a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (02/10
    11h): 14 das 24 COMPRA das 22h viraram SEM ENTRADA, e o relatorio nao
    diz o que fazer com quem comprou. Em 24h, 3 de 8 stops desceram (SEI
    -4,40%).
21. **(13a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(13a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (02/10 11h): indisponivel, 403 da rede do ambiente, decima terceira
    coleta seguida.
23. **(5a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h fez +3,33% ate as 11h contra +2,70% do painel (+0,63
    pp); a das 11h de ontem fez +2,84% em 24h contra +3,70% (-0,86 pp).
    Cinco vitorias nas ultimas oito medicoes, depois de cinco derrotas.
