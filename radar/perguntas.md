# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 06/10 11h.

1. **(53a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (06/10 11h): 3 barrados (RENDER +0,93 ATR,
    LPT +0,85, AVAX +0,40). Os tres eram COMPRA as 22h, quando a vela
    diaria nova zerou a deriva, e fizeram +4,09% desde entao, contra -0,60%
    das outras 22 COMPRA. Nao havia barrado as 22h: sem medida do portao
    nesta janela. Placar do portao: sete contra, oito a favor.
2. **(50a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 22→12 sem o bonus; 10 COMPRA so existem
   por ele (AAVE, AR, ETH, IMX, LINK, NEAR, ONDO, SOL, SUPER, UNI); com
   regime em baixa UNI vira VENDA. A favor da pergunta nesta janela: o
   REGIME das 22h fez -0,85% contra +0,43% das outras COMPRA. Contra, em
   24h: o REGIME das 11h de ontem fez +0,78% contra +0,35%. Placar na
   janela curta: sete a favor do bonus, cinco contra.
3. **(47a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 14 de 22 COMPRA. Contra a pergunta: o LIQ
   das 22h fez +0,25% contra -0,55% do resto; o das 11h de ontem, +0,76%
   contra +0,06% em 24h (sem RENDER, -0,01%).
4. **(49a)** A leitura das 11h deve considerar a vela em formacao? Hoje:
   sem vela diaria nova, a vela em formacao tirou de COMPRA as tres que
   mais subiram desde as 22h (RENDER, LPT, AVAX) e pos PYTH em "gatilho 4h".
5. **(48a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: 1, PYTH. Em 24h, os 6
   das 11h de ontem fizeram -0,27% contra +0,80% das outras COMPRA.
6. **(47a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (06/10 11h): 6 COMPRA com
    marca MORTA (IMX, DYDX, AR, SUPER, AIOZ, ASTR). AIOZ esta sem negocio
    desde 05/10 08:00 UTC. DYDX teve um unico negocio de US$ 545,01 no dia.
    Contra a pergunta: o MORTA das 22h fez +0,37% contra -0,26% (sem RENDER
    e LPT, -0,21% contra -0,67%).
7. **(44a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(41a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (06/10 11h): 2 COMPRA com X4H- (UNI, PYTH). Contra a
   pergunta: o X4H- das 22h fez +0,50% contra -0,17%.
9. **(39a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (06/10 11h): nenhuma DER-BORDA.
10. **(38a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 73 (AAVE, ICP,
    SUPER).
11. **(35a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 3
    barrados por preco ja corrido (RENDER, LPT, AVAX). Nenhum chegou ao
    alvo.
12. **(34a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(31a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    **0**. Hoje: com teto 85, nada muda (22 COMPRA nas duas versoes).
14. **(29a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(29a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a SOL voltou a bater
    com a base em todas as velas que vinham divergindo; a ETH diaria de
    07/09, 30/08 e 29/08 e a AAVE de 01/10 voltaram a divergir (2490,08,
    2417,19, 2457,70; 171,454). A fonte alterna a cada coleta.
16. **(28a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "22 de 28" e "Comprar os 20". O numero fixo erra pela terceira leitura
    seguida.
17. **(27a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 22 das 22 COMPRA ja eram COMPRA as 22h; nenhuma e nova.
    3 COMPRA das 22h viraram SEM ENTRADA (RENDER, LPT, AVAX).
18. **(27a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(23a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. 1 COMPRA por gatilho 4h (PYTH).
20. **(22a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (06/10
    11h): das 22h para ca, nenhum stop mudou. Em 24h, 8 de 18 desceram
    (SUPER -3,87%, LINK -3,09%, BTC -0,90%...). E o relatorio nao diz a
    quem entrou as 22h em RENDER, LPT e AVAX o que fazer com uma COMPRA que
    virou SEM ENTRADA.
21. **(22a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(22a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (06/10 11h): indisponivel, 403 da rede do ambiente, vigesima segunda
    coleta seguida.
23. **(14a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (BTC, SUI, SHIB) fez -0,50% contra +0,06% do painel
    (-0,56 pp); a das 11h de ontem fez -0,77% em 24h contra +0,38% (-1,15
    pp). No total, 12 vitorias em 29; perdeu as ultimas quatro.
