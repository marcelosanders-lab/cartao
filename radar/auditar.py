"""Marca, sinal a sinal, os defeitos ja medidos do motor. So le; nao muda sinal.

  python3 radar/auditar.py --janela <manha|noite>

Roda o analisar.py do repositorio (sem alteracao) sobre radar/dados, le a
vela do topo de cada CSV e imprime, para cada COMPRA:

  MORTA     vela 4h em formacao sem negocio ou com negocio unico (O=H=L=C):
            o "Agora" repete o fechamento e a deriva 0,00 passa sozinha      P6
  LIQ       volume medio abaixo do piso de liquidez                          P3
  REGIME    so vira COMPRA por causa do +1 do regime do BTC                  P2
  X4H-      cruzamento de baixa no 4h ignorado pelo portao                   P8
  RSI-BORDA RSI a menos de 2 pontos do teto de sobrecompra                   P10
  DER-BORDA deriva colada em um dos limites do portao                        P9

No fim imprime a LISTA DE SOBREVIVENCIA: as COMPRA sem nenhuma marca e com
RSI < 75. Isto NAO e sinal do motor - e o que sobra depois de descontar os
defeitos medidos. O relatorio deve apresentar com esse rotulo, nunca como
"as melhores compras".
"""
import argparse
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import analisar as A  # noqa: E402  (so para ler as constantes)

RSI_SOBREVIVENCIA = 75
BORDA_RSI = 2
BORDA_DERIVA = 0.05


def topo(par, tf):
    caminho = os.path.join(AQUI, "dados", f"{par}_{tf}.csv")
    try:
        return open(caminho).readline().strip().split(",")
    except OSError:
        return None


def rodar_motor(janela):
    """Saida JSON do analisar.py do repositorio sobre radar/dados."""
    bruto = subprocess.run(
        [sys.executable, os.path.join(AQUI, "analisar.py"), "--dir",
         os.path.join(AQUI, "dados"), "--janela", janela, "--json"],
        capture_output=True, text=True, check=True).stdout
    return json.loads(bruto)


def marcar(r):
    """Marcas de defeito medido para um resultado COMPRA do motor."""
    limite_queda = -A.FRACAO_RISCO_CONSUMIDO * A.STOP_ATR
    marcas = []
    t4 = topo(r["par"], "4h")
    # sem negocio (volume zero) ou negocio unico (abertura = maxima =
    # minima = fechamento): o "Agora" e o fechamento, deriva 0,00 exata.
    if t4 and (float(t4[5]) == 0 or len({float(x) for x in t4[1:5]}) == 1):
        marcas.append("MORTA")
    if not r.get("liquidez_ok", True):
        marcas.append("LIQ")
    motivos = r.get("motivos", [])
    if any("regime de alta" in m for m in motivos):
        c = r["score_compra"] - 1
        if not (c >= A.SCORE_COMPRA and c > r["score_venda"]):
            marcas.append("REGIME")
    if any("cruzamento de baixa no 4h" in m for m in motivos):
        marcas.append("X4H-")
    rsi = r.get("rsi") or 0
    if rsi >= A.RSI_SOBRECOMPRA - BORDA_RSI:
        marcas.append("RSI-BORDA")
    der = r.get("deriva_atr")
    if der is not None and (der >= A.ENTRADA_MAX_ATR - BORDA_DERIVA
                            or der <= limite_queda + BORDA_DERIVA):
        marcas.append("DER-BORDA")
    return marcas


def sobrevive(r, marcas):
    return not marcas and (r.get("rsi") or 0) < RSI_SOBREVIVENCIA


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--janela", required=True, choices=["manha", "noite"])
    a = ap.parse_args()
    dados = rodar_motor(a.janela)
    limite_queda = -A.FRACAO_RISCO_CONSUMIDO * A.STOP_ATR
    print(f"regime {dados['regime']}  |  portao de deriva [{limite_queda:+.2f}, "
          f"{A.ENTRADA_MAX_ATR:+.2f}] ATR  |  teto RSI {A.RSI_SOBRECOMPRA}")

    compras, sobreviventes, contagem = [], [], {}
    for r in dados["resultados"]:
        if not r.get("sinal", "").startswith("COMPRA"):
            continue
        marcas = marcar(r)
        for m in marcas:
            contagem[m] = contagem.get(m, 0) + 1
        compras.append((r, marcas))
        if sobrevive(r, marcas):
            sobreviventes.append(r)

    print(f"\n{len(compras)} COMPRA")
    print(f"{'par':12s} {'rsi':>4s} {'deriva':>7s} {'vol/dia':>13s}  marcas")
    for r, marcas in compras:
        der = r.get("deriva_atr")
        print(f"{r['par']:12s} {r.get('rsi', 0):4.0f} {der if der is not None else 0:+7.2f} "
              f"{r.get('vol_usd_medio', 0):13,.0f}  {' '.join(marcas) or '-'}")
    print("\nCONTAGEM: " + (", ".join(f"{k} {v}" for k, v in sorted(contagem.items())) or "nenhuma marca"))

    print(f"\nLISTA DE SOBREVIVENCIA ({len(sobreviventes)} de {len(compras)}) - "
          "NAO e sinal do motor; e o que sobra sem os defeitos medidos:")
    for r in sorted(sobreviventes, key=lambda x: -x.get("vol_usd_medio", 0)):
        print(f"  {r['par']:12s} RSI {r['rsi']:.0f}  deriva {r['deriva_atr']:+.2f} ATR  "
              f"stop {r['stop']:.6g}  R:R {r['rr_real']:.2f}  vol US$ {r['vol_usd_medio']:,.0f}/dia")
    if not sobreviventes:
        print("  nenhuma")


if __name__ == "__main__":
    main()
