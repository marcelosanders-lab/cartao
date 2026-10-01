# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 01/10 11h.

1. **(42a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (01/10 11h): em 24h, os 10 bloqueados das 11h
    de ontem fizeram -3,51%, as 13 COMPRA -1,56%, o painel -2,03%. Confirma
    a leitura das 22h, mas nao e voto novo. Placar do portao: seis leituras
    contra, duas a favor. As 11h, 3 bloqueados: AAVE e AR (preco ja correu),
    NEAR (risco ja consumido).
2. **(39a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 21→15 sem o bonus; 6 COMPRA so existem
   por ele (SOL, UNI, SEI, AIOZ, PYTH, LMWR). O BTC segue NEUTRO (5/2).
   Contra a pergunta: o grupo REGIME das 22h fez +0,11% ate as 11h, contra
   -0,71% das outras COMPRA. Sem AR (+5,82%), fez -0,60%.
3. **(36a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 11 de 21 COMPRA. Contra a pergunta: o grupo
   LIQ das 22h fez -0,23% ate as 11h; o resto das COMPRA, -0,57%.
4. **(38a)** A leitura das 11h deve considerar a vela em formacao? Hoje: 3
   COMPRA das 22h viraram bloqueadas as 11h. AAVE (+4,24%) e AR (+5,82%)
   por preco ja corrido; NEAR (-6,21%) por risco ja consumido.
5. **(37a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: 3 COMPRA por gatilho
   4h (IMX, ETH, SHIB). As quatro velas de 4h de IMX hoje somam US$ 360
   negociados, e o preco caiu em todas elas.
6. **(36a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (01/10 11h): 3 COMPRA com
    marca MORTA (LPT, AIOZ, LMWR). O dia inteiro de LPT e um negocio de
    US$ 9,46; LMWR nao teve negocio hoje; AIOZ nao negocia desde 04:00 UTC.
7. **(33a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(30a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (01/10 11h): 4 das 21 COMPRA (ETH, SHIB, SEI, PENGU). ETH e
   SHIB tem cruzamento de alta e de baixa nas mesmas 3 velas e, mesmo
   assim, saem rotuladas "COMPRA (gatilho 4h)".
9. **(28a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (01/10 11h): nenhuma marca DER-BORDA. As mais perto do teto
    sao UNI (+0,22 ATR) e AIOZ (+0,20 ATR).
10. **(27a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA. NEAR (RSI 76) foi barrado por risco
    ja consumido.
11. **(24a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: AAVE
    (+0,63 ATR) e AR (+0,68 ATR) barrados por preco ja corrido.
12. **(23a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: NEAR barrado com R:R 5,48:1 (deriva -0,81 ATR).
13. **(20a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, **0**. Hoje: com teto 85, SUPER sai
    de NEUTRO para "preco ja correu", nao para COMPRA.
14. **(18a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: nos 28 pares, o fechamento da diaria em formacao e o da ultima
    vela de 4h vieram iguais.
15. **(18a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a ETH diaria de 07/09
    voltou a 2490,08 (base 2490,49); a SOL diaria de 30/08 veio 101,78 (as
    22h tinha vindo 101,75). A alternancia continua.
16. **(17a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "21 de 28" e, na frase seguinte, "Comprar os 20".
17. **(16a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (11h): as 21 COMPRA ja eram COMPRA as 22h. Nenhuma e nova.
18. **(16a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(12a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: LMWR segue
    COMPRA com a EMA9 diaria abaixo da EMA21.
20. **(11a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (01/10
    11h): das 22h para ca nenhum stop mudou (mesma vela diaria). Em 24h, 5
    de 11 desceram (AVAX -4,84%, ICP -2,95%).
21. **(11a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(11a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (01/10 11h): indisponivel, 403 da rede do ambiente, decima primeira
    coleta seguida.
23. **(3a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h fez -0,02% ate as 11h contra -0,27% do painel (+0,25
    pp); a das 11h de ontem fez -0,61% em 24h contra -2,03% (+1,42 pp).
    Tres vitorias nas ultimas quatro medicoes, depois de cinco derrotas.
