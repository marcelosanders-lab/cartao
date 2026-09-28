# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 27/09 22h.

1. **(35a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (27/09 22h): as seis bloqueadas como "preco ja
    correu" as 11h fizeram +4,93% ate as 22h; as 17 COMPRA, +0,60%. SEI
    (+14,43%) e IMX (+13,08%) agora sao barradas pelo teto de RSI (80).
2. **(32a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 21→14; ETH e COMPRA com histograma MACD
   diario negativo.
3. **(29a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 11 de 21 COMPRA.
4. **(31a)** A leitura das 11h deve considerar a vela em formacao?
5. **(30a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(29a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (27/09 22h): DYDX, AR, LPT e
    WLFI em COMPRA com a vela 4h atual sem negocio (deriva +0,00); LMWR com a
    terceira vela diaria seguida de volume zero.
7. **(26a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao.
8. **(23a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (27/09 22h): nao medido.
9. **(21a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (27/09 22h): nenhuma a menos de 0,05 ATR; ONDO a 0,08 do
    limite inferior (-0,67).
10. **(20a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SUI e JUP com RSI 77, ONDO e RENDER 76.
11. **(17a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(16a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio - a vela diaria nova zerou a deriva.
13. **(13a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, **4**. Na janela 11h→22h os 2 barrados (LTC -1,14%, PYTH
    +0,38%) fizeram -0,38% contra +0,60% das COMPRA: o teto evitou 0,98 pp.
14. **(11a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(11a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: nenhuma divergencia,
    terceira leitura seguida.
16. **(10a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje (27/09 22h): o
    aviso diz "comprar os 20" com 21 COMPRA.
17. **(9a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): das 21 COMPRA, 17 ja eram COMPRA as 11h; ONDO,
    PENDLE, PENGU e SUI voltaram porque a vela nova zerou a deriva.
18. **(9a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(5a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(4a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (27/09
    22h): com a vela diaria nova, 8 de 21 stops rebaixados; o maior, ICP,
    -1,71%.
21. **(4a)** Outra fonte de velas. Todos os sites de preço testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa acessivel.
22. **(4a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (27/09 22h): indisponivel, 403 da rede do ambiente, quarta coleta
    seguida.
