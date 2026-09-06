# Instruções da rotina (leituras das 11h e 22h)

Este arquivo é o roteiro que a sessão agendada executa. Para mudar o que a
rotina faz, edite este arquivo — não é preciso recriar o agendamento.

A sessão agendada recebe apenas: a janela (`manha` ou `noite`) e a ordem de ler
este arquivo. Tudo o mais está aqui.

---

## Regra número um

**Nunca escreva um preço, um RSI ou um sinal que não tenha saído de
`analisar.py` rodando sobre dados baixados nesta execução.**

Se a ferramenta de mercado da Crypto.com não estiver disponível, ou se as
chamadas falharem, o resultado da rotina é uma mensagem dizendo que a coleta
falhou. Não estime, não use preço de memória, não repita a leitura anterior.
Um relatório inventado é pior do que relatório nenhum, porque parece verdadeiro.

## Passo 1 — preparar o repositório

```bash
cd /home/user/cartao
git fetch origin claude/moedas-sinais-compra-venda-zhq66i
git checkout claude/moedas-sinais-compra-venda-zhq66i
git pull origin claude/moedas-sinais-compra-venda-zhq66i
rm -rf radar/dados && mkdir -p radar/dados
python3 radar/testes.py
```

Se os testes falharem, pare e reporte. Motor quebrado não gera sinal.

## Passo 2 — coletar as velas

Os pares estão em `radar/cobertas.txt` (um por linha). São 28.

Para cada par, duas chamadas à ferramenta da Crypto.com:

- `get_candlestick(instrument_name="<PAR>", timeframe="1D")` — atenção: **`1D`
  maiúsculo**. `1d` retorna erro.
- `get_candlestick(instrument_name="<PAR>", timeframe="4h")` — minúsculo.

Dispare 6 a 8 chamadas em paralelo por vez. Depois de cada lote, grave cada
resposta **na íntegra e sem reformatar** em:

- `radar/dados/<PAR>_1d.json`
- `radar/dados/<PAR>_4h.json`

Copie o JSON exatamente como veio (`{"data":[...],...}`). Não reordene, não
arredonde, não remova campos, não recalcule nada. O motor faz a matemática; sua
única função aqui é transportar os números sem tocá-los.

Se um par falhar, tente uma vez mais. Se falhar de novo, siga em frente — o
relatório vai listar a falha de coleta sozinho.

## Passo 3 — rodar o motor

```bash
python3 radar/analisar.py --dir radar/dados --janela <manha|noite> \
  --saida radar/relatorios/$(date +%Y-%m-%d)-<manha|noite>.md
```

Crie `radar/relatorios/` se não existir.

## Passo 4 — entregar

Responda com o conteúdo do relatório, sem enfeitar e sem acrescentar opinião
própria sobre nenhuma moeda. Acrescente apenas, no fim:

1. O que mudou em relação ao relatório anterior em `radar/relatorios/`
   (compare os sinais: quais entraram, quais saíram, quais viraram de lado).
2. Quantos pares falharam na coleta, se houver.

Depois faça commit dos relatórios na branch de trabalho:

```bash
git add radar/relatorios && \
git commit -m "radar: leitura de $(date +%Y-%m-%d) (<manha|noite>)" && \
git push -u origin claude/moedas-sinais-compra-venda-zhq66i
```

Não faça commit de `radar/dados/` — são dados brutos descartáveis.

## O que não fazer

- Não altere `regras.md` nem as constantes de `analisar.py` por conta própria.
  Se um sinal parecer errado, reporte o que viu; quem muda o sistema é o dono.
- Não acrescente moedas que não estejam em `radar/cobertas.txt`.
- Não transforme `NEUTRO` em conselho ("dá para acumular aqui"). Neutro é
  neutro.
- Não amenize o alerta de volume baixo.
