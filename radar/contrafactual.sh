#!/usr/bin/env bash
# Roda o motor real e tres copias alteradas sobre as MESMAS velas de radar/dados
# e compara os sinais. As copias vivem num diretorio temporario e sao apagadas
# no fim. Nada no repositorio e alterado.
#
#   bash radar/contrafactual.sh <manha|noite>
#
#   real       analisar.py como esta
#   sem_bonus  regime de alta nao soma ponto de compra (analisar.py:310)
#   baixa      definir_regime() sempre devolve "baixa"
#   rsi85      RSI_SOBRECOMPRA = 85 em vez de 78
set -euo pipefail

JANELA="${1:?uso: bash radar/contrafactual.sh <manha|noite>}"
RAIZ="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cp "$RAIZ/analisar.py" "$TMP/real.py"
cp "$RAIZ/moedas.json" "$TMP/moedas.json"   # o motor le este arquivo ao lado de si

sed 's/pc(1, "BTC em regime de alta")/pc(0, "BTC em regime de alta (SIMULACAO: sem bonus)")/' \
  "$RAIZ/analisar.py" > "$TMP/sem_bonus.py"
sed '/^def definir_regime(/a\    return "baixa"  # SIMULACAO' \
  "$RAIZ/analisar.py" > "$TMP/baixa.py"
sed 's/^RSI_SOBRECOMPRA = 78$/RSI_SOBRECOMPRA = 85  # SIMULACAO/' \
  "$RAIZ/analisar.py" > "$TMP/rsi85.py"

# Se o motor mudou e um sed nao casou, a copia seria igual ao real e o
# contrafactual mentiria dizendo "sem efeito". Pare em vez disso.
for v in sem_bonus baixa rsi85; do
  if ! grep -q SIMULACAO "$TMP/$v.py"; then
    echo "ERRO: o patch '$v' nao casou com analisar.py. Contrafactual invalido." >&2
    exit 1
  fi
done

for v in real sem_bonus baixa rsi85; do
  python3 "$TMP/$v.py" --dir "$RAIZ/dados" --janela "$JANELA" --json > "$TMP/$v.json"
done

python3 - "$TMP" <<'PY'
import json, sys, os
d = sys.argv[1]

def sinais(v):
    bruto = json.load(open(os.path.join(d, v + ".json")))
    itens = bruto["resultados"]
    out = {}
    for x in itens:
        if isinstance(x, dict) and x.get("par") and x.get("sinal"):
            out[x["par"]] = x["sinal"]
    if not out:
        sys.exit(f"ERRO: nao achei sinais no JSON de {v}; chaves: {list(bruto)[:10]}")
    return out

r = sinais("real")
def conta(s, p): return sum(1 for x in s.values() if x.startswith(p))
print(f"{'versao':10s} {'COMPRA':>6s} {'VENDA':>6s} {'PARCIAL':>7s}")
for v in ("real", "sem_bonus", "baixa", "rsi85"):
    s = sinais(v)
    print(f"{v:10s} {conta(s,'COMPRA'):6d} {conta(s,'VENDA'):6d} {conta(s,'REALIZAR'):7d}")
    if v != "real":
        for par in sorted(set(r) | set(s)):
            if r.get(par) != s.get(par):
                print(f"    {par:14s} {r.get(par)!s:34s} -> {s.get(par)}")
PY
