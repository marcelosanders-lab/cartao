# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 07/10 11h.

1. **(55a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (07/10 11h): nenhum barrado por "preco ja
    correu"; 14 por "risco ja consumido". Os 3 que a vela nova readmitiu as
    22h (RENDER, LPT, AVAX) fizeram -5,93% contra -5,35% do painel, e LPT
    ja esta com o preco abaixo do stop. Nao havia barrado as 22h: sem
    medida do portao nesta janela. Placar do portao: oito contra, oito a
    favor.
2. **(52a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 7→1 sem o bonus; 6 COMPRA so existem por
   ele (AIOZ, AVAX, LINK, LTC, NEAR, ONDO) e so SUI sobra. Com regime em
   baixa, AIOZ vira VENDA. Contra a pergunta nesta janela: o REGIME das 22h
   fez -4,77% contra -6,41% das outras COMPRA; em 24h, o das 11h de ontem
   fez -5,24% contra -7,89%. Placar na janela curta: nove a favor do
   bonus, cinco contra.
3. **(49a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 2 de 7 COMPRA (ONDO, AIOZ). A favor da
   pergunta: o LIQ das 22h fez -6,52% contra -3,80% do resto; o das 11h de
   ontem, -7,79% contra -4,74% em 24h.
4. **(51a)** A leitura das 11h deve considerar a vela em formacao? Hoje: a
   vela em formacao tirou de COMPRA 18 das 25 COMPRA das 22h (14 "risco
   ja consumido", 4 "abaixo do stop"). Ficaram 7.
5. **(50a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: nenhum.
6. **(49a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (07/10 11h): 1 COMPRA com
    marca MORTA (AIOZ). A favor da pergunta nesta janela: o MORTA das 22h
    fez -6,23% contra -5,18% das outras COMPRA. Nos 6 MORTA das 22h, o
    "Agora" vinha de vela sem negocio; em 5 deles (IMX, DYDX, SUPER, AIOZ,
    ASTR) o primeiro negocio de 07/10 saiu abaixo desse valor, e em AR
    acima.
7. **(46a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z) com a base das 22h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(43a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (07/10 11h): 1 COMPRA com X4H- (AIOZ). Contra a pergunta,
   por pouco: o X4H- das 22h fez -5,26% contra -5,48%. A favor, em 24h:
   UNI e PYTH fizeram -10,21% contra -6,33%.
9. **(41a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (07/10 11h): 3 DER-BORDA, todas junto ao limite de baixo
    (-0,75 ATR): LINK -0,72, LTC -0,71, ONDO -0,71.
10. **(40a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 69 (AVAX).
11. **(37a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje:
    nenhum "preco ja correu". Nenhum chegou ao alvo.
12. **(36a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: 14 bloqueios desse tipo, todos com R:R "agora" entre
    5,18:1 (AAVE) e 166,08:1 (DYDX). Perto do stop, o R:R explode e deixa
    de medir alguma coisa.
13. **(32a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, **0**. Hoje: com teto 85, nada muda (7 COMPRA nas duas versoes).
14. **(31a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(31a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    22h: SOL 4h de 05/10 08:00 (120,83, base 120,81) e de 02/10, 30/09 e
    29/09 16:00; SUI diaria de 30/08 (0,71134, base 0,71114); volume da
    LINK diaria de 13/09; AAVE 4h de 01/10 20:00 agora 171,454 (base
    171,387), igual a diaria. A base nao foi alterada.
16. **(30a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 7 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(29a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 7 das 7 COMPRA ja eram COMPRA as 22h; nenhuma e nova.
    18 COMPRA das 22h sairam (14 "risco ja consumido", 4 "abaixo do
    stop").
18. **(29a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(25a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: nenhuma COMPRA
    com EMA9 diaria abaixo da EMA21. Nenhuma COMPRA por gatilho 4h.
20. **(24a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (07/10
    11h): mesma vela diaria, nenhum stop mudou desde as 22h. Mas 4 COMPRA
    das 22h ja estao com o preco abaixo do stop (IMX, LPT, ASTR, ETH), e o
    relatorio nao diz a quem entrou se sai agora ou espera o fechamento
    diario das 21h. Em 24h, 4 de 5 stops desceram (NEAR -4,62%, AIOZ
    -4,55%, SUI -2,90%, ONDO -1,20%).
21. **(24a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(24a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (07/10 11h): indisponivel, 403 da rede do ambiente, vigesima quarta
    coleta seguida.
23. **(16a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (so BTC) fez -2,72% contra -5,35% do painel (+2,63
    pp); a das 11h de ontem (BTC, SUI, SHIB) fez -5,89% em 24h contra
    -6,33% (+0,43 pp). No total, 14 vitorias em 33; a sequencia de seis
    derrotas acabou. A lista de agora tem 1 par (SUI) de 7 COMPRA.
