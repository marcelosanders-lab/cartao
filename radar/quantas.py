"""Quantas velas passar ao helper v1/v4 nesta execucao, e os topos esperados.

  python3 radar/quantas.py

Le o topo da base (radar/dados/BTC_USDT_<tf>.csv, primeira linha) e o relogio
UTC. Velas a passar = a que estava em formacao na base (agora fechada) + as
que fecharam depois + a nova em formacao = (topo_agora - topo_base)/passo + 1.

Substitui a tabela fixa "22h = 2/4, 11h = 1/4", que erra sempre que houve
leitura extra ou leitura pulada. O numero e o esperado; quem manda e o helper,
que recusa o arquivo se a serie nao encostar.
"""
import os
import sys
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
PASSO = {"1d": 86400, "4h": 14400}


def topo_base(tf):
    caminho = os.path.join(AQUI, "dados", f"BTC_USDT_{tf}.csv")
    if not os.path.exists(caminho):
        return None
    primeira = open(caminho).readline().split(",")[0]
    return datetime.strptime(primeira, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main():
    agora = datetime.now(timezone.utc)
    print(f"agora UTC: {agora:%Y-%m-%dT%H:%M:%SZ}")
    for tf, passo in PASSO.items():
        ts = int(agora.timestamp()) // passo * passo
        topo = datetime.fromtimestamp(ts, timezone.utc)
        base = topo_base(tf)
        if base is None:
            print(f"{tf}: SEM BASE -> caminho B (50 velas); topo esperado {topo:%Y-%m-%dT%H:%M:%SZ}")
            continue
        n = int((topo - base).total_seconds()) // passo + 1
        aviso = ""
        if n > 49:
            aviso = "  -> base velha demais, caminho B"
        elif n == 1:
            aviso = "  (so a vela em formacao mudou)"
        print(f"{tf}: base {base:%Y-%m-%dT%H:%M:%SZ}  topo esperado {topo:%Y-%m-%dT%H:%M:%SZ}"
              f"  velas a passar: {n}{aviso}")
    print("Perto da virada de vela (menos de 5 min), confira o topo na resposta da fonte.")


if __name__ == "__main__":
    sys.exit(main())
