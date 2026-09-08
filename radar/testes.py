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
                  "open": str(100 + i), "high": str(101 + i), "low": str(99 + i),
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

# --- formato CSV compacto ---------------------------------------------------
csv = "\n".join(f"2026-07-{d:02d}T00:00:00Z,10,11,9,10.5,1000" for d in range(1, 20))
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
    fh.write(csv)
    caminho_csv = fh.name
v_csv, p_csv = A.carregar_velas(caminho_csv, "1d")
os.unlink(caminho_csv)
checar_bool("le CSV compacto", len(v_csv) == 19, True)
checar("preco atual do CSV", p_csv, 10.5)

# vela impossivel (fechamento acima da maxima) tem de ser rejeitada
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
    fh.write("2026-07-01T00:00:00Z,10,10.2,9,10.5,1000")
    caminho_ruim = fh.name
try:
    A.carregar_velas(caminho_ruim, "1d")
    rejeitou = False
except ValueError:
    rejeitou = True
os.unlink(caminho_ruim)
checar_bool("rejeita vela inconsistente", rejeitou, True)

# numero errado de colunas tem de ser rejeitado
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
    fh.write("2026-07-01T00:00:00Z,10,11,9,10.5")
    caminho_curto = fh.name
try:
    A.carregar_velas(caminho_curto, "1d")
    rejeitou_curto = False
except ValueError:
    rejeitou_curto = True
os.unlink(caminho_curto)
checar_bool("rejeita linha com colunas faltando", rejeitou_curto, True)

# --- portao de risco/retorno no preco atual ------------------------------------
# Stop e alvo saem do fechamento diario. Se o preco ja correu depois desse
# fechamento, o 2:1 anunciado nao existe mais para quem entra agora.
def _serie_compra(atual):
    """Alta firme + lateralizacao: gera COMPRA limpa (RSI ~68), sem exaustao."""
    import math
    base = [100.0 + i * 1.5 for i in range(26)]
    topo = base[-1]
    base += [topo + 1.5 * math.sin(i * 1.1) - i * 0.15 for i in range(15)]
    velas = [{"t": f"2026-01-{i+1:02d}T00:00:00Z", "o": p, "h": p * 1.012,
              "l": p * 0.988, "c": p, "vusd": 5_000_000} for i, p in enumerate(base)]
    return base, A.indicadores(velas, atual)

_base, _d = _serie_compra(None)
_fech = _base[-1]
_stop = _fech - A.STOP_ATR * _d["atr"]
_alvo = _fech + A.ALVO_RR * (_fech - _stop)

def _sinal_com_preco(atual):
    return A.avaliar("X_USDT", _serie_compra(atual)[1], None, "alta", "noite")

_r = _sinal_com_preco(_fech)
checar_bool("no fechamento o sinal e COMPRA", _r["sinal"] == "COMPRA", True)
checar("R:R no fechamento e 2:1", _r["rr_real"], 2.0, tol=1e-9)

# a 5% do caminho ate o alvo o R:R cai para ~1,73 - ainda acima do minimo
checar_bool("avanco pequeno mantem a COMPRA",
            _sinal_com_preco(_fech + 0.05 * (_alvo - _fech))["sinal"] == "COMPRA", True)
# a 15% do caminho o preco ja correu 0,45 ATR, acima do limite de 0,30 ATR
checar_bool("avanco de 15% bloqueia por perseguicao",
            _sinal_com_preco(_fech + 0.15 * (_alvo - _fech))["sinal"]
            == "SEM ENTRADA (preco ja correu)", True)
checar_bool("preco no alvo vira ALVO JA ALCANCADO",
            _sinal_com_preco(_alvo)["sinal"] == "ALVO JA ALCANCADO", True)
checar_bool("preco acima do alvo tambem",
            _sinal_com_preco(_alvo * 1.02)["sinal"] == "ALVO JA ALCANCADO", True)
checar_bool("preco abaixo do stop vira ABAIXO DO STOP",
            _sinal_com_preco(_stop * 0.98)["sinal"] == "ABAIXO DO STOP", True)
checar_bool("o bloqueio aparece nos motivos",
            any("BLOQUEIO" in m for m in _sinal_com_preco(_alvo)["motivos"]), True)

# --- portao de entrada: os dois lados ---------------------------------------
_atr = _d["atr"]
_risco = _fech - _stop

# limite de cima: 0,30 ATR e exatamente o RR_MINIMO de 1,5:1 reescrito em ATR
checar("ENTRADA_MAX_ATR equivale ao RR_MINIMO", A.ENTRADA_MAX_ATR, 0.30, tol=1e-12)
_no_limite = _sinal_com_preco(_fech + A.ENTRADA_MAX_ATR * _atr)
checar_bool("no limite de perseguicao ainda e COMPRA", _no_limite["sinal"] == "COMPRA", True)
checar("no limite o R:R e exatamente o minimo", _no_limite["rr_real"], A.RR_MINIMO, tol=1e-9)
checar_bool("um passo acima do limite bloqueia",
            _sinal_com_preco(_fech + 1.01 * A.ENTRADA_MAX_ATR * _atr)["sinal"]
            == "SEM ENTRADA (preco ja correu)", True)

# limite de baixo: o R:R sobe quando o preco cai, entao ele nao pode ser o portao
_caiu_40 = _sinal_com_preco(_fech - 0.40 * _risco)
checar_bool("queda de 40% do risco ainda e COMPRA", _caiu_40["sinal"] == "COMPRA", True)
checar_bool("mesmo assim o R:R ja aparece inflado", _caiu_40["rr_real"] > A.ALVO_RR, True)

_caiu_60 = _sinal_com_preco(_fech - 0.60 * _risco)
checar_bool("queda de 60% do risco bloqueia",
            _caiu_60["sinal"] == "SEM ENTRADA (risco ja consumido)", True)
checar_bool("o bloqueio de queda vem COM R:R alto, nao baixo",
            _caiu_60["rr_real"] > 6.0, True)
checar_bool("o motivo explica que o R:R subiu por causa da queda",
            any("porque o preco caiu" in m for m in _caiu_60["motivos"]), True)

# regressao JUP 07/09: -7,4% do fechamento mostrava 9,30:1 e passava como COMPRA
_jup = _sinal_com_preco(_fech - 0.71 * _risco)
checar_bool("caso JUP: R:R acima de 9:1", _jup["rr_real"] > 9.0, True)
checar_bool("caso JUP: agora e bloqueado",
            _jup["sinal"] == "SEM ENTRADA (risco ja consumido)", True)

# a deriva fica registrada para a tabela poder mostrar de onde veio o bloqueio
checar("deriva em ATR e registrada",
       _sinal_com_preco(_fech + 0.5 * _atr)["deriva_atr"], 0.5, tol=1e-9)

print()
if falhas:
    print(f"{len(falhas)} FALHA(S): " + ", ".join(falhas))
    sys.exit(1)
print("todos os testes passaram")
