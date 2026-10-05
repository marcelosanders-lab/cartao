# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 05/10 extra 12h08.

1. **(51a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (05/10 extra 12h08): 4 barrados: AIOZ (+0,55
    ATR), LPT (+0,46), AAVE (+0,38) e ICP (+0,35). PENDLE, barrado as 11h
    com +0,63, virou COMPRA porque caiu 3,11% em uma hora, ate a minima da
    vela de 4h, com US$ 1.913,87 negociados. Stop e alvo nao mudaram; o
    R:R subiu de 1,11 para 1,75 so pela queda. Na janela 11h → 12h08, os 5
    barrados das 11h fizeram -0,80% contra -0,93% das COMPRA; sem os pares
    parados, -1,33% contra -1,16%. Leitura extra: fora do placar do portao,
    que segue sete contra, sete a favor.
2. **(48a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje (extra 12h08): 21→15 sem o bonus; 6 COMPRA
   so existem por ele (AR, AVAX, IMX, JUP, SUPER, UNI) e 3 barrados
   virariam NEUTRO. Na janela de uma hora, o REGIME das 11h fez -0,34%
   contra -1,18% das outras COMPRA (sem os parados, -0,68% contra -1,28%):
   contra a pergunta. Fora da contagem (leitura extra): placar na janela
   curta segue seis a favor do bonus, quatro contra.
3. **(45a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje (extra 12h08): 13 de 21 COMPRA, com PENDLE.
   Na janela, o LIQ das 11h fez -0,79% contra -1,14%, mas 4 dos 12 nao
   negociaram; sem eles, -1,19% contra -1,14%.
4. **(47a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (extra 12h08): sem vela diaria nova, uma hora de vela em formacao mudou
   um sinal: PENDLE de SEM ENTRADA para COMPRA, na queda. As 11h, cinco
   COMPRA das 22h tinham virado SEM ENTRADA na alta.
5. **(46a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje (extra 12h08): os
   mesmos 6, LINK, DYDX, PYTH, NEAR, ONDO e PENGU. Na janela fizeram -1,27%
   contra -0,78% das outras COMPRA. DYDX nao negociou.
6. **(45a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (05/10 extra 12h08): 2
    COMPRA com marca MORTA (IMX, DYDX). Em uma hora, 7 dos 28 pares nao
    mudaram de preco (AIOZ, AR, DYDX, IMX, LMWR, LPT, SUPER); 4 deles sao
    COMPRA. O 0,00% deles faz as COMPRA parecerem 0,23 pp melhores (-0,93%
    contra -1,16% sem eles).
7. **(42a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: leitura pedida pelo dono, rodou (15:08Z); as 56
   chamadas foram pela instancia principal, sem pedido de login.
8. **(39a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (05/10 extra 12h08): 1 COMPRA com X4H- (DYDX), sem negocio
   na janela.
9. **(37a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (05/10 extra 12h08): nenhuma DER-BORDA. PENGU (+0,30 →
    +0,11) e NEAR (+0,27 → +0,19) sairam da borda porque o preco caiu, e
    NEAR entrou na lista de sobrevivencia.
10. **(36a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SUPER segue com RSI 77,976 e marca RSI-BORDA, sem negocio que
    mudasse o preco desde as 11h.
11. **(33a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 4
    barrados por preco ja corrido (AIOZ, LPT, AAVE, ICP). Nenhum chegou ao
    alvo.
12. **(32a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(29a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, **0**. Hoje
    (extra 12h08, fora da serie): com teto 85, nada muda (21 COMPRA nas
    duas versoes).
14. **(27a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(27a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje (extra 12h08):
    `fonte.py` de novo "nenhuma vela fechada divergente", mas so viu a vela
    em formacao. A SOL 4h de 05/10 08:00, fechada antes da coleta das 11h,
    veio 120,81 (base 120,83). A AAVE 4h de 01/10 20:00 veio 171,454 e a
    diaria de 01/10 voltou a 171,387: os dois prazos trocaram de valor. ETH
    diaria de 07/09 2490,08 (base 2490,49), SUI 4h de 02/10 1,12102 (base
    1,12126), BTC diaria de 06/09 80344,16 (base 80344,15). A fonte segue
    alternando.
16. **(26a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: leitura extra
    das 12h08 com cabecalho "Leitura das 11h". O aviso diz "21 de 28" e
    "Comprar os 20": o numero fixo agora erra.
17. **(25a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (extra 12h08): 20 das 21 COMPRA ja eram COMPRA as 22h;
    PENDLE e nova.
18. **(25a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(21a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. 6 COMPRA por gatilho 4h, nenhuma no
    limite de deriva.
20. **(20a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (05/10
    extra 12h08): das 11h para ca, nenhum dos 20 stops mudou (mesma vela
    diaria). Os R:R subiram porque o preco caiu em direcao a stops fixos.
21. **(20a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(20a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (05/10 extra 12h08): indisponivel, 403 da rede do ambiente, vigesima
    coleta seguida.
23. **(12a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje
    (extra 12h08): a lista das 11h (BTC, ETH, SOL, SUI, LINK, SHIB) fez
    -1,27% em uma hora contra -0,84% do painel (-0,43 pp); contra os 21
    pares que negociaram, -0,15 pp. No total, 12 vitorias em 25 (extra nao
    conta).
