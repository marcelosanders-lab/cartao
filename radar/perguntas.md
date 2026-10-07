# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 06/10 22h.

1. **(54a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (06/10 22h): a vela diaria nova zerou a
    deriva e readmitiu os 3 barrados das 11h (RENDER +0,24 ATR, LPT -0,21,
    AVAX +0,02). Das 11h as 22h, os tres barrados fizeram +0,18%, contra
    -1,02% do painel e -1,25% das COMPRA: o portao recusou o grupo que
    mais rendeu. Placar do portao: oito contra, oito a favor.
2. **(51a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 25→10 sem o bonus; 15 COMPRA so existem
   por ele (AAVE, AIOZ, ASTR, AVAX, ETH, IMX, LINK, LTC, NEAR, PYTH, SEI,
   SHIB, SOL, SUPER, UNI), o maior numero desde 27/09 (maximo anterior:
   11). Com regime em baixa, LTC, PYTH e SEI viram VENDA. Contra a
   pergunta nesta janela: o REGIME das 11h fez -0,03% contra -2,26% das
   outras COMPRA; em 24h, o das 22h de ontem fez -0,44% contra -1,50%.
   Placar na janela curta: oito a favor do bonus, cinco contra.
3. **(48a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 15 de 25 COMPRA. A favor da pergunta: o
   LIQ das 11h fez -1,50% contra -0,82% do resto; o das 22h de ontem,
   -1,16% contra -1,05% em 24h.
4. **(50a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (22h): os tres que a vela em formacao tirou de COMPRA as 11h (RENDER,
   LPT, AVAX) voltaram a COMPRA com a vela diaria nova, depois de render
   +0,18% contra -1,25% das COMPRA.
5. **(49a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhum. PYTH, o gatilho
   4h das 11h, fez -4,80% e agora e COMPRA comum.
6. **(48a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (06/10 22h): 6 COMPRA com
    marca MORTA (IMX, DYDX, AR, SUPER, AIOZ, ASTR). Em DYDX, o ultimo
    negocio foi de US$ 19,47 as 16:00 UTC. Contra a pergunta: o MORTA das
    11h fez +0,21% contra -1,80% das outras COMPRA; o das 22h de ontem,
    -0,29% contra -1,58% em 24h.
7. **(45a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:03Z) em container novo, sem base
   anterior; 56 chamadas de velas pela instancia principal, sem pedido de
   login.
8. **(42a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (06/10 22h): 6 COMPRA com X4H- (LTC, SUI, SEI, PENDLE,
   ONDO, PYTH). A favor da pergunta: o X4H- das 11h (UNI, PYTH) fez -4,48%
   contra -0,93%; o das 22h de ontem, -1,40% contra -1,05% em 24h.
9. **(40a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (06/10 22h): nenhuma DER-BORDA.
10. **(39a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 74 (RENDER,
    SUPER).
11. **(36a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje:
    nenhum barrado. Nenhum chegou ao alvo.
12. **(35a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(32a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    **0**. Hoje: com teto 85, nada muda (25 COMPRA nas duas versoes).
14. **(30a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(30a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: container novo,
    sem base; `fonte.py` nao rodou. Dentro desta propria coleta, a AAVE de
    01/10 fecha 171,454 na diaria e 171,387 na vela de 4h das 20:00. A ETH
    diaria de 07/09, 30/08 e 29/08 veio igual a das 11h (2490,08, 2417,19,
    2457,70).
16. **(29a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "25 de 28" e "Comprar os 20". O numero fixo erra pela quarta leitura
    seguida.
17. **(28a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 21 das 25 COMPRA ja eram COMPRA as 11h; entraram
    RENDER, LPT, AVAX (readmitidos) e LTC (era NEUTRO). PENGU saiu de
    COMPRA para VENDA.
18. **(28a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(24a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. Nenhuma COMPRA por gatilho 4h.
20. **(23a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (06/10
    22h): com a vela diaria nova, 14 de 21 stops desceram desde as 11h (UNI
    -6,31%, ICP -6,27%, PYTH -4,68%, NEAR -4,62%, AIOZ -4,55%...). Quem
    entrou as 11h em UNI tem hoje um stop 6,31% mais baixo.
21. **(23a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(23a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (06/10 22h): indisponivel, 403 da rede do ambiente, vigesima terceira
    coleta seguida.
23. **(15a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h (BTC, SUI, SHIB) fez -1,40% contra -1,02% do painel
    (-0,38 pp); a das 22h de ontem (a mesma) fez -1,89% em 24h contra
    -0,96% (-0,93 pp). No total, 12 vitorias em 31; perdeu as ultimas
    seis. A lista de agora tem 1 par (BTC) de 25 COMPRA. So ficou menor
    uma vez: vazia, em 28/09 11h (de 8 COMPRA).
