# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 29/09 22h.

1. **(39a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (29/09 22h): **a serie de seis leituras
    contra o portao quebrou.** Das 11h as 22h os 10 bloqueados fizeram
    -1,65%, as 15 COMPRA -1,03%, o painel -1,21%; 9 dos 10 voltaram a COMPRA
    mais baratos (AAVE -5,76%, IMX -4,97%). Placar do portao: seis leituras
    contra, uma a favor. Novo bloqueado: NEAR, +0,37 ATR.
2. **(36a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 22→18 sem o bonus (saem ETH, PYTH, SEI,
   UNI); o BTC segue NEUTRO (5/2). Contra o filtro, nada nesta janela: o
   grupo REGIME das 11h fez -0,00% contra -1,21% do painel.
3. **(33a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 11 de 22 COMPRA. O grupo LIQ das 11h fez
   -1,61% ate as 22h (painel -1,21%).
4. **(35a)** A leitura das 11h deve considerar a vela em formacao? Hoje: a
   lista das 11h (15 COMPRA) fez -1,03% ate as 22h, 0,18 pp acima do painel.
5. **(34a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhuma COMPRA por
   gatilho 4h.
6. **(33a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (29/09 22h): 5 COMPRA com
    marca MORTA (IMX, DYDX, AR, LPT, AIOZ). O "Agora" de DYDX e a sua marca
    de borda de deriva vem de um negocio de US$ 2,61. As MORTA das 11h
    fizeram -2,33% ate as 22h.
7. **(30a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo as 01:04Z); as 56 chamadas de velas
   foram todas pela instancia principal do conector, sem pedido de login.
8. **(27a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (29/09 22h): 3 das 22 COMPRA (ETH, SUI, ONDO). O grupo X4H-
   das 11h fez -0,13% ate as 22h (painel -1,21%).
9. **(25a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (29/09 22h): IMX +0,27, DYDX +0,27, PYTH +0,29 ATR (limite
    +0,30).
10. **(24a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma marca RSI-BORDA; os maiores RSI entre as COMPRA sao 72
    (AVAX, ICP).
11. **(21a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 1
    caso (NEAR), nenhum perto do alvo.
12. **(20a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(17a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, **1**. Hoje: SUPER (RSI 79) barrado; com teto
    85 viraria COMPRA. SUPER fez -2,73% das 11h as 22h, sem negocio desde
    as 16:00 UTC.
14. **(15a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: as 22h o "Agora" vem de uma vela aberta ha 1h; em SUPER, LPT,
    AIOZ, WLFI e LMWR ela nao tem negocio nenhum.
15. **(15a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente"; uma amostra manual de 12 velas
    diarias (27 e 28/09 de ONDO, DYDX, RENDER, AR, PYTH, WLFI) bateu com a
    base. Nao foi conferencia completa.
16. **(14a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso
    apareceu e diz "22 de 28" e, na frase seguinte, "Comprar os 20".
17. **(13a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 9 das 22 COMPRA sao os pares que o portao barrou as
    11h e que cairam ate aqui.
18. **(13a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(9a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(8a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (29/09
    22h): das 11h para ca, 11 de 13 stops desceram; SEI caiu 0,92% e o stop
    6,23%; PYTH subiu 2,13% e o stop desceu 4,05%. Em 24h, 13 de 22.
21. **(8a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(8a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (29/09 22h): indisponivel, 403 da rede do ambiente, oitava coleta
    seguida.
