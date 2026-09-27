"""Compara dois relatorios do radar, ou imprime o placar acumulado.

So le arquivos. Nao baixa preco, nao roda o motor, nao escreve nada.

  python3 radar/comparar.py ANTES.md AGORA.md [--excluir PAR,PAR]
      variacao do "Agora" par a par, media por grupo de sinal (pelo sinal
      do relatorio ANTES) e do painel inteiro; stops dos pares que eram
      COMPRA nos dois relatorios (Pergunta 20).

  python3 radar/comparar.py --serie
      le radar/placar.csv e imprime a tabela e a serie composta (so as
      linhas com encadeia=sim).
"""
import argparse
import csv
import os
import statistics as st
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def ler(caminho):
    """{PAR: (sinal, agora, stop)} a partir das tabelas Sinais e Neutros."""
    out, sec = {}, None
    for linha in open(caminho, encoding="utf-8"):
        if linha.startswith("| Par | Sinal"):
            sec = "s"
            continue
        if linha.startswith("| Par | Fech"):
            sec = "n"
            continue
        if not linha.startswith("|"):
            sec = None
            continue
        if sec is None or linha.startswith("|---"):
            continue
        c = [x.strip() for x in linha.strip().strip("|").split("|")]
        if not c[0].endswith("_USDT"):
            continue
        if sec == "s" and len(c) >= 7:
            out[c[0]] = (c[1].replace("**", ""), num(c[3]), num(c[6]))
        elif sec == "n" and len(c) >= 3:
            out[c[0]] = ("NEUTRO", num(c[2]), None)
    return out


def grupo(sinal):
    for g in ("COMPRA", "VENDA", "SEM ENTRADA", "REALIZAR PARCIAL", "NEUTRO"):
        if sinal.startswith(g):
            return g
    return sinal


def comparar(a_path, b_path, excluir):
    a, b = ler(a_path), ler(b_path)
    if not a or not b:
        sys.exit("nenhuma tabela de sinais encontrada em um dos arquivos")
    linhas = []
    for par in sorted(set(a) & set(b)):
        (sa, pa, _), (sb, pb, _) = a[par], b[par]
        if par in excluir or pa is None or pb is None:
            continue
        linhas.append((par, sa, sb, (pb / pa - 1) * 100))
    if not linhas:
        sys.exit("nenhum par em comum com preco nos dois relatorios")

    print(f"{'par':14s} {'antes':34s} -> {'agora':34s} {'var%':>8}")
    for par, sa, sb, v in linhas:
        print(f"{par:14s} {sa:34s} -> {sb:34s} {v:+7.2f}%")

    grupos = {}
    for par, sa, _, v in linhas:
        grupos.setdefault(grupo(sa), []).append((par, v))
    painel = st.mean(v for *_, v in linhas)
    print(f"\nPAINEL n={len(linhas)} media {painel:+.2f}%"
          + (f"  (excluidos: {', '.join(sorted(excluir))})" if excluir else ""))
    for g, vs in sorted(grupos.items()):
        m = st.mean(v for _, v in vs)
        melhor, pior = max(vs, key=lambda x: x[1]), min(vs, key=lambda x: x[1])
        print(f"  {g:18s} n={len(vs):2d} media {m:+6.2f}%  vs painel {m - painel:+.2f}pp"
              f"  melhor {melhor[0]} {melhor[1]:+.2f}%  pior {pior[0]} {pior[1]:+.2f}%")

    stops = []
    for par in sorted(set(a) & set(b)):
        (sa, _, ta), (sb, _, tb) = a[par], b[par]
        if grupo(sa) == "COMPRA" and grupo(sb) == "COMPRA" and ta and tb:
            stops.append((par, ta, tb, (tb / ta - 1) * 100))
    if stops:
        baixou = [s for s in stops if s[3] < 0]
        print(f"\nSTOPS de pares COMPRA nos dois: {len(stops)}, "
              f"rebaixados {len(baixou)} (Pergunta 20)")
        for par, ta, tb, v in stops:
            marca = "  <- desceu" if v < 0 else ""
            print(f"  {par:14s} {ta:>14g} -> {tb:<14g} {v:+6.2f}%{marca}")


def serie():
    caminho = os.path.join(AQUI, "placar.csv")
    linhas = list(csv.DictReader(open(caminho, encoding="utf-8")))
    print(f"{'janela':8s} {'de':10s} {'para':10s} {'painel':>8s} {'compra':>8s} {'dif':>7s} {'n':>3s}")
    cp = cc = 1.0
    for r in linhas:
        p, c = float(r["painel"]), float(r["compra"])
        print(f"{r['janela']:8s} {r['de']:10s} {r['para']:10s} {p:+7.2f}% {c:+7.2f}% "
              f"{c - p:+6.2f} {r['n']:>3s}  {'encadeia' if r['encadeia'] == 'sim' else ''}")
        if r["encadeia"] == "sim":
            cp *= 1 + p / 100
            cc *= 1 + c / 100
    enc = [r for r in linhas if r["encadeia"] == "sim"]
    if enc:
        print(f"\nSERIE COMPOSTA ({len(enc)} janelas, {enc[0]['de']} a {enc[-1]['para']}): "
              f"COMPRA {(cc - 1) * 100:+.2f}%  painel {(cp - 1) * 100:+.2f}%  "
              f"diferenca {((cc - cp) * 100):+.2f}pp")
    v24 = [r for r in linhas if r["janela"] == "24h"]
    if v24:
        ganhou = sum(float(r["compra"]) > float(r["painel"]) for r in v24)
        print(f"JANELAS DE 24H: COMPRA venceu o painel em {ganhou} de {len(v24)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("antes", nargs="?")
    ap.add_argument("agora", nargs="?")
    ap.add_argument("--excluir", default="")
    ap.add_argument("--serie", action="store_true")
    a = ap.parse_args()
    if a.serie:
        serie()
    elif a.antes and a.agora:
        comparar(a.antes, a.agora, {x for x in a.excluir.split(",") if x})
    else:
        ap.error("passe dois relatorios ou --serie")


if __name__ == "__main__":
    main()
