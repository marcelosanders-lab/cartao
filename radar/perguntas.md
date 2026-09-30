# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 29/09 11h.

1. **(38a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (29/09 11h): das 25 COMPRA das 22h, as 10 que
    subiram +6,06% viraram "preco ja correu"; as 15 que continuam COMPRA
    fizeram -0,16%. Sexta leitura seguida em que o bloqueio cai sobre quem
    sobe. SOL passa com deriva +0,30 ATR (no limite); ETH, com +0,32, e
    barrado.
2. **(35a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 15→10 sem o bonus; o BTC segue NEUTRO
   (5/2). O grupo REGIME das 22h fez +1,00%, o painel +2,17%.
3. **(32a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 8 de 15 COMPRA.
4. **(34a)** A leitura das 11h deve considerar a vela em formacao?
5. **(33a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(32a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (29/09 11h): 4 COMPRA com
    marca MORTA (AR, LPT, AIOZ, ASTR). AIOZ: o dia inteiro e um negocio de
    US$ 20,71; velas 4h das 04:00, 08:00 e 12:00 sem negocio.
7. **(29a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 11:10), mas o conector da Crypto.com pediu
   novo login duas vezes no meio da coleta; completei pela segunda instancia
   do mesmo conector.
8. **(26a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (29/09 11h): 5 das 15 COMPRA (LTC, NEAR, JUP, ONDO, RENDER).
9. **(24a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (29/09 11h): SOL em +0,30 ATR, no limite exato.
10. **(23a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SEI com RSI 77, PYTH 76.
11. **(20a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(19a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(16a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, **0**. Nas 22h nao havia par barrado pelo teto;
    nada a medir nesta janela.
14. **(14a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(14a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Na resposta desta coleta: SOL 4h
    22/09 16:00 voltou a 118,26 (base 118,21); ETH 4h 24/09 16:00 2696,50
    (base 2695,89); e tres velas que ontem as 22h vieram diferentes voltaram
    ao valor da base: BTC 4h 24/09 16:00 (84418,23), LTC 4h 24/09 16:00
    (71,403), SUI 1d 30/08 (0,71134). A fonte alterna entre duas versoes a
    cada chamada.
16. **(13a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: 15 COMPRA, o
    aviso nao apareceu.
17. **(12a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: as 15 sao residuo; nenhuma nova.
18. **(12a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(8a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(7a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (29/09
    11h): contra as 22h nenhum stop mudou (mesma vela diaria); em 24h, 5 de
    5 rebaixados. JUP, ONDO e PENDLE seguem COMPRA depois de fecharem ontem
    abaixo da propria invalidacao.
21. **(7a)** Outra fonte de velas. Todos os sites de preço testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa; a segunda instancia usada
    na coleta e o mesmo conector da Crypto.com.
22. **(7a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (29/09 11h): indisponivel, 403 da rede do ambiente, setima coleta
    seguida.
