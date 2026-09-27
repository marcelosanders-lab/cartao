"""Velas FECHADAS que a fonte devolveu diferentes entre duas coletas.

  python3 radar/fonte.py radar/dados.antigo radar/dados

Compara, par a par e prazo a prazo, as linhas com o mesmo timestamp. Ignora a
vela que estava em formacao na base antiga (primeira linha): ela mudar e
normal. Qualquer outra diferenca e a fonte reescrevendo vela fechada
(Pergunta 15). Rode ANTES de apagar radar/dados.antigo.
"""
import glob
import os
import sys

CAMPOS = ["open", "high", "low", "close", "volume"]


def ler(caminho):
    linhas = [l.strip().split(",") for l in open(caminho) if l.strip()]
    return linhas[0][0] if linhas else None, {l[0]: l[1:] for l in linhas}


def main():
    if len(sys.argv) != 3:
        sys.exit("uso: python3 radar/fonte.py <dir antigo> <dir novo>")
    antigo, novo = sys.argv[1:]
    total, pares = 0, set()
    for pa in sorted(glob.glob(os.path.join(antigo, "*.csv"))):
        pn = os.path.join(novo, os.path.basename(pa))
        if not os.path.exists(pn):
            continue
        topo_antigo, a = ler(pa)
        _, n = ler(pn)
        for ts in sorted(set(a) & set(n)):
            if ts == topo_antigo:
                continue
            for campo, va, vn in zip(CAMPOS, a[ts], n[ts]):
                try:
                    igual = float(va) == float(vn)
                except ValueError:
                    igual = va == vn
                if not igual:
                    total += 1
                    pares.add(os.path.basename(pa))
                    print(f"{os.path.basename(pa):18s} {ts}  {campo:6s} {va} -> {vn}")
    print(f"\n{total} campos divergentes em {len(pares)} arquivos"
          if total else "nenhuma vela fechada divergente")


if __name__ == "__main__":
    main()
