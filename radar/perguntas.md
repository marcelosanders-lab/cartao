# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 03/10 11h.

1. **(46a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (03/10 11h): das 22h as 11h os 2 barrados das
    22h (SUI, PYTH) fizeram -1,29%, contra +1,73% das COMPRA: ponto contra
    o portao. Placar do portao: sete leituras contra, quatro a favor. Mas a
    vantagem das COMPRA vem de AR e LPT; sem os dois, as COMPRA fizeram
    +0,54% e o portao teria acertado. Em 24h, os 16 barrados das 11h de
    ontem fizeram -2,46%, contra -0,97% das COMPRA. Agora, 8 barrados.
2. **(43a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 14→7 sem o bonus; 7 COMPRA so existem
   por ele, e o proprio BTC segue NEUTRO. A favor da pergunta: na janela, o
   grupo REGIME das 22h fez +1,10% contra +2,49% das outras COMPRA (placar
   na janela curta: duas a favor do bonus, quatro contra). Contra: em 24h, o
   REGIME das 11h de ontem (UNI, AR) fez +3,67% contra -2,13%.
3. **(40a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 6 de 14 COMPRA. Contra a pergunta nesta
   janela: o grupo LIQ das 22h fez +2,93%, contra -0,09% do resto, mas so
   por AR e LPT.
4. **(42a)** A leitura das 11h deve considerar a vela em formacao? Hoje: 7
   das 20 COMPRA das 22h viraram SEM ENTRADA sem vela diaria nova (AR, LPT,
   SEI, IMX, DYDX, AVAX, JUP). Duas delas por um unico bloco de negocio.
5. **(41a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: 2, PYTH e UNI. UNI tem
   marca LIQ.
6. **(40a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (03/10 11h): 1 COMPRA com
    marca MORTA (AIOZ, US$ 51,38 no dia). LPT subiu 10,59% com US$ 10,88 no
    dia; AR subiu 14,27% com US$ 921,17. As duas variacoes entraram no
    placar como se fossem mercado.
7. **(37a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:04Z); as 56 chamadas foram pela
   instancia principal, sem pedido de login.
8. **(34a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (03/10 11h): 1 COMPRA com X4H- (ETH). O grupo X4H- das 22h
   (AVAX, SHIB, AR, ASTR) fez +3,81%, contra +1,20% do resto, por causa de
   AR.
9. **(32a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (03/10 11h): 1 COMPRA com DER-BORDA, UNI (+0,25 ATR). O
    limite e +0,30. O DER-BORDA das 22h (LTC, ASTR) fez -1,03%, contra
    +2,03% do resto.
10. **(31a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma COMPRA com RSI-BORDA; AAVE com RSI 73 e a mais alta.
11. **(28a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 8
    barrados por preco ja corrido. Nenhum chegou ao alvo.
12. **(27a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(24a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, **0**. Hoje: SUPER, com
    RSI 86, segue como REALIZAR PARCIAL.
14. **(22a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(22a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py` de novo
    "nenhuma vela fechada divergente". Nas respostas, a vela de 4h de 02/10
    16:00 veio revista no BTC (84321,29; base 84320,19) e no ETH (2668,73;
    base 2668,68). `fonte.py` nao ve isso porque essas linhas vem da base.
16. **(21a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: o aviso nao
    apareceu; 14 de 28 COMPRA fica abaixo do gatilho de 60%.
17. **(20a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 13 das 14 COMPRA ja eram COMPRA as 22h; so PYTH e nova.
18. **(20a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(16a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. AR e LPT tem cruzamento de alta no 4h
    e estao barrados a +1,67 e +1,72 ATR.
20. **(15a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (03/10
    11h): das 22h para ca, nenhum dos 13 stops mudou (mesma vela diaria).
    Em 24h, 4 de 5 desceram; LINK -5,03%.
21. **(15a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(15a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (03/10 11h): indisponivel, 403 da rede do ambiente, decima quinta
    coleta seguida.
23. **(7a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (AAVE, LINK) fez +0,21% ate as 11h contra +1,53% do
    painel (-1,32 pp); a das 11h de ontem fez -2,42% em 24h contra -1,40%
    (-1,02 pp). Duas derrotas. No total, 7 vitorias em 17.
