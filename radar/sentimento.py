"""Sentimento do mercado pela CoinMarketCap: medo e ganancia + metricas globais.

  python3 radar/sentimento.py

Tenta, nesta ordem:
  1. API oficial (pro-api.coinmarketcap.com), se CMC_PRO_API_KEY estiver no
     ambiente;
  2. a API publica que o proprio site coinmarketcap.com/pt-br usa
     (api.coinmarketcap.com/data-api).

Acrescenta UMA linha em radar/sentimento.csv por execucao - com os numeros, ou
com fonte=INDISPONIVEL e o motivo. Numero fora da faixa ou campo ausente e
tratado como falha: nada e gravado como se fosse dado.

Nao altera sinal nenhum. O motor (analisar.py) nao le este arquivo; o painel so
mostra. Se o indice deve pesar na decisao, e em que direcao, e a Pergunta 22.

Saida: 0 = medo e ganancia coletado; 2 = indisponivel (motivo impresso).
"""
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, "sentimento.csv")
CAMPOS = ["coletado_utc", "fonte", "fg_valor", "fg_classe", "fg_atualizado",
          "btc_dom", "eth_dom", "mcap_usd", "mcap_var24h", "vol24h_usd", "motivo"]
UA = {"User-Agent": "radar-cripto/1.0", "Accept": "application/json"}


def baixar(url, cab=None):
    req = urllib.request.Request(url, headers={**UA, **(cab or {})})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def num(x, lo=None, hi=None, nome="valor"):
    v = float(x)
    if (lo is not None and v < lo) or (hi is not None and v > hi):
        raise ValueError(f"{nome}={v} fora da faixa [{lo}, {hi}]")
    return v


# ------------------------------ parsers ------------------------------
# Cada parser devolve dict com as chaves de CAMPOS ou levanta erro. Campo
# ausente = KeyError = falha, nunca zero.

def fg_pro(j):
    d = j["data"]
    return {"fg_valor": int(num(d["value"], 0, 100, "medo e ganancia")),
            "fg_classe": str(d["value_classification"]),
            "fg_atualizado": str(d.get("update_time", ""))}


def fg_publica(j):
    d = j["data"]
    agora = d["historicalValues"]["now"]
    return {"fg_valor": int(num(agora["score"], 0, 100, "medo e ganancia")),
            "fg_classe": str(agora["name"]),
            "fg_atualizado": str(agora.get("timestamp", ""))}


def global_(j):
    d = j["data"]
    q = d["quote"]["USD"]
    return {"btc_dom": round(num(d["btc_dominance"], 0, 100, "dominancia BTC"), 2),
            "eth_dom": round(num(d["eth_dominance"], 0, 100, "dominancia ETH"), 2),
            "mcap_usd": round(num(q["total_market_cap"], 1e9, None, "valor de mercado")),
            "mcap_var24h": round(float(q.get("total_market_cap_yesterday_percentage_change", "nan")), 2),
            "vol24h_usd": round(num(q["total_volume_24h"], 0, None, "volume 24h"))}


def global_publica(j):
    d = j["data"]
    q = d["quotes"][0] if isinstance(d.get("quotes"), list) else d["quote"]["USD"]
    return {"btc_dom": round(num(d["btcDominance"], 0, 100, "dominancia BTC"), 2),
            "eth_dom": round(num(d["ethDominance"], 0, 100, "dominancia ETH"), 2),
            "mcap_usd": round(num(q["totalMarketCap"], 1e9, None, "valor de mercado")),
            "mcap_var24h": round(float(q.get("totalMarketCapYesterdayPercentageChange", "nan")), 2),
            "vol24h_usd": round(num(q["totalVolume24H"], 0, None, "volume 24h"))}


# ------------------------------ coleta ------------------------------

def tentativas():
    chave = os.environ.get("CMC_PRO_API_KEY", "").strip()
    fim = int(datetime.now(timezone.utc).timestamp())
    ini = fim - 3 * 86400
    t = []
    if chave:
        cab = {"X-CMC_PRO_API_KEY": chave}
        t.append(("cmc-api-oficial",
                  ("https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest", cab, fg_pro),
                  ("https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest", cab, global_)))
    t.append(("cmc-site-publico",
              (f"https://api.coinmarketcap.com/data-api/v3/fear-greed/chart?start={ini}&end={fim}",
               None, fg_publica),
              ("https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/latest",
               None, global_publica)))
    return t


def main():
    linha = {c: "" for c in CAMPOS}
    linha["coletado_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    falhas = []
    for fonte, (u_fg, cab_fg, p_fg), (u_gl, cab_gl, p_gl) in tentativas():
        try:
            linha.update(p_fg(baixar(u_fg, cab_fg)))
        except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError,
                IndexError, json.JSONDecodeError) as ex:
            falhas.append(f"{fonte} medo e ganancia: {type(ex).__name__}: {ex}")
            continue
        linha["fonte"] = fonte
        try:
            linha.update(p_gl(baixar(u_gl, cab_gl)))
        except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError,
                IndexError, json.JSONDecodeError) as ex:
            linha["motivo"] = f"metricas globais indisponiveis: {type(ex).__name__}: {ex}"[:300]
        break
    else:
        linha["fonte"] = "INDISPONIVEL"
        linha["motivo"] = " | ".join(falhas)[:600] or "nenhuma fonte tentada"

    novo = not os.path.exists(ARQ)
    with open(ARQ, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        if novo:
            w.writeheader()
        w.writerow(linha)

    if linha["fonte"] == "INDISPONIVEL":
        print(f"INDISPONIVEL: {linha['motivo']}")
        return 2
    brt = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m %H:%M")
    print(f"{brt} BRT  fonte {linha['fonte']}")
    print(f"  medo e ganancia: {linha['fg_valor']} ({linha['fg_classe']})  atualizado {linha['fg_atualizado']}")
    if linha["btc_dom"] != "":
        print(f"  dominancia BTC {linha['btc_dom']}%  ETH {linha['eth_dom']}%")
        print(f"  valor de mercado US$ {linha['mcap_usd']:,}  ({linha['mcap_var24h']:+}% em 24h)"
              f"  volume 24h US$ {linha['vol24h_usd']:,}")
    if linha["motivo"]:
        print(f"  aviso: {linha['motivo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
