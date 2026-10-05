# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 04/10 22h.

1. **(49a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (04/10 22h): nenhum par barrado. Os 3 barrados
    das 11h (ASTR, SOL, SEI) voltaram a COMPRA e fizeram +0,83% desde as
    11h, contra +0,86% das COMPRA: ponto a favor do portao por 0,03 pp,
    dentro do ruido. Placar do portao: sete leituras contra, sete a favor.
    Em 24h, o barrado das 22h de ontem (PENDLE) fez -0,34%, contra +0,59%
    das COMPRA.
2. **(46a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 25→14 sem o bonus; 11 COMPRA so existem
   por ele. O proprio BTC virou COMPRA (score 6/0) sem depender do bonus.
   Contra a pergunta, nas duas medidas desta leitura: na janela, o REGIME
   das 11h fez +1,66% contra +0,36% das outras COMPRA (sem PENGU, +1,16%);
   em 24h, o das 22h de ontem fez +1,78% contra -0,32%. Placar na janela
   curta: cinco a favor do bonus, quatro contra.
3. **(43a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 16 de 25 COMPRA. A favor da pergunta nesta
   janela: o grupo LIQ das 11h fez +0,53% contra +1,29% do resto. Sem
   PENGU (+5,17%), +0,11% contra +1,29%.
4. **(45a)** A leitura das 11h deve considerar a vela em formacao? Hoje: os
   3 barrados das 11h (ASTR, SEI, SOL) voltaram a COMPRA com a vela diaria
   nova. 20 das 21 COMPRA das 11h seguiram COMPRA; LTC virou NEUTRO.
5. **(44a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhuma. As 3 das 11h
   (PENDLE, ETH, JUP) fizeram +1,29% contra +0,78% das outras COMPRA:
   contra a pergunta nesta janela.
6. **(43a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (04/10 22h): 6 COMPRA com
    marca MORTA (IMX, DYDX, AR, SUPER, LPT, AIOZ); 5 delas com deriva 0,00.
    AR teve um unico negocio em todo o dia 04/10 (US$ 15,68): a vela diaria
    fechou com abertura, maxima, minima e fechamento iguais, e o motor deu
    COMPRA com R:R 2,00:1. Na janela, o MORTA das 11h fez -0,63% contra
    +1,45% das outras COMPRA.
7. **(40a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:04Z de 05/10); as 56 chamadas foram
   pela instancia principal, sem pedido de login.
8. **(37a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (04/10 22h): 2 COMPRA com X4H- (LPT, PYTH). O X4H- das 22h
   de ontem (UNI, ICP) fez -0,21% em 24h contra +0,67% do resto.
9. **(35a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (04/10 22h): nenhuma COMPRA com DER-BORDA. Maiores
    derivas: ASTR +0,24 e PENGU +0,22 ATR (limite +0,30).
10. **(34a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SUPER, com RSI 78, exatamente no teto, virou COMPRA com marca
    RSI-BORDA. As 11h era REALIZAR PARCIAL (RSI 89). Fez -0,84% desde as
    11h e -6,50% em 24h.
11. **(31a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje:
    nenhum barrado por preco ja corrido. Nenhum chegou ao alvo.
12. **(30a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(27a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, **0**. Hoje:
    com teto 85, nada muda (25 COMPRA nas duas versoes). SUPER caiu de RSI
    89 para 78 e passou no limite atual.
14. **(25a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 27 dos 28 pares vieram iguais. BTC: diaria em formacao
    86596,00, ultima vela de 4h 86589,44; o motor usou o 4h.
15. **(25a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a AAVE diaria de 01/10
    voltou para 171,387, igual ao proprio 4h e a base (as 11h veio
    171,454). A ETH de 4h de 02/10 16:00 voltou para 2668,73 (as 11h,
    2668,68). As quatro velas fechadas da SOL que as 11h vieram diferentes
    voltaram aos valores da base. Novas: BTC diaria de 06/09 com fechamento
    80344,16 (base 80344,15) e AVAX 4h de 29/09 16:00 com volume diferente
    da base. A fonte alterna valores de velas fechadas entre coletas.
16. **(24a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso diz
    "25 de 28 pares deram COMPRA" e "Comprar os 20". O numero esta errado
    pela terceira leitura seguida.
17. **(23a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 20 das 25 COMPRA ja eram COMPRA as 11h; 3 voltaram
    do bloqueio das 11h; BTC veio de NEUTRO; SUPER veio de REALIZAR PARCIAL.
18. **(23a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(19a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21.
20. **(18a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (04/10
    22h): das 11h para ca, 5 de 20 stops desceram com a vela diaria nova:
    AR -5,05%, LPT -4,76%, AAVE -1,09%, DYDX -0,81%, ONDO -0,17%. O de AR
    desceu por causa do negocio isolado de US$ 15,68. Em 24h, 5 de 22, os
    mesmos.
21. **(18a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(18a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (04/10 22h): indisponivel, 403 da rede do ambiente, decima oitava
    coleta seguida.
23. **(10a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h (ETH, AAVE, SUI, LINK, PYTH) fez +1,31% ate as 22h
    contra +0,73% do painel (+0,58 pp); a das 22h de ontem (SOL, AAVE, SUI,
    AVAX, LINK, PYTH) fez +0,67% em 24h contra +0,34% (+0,33 pp). No total,
    11 vitorias em 23.
