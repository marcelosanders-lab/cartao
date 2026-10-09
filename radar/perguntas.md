# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 08/10 22h.

1. **(58a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (08/10 22h): nenhum barrado. Os 2 barrados
    das 11h por "preco ja correu" (JUP, SUPER) fizeram -7,84% ate as 22h,
    contra -3,74% do painel e -3,43% das COMPRA: o portao acertou. SUPER
    voltou a COMPRA. Placar do portao: dez contra, nove a favor.
2. **(55a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: regime em BAIXA pela terceira leitura;
   4→4 sem o bonus, nenhuma COMPRA depende dele. Nao havia REGIME as 11h
   nem as 22h de ontem: sem medida. Placar na janela curta: nove a favor
   do bonus, seis contra.
3. **(52a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 3 de 4 COMPRA (IMX, SUPER, PYTH). Contra
   a pergunta nas duas medidas: o LIQ das 11h fez -1,68% contra -6,06% do
   resto; o das 22h de ontem, -3,12% contra -9,84% em 24h.
4. **(54a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (22h): das 5 COMPRA das 11h, 2 continuam COMPRA (AAVE, IMX), 2 viraram
   VENDA (NEAR, RENDER) e 1 NEUTRO (AIOZ). SUPER, barrada as 11h por
   "preco ja correu", voltou a COMPRA.
5. **(53a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhum. PYTH tem +2
   por cruzamento de alta no 4h, mas seria COMPRA sem ele (6/3).
6. **(52a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (08/10 22h): 2 COMPRA com
    marca MORTA (IMX, SUPER). O fechamento de IMX (0,17932) vem da vela das
    16:00 UTC (US$ 1.806,34 de US$ 1.857,95 do dia); o de SUPER (0,221544),
    da vela das 20:00 (US$ 524,84). Contra a pergunta nas duas medidas: o
    MORTA das 11h (IMX, AIOZ) fez +1,22% contra -6,53%; o das 22h de ontem
    (IMX, SUPER), +1,22% contra -8,65% em 24h.
7. **(49a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:04Z) com a base das 11h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(46a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (08/10 22h): nenhuma COMPRA com X4H-. A favor da pergunta
   na janela: o X4H- das 11h (RENDER) fez -7,47% contra -2,42% e virou
   VENDA.
9. **(44a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (08/10 22h): nenhuma DER-BORDA. Contra a pergunta na
    janela: a DER-BORDA das 11h (AIOZ) fez +0,20% contra -4,34%. NEAR, a
    -0,70 ATR e sem a marca, foi a pior COMPRA (-9,55%) e fechou abaixo do
    stop.
10. **(43a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 65 (PYTH).
11. **(40a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje:
    nenhum "preco ja correu". Os 2 das 11h nao chegaram ao alvo: JUP caiu
    8,54% e SUPER 7,14%.
12. **(39a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(35a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, **0**. Hoje: com teto 85, nada muda (4 COMPRA nas duas
    versoes).
14. **(34a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(34a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    11h: SOL 4h de 05/10 08:00 (120,83) e de 02/10 16:00 (117,99) vieram
    iguais a resposta das 11h, diferentes da base (120,81 e 118,00); AAVE
    4h de 01/10 20:00 voltou a 171,387, igual a base. A diaria de AIOZ de
    08/10 soma US$ 1.768,69, menos que as velas de 4h (US$ 1.798,65). A
    base nao foi alterada.
16. **(33a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 4 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(32a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): 2 das 4 COMPRA ja eram COMPRA as 11h (AAVE, IMX);
    SUPER veio de "preco ja correu" e PYTH de NEUTRO.
18. **(32a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(28a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. Nenhuma COMPRA por gatilho 4h.
20. **(27a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (08/10
    22h): NEAR fechou 4,4644, 3,48% abaixo do stop das 11h (4,6255425), e
    virou VENDA. AAVE segue COMPRA com o stop rebaixado 5,42% (158,076 →
    149,514). Em 24h, 2 de 3 stops desceram (AAVE -5,42%, SUPER -1,72%).
    AIOZ tocou 0,095000 intradia, abaixo do stop 0,10096188, e fechou
    acima.
21. **(27a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(27a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (08/10 22h): indisponivel, 403 da rede do ambiente, vigesima setima
    coleta seguida.
23. **(19a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 11h (AAVE, NEAR) fez -6,06% contra -3,74% do painel (-2,32
    pp); a das 22h de ontem (os mesmos dois) fez -9,84% em 24h contra
    -4,57% (-5,27 pp). NEAR fechou abaixo do stop. No total, 16 vitorias em
    39. A lista de agora tem 1 par (AAVE) de 4 COMPRA.
