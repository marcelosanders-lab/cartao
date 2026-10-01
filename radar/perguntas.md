# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 30/09 22h.

1. **(41a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (30/09 22h): das 11h as 22h os 10 bloqueados
    fizeram -2,09%, as 13 COMPRA -1,90%, o painel -1,76%. O portao poupou
    0,19 pp. Placar do portao: seis leituras contra, duas a favor. As 22h
    nao ha bloqueado: os 10 voltaram a COMPRA.
2. **(38a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 24→15 sem o bonus; 9 COMPRA so existem
   por ele (ETH, SOL, UNI, NEAR, SEI, AR, AIOZ, PYTH, LMWR). O BTC segue
   NEUTRO (5/2) e caiu 1,24% desde as 11h. Contra a pergunta: o grupo
   REGIME das 11h fez -1,05% contra -1,76% do painel.
3. **(35a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 12 de 24 COMPRA. O grupo LIQ das 11h fez
   -2,16% ate as 22h; o resto das COMPRA, -1,60%.
4. **(37a)** A leitura das 11h deve considerar a vela em formacao? Hoje: a
   lista das 11h (13 COMPRA) fez -1,90% ate as 22h, 0,15 pp abaixo do
   painel.
5. **(36a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhuma COMPRA por
   gatilho 4h.
6. **(35a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (30/09 22h): 6 COMPRA com
    marca MORTA (IMX, DYDX, AR, LPT, AIOZ, LMWR). O fechamento de AR e um
    negocio de US$ 4,98; o dia inteiro de LMWR e um negocio de US$ 12,90.
7. **(32a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(29a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (30/09 22h): 4 das 24 COMPRA (SEI, SHIB, PENGU, PYTH). SHIB
   tem cruzamento de alta e de baixa nas mesmas 3 velas, e os dois pontos
   se anulam.
9. **(27a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (30/09 22h): nenhuma marca DER-BORDA; 9 COMPRA com deriva
    entre -0,01 e +0,01 ATR (vela recem-aberta).
10. **(26a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: NEAR com RSI 76 (RSI-BORDA).
11. **(23a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje:
    nenhum bloqueado.
12. **(22a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(19a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, **1**. Hoje: SUPER (RSI 79) barrado;
    com teto 85 viraria COMPRA. SUPER nao negocia desde 29/09 16:00 UTC.
14. **(17a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em UNI as duas chamadas devolveram a mesma vela em formacao com
    precos diferentes (diaria 8,8395, 4h 8,8375). O motor usou a de 4h.
15. **(17a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a ETH diaria de 07/09
    voltou a 2490,49 (as 11h tinha vindo 2490,08); a SOL diaria de 30/08 veio
    101,75 (base 101,78). A alternancia continua.
16. **(16a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "24 de 28" e, na frase seguinte, "Comprar os 20".
17. **(15a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 10 das 24 COMPRA sao os pares que o portao barrou
    as 11h; LMWR e nova.
18. **(15a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(11a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: LMWR e COMPRA
    com a EMA9 diaria abaixo da EMA21.
20. **(10a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (30/09
    22h): das 11h para ca, 7 de 13 stops desceram (AR -6,03%, AVAX -4,84%,
    AAVE -3,70%). Em 24h, 11 de 22.
21. **(10a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(10a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (30/09 22h): indisponivel, 403 da rede do ambiente, decima coleta
    seguida.
23. **(2a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h fez -1,52% contra -1,76% do painel (+0,24 pp, primeira
    vitoria em seis medicoes); a das 22h de ontem fez -1,67% em 24h contra
    -0,40% (-1,27 pp).
