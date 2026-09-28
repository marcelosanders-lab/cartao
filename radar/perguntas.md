# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 28/09 11h.

1. **(36a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (28/09 11h): na queda, o portao virou do
    avesso - 9 COMPRA das 22h viraram "risco ja consumido" (media -5,87%) e a
    unica que subiu, LINK (+2,07%), virou "preco ja correu". Quarta leitura
    seguida em que o bloqueio "ja correu" cai sobre quem subiu.
2. **(33a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 8→4. O grupo REGIME das 22h caiu -4,75%,
   o painel -4,68%.
3. **(30a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 5 de 8 COMPRA.
4. **(32a)** A leitura das 11h deve considerar a vela em formacao?
5. **(31a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(30a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (28/09 11h): ICP, LPT e AIOZ
    em COMPRA com a vela 4h atual morta; LMWR com a quarta vela diaria
    seguida de volume zero.
7. **(27a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: a rotina das 11h disparou as 11:05 e nao rodou - o
   verificador do shell nao respondia; rodou as 11:30 por reagendamento.
8. **(24a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (28/09 11h): 4 das 8 COMPRA com cruzamento de baixa no 4h
   (BTC, ETH, ICP, AR).
9. **(22a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (28/09 11h): AR em -0,75 ATR, no limite exato.
10. **(21a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: AR com RSI 75, AIOZ 70.
11. **(18a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(17a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: 9 bloqueios, com R:R de 5,49:1 a 13,58:1 (SUI).
13. **(14a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, **4**. Na janela 22h→11h os 4 barrados (SEI, IMX, PYTH,
    LTC) cairam -5,27% contra -4,86% das COMPRA: o teto evitou 0,41 pp.
14. **(12a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(12a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` nao ve
    nada no caminho A (so compara as linhas repassadas), mas a resposta
    desta coleta trouxe outra versao de velas antigas - ETH 4h 24/09 16:00
    (2695,89 na base, 2696,50 agora), SOL 4h 22/09 16:00 (118,21 / 118,26),
    BTC 1d 06/09 (80344,15 / 80344,16) - e o BTC 4h 24/09 16:00 veio com
    dois fechamentos em 25 minutos.
16. **(11a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso nao
    apareceu (8 COMPRA).
17. **(10a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: as 8 sao residuo; nenhuma nova.
18. **(10a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(6a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(5a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (28/09
    11h): em 24h, 4 de 8 stops rebaixados; JUP, ONDO e PENDLE ja estao
    abaixo do stop no preco atual.
21. **(5a)** Outra fonte de velas. Todos os sites de preço testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa acessivel.
22. **(5a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (28/09 11h): indisponivel, 403 da rede do ambiente, quinta coleta
    seguida.
