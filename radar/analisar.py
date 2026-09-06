#!/usr/bin/env python3
"""Motor de sinais do radar de cripto.

Le velas OHLCV salvas em disco (formato bruto devolvido pelo MCP da Crypto.com),
calcula os indicadores de forma deterministica e aplica o conjunto de regras
descrito em radar/regras.md. Nenhum numero deste relatorio e estimado.

Uso:
    python3 radar/analisar.py --dir radar/dados --janela noite --saida relatorio.md

Arquivos esperados em --dir:  <PAR>_1d.json  e  <PAR>_4h.json
(ex.: BTC_USDT_1d.json, BTC_USDT_4h.json)
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

# --- parametros do sistema (alterar aqui muda o comportamento de tudo) -------
EMA_RAPIDA = 9
EMA_LENTA = 21
RSI_PERIODO = 14
ATR_PERIODO = 14
MACD_RAPIDA, MACD_LENTA, MACD_SINAL = 12, 26, 9

RSI_SOBRECOMPRA = 78
RSI_EXAUSTAO = 85
RSI_SOBREVENDA = 30
ESTICADO_PCT = 0.15          # 15% acima da EMA21 diaria = preco esticado
CRUZAMENTO_JANELA = 3        # cruzamento vale por N velas de 4h
STOP_ATR = 1.5               # stop = 1.5 x ATR14 diario
ALVO_RR = 2.0                # alvo = 2x o risco
LIQUIDEZ_MINIMA_USD = 50_000 # media diaria de volume em USD na fonte
SCORE_COMPRA = 6
SCORE_VENDA = 5

BRT = timezone(timedelta(hours=-3))


# --- indicadores ------------------------------------------------------------
def ema(valores, periodo):
    """EMA com semente em SMA. Retorna lista alinhada (None ate ter dados)."""
    if len(valores) < periodo:
        return [None] * len(valores)
    saida = [None] * (periodo - 1)
    k = 2.0 / (periodo + 1)
    atual = sum(valores[:periodo]) / periodo
    saida.append(atual)
    for v in valores[periodo:]:
        atual = v * k + atual * (1 - k)
        saida.append(atual)
    return saida


def rsi(fechamentos, periodo=RSI_PERIODO):
    """RSI de Wilder."""
    if len(fechamentos) <= periodo:
        return [None] * len(fechamentos)
    ganhos, perdas = [], []
    for i in range(1, len(fechamentos)):
        d = fechamentos[i] - fechamentos[i - 1]
        ganhos.append(max(d, 0.0))
        perdas.append(max(-d, 0.0))
    saida = [None] * periodo
    mg = sum(ganhos[:periodo]) / periodo
    mp = sum(perdas[:periodo]) / periodo
    saida.append(100.0 if mp == 0 else 100 - 100 / (1 + mg / mp))
    for i in range(periodo, len(ganhos)):
        mg = (mg * (periodo - 1) + ganhos[i]) / periodo
        mp = (mp * (periodo - 1) + perdas[i]) / periodo
        saida.append(100.0 if mp == 0 else 100 - 100 / (1 + mg / mp))
    return saida


def macd(fechamentos):
    """Retorna (linha_macd, linha_sinal, histograma), alinhados aos fechamentos."""
    r = ema(fechamentos, MACD_RAPIDA)
    l = ema(fechamentos, MACD_LENTA)
    linha = [(a - b) if (a is not None and b is not None) else None for a, b in zip(r, l)]
    validos = [v for v in linha if v is not None]
    if len(validos) < MACD_SINAL:
        return linha, [None] * len(linha), [None] * len(linha)
    inicio = len(linha) - len(validos)
    sinal_validos = ema(validos, MACD_SINAL)
    sinal = [None] * inicio + sinal_validos
    hist = [(m - s) if (m is not None and s is not None) else None
            for m, s in zip(linha, sinal)]
    return linha, sinal, hist


def atr(maximas, minimas, fechamentos, periodo=ATR_PERIODO):
    """ATR de Wilder."""
    if len(fechamentos) <= periodo:
        return [None] * len(fechamentos)
    tr = [maximas[0] - minimas[0]]
    for i in range(1, len(fechamentos)):
        tr.append(max(maximas[i] - minimas[i],
                      abs(maximas[i] - fechamentos[i - 1]),
                      abs(minimas[i] - fechamentos[i - 1])))
    saida = [None] * (periodo - 1)
    atual = sum(tr[:periodo]) / periodo
    saida.append(atual)
    for i in range(periodo, len(tr)):
        atual = (atual * (periodo - 1) + tr[i]) / periodo
        saida.append(atual)
    return saida


# --- leitura dos dados ------------------------------------------------------
MINUTOS_TF = {"1d": 1440, "4h": 240}


def carregar_velas(caminho, tf):
    """Le o JSON bruto do MCP e devolve (velas_fechadas, ultimo_preco).

    A vela mais recente devolvida pela corretora quase sempre ainda esta em
    formacao. Ela nunca entra no calculo dos indicadores - sinal calculado sobre
    vela aberta muda sozinho ate o fechamento e nao e reproduzivel. O fechamento
    dessa vela aberta e usado apenas como preco de referencia atual.
    """
    texto = open(caminho).read().strip()
    if not texto:
        raise ValueError(f"{caminho}: arquivo vazio")

    if texto[0] in "{[":
        # JSON bruto do MCP, copiado sem alteracao
        bruto = json.loads(texto)
        dados = bruto.get("data", bruto) if isinstance(bruto, dict) else bruto
        if not isinstance(dados, list) or not dados:
            raise ValueError(f"{caminho}: sem velas")
        velas = [{"t": v["timestamp"], "o": float(v["open"]), "h": float(v["high"]),
                  "l": float(v["low"]), "c": float(v["close"]),
                  "vusd": float(v.get("volume_usd") or 0.0)} for v in dados]
    else:
        # CSV compacto: timestamp,open,high,low,close,volume_usd (uma vela por linha)
        velas = []
        for n, linha in enumerate(texto.splitlines(), 1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            campos = linha.split(",")
            if len(campos) != 6:
                raise ValueError(
                    f"{caminho}: linha {n} tem {len(campos)} campos, esperava 6 "
                    f"(timestamp,open,high,low,close,volume_usd): {linha!r}")
            t, o, h, l, c, vusd = campos
            velas.append({"t": t.strip(), "o": float(o), "h": float(h),
                          "l": float(l), "c": float(c), "vusd": float(vusd)})
        if not velas:
            raise ValueError(f"{caminho}: sem velas")

    # coerencia basica: high tem de ser o maior e low o menor da vela
    for v in velas:
        if not (v["h"] >= max(v["o"], v["c"]) and v["l"] <= min(v["o"], v["c"])):
            raise ValueError(
                f"{caminho}: vela {v['t']} inconsistente "
                f"(o={v['o']} h={v['h']} l={v['l']} c={v['c']}) - erro de transcricao")
    velas.sort(key=lambda x: x["t"])
    preco_atual = velas[-1]["c"]

    duracao = timedelta(minutes=MINUTOS_TF[tf])
    agora = datetime.now(timezone.utc)
    while velas:
        abertura = datetime.fromisoformat(velas[-1]["t"].replace("Z", "+00:00"))
        if abertura + duracao > agora:
            velas.pop()          # vela ainda aberta
        else:
            break
    if not velas:
        raise ValueError(f"{caminho}: nenhuma vela fechada")
    return velas, preco_atual


def ultimo(serie):
    for v in reversed(serie):
        if v is not None:
            return v
    return None


# --- calculo por par --------------------------------------------------------
def indicadores(velas, preco_atual=None):
    c = [v["c"] for v in velas]
    h = [v["h"] for v in velas]
    l = [v["l"] for v in velas]
    e_rap, e_len = ema(c, EMA_RAPIDA), ema(c, EMA_LENTA)
    r = rsi(c)
    _, _, hist = macd(c)
    a = atr(h, l, c)
    hist_validos = [x for x in hist if x is not None]
    return {
        "n_velas": len(velas),
        "ultima_vela_fechada": velas[-1]["t"],
        "fechamento": c[-1],
        "preco_atual": preco_atual if preco_atual is not None else c[-1],
        "ema_rapida": ultimo(e_rap),
        "ema_lenta": ultimo(e_len),
        "ema_rapida_serie": e_rap,
        "ema_lenta_serie": e_len,
        "rsi": ultimo(r),
        "macd_hist": ultimo(hist),
        "macd_hist_ant": hist_validos[-2] if len(hist_validos) >= 2 else None,
        "atr": ultimo(a),
        "vol_usd_medio": sum(v["vusd"] for v in velas[-7:]) / min(7, len(velas)),
    }


def cruzou_para_cima(e_rap, e_len, janela=CRUZAMENTO_JANELA):
    """True se a EMA rapida cruzou acima da lenta nas ultimas `janela` velas."""
    pares = [(a, b) for a, b in zip(e_rap, e_len) if a is not None and b is not None]
    if len(pares) < janela + 1:
        return False
    recorte = pares[-(janela + 1):]
    for i in range(1, len(recorte)):
        if recorte[i - 1][0] <= recorte[i - 1][1] and recorte[i][0] > recorte[i][1]:
            return True
    return False


def cruzou_para_baixo(e_rap, e_len, janela=CRUZAMENTO_JANELA):
    pares = [(a, b) for a, b in zip(e_rap, e_len) if a is not None and b is not None]
    if len(pares) < janela + 1:
        return False
    recorte = pares[-(janela + 1):]
    for i in range(1, len(recorte)):
        if recorte[i - 1][0] >= recorte[i - 1][1] and recorte[i][0] < recorte[i][1]:
            return True
    return False


# --- regras -----------------------------------------------------------------
def avaliar(par, d1, h4, regime_btc, janela):
    """Aplica as regras e devolve o veredito do par. Ver radar/regras.md."""
    compra, venda, motivos = 0, 0, []

    def pc(pontos, texto):
        nonlocal compra
        compra += pontos
        motivos.append(f"+{pontos} {texto}")

    def pv(pontos, texto):
        nonlocal venda
        venda += pontos
        motivos.append(f"-{pontos} {texto}")

    preco, ema21 = d1["fechamento"], d1["ema_lenta"]
    if ema21 is None or d1["rsi"] is None:
        return {"par": par, "sinal": "DADOS INSUFICIENTES", "motivos": ["historico curto demais"]}

    # tendencia diaria
    if preco > ema21:
        pc(2, "preco diario acima da EMA21")
    else:
        pv(2, "preco diario abaixo da EMA21")
    if d1["ema_rapida"] is not None:
        if d1["ema_rapida"] > ema21:
            pc(2, "EMA9 diaria acima da EMA21")
        else:
            pv(2, "EMA9 diaria abaixo da EMA21")

    # momento diario
    if d1["macd_hist"] is not None:
        if d1["macd_hist"] > 0:
            pc(1, "histograma MACD diario positivo")
        else:
            pv(1, "histograma MACD diario negativo")
        if d1["macd_hist_ant"] is not None:
            if d1["macd_hist"] > d1["macd_hist_ant"]:
                pc(1, "MACD diario acelerando")
            else:
                pv(1, "MACD diario perdendo forca")

    # gatilho de 4h
    gatilho_4h_alta = False
    if h4:
        if cruzou_para_cima(h4["ema_rapida_serie"], h4["ema_lenta_serie"]):
            pc(2, f"cruzamento de alta no 4h nas ultimas {CRUZAMENTO_JANELA} velas")
            gatilho_4h_alta = True
        if cruzou_para_baixo(h4["ema_rapida_serie"], h4["ema_lenta_serie"]):
            pv(2, f"cruzamento de baixa no 4h nas ultimas {CRUZAMENTO_JANELA} velas")

    # RSI
    r = d1["rsi"]
    if 45 <= r <= 68:
        pc(1, f"RSI diario em zona de tendencia ({r:.0f})")
    if r > RSI_SOBRECOMPRA:
        pv(2, f"RSI diario sobrecomprado ({r:.0f}) - nao perseguir")
    if r < RSI_SOBREVENDA:
        motivos.append(f"nota: RSI diario {r:.0f} (sobrevendido, nao e sinal de compra isolado)")

    # preco esticado
    if preco > ema21 * (1 + ESTICADO_PCT):
        pv(1, f"preco {100*(preco/ema21-1):.0f}% acima da EMA21 (esticado)")

    # regime de mercado
    if regime_btc == "alta" and par != "BTC_USDT":
        pc(1, "BTC em regime de alta")
    elif regime_btc == "baixa" and par != "BTC_USDT":
        pv(2, "BTC em regime de baixa (risco sistemico para alts)")

    # confiabilidade da fonte
    liquidez_ok = d1["vol_usd_medio"] >= LIQUIDEZ_MINIMA_USD
    if not liquidez_ok:
        motivos.append(
            f"ALERTA: volume medio de US$ {d1['vol_usd_medio']:,.0f}/dia na fonte - "
            "preco pouco confiavel, conferir na corretora onde voce opera")

    # decisao
    if r >= RSI_EXAUSTAO:
        sinal = "REALIZAR PARCIAL"
    elif compra >= SCORE_COMPRA and compra > venda and r < RSI_SOBRECOMPRA:
        sinal = "COMPRA"
    elif venda >= SCORE_VENDA and venda > compra:
        sinal = "VENDA"
    else:
        sinal = "NEUTRO"

    # As 11h a vela diaria fechada e a mesma da leitura das 22h. So marca
    # "gatilho 4h" o sinal que de fato veio de um cruzamento no prazo curto -
    # o resto e a mesma tendencia diaria de ontem, sem novidade.
    if janela == "manha" and sinal == "COMPRA" and gatilho_4h_alta:
        sinal = "COMPRA (gatilho 4h)"

    res = {
        "par": par, "sinal": sinal, "preco": preco,
        "preco_atual": d1.get("preco_atual", preco),
        "score_compra": compra, "score_venda": venda,
        "rsi": r, "ema21": ema21, "atr": d1["atr"],
        "vol_usd_medio": d1["vol_usd_medio"], "liquidez_ok": liquidez_ok,
        "ultima_vela_1d": d1["ultima_vela_fechada"],
        "ultima_vela_4h": h4["ultima_vela_fechada"] if h4 else None,
        "motivos": motivos,
    }
    if d1["atr"]:
        if sinal.startswith("COMPRA"):
            stop = preco - STOP_ATR * d1["atr"]
            res["stop"] = stop
            res["alvo"] = preco + ALVO_RR * (preco - stop)
            res["invalidacao"] = f"fechamento diario abaixo de {stop:.8g}"
        elif sinal in ("VENDA", "REALIZAR PARCIAL"):
            res["reentrada"] = f"reavaliar apenas com fechamento diario acima de {ema21:.8g}"
    return res


def definir_regime(d1_btc):
    if not d1_btc or d1_btc["ema_lenta"] is None:
        return "indefinido"
    if d1_btc["fechamento"] > d1_btc["ema_lenta"] and (d1_btc["ema_rapida"] or 0) > d1_btc["ema_lenta"]:
        return "alta"
    if d1_btc["fechamento"] < d1_btc["ema_lenta"]:
        return "baixa"
    return "neutro"


# --- relatorio --------------------------------------------------------------
def formatar(n, casas=8):
    if n is None:
        return "-"
    return f"{n:.{casas}g}"


def montar_relatorio(resultados, regime, janela, fora_da_fonte, nao_coletadas, sem_4h):
    agora = datetime.now(BRT).strftime("%d/%m/%Y %H:%M")
    titulo = ("Leitura das 22h - a vela diaria acabou de fechar (21h de Brasilia)"
              if janela == "noite" else
              "Leitura das 11h - a vela diaria fechada e a MESMA de ontem as 22h; "
              "so o grafico de 4h mudou")
    ordem = {"COMPRA": 0, "COMPRA (gatilho 4h)": 1,
             "REALIZAR PARCIAL": 2, "VENDA": 3, "NEUTRO": 4, "DADOS INSUFICIENTES": 5}
    resultados = sorted(resultados, key=lambda x: (ordem.get(x["sinal"], 9), -x.get("score_compra", 0)))

    L = [f"# Radar de cripto - {agora} (horario de Brasilia)", "",
         f"**{titulo}**", "",
         f"Regime do BTC: **{regime.upper()}**  |  Fonte de precos: Crypto.com Exchange", ""]

    avaliados = [r for r in resultados if r["sinal"] != "DADOS INSUFICIENTES"]
    compras = [r for r in avaliados if r["sinal"].startswith("COMPRA")]
    if avaliados and len(compras) / len(avaliados) >= 0.6:
        L += [f"> **Atencao: {len(compras)} de {len(avaliados)} pares deram COMPRA.** "
              "Quando quase tudo dispara junto, o radar nao esta escolhendo moeda - "
              "esta so dizendo que o mercado inteiro esta acima da media. "
              "Isso e leitura de regime, nao selecao. Comprar os 20 e comprar o "
              "mercado com 20 taxas; se for operar, escolha por criterio proprio "
              "(liquidez, conviccao, tamanho de posicao) e nao pela lista inteira.", ""]

    acoes = [r for r in resultados if r["sinal"] not in ("NEUTRO", "DADOS INSUFICIENTES")]
    if acoes:
        L += ["## Sinais", "",
              "| Par | Sinal | Fech. 1d | Agora | RSI(1d) | Stop | Alvo | Score C/V |",
              "|---|---|---|---|---|---|---|---|"]
        for r in acoes:
            L.append(f"| {r['par']} | **{r['sinal']}** | {formatar(r['preco'])} | "
                     f"{formatar(r['preco_atual'])} | "
                     f"{r['rsi']:.0f} | {formatar(r.get('stop'))} | {formatar(r.get('alvo'))} | "
                     f"{r.get('score_compra','-')}/{r.get('score_venda','-')} |")
        L.append("")
        L += ["### Por que", ""]
        for r in acoes:
            L.append(f"**{r['par']} - {r['sinal']}**")
            for m in r["motivos"]:
                L.append(f"- {m}")
            if r.get("invalidacao"):
                L.append(f"- Invalidacao: {r['invalidacao']}")
            if r.get("reentrada"):
                L.append(f"- Reentrada: {r['reentrada']}")
            L.append("")
    else:
        L += ["## Sinais", "", "Nenhum par cruzou o limiar de sinal nesta leitura.", ""]

    neutros = [r for r in resultados if r["sinal"] == "NEUTRO"]
    if neutros:
        L += ["## Neutros (sem acao)", "",
              "| Par | Fech. 1d | Agora | RSI(1d) | Score C/V |", "|---|---|---|---|---|"]
        for r in neutros:
            L.append(f"| {r['par']} | {formatar(r['preco'])} | {formatar(r['preco_atual'])} | {r['rsi']:.0f} | "
                     f"{r['score_compra']}/{r['score_venda']} |")
        L.append("")

    frageis = [r for r in resultados if r.get("liquidez_ok") is False]
    if frageis:
        L += ["## Precos pouco confiaveis na fonte", "",
              f"Volume medio abaixo de US$ {LIQUIDEZ_MINIMA_USD:,}/dia na Crypto.com. "
              "O sinal desses pares vale menos - confira o grafico na corretora onde voce opera.", ""]
        for r in frageis:
            L.append(f"- {r['par']}: US$ {r['vol_usd_medio']:,.0f}/dia")
        L.append("")

    if nao_coletadas:
        L += ["## FALHA DE COLETA", "",
              "Estes pares existem na fonte mas os dados nao chegaram nesta rodada. "
              "Nenhum sinal foi gerado para eles - **nao assuma que estao neutros**:", "",
              "- " + ", ".join(nao_coletadas), ""]
    if sem_4h:
        L += ["## Sem grafico de 4h", "",
              "Avaliados so pelo diario, sem gatilho de curto prazo: "
              + ", ".join(sem_4h), ""]
    if fora_da_fonte:
        L += ["## Moedas fora do radar", "",
              "Nao sao negociadas na Crypto.com, entao este radar nao consegue le-las. "
              "Continuam sem qualquer sinal:", "",
              "- " + ", ".join(fora_da_fonte), ""]

    L += ["---", "",
          "Sinais mecanicos de seguimento de tendencia, gerados por regra fixa "
          "(radar/regras.md), sem backtest. Nao sao recomendacao de investimento.", ""]
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="radar/dados", help="pasta com os JSON de velas")
    p.add_argument("--janela", choices=["manha", "noite"], default="noite")
    p.add_argument("--saida", help="arquivo markdown de saida (padrao: stdout)")
    p.add_argument("--json", action="store_true", help="imprime o resultado bruto em JSON")
    args = p.parse_args()

    universo = json.load(open(os.path.join(os.path.dirname(__file__), "moedas.json")))
    pares = [c["par"] for c in universo["cobertas"]]
    ausentes_config = [c["tv"] for c in universo["sem_cobertura"]]

    d1, h4 = {}, {}
    sem_arquivo, sem_4h = [], []
    for par in pares:
        def achar(sufixo):
            for ext in (".json", ".csv"):
                caminho = os.path.join(args.dir, f"{par}_{sufixo}{ext}")
                if os.path.exists(caminho):
                    return caminho
            return None

        f1, f4 = achar("1d"), achar("4h")
        if not f1:
            sem_arquivo.append(par)
            continue
        velas1, preco_1d = carregar_velas(f1, "1d")
        preco_atual = preco_1d          # fechamento da vela diaria em formacao
        if f4:
            velas4, preco_4h = carregar_velas(f4, "4h")
            h4[par] = indicadores(velas4)
            preco_atual = preco_4h      # o 4h e mais recente, entao tem prioridade
        else:
            sem_4h.append(par)
        d1[par] = indicadores(velas1, preco_atual)

    if not d1:
        sys.exit("Nenhum arquivo de velas encontrado em " + args.dir +
                 ". Colete os dados antes de rodar o motor - nao invente precos.")

    regime = definir_regime(d1.get("BTC_USDT"))
    resultados = [avaliar(par, d1[par], h4.get(par), regime, args.janela) for par in d1]

    if args.json:
        print(json.dumps({"regime": regime, "resultados": resultados}, indent=2, default=str))
        return

    texto = montar_relatorio(resultados, regime, args.janela,
                             ausentes_config, sem_arquivo, sem_4h)
    if args.saida:
        with open(args.saida, "w") as fh:
            fh.write(texto)
        print(f"relatorio gravado em {args.saida}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
