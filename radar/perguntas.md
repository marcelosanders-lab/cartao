# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 27/09 extra 08:09.

1. **(33a)** Reancorar stop e deriva em referencia mais antiga que o
    fechamento anterior. Hoje (27/09 08:09): SUI era COMPRA as 22h e virou
    "preco ja correu" (+1,03 ATR) nove horas depois, sem vela diaria nova.
2. **(30a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 23→18.
3. **(27a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 13 de 23 COMPRA.
4. **(29a)** A leitura das 11h deve considerar a vela em formacao?
5. **(28a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(27a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
    vela sem negocio ou de negocio isolado. Hoje (27/09 08:09): AR, LPT e
    AIOZ em COMPRA com a vela 4h atual sem negocio; AR sem negocio ha 12
    horas.
7. **(24a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao.
8. **(21a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje: ETH com cruzamento de alta e de baixa simultaneos.
9. **(19a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
    deriva. Hoje (27/09 08:09): LPT +0,30 (no limite exato, R:R 1,50:1) e
    DYDX +0,29.
10. **(18a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SEI com RSI 76, AR 75.
11. **(15a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(14a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: SUI.
13. **(11a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, **2**. Efeito medido: +0,46 pp na janela anterior, -0,93 pp
    nesta.
14. **(9a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(9a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: seis velas.
16. **(8a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444`. Hoje (27/09 08:09):
    o cabecalho diz "Leitura das 11h" numa leitura das 08:09.
17. **(7a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h.
18. **(7a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(3a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(2a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje (27/09
    08:09): 0 de 14 rebaixados - a vela diaria nao mudou; o teste real e as
    22h.
21. **(2a)** Outra fonte de velas. Todos os sites de preço testados estao
    bloqueados pela rede do ambiente; CoinDesk e Twelve Data existem como
    conectores mas nao estao conectados. Se conectar um, ele deve (a) so
    conferir as velas da Crypto.com, (b) substituir a Crypto.com nos pares
    magros, ou (c) cobrir as 14 moedas que a Crypto.com nao lista (ANKR,
    TOSHI...)? Hoje: nenhuma fonte alternativa acessivel.
22. **(2a)** Medo e ganancia da CoinMarketCap como indicador de compra: em
    que direcao? (a) contrario - medo extremo favorece COMPRA, ganancia
    extrema bloqueia; (b) a favor - ganancia confirma tendencia; (c) so
    registrar ate haver 30+ leituras para medir contra o placar. As duas
    primeiras leituras sao opostas e nenhuma foi testada nestas moedas. Hoje
    (27/09 08:09): indice indisponivel, 403 da rede do ambiente.
