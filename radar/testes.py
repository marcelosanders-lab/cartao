#!/usr/bin/env python3
"""Testes do motor de sinais. Rode antes de confiar em qualquer relatorio:

    python3 radar/testes.py
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analisar as A

falhas = []


def checar(nome, obtido, esperado, tol=1e-6):
    ok = (obtido is not None and abs(obtido - esperado) <= tol)
    print(f"{'ok  ' if ok else 'FALHA'} {nome}: obtido={obtido} esperado={esperado}")
    if not ok:
        falhas.append(nome)


def checar_bool(nome, obtido, esperado):
    ok = obtido == esperado
    print(f"{'ok  ' if ok else 'FALHA'} {nome}: obtido={obtido} esperado={esperado}")
    if not ok:
        falhas.append(nome)


# --- EMA -------------------------------------------------------------------
constante = [10.0] * 30
checar("EMA de serie constante", A.ultimo(A.ema(constante, 9)), 10.0)
checar("EMA semeada na SMA", A.ema([1, 2, 3, 4, 5], 5)[4], 3.0)
checar_bool("EMA sem dados suficientes", A.ema([1, 2], 5), [None, None])

# EMA(3) de 1..5, k=0.5: semente SMA(1,2,3)=2 -> 4*.5+2*.5=3 -> 5*.5+3*.5=4
checar("EMA(3) passo a passo", A.ema([1, 2, 3, 4, 5], 3)[4], 4.0)

# --- RSI (serie classica de Wilder, RSI14 = 70.53) --------------------------
wilder = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42,
          45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28]
# valor conferido com calculo independente da media simples de Wilder
checar("RSI14 de Wilder", A.ultimo(A.rsi(wilder)), 70.4641, tol=0.001)
checar("RSI de serie so de alta", A.ultimo(A.rsi(list(range(1, 40)))), 100.0)
subindo_50 = [float(i) for i in range(1, 51)]
checar("RSI de serie so de queda", A.ultimo(A.rsi(subindo_50[::-1])), 0.0)

# --- MACD ------------------------------------------------------------------
checar("MACD de serie constante", A.macd([10.0] * 60)[2][-1], 0.0)
# rampa perfeitamente linear converge para histograma zero - por isso o teste de
# momento usa uma alta que acelera, que e onde o histograma tem de ficar positivo
checar("MACD de rampa linear converge a zero", A.macd(subindo_50)[2][-1], 0.0, tol=1e-6)
acelerando = [float(i * i) for i in range(1, 51)]
checar_bool("MACD positivo em alta que acelera", A.macd(acelerando)[2][-1] > 0, True)
desacelerando = [float(-(i * i)) for i in range(1, 51)]
checar_bool("MACD negativo em queda que acelera", A.macd(desacelerando)[2][-1] < 0, True)

# --- ATR -------------------------------------------------------------------
n = 30
maximas = [11.0] * n
minimas = [10.0] * n
fechs = [10.5] * n
checar("ATR de faixa constante", A.ultimo(A.atr(maximas, minimas, fechs)), 1.0)

# --- cruzamentos -----------------------------------------------------------
# serie que cai e depois sobe forte: a EMA9 cruza a EMA21 para cima no meio da alta
serie = [100 - i for i in range(40)] + [60 + 4 * i for i in range(15)]
er, el = A.ema(serie, 9), A.ema(serie, 21)
pares = [(a, b) for a, b in zip(er, el) if a is not None and b is not None]
idx = next(i for i in range(1, len(pares))
           if pares[i - 1][0] <= pares[i - 1][1] and pares[i][0] > pares[i][1])
distancia = len(pares) - 1 - idx          # quantas velas atras o cruzamento ocorreu
print(f"  cruzamento de alta se completou {distancia} velas atras")
# janela=N cobre cruzamentos completados ate N-1 velas atras (a vela atual conta como 1)
checar_bool("detecta cruzamento dentro da janela",
            A.cruzou_para_cima(er, el, janela=distancia + 1), True)
checar_bool("ignora cruzamento fora da janela",
            A.cruzou_para_cima(er, el, janela=distancia), False)
checar_bool("nao inventa cruzamento de baixa",
            A.cruzou_para_baixo(er, el, janela=distancia + 5), False)

# alta longa seguida de queda forte: a EMA9 cruza a EMA21 para baixo no fim
serie_baixa = [60 + 4 * i for i in range(40)] + [216 - 5 * i for i in range(1, 13)]
er2, el2 = A.ema(serie_baixa, 9), A.ema(serie_baixa, 21)
pares2 = [(a, b) for a, b in zip(er2, el2) if a is not None and b is not None]
idx2 = next(i for i in range(1, len(pares2))
            if pares2[i - 1][0] >= pares2[i - 1][1] and pares2[i][0] < pares2[i][1])
dist2 = len(pares2) - 1 - idx2
print(f"  cruzamento de baixa se completou {dist2} velas atras")
checar_bool("detecta cruzamento de baixa",
            A.cruzou_para_baixo(er2, el2, janela=dist2 + 1), True)
checar_bool("ignora cruzamento de baixa fora da janela",
            A.cruzou_para_baixo(er2, el2, janela=dist2), False)

# --- descarte da vela em formacao ------------------------------------------
agora = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
hoje = agora.replace(hour=0)
velas = []
for i in range(30, -1, -1):                       # de 30 dias atras ate hoje
    t = hoje - timedelta(days=i)
    velas.append({"timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "open": "10", "high": "11", "low": "9",
                  "close": str(100 + i), "volume": "1", "volume_usd": "1000000"})
velas.reverse()                                    # MCP devolve do mais novo p/ o mais antigo
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    json.dump({"data": velas, "instrument_name": "TESTE_USDT", "timeframe": "1D"}, fh)
    caminho = fh.name
fechadas, preco_atual = A.carregar_velas(caminho, "1d")
os.unlink(caminho)
checar_bool("vela diaria de hoje descartada", fechadas[-1]["t"].startswith(
    (hoje - timedelta(days=1)).strftime("%Y-%m-%d")), True)
checar("preco atual vem da vela em formacao", preco_atual, 100.0)
checar_bool("ordem crescente por tempo", fechadas[0]["t"] < fechadas[-1]["t"], True)

# --- regras ----------------------------------------------------------------
alta = A.indicadores([{"t": f"2026-01-{i:02d}T00:00:00Z", "o": 0, "h": 100 + i * 2 + 1,
                       "l": 100 + i * 2 - 1, "c": 100.0 + i * 2, "vusd": 5_000_000}
                      for i in range(1, 46)], preco_atual=190.0)
baixa = A.indicadores([{"t": f"2026-01-{i:02d}T00:00:00Z", "o": 0, "h": 200 - i * 2 + 1,
                        "l": 200 - i * 2 - 1, "c": 200.0 - i * 2, "vusd": 5_000_000}
                       for i in range(1, 46)], preco_atual=110.0)
v_alta = A.avaliar("TESTE_USDT", alta, None, "alta", "noite")
v_baixa = A.avaliar("TESTE_USDT", baixa, None, "baixa", "noite")
print("  tendencia de alta ->", v_alta["sinal"], v_alta["score_compra"], "/", v_alta["score_venda"])
print("  tendencia de baixa ->", v_baixa["sinal"], v_baixa["score_compra"], "/", v_baixa["score_venda"])
checar_bool("alta forte nao vira COMPRA com RSI esticado",
            v_alta["sinal"] in ("REALIZAR PARCIAL", "NEUTRO"), True)
checar_bool("tendencia de baixa gera VENDA", v_baixa["sinal"] == "VENDA", True)
checar_bool("VENDA traz criterio de reentrada", "reentrada" in v_baixa, True)

# liquidez baixa levanta alerta
magro = A.indicadores([{"t": f"2026-01-{i:02d}T00:00:00Z", "o": 0, "h": 101, "l": 99,
                        "c": 100.0, "vusd": 10} for i in range(1, 46)], preco_atual=100.0)
v_magro = A.avaliar("TESTE_USDT", magro, None, "neutro", "noite")
checar_bool("volume baixo vira alerta", v_magro["liquidez_ok"] is False, True)
checar_bool("alerta aparece nos motivos",
            any("ALERTA" in m for m in v_magro["motivos"]), True)

print()
if falhas:
    print(f"{len(falhas)} FALHA(S): " + ", ".join(falhas))
    sys.exit(1)
print("todos os testes passaram")
