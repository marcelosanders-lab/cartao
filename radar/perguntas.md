# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 09/10 22h.

1. **(60a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (09/10 22h): 1 barrado por "preco ja
    correu": IMX (+0,45 ATR, R:R 1,31:1). Nenhum por "risco ja consumido".
    Os 3 barrados das 11h (IMX, SUPER, PYTH) fizeram -0,64% ate as 22h,
    contra +1,65% do painel e +0,07% das COMPRA: o portao acertou na
    media, mas IMX, barrada, foi a melhor do painel (+9,20%). Placar do
    portao: dez contra, dez a favor.
2. **(57a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: regime em BAIXA pela quinta leitura;
   5→5 sem o bonus, nenhuma COMPRA depende dele. Nao havia REGIME as 11h
   nem as 22h de ontem: sem medida. Placar na janela curta: nove a favor
   do bonus, seis contra.
3. **(54a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 5 de 5 COMPRA (ONDO, PYTH, JUP, WLFI,
   AIOZ). Na janela, o LIQ das 11h (LPT) fez 0,00% contra +0,14% de AAVE.
   Contra a pergunta em 24h: o LIQ das 22h de ontem (IMX, SUPER, PYTH)
   fez +5,72% contra +1,26%.
4. **(56a)** A leitura das 11h deve considerar a vela em formacao? Hoje
   (22h): das 2 COMPRA das 11h, nenhuma continua COMPRA: AAVE virou NEUTRO
   e LPT, VENDA. Das 3 barradas das 11h, PYTH voltou a COMPRA, SUPER virou
   NEUTRO e IMX segue barrada.
5. **(55a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`). Hoje: LPT, COMPRA por
   gatilho 4h as 11h, virou VENDA sem nenhum negocio depois das 12:00 UTC.
   E WLFI e COMPRA as 22h por um cruzamento de alta no 4h fechado na vela
   das 20:00 (US$ 539,64); sem os +2 dele seria 5/4. As 22h o motor nao
   poe o rotulo "gatilho 4h" (so marca na janela `manha`).
6. **(54a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (09/10 22h): 1 COMPRA com
    MORTA (AIOZ). O fechamento (0,115721) vem da vela das 20:00 UTC (US$
    859,69); as velas das 12:00, 16:00 e de 10/10 nao tem negocio. Nao
    havia MORTA entre as COMPRA das 11h: sem medida na janela. Contra a
    pergunta em 24h: o MORTA das 22h de ontem (IMX, SUPER) fez +7,69%
    contra +1,52%.
7. **(51a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao. Hoje: rodou (disparo 01:04Z) com a base das 11h
   reaproveitada; 56 chamadas de velas pela instancia principal, sem
   pedido de login.
8. **(48a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje (09/10 22h): nenhuma COMPRA com X4H-. Nao havia X4H- as 11h
   nem as 22h de ontem: sem medida.
9. **(46a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (09/10 22h): nenhuma DER-BORDA. Sem medida.
10. **(45a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: nenhuma RSI-BORDA. Maior RSI entre as COMPRA: 66 (JUP).
11. **(42a)** Separar "preco ja correu" de "preco chegou ao alvo". Hoje: 1
    "preco ja correu": IMX (0,20697, alvo 0,23808232). Nao chegou ao alvo.
12. **(41a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: nenhum bloqueio desse tipo.
13. **(37a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, 2, 2, 4, 4, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, **0**. Hoje: com teto 85, nada muda (5 COMPRA nas
    duas versoes).
14. **(36a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
    Hoje: em 28 dos 28 pares vieram iguais.
15. **(36a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: `fonte.py`
    "nenhuma vela fechada divergente". Nas respostas, contra a base das
    11h: ETH diaria de 07/09 (2490,49 contra 2490,08), 30/08 (2416,87
    contra 2417,19) e 29/08 (2457,69 contra 2457,70); SOL diaria de 30/08
    (101,78 contra 101,75). AAVE de 01/10 e BTC 4h de 08/10, 05/10 e 02/10
    voltaram a bater com a base. A base nao foi alterada.
16. **(35a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje: com 5 COMPRA
    o aviso nao apareceu; o numero fixo continua no codigo.
17. **(34a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h. Hoje (22h): nenhuma das 5 COMPRA era COMPRA as 11h. PYTH veio
    de "preco ja correu", JUP e AIOZ de NEUTRO, ONDO e WLFI de VENDA.
18. **(34a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(30a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA? Hoje: 1 COMPRA com
    EMA9 diaria abaixo da EMA21 (WLFI), sustentada pelo +2 do cruzamento
    de alta no 4h; sem ele seria 5/4.
20. **(29a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (09/10
    22h): as 2 COMPRA das 11h fecharam acima do stop. Em 24h, 1 par COMPRA
    nas duas leituras (PYTH), stop rebaixado 1,62% (0,0720072 →
    0,070838).
21. **(29a)** Outra fonte de velas. Todos os sites de preco testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa.
22. **(29a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (09/10 22h): indisponivel, 403 da rede do ambiente, vigesima nona
    coleta seguida.
23. **(21a)** A lista de sobrevivencia (e as marcas do auditor que a formam)
    deve continuar sendo entregue quando alguem perguntar "quais as
    melhores"? Opcoes: (a) manter com o rotulo atual, (b) entregar so com o
    placar dela ao lado, (c) parar de entregar ate haver 30 medicoes. Hoje:
    a lista esta vazia (0 de 5). A das 11h (so AAVE) fez +0,14% contra
    +1,65% do painel (-1,51 pp); a das 22h de ontem (so AAVE) fez +1,26%
    em 24h contra +3,29% (-2,03 pp). Oito derrotas seguidas; no total, 16
    vitorias em 43.
