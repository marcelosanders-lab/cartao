# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 30/09 11h.

1. **(40a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (30/09 11h): em 24h (29/09 11h → 30/09 11h),
    os 10 bloqueados das 11h de ontem fizeram -0,97%, as 15 COMPRA +0,67%, o
    painel +0,16%. Confirma a leitura das 22h, mas nao e voto novo: a janela
    contem a das 22h. Placar do portao: seis leituras contra, uma a favor.
    Hoje as 11h o padrao se repetiu: 9 das 22 COMPRA das 22h viraram "preco
    ja correu" (+2,76% desde as 22h); as 13 que sobraram fizeram -0,02%. A
    medida justa so sai as 22h.
2. **(37a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 13→10 sem o bonus (saem UNI, SEI, PYTH); o
   BTC segue NEUTRO (5/2). O grupo REGIME das 22h fez +0,07% contra +1,38%
   do painel; o das 11h de ontem fez +1,07% em 24h contra +0,16%. Sinal
   alternado.
3. **(34a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 7 de 13 COMPRA. Contra a pergunta: o grupo
   LIQ das 22h fez +1,59% ate as 11h, o resto das COMPRA +0,65%.
4. **(36a)** A leitura das 11h deve considerar a vela em formacao? Hoje: a
   lista das 11h de ontem fez +0,67% em 24h, 0,51 pp acima do painel.
5. **(35a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhuma COMPRA por
   gatilho 4h.
6. **(34a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (30/09 11h): nenhuma COMPRA
    com marca MORTA, mas o bloqueio de DYDX (+0,76 ATR) vem de um unico
    negocio de US$ 217,33 na vela das 08:00; LMWR subiu 4,93% com um negocio
    de US$ 12,90; SUPER nao tem negocio desde 29/09 16:00 UTC. As MORTA das
    22h fizeram +2,62% ate as 11h, acima do painel.
7. **(31a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z); as 56 chamadas de velas foram
   pela instancia principal, sem pedido de login.
8. **(28a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (30/09 11h): 2 das 13 COMPRA (IMX, ASTR). O grupo X4H- das
   22h fez +2,20% ate as 11h, acima do painel.
9. **(26a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (30/09 11h): RENDER em +0,30 ATR, no limite exato; IMX
    +0,25.
10. **(25a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma marca RSI-BORDA; os maiores RSI entre as COMPRA sao 72
    (AVAX, ICP).
11. **(22a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 10
    bloqueados; nenhum perto do alvo (NEAR com R:R 0,76, LPT 0,96).
12. **(21a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(18a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, **1**. Hoje: SUPER (RSI 79) barrado; com
    teto 85 viraria COMPRA. SUPER nao negociou nada desde as 22h (0,00%).
14. **(16a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: o "Agora" de DYDX e o negocio de US$ 217,33 das 08:00; a vela das
    12:00 nao tem negocio.
15. **(16a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas: ETH 4h 24/09 16:00
    veio 2696,50 (base 2695,89); LTC 4h 24/09 16:00 veio 71,399 (base
    71,403). BTC, SOL e SUI vieram iguais a base. A alternancia continua.
16. **(15a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: 13 COMPRA, o
    aviso nao apareceu.
17. **(14a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: as 13 sao residuo; nenhuma nova.
18. **(14a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(10a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(9a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (30/09
    11h): contra as 22h nenhum stop mudou (mesma vela diaria); em 24h, 7 de
    8 rebaixados (LINK -6,31%, SEI -6,23%, PYTH -4,05%).
21. **(9a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(9a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (30/09 11h): indisponivel, 403 da rede do ambiente, nona coleta seguida.
23. **(1a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Ela perdeu para o painel em cinco medicoes seguidas (-0,56,
    -0,31, -0,56, -1,22 e -0,20 pp). Opcoes: (a) manter com o rotulo atual,
    (b) entregar so com o placar dela ao lado, (c) parar de entregar ate
    haver 30 medicoes.
