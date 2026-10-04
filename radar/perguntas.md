# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 04/10 11h.

1. **(48a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (04/10 11h): das 22h as 11h o barrado das
    22h (PENDLE) fez -1,67%, contra -0,24% das COMPRA: ponto a favor do
    portao. Placar do portao: sete leituras contra, seis a favor. Em 24h,
    os 8 barrados das 11h de ontem fizeram -0,74%, contra +1,02% das COMPRA.
    Agora, 3 barrados: ASTR (+0,49 ATR), SOL (+0,42) e SEI (+0,31).
2. **(45a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 21→13 sem o bonus; 8 COMPRA so existem
   por ele, e o proprio BTC segue NEUTRO. Contra a pergunta, nas duas
   medidas desta leitura: na janela, o REGIME das 22h fez +0,08% contra
   -0,48% das outras COMPRA; em 24h, o das 11h de ontem fez +1,94% contra
   +0,11%. Placar na janela curta: quatro a favor do bonus, quatro contra.
3. **(42a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 12 de 21 COMPRA. A favor da pergunta nesta
   janela: o grupo LIQ das 22h fez -0,39% contra -0,04% do resto. Sem AR e
   LPT, inverte: +0,19% contra -0,04%.
4. **(44a)** A leitura das 11h deve considerar a vela em formacao? Hoje: 3
   das 23 COMPRA das 22h viraram SEM ENTRADA sem vela diaria nova (ASTR,
   SEI, SOL). Fizeram +1,59% em media desde as 22h; as outras 20, -0,51%.
5. **(43a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: 3, PENDLE, ETH e JUP.
   PENDLE negociou US$ 2.041 no dia e US$ 6,32 na vela das 12:00.
6. **(42a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (04/10 11h): 6 COMPRA com
    marca MORTA (PENDLE, IMX, DYDX, AR, LPT, AIOZ). O "Agora" de AR saiu de
    um unico negocio de US$ 15,68, que derrubou o preco 4,77% e deu a AR o
    melhor R:R da lista (4,04:1).
7. **(39a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:04Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(36a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (04/10 11h): nenhuma COMPRA com X4H-. O X4H- das 22h (UNI,
   ICP) fez -0,64% contra -0,20% do resto.
9. **(34a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (04/10 11h): nenhuma COMPRA com DER-BORDA. O DER-BORDA das
    11h de ontem (UNI) fez -1,72% em 24h contra +1,23% do resto.
10. **(33a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA; AAVE com RSI 73 e a mais alta.
11. **(30a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 3
    barrados por preco ja corrido (ASTR, SOL, SEI). Nenhum chegou ao alvo.
12. **(29a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(26a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, **0**. Hoje:
    SUPER, com RSI 89, segue como REALIZAR PARCIAL.
14. **(24a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(24a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a AAVE diaria de 01/10
    veio de novo com fechamento 171,454, mas a ultima vela de 4h do mesmo
    dia (20:00) fecha 171,387, igual a base: a diaria da fonte contradiz o
    proprio 4h. A ETH de 4h de 02/10 16:00 voltou para 2668,68 (ontem as
    22h veio 2668,73). SOL veio com quatro velas fechadas diferentes da
    base.
16. **(23a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "21 de 28 pares deram COMPRA" e "Comprar os 20". O numero esta errado
    pela segunda leitura seguida.
17. **(22a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 20 das 21 COMPRA ja eram COMPRA as 22h; so PENDLE e nova.
18. **(22a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(18a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21.
20. **(17a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (04/10
    11h): das 22h para ca, nenhum dos 20 stops mudou (mesma vela diaria). Em
    24h, 1 de 12 desceu (PYTH -0,44%).
21. **(17a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(17a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (04/10 11h): indisponivel, 403 da rede do ambiente, decima setima
    coleta seguida.
23. **(9a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (SOL, AAVE, SUI, AVAX, LINK, PYTH) fez -0,19% ate as 11h
    contra -0,39% do painel (+0,20 pp); a das 11h de ontem (AAVE, LINK,
    PYTH) fez -0,12% em 24h contra +0,38% (-0,50 pp). No total, 9 vitorias
    em 21.
