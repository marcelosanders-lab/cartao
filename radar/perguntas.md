# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 03/10 22h.

1. **(47a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (03/10 22h): das 11h as 22h os 8 barrados das
    11h fizeram -0,24%, contra +1,15% das COMPRA: ponto a favor do portao.
    Placar do portao: sete leituras contra, cinco a favor. Mas os 8 voltaram
    a COMPRA as 22h. AR e LPT voltaram com deriva 0,00 porque o negocio
    isolado que o portao barrou virou o fechamento do dia. Agora, 1
    barrado: PENDLE (+0,43 ATR).
2. **(44a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 23→13 sem o bonus; 10 COMPRA so existem
   por ele, e o proprio BTC segue NEUTRO. A favor da pergunta: em 24h, o
   grupo REGIME de ontem as 22h fez +1,81% contra +3,17% das outras COMPRA
   (sem AR e LPT: +1,11% contra +1,78%). Contra: na janela, o REGIME das 11h
   fez +1,25% contra +1,04%. Placar na janela curta: tres a favor do bonus,
   quatro contra.
3. **(41a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 13 de 23 COMPRA. Contra a pergunta, de
   novo: em 24h o grupo LIQ de ontem fez +3,29% contra +1,12% do resto, e
   ainda +1,64% contra +1,12% sem AR e LPT.
4. **(43a)** A leitura das 11h deve considerar a vela em formacao? Hoje: os
   8 barrados das 11h viraram COMPRA as 22h. 14 das 14 COMPRA das 11h
   seguiram COMPRA.
5. **(42a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhuma COMPRA
   rotulada por gatilho 4h.
6. **(41a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (03/10 22h): 7 COMPRA com
    marca MORTA (IMX, DYDX, AR, LPT, PENGU, AIOZ, ASTR); 6 delas com deriva
    0,00. O dia 03/10 de AIOZ foi US$ 51,38; o de PENGU, US$ 148,13; o de
    LPT, US$ 385,05; o de AR, uma vela de 4h com US$ 921,17.
7. **(38a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(35a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (03/10 22h): 2 COMPRA com X4H- (UNI, ICP). O X4H- de ontem
   as 22h fez +4,20% em 24h contra +1,98% do resto; sem AR, +0,84% contra
   +1,52%.
9. **(33a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (03/10 22h): nenhuma COMPRA com DER-BORDA. O DER-BORDA de
    ontem as 22h (LTC, ASTR) fez +0,32% em 24h contra +2,66% do resto; o
    das 11h (UNI) fez -0,94% contra +1,31%.
10. **(32a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA; AAVE com RSI 73 e a mais alta.
11. **(29a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 1
    barrado por preco ja corrido (PENDLE). Nenhum chegou ao alvo.
12. **(28a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(25a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, **0**. Hoje: SUPER,
    com RSI 89, segue como REALIZAR PARCIAL.
14. **(23a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(23a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a AAVE diaria de 01/10
    veio com fechamento 171,454 (base 171,387): o fechamento de uma vela
    diaria de dois dias atras mudou. A AVAX de 4h de 29/09 16:00 mudou de
    volume de novo; a SUI diaria de 30/08 veio 0,71114 (base 0,71134).
16. **(22a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "23 de 28 pares deram COMPRA" e, na frase seguinte, "Comprar os 20". O
    numero esta errado.
17. **(21a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 14 das 23 COMPRA ja eram COMPRA as 11h; 8 voltaram
    do bloqueio das 11h; PENGU veio de NEUTRO.
18. **(21a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(17a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21.
20. **(16a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (03/10
    22h): das 11h para ca, 1 de 14 stops desceu (PYTH -0,44%). Em 24h,
    nenhum de 20 desceu. O de AR subiu 15,65% por causa de um unico bloco
    de US$ 921,17.
21. **(16a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(16a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (03/10 22h): indisponivel, 403 da rede do ambiente, decima sexta
    coleta seguida.
23. **(8a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h (AAVE, LINK, PYTH) fez +0,82% ate as 22h contra +0,77%
    do painel (+0,05 pp); a das 22h de ontem (AAVE, LINK) fez +1,61% em 24h
    contra +2,28% (-0,67 pp). No total, 8 vitorias em 19.
