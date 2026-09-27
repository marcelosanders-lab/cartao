# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 27/09 11h.

1. **(34a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (27/09 11h): seis COMPRA das 22h viraram
    "preco ja correu" (media +4,08%); as 17 que ficaram fizeram +0,59%.
    RENDER, SOL e UNI, bloqueadas as 08:09, voltaram a COMPRA as 11h
    porque cairam de volta - mesma vela diaria.
2. **(31a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 17→13.
3. **(28a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 9 de 17 COMPRA.
4. **(30a)** A leitura das 11h deve considerar a vela em formacao?
5. **(29a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(28a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (27/09 11h): AIOZ sem
    negocio ha 12 horas, WLFI com a vela 4h atual vazia e ASTR com negocio
    unico, os tres em COMPRA; LMWR sem nenhum negocio desde 25/09 12:00Z; o
    +1,13% de AR desde as 08:09 e o primeiro negocio em 16 horas (US$ 307).
7. **(25a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao.
8. **(22a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (27/09 11h): nao medido.
9. **(20a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (27/09 11h): SOL +0,29 e RENDER +0,29, a 0,01 ATR do
    limite.
10. **(19a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: AR com RSI 75, RENDER 74.
11. **(16a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(15a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: SUI (+1,13 ATR, R:R 0,71:1).
13. **(12a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, **2**. Nesta janela (22h→11h) os 2 barrados (LTC -1,13%,
    PYTH +2,48%) fizeram +0,68% contra +1,50% das COMPRA: o teto evitou
    0,83 pp de perda relativa.
14. **(10a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(10a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: nenhuma divergencia,
    segunda leitura seguida.
16. **(9a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje (27/09 11h): o
    aviso diz "comprar os 20" com 17 COMPRA.
17. **(8a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: as 17 sao residuo; nenhuma nova.
18. **(8a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(4a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(3a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (27/09
    11h): em 24h, 5 de 13 stops rebaixados; o maior, AIOZ, -3,38%.
21. **(3a)** Outra fonte de velas. Todos os sites de preço testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa acessivel.
22. **(3a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (27/09 11h): indisponivel, 403 da rede do ambiente, terceira coleta
    seguida.
