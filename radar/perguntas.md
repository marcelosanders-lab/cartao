# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 09/10 11h.

1. **(59a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (09/10 11h): 3 barrados por "preco ja
    correu": IMX (+0,89 ATR, R:R 0,88:1), SUPER (+0,86 ATR, R:R 0,91:1) e
    PYTH (+0,73 ATR, R:R 1,02:1), as tres COMPRA das 22h que subiram
    5,5% a 8,1%. Nenhum por "risco ja consumido". Nao havia barrados as
    22h: sem medida na janela. Placar do portao: dez contra, nove a favor.
    Em 24h, os barrados das 11h de ontem (JUP, SUPER) fizeram -2,69%
    contra -2,17% do painel e -0,78% das COMPRA.
2. **(56a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: regime em BAIXA pela quarta leitura;
   2→2 sem o bonus, nenhuma COMPRA depende dele. Nao havia REGIME as 22h
   nem as 11h de ontem: sem medida. Placar na janela curta: nove a favor
   do bonus, seis contra.
3. **(53a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 1 de 2 COMPRA (LPT, US$ 1.924/dia). Contra
   a pergunta nas duas medidas: o LIQ das 22h fez +6,44% contra +1,12% do
   resto; o das 11h de ontem, +0,70% contra -3,00% em 24h.
4. **(55a)** A leitura das 11h deve considerar a vela em formacao? Hoje: das
   4 COMPRA das 22h, 1 continua COMPRA (AAVE) e 3 viraram "preco ja
   correu" (IMX, SUPER, PYTH), justamente as que subiram 5,5% a 8,1%. Quem
   nao entrou as 22h recebe "nao entre" nas tres.
5. **(54a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: 1 caso, LPT. O
   cruzamento fechou na vela de 4h das 08:00, com US$ 0 negociados; a das
   04:00 tambem teve US$ 0; o preco que puxou a EMA9 (1,692 → 1,756) e um
   negocio de US$ 25,01 as 00:00. O "Agora" (1,716) ja esta abaixo desse
   preco.
6. **(53a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (09/10 11h): nenhuma
    COMPRA com MORTA. IMX e SUPER, MORTA as 22h, continuam com preco de
    vela morta e estao barradas. LPT nao leva a marca, mas o cruzamento
    que a fez COMPRA saiu de velas sem negocio (Pergunta 5). Contra a
    pergunta nas duas medidas: o MORTA das 22h (IMX, SUPER) fez +5,62%
    contra +4,60%; o das 11h de ontem (IMX, AIOZ), +3,70% contra -3,77% em
    24h.
7. **(50a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 14:05Z) com a base das 22h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(47a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (09/10 11h): nenhuma COMPRA com X4H-. A favor da pergunta em
   24h: o X4H- das 11h de ontem (RENDER) fez -5,31% contra +0,35%.
9. **(45a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (09/10 11h): nenhuma DER-BORDA. Em 24h, a DER-BORDA das
    11h de ontem (AIOZ) fez -0,65% contra -0,81%: diferenca pequena, contra
    a pergunta.
10. **(44a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 56 (AAVE).
11. **(41a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 3
    "preco ja correu": IMX (0,18953, alvo 0,21372244), SUPER (0,233814,
    alvo 0,26425242) e PYTH (0,08578, alvo 0,099765604). Nenhum chegou ao
    alvo.
12. **(40a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(36a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, **0**. Hoje: com teto 85, nada muda (2 COMPRA nas duas
    versoes).
14. **(35a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(35a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    22h: AAVE de 01/10 veio com os valores trocados entre as series (4h
    das 20:00 171,454 contra 171,387 na base; diaria 171,387 contra
    171,454 na base); SOL 4h de 05/10 08:00 (120,83) e de 02/10 16:00
    (117,99) iguais as respostas anteriores, diferentes da base. A base
    nao foi alterada.
16. **(34a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 2 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(33a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje: 1 das 2 COMPRA ja era COMPRA as 22h (AAVE); LPT e nova
    (era NEUTRO), por gatilho 4h.
18. **(33a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(29a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: 1 COMPRA por
    gatilho 4h (LPT), com EMA9 diaria acima da EMA21 e deriva +0,20 ATR,
    dentro do portao. Nenhuma COMPRA com EMA9 diaria abaixo da EMA21.
20. **(28a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (09/10
    11h): mesma vela diaria, nenhum stop mudou desde as 22h. Em 24h, 1 par
    COMPRA nas duas leituras (AAVE), stop rebaixado 5,42% (158,076 →
    149,514).
21. **(28a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(28a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (09/10 11h): indisponivel, 403 da rede do ambiente, vigesima oitava
    coleta seguida.
23. **(20a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista das 22h (so AAVE) fez +1,12% contra +1,63% do painel (-0,51
    pp); a das 11h de ontem (AAVE, NEAR) fez -3,00% em 24h contra -2,17%
    (-0,82 pp). Seis derrotas seguidas; no total, 16 vitorias em 41. Na
    janela em que as COMPRA mais ganharam, a lista ficou com a pior delas.
    A lista de agora tem 1 par (AAVE) de 2 COMPRA.
