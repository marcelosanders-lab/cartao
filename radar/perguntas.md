# Perguntas em aberto ao dono

Lista canônica. A rotina **atualiza este arquivo** a cada leitura (incrementa o
contador, troca o "Hoje:" pelo dado medido nesta execução) e o relatório copia
a lista daqui — nunca do relatório anterior.

Nenhuma é implementada sem resposta do dono, dada em mensagem dele. Disparo de
rotina, notificação ou lembrete não conta como resposta.

Contador = número de relatórios em que a pergunta apareceu sem resposta.
Última atualização: 26/09 noite.

1. **(32a)** Reancorar stop e deriva em referencia mais antiga que o
   fechamento anterior. Hoje: SUI "risco consumido" as 17:49 e COMPRA as 22h.
2. **(29a, COM CONTRAPROVA)** Consertar ou remover o filtro de regime do BTC
   (`analisar.py:309-310`). Hoje: 23→18.
3. **(26a)** Suprimir o sinal, e nao so avisar, quando a vela diaria tiver
   volume abaixo do piso. Hoje: 13 de 23 COMPRA.
4. **(28a)** A leitura das 11h deve considerar a vela em formacao?
5. **(27a)** Exigir volume minimo nas velas do cruzamento antes de emitir
   "COMPRA (gatilho 4h)" (`analisar.py:334`).
6. **(26a)** Marcar, ou suprimir, os pares cujo "Agora" ou fechamento vem de
   vela sem negocio ou de negocio isolado. Hoje: sete COMPRA com R:R 2,00:1
   exato, AR com fechamento de US$ 104.
7. **(23a)** O que fazer quando a sessao fica ociosa e a rotina dispara sem
   execucao.
8. **(20a)** Marcar quando o portao ignora um cruzamento de 4h contrario ao
   sinal. Hoje: ETH com cruzamento de alta e de baixa simultaneos.
9. **(18a)** Marcar quando uma COMPRA nasce colada ao proprio limite de
   deriva. Hoje: UNI +0,28, LPT -0,63.
10. **(17a)** Marcar quando uma COMPRA nasce perto do teto de sobrecompra.
    Hoje: SEI com RSI 76, AR 75.
11. **(14a)** Separar "preco ja correu" de "preco chegou ao alvo".
12. **(13a)** O bloqueio "risco ja consumido" deveria olhar o R:R antes de
    recusar? Hoje: SUI.
13. **(10a)** Medir o teto de sobrecompra toda janela. Serie: 3, 0, 1, 0, 3,
    2, 4, 4, **2**. Efeito medido: +0,46 pp na janela anterior, -0,93 pp
    nesta.
14. **(8a)** O "Agora" deve vir da serie de 4h ou da diaria em formacao?
15. **(8a)** A fonte devolve valores diferentes para a mesma vela fechada.
    Aceitar como ruido ou cruzar com outra fonte? Hoje: seis velas.
16. **(7a)** Leituras fora de horario: janela `extra` com cabecalho honesto,
    ou proibir? E o "20" chumbado em `analisar.py:444` (hoje com 23).
17. **(6a)** Marcar no relatorio das 11h quais COMPRA sao residuo da leitura
    das 22h.
18. **(6a, PRAZO VENCIDO)** Guardar as velas de entrada de cada lote fora da
    janela rolante de 50. O placar em R esta congelado.
19. **(2a)** O cruzamento de alta no 4h deve ser dispensado do portao de
    deriva, ou medido contra outra referencia? Deve existir uma regra de
    tendencia diaria antes de aceitar qualquer COMPRA?
20. **(1a)** O stop de uma posicao ja aberta deve ficar fixo no valor da
    entrada, em vez de ser recalculado a partir de cada fechamento novo? O
    relatorio deve separar "entrada nova" de "posicao aberta"? Hoje: 8 de 20
    stops rebaixados em 24 horas.
