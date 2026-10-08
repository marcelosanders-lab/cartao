# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 08/10 11h.

1. **(57a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (08/10 11h): 2 barrados por "preco ja
    correu": JUP (+0,37 ATR, R:R 1,41:1) e SUPER (+1,03 ATR, R:R 0,78:1).
    Nenhum por "risco ja consumido". O barrado das 22h (JUP) fez -0,42%
    ate as 11h, contra -0,89% do painel e -1,37% das COMPRA: o portao
    recusou um par que caiu menos que o painel. Placar do portao: dez
    contra, oito a favor.
    Em 24h, os 14 barrados das 11h de ontem fizeram +1,44% contra +0,79%
    do painel; sem JUP, +0,33%.
2. **(54a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: regime em BAIXA pela segunda leitura;
   5→5 sem o bonus, nenhuma COMPRA depende dele. Nao havia REGIME as 22h:
   sem medida na janela curta. A favor da pergunta em 24h: o REGIME das
   11h de ontem fez -1,75% contra -1,46% da unica outra COMPRA (SUI).
   Placar na janela curta: nove a favor do bonus, seis contra.
3. **(51a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 3 de 5 COMPRA (IMX, RENDER, AIOZ). Contra
   a pergunta nas duas medidas: o LIQ das 22h fez -0,01% contra -4,10% do
   resto; o das 11h de ontem, +1,55% contra -3,02% em 24h.
4. **(53a)** A leitura das 11h deve considerar a vela em formacao? Hoje: das
   6 COMPRA das 22h, 5 continuam COMPRA; SUPER virou "preco ja correu"
   (+1,03 ATR). Nenhuma virou "risco ja consumido".
5. **(52a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhum.
6. **(51a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (08/10 11h): 2 COMPRA com
    marca MORTA (IMX, AIOZ). O "Agora" de IMX (0,17541) vem de US$ 23,50
    negociados as 08:00 UTC; o dia inteiro somou US$ 24,57. O de AIOZ
    (0,107375) vem de um negocio de US$ 4,83 as 04:00 UTC, e e ele que poe
    AIOZ a -0,73 ATR, colada ao limite do portao. Contra a pergunta nesta
    janela: o MORTA das 22h (IMX, SUPER) fez +3,88% contra -4,00%. A
    favor, em 24h: o das 11h de ontem (AIOZ) fez -2,63% contra -1,56%.
7. **(48a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z) com a base das 22h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(45a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (08/10 11h): 1 COMPRA com X4H- (RENDER). Nao havia X4H- as
   22h. A favor da pergunta em 24h: o X4H- das 11h de ontem (AIOZ) fez
   -2,63% contra -1,56%.
9. **(43a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (08/10 11h): 1 DER-BORDA (AIOZ, -0,73 ATR), produzida pelo
    negocio de US$ 4,83 da Pergunta 6. NEAR esta a -0,70 e nao leva a
    marca. Contra a pergunta em 24h: as 3 DER-BORDA das 11h de ontem fizeram
    -0,22% contra -2,83% das outras COMPRA.
10. **(42a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 67 (NEAR).
11. **(39a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 2
    "preco ja correu": JUP (0,36874, alvo 0,43835) e SUPER (0,238577, alvo
    0,26573). Nenhum chegou ao alvo.
12. **(38a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(34a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, **0**. Hoje: com teto 85, nada muda (5 COMPRA nas duas
    versoes).
14. **(33a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(33a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    22h: SOL 4h de 05/10 08:00 voltou a 120,83 (base 120,81) e a de 02/10
    16:00 a 117,99 (base 118,00), a terceira troca seguida nas duas; AAVE
    4h de 01/10 20:00 veio 171,454 (base 171,387). A base nao foi alterada.
16. **(32a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 5 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(31a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 5 das 5 COMPRA ja eram COMPRA as 22h; nenhuma e nova.
    SUPER saiu ("preco ja correu").
18. **(31a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(27a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. Nenhuma COMPRA por gatilho 4h.
20. **(26a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (08/10
    11h): mesma vela diaria, nenhum stop mudou desde as 22h. Em 24h, 2
    pares COMPRA nas duas leituras (NEAR, AIOZ), os dois stops subiram
    (+5,90% e +3,57%). O stop de IMX continua 10,90% abaixo do de
    anteontem, sem aviso a quem entrou antes.
21. **(26a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(26a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (08/10 11h): indisponivel, 403 da rede do ambiente, vigesima sexta
    coleta seguida.
23. **(18a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (AAVE, NEAR) fez -4,10% contra -0,89% do painel (-3,21
    pp), puxada por NEAR -6,28%; a das 11h de ontem (so SUI) fez -1,46% em
    24h contra +0,79% (-2,25 pp). No total, 16 vitorias em 37; a sequencia
    de quatro vitorias acabou. A lista de agora tem os mesmos 2 pares
    (AAVE, NEAR) de 5 COMPRA.
