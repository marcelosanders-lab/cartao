#!/usr/bin/env python3
"""Monta radar/dados.novo/<PAR>_4h.csv a partir da base, inserindo velas que
faltam no meio da serie e anexando as novas no topo. Nunca escreve na base.

    python3 radar/remendar4h.py PAR --faltante "<linha>" --nova "<linha>" ...

Recusa se o resultado nao tiver 50 linhas ou sobrar buraco.
"""
import argparse, datetime as dt, os, sys

PASSO = 14400


def marco(l):
    return dt.datetime.fromisoformat(l.split(",")[0].replace("Z", "+00:00"))


a = argparse.ArgumentParser()
a.add_argument("par")
a.add_argument("--faltante", action="append", default=[])
a.add_argument("--nova", action="append", default=[])
a = a.parse_args()

base = f"radar/dados/{a.par}_4h.csv"
if not os.path.exists(base):
    sys.exit(f"ERRO {a.par}: sem base em {base}")
linhas = [l.rstrip("\n") for l in open(base) if l.strip()]

# 1. descarta a antiga vela em formacao (a do topo) - as novas a substituem
if a.nova:
    linhas = linhas[1:]

# 2. insere as faltantes no lugar certo
for f in a.faltante:
    m = marco(f)
    if any(marco(l) == m for l in linhas):
        continue
    pos = next((i for i, l in enumerate(linhas) if marco(l) < m), len(linhas))
    linhas.insert(pos, f)

# 3. anexa as novas no topo, da mais nova para a mais antiga
linhas = list(a.nova) + linhas
linhas = linhas[:50]

marcos = [marco(l) for l in linhas]
buracos = [
    f"{b:%Y-%m-%dT%H:%M:%SZ}->{x:%Y-%m-%dT%H:%M:%SZ}"
    for x, b in zip(marcos, marcos[1:])
    if (x - b).total_seconds() != PASSO
]
if len(linhas) != 50 or buracos:
    sys.exit(f"ERRO {a.par}: {len(linhas)} linhas, buracos={buracos}")

os.makedirs("radar/dados.novo", exist_ok=True)
with open(f"radar/dados.novo/{a.par}_4h.csv", "w") as fh:
    fh.write("\n".join(linhas) + "\n")
print(f"{a.par}_4h: ok")
