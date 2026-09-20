#!/usr/bin/env python3
"""Valida um diretorio de velas antes de ele virar radar/dados/.

Checa o que a conferencia manual nao alcanca: serie contigua, OHLC coerente,
cobertura completa dos pares e topo igual em todos os arquivos do mesmo prazo.

    python3 radar/validar.py radar/dados.novo
    python3 radar/validar.py radar/dados --topo-1d 2026-09-20T00:00:00Z

Sai com codigo 1 se qualquer arquivo reprovar. Nao corrige nada: so acusa.
"""
import argparse
import datetime as dt
import glob
import os
import sys

PASSO = {"1d": 86400, "4h": 14400}
LINHAS = 50
CAMPOS = 6


def instante(t):
    return dt.datetime.fromisoformat(t.replace("Z", "+00:00"))


def conferir(caminho, tf):
    erros = []
    linhas = [l.rstrip("\n") for l in open(caminho) if l.strip()]
    nome = os.path.basename(caminho)

    if len(linhas) != LINHAS:
        erros.append(f"{nome}: {len(linhas)} linhas, esperado {LINHAS}")
        return erros, None

    marcos = []
    for i, l in enumerate(linhas, 1):
        c = l.split(",")
        if len(c) != CAMPOS:
            erros.append(f"{nome}:{i}: {len(c)} campos, esperado {CAMPOS}")
            continue
        try:
            marco = instante(c[0])
        except ValueError:
            erros.append(f"{nome}:{i}: timestamp invalido {c[0]!r}")
            continue
        try:
            o, h, b, f, v = (float(x) for x in c[1:])
        except ValueError:
            erros.append(f"{nome}:{i}: campo numerico invalido em {l!r}")
            continue
        marcos.append(marco)
        # coerencia OHLC - pega erro de transporte (coluna trocada, digito a mais)
        if h < max(o, f) or b > min(o, f) or h < b:
            erros.append(f"{nome}:{i}: OHLC incoerente o={o} h={h} l={b} c={f}")
        if v < 0:
            erros.append(f"{nome}:{i}: volume negativo {v}")

    if len(marcos) != LINHAS:
        return erros, None

    # serie contigua e do mais novo para o mais antigo
    passo = PASSO[tf]
    for i in range(len(marcos) - 1):
        d = (marcos[i] - marcos[i + 1]).total_seconds()
        if d != passo:
            erros.append(
                f"{nome}: buraco na serie entre {marcos[i+1]:%Y-%m-%dT%H:%M:%SZ} e "
                f"{marcos[i]:%Y-%m-%dT%H:%M:%SZ} ({d/3600:.0f}h, esperado {passo/3600:.0f}h)"
            )

    return erros, marcos[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("diretorio", nargs="?", default="radar/dados.novo")
    p.add_argument("--pares", default="radar/cobertas.txt")
    p.add_argument("--topo-1d", help="timestamp esperado no topo dos arquivos 1d")
    p.add_argument("--topo-4h", help="timestamp esperado no topo dos arquivos 4h")
    a = p.parse_args()

    pares = [l.strip() for l in open(a.pares) if l.strip()]
    erros, topos = [], {"1d": {}, "4h": {}}

    for par in pares:
        for tf in ("1d", "4h"):
            caminho = os.path.join(a.diretorio, f"{par}_{tf}.csv")
            if not os.path.exists(caminho):
                erros.append(f"FALTA {par}_{tf}.csv")
                continue
            e, topo = conferir(caminho, tf)
            erros += e
            if topo:
                topos[tf][par] = topo

    extras = set(os.path.basename(f) for f in glob.glob(os.path.join(a.diretorio, "*.csv")))
    esperados = {f"{p_}_{tf}.csv" for p_ in pares for tf in ("1d", "4h")}
    for x in sorted(extras - esperados):
        erros.append(f"ARQUIVO FORA DA LISTA {x}")

    # o topo tem de ser o mesmo em todos os arquivos do mesmo prazo
    for tf in ("1d", "4h"):
        if not topos[tf]:
            continue
        vistos = {}
        for par, t in topos[tf].items():
            vistos.setdefault(t, []).append(par)
        if len(vistos) > 1:
            for t, ps in sorted(vistos.items()):
                erros.append(
                    f"TOPO {tf} divergente {t:%Y-%m-%dT%H:%M:%SZ}: {len(ps)} pares "
                    f"({', '.join(sorted(ps)[:4])}{'...' if len(ps) > 4 else ''})"
                )
        esperado = getattr(a, f"topo_{tf}")
        if esperado:
            alvo = instante(esperado)
            for par, t in sorted(topos[tf].items()):
                if t != alvo:
                    erros.append(f"TOPO {par}_{tf} = {t:%Y-%m-%dT%H:%M:%SZ}, esperado {esperado}")

    if erros:
        print(f"REPROVADO - {len(erros)} problema(s) em {a.diretorio}:")
        for e in erros:
            print("  " + e)
        sys.exit(1)

    print(f"OK - {len(pares)*2} arquivos, {LINHAS} velas cada, series contiguas, OHLC coerente")
    for tf in ("1d", "4h"):
        if topos[tf]:
            print(f"  topo {tf}: {next(iter(topos[tf].values())):%Y-%m-%dT%H:%M:%SZ}")


if __name__ == "__main__":
    main()
