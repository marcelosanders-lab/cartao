"""
Monitor BTC/ETH/SOL/LINK e envia relatório diário às 21h via Gmail.
Também envia alerta imediato se Fear & Greed entrar em Medo Extremo (≤ 25).

Uso:
  GMAIL_USER=seu@gmail.com GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx" python monitor.py

Opcional:
  ALERT_RECIPIENT=outro@gmail.com   (padrão: mesmo que GMAIL_USER)
  HORARIO_RELATORIO=21              (padrão: 21 = 21:00 horário local)
  INTERVALO_MIN=30                  (padrão: 30 min entre verificações)
"""

import asyncio
import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx

FEAR_GREED_URL = "https://api.alternative.me/fng/"
COINGECKO_URL  = "https://api.coingecko.com/api/v3/simple/price"

GMAIL_USER      = os.environ["GMAIL_USER"]
GMAIL_APP_PASS  = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT       = os.environ.get("ALERT_RECIPIENT") or GMAIL_USER
HORARIO         = int(os.environ.get("HORARIO_RELATORIO", "21"))
INTERVALO_MIN   = int(os.environ.get("INTERVALO_MIN", "30"))

MOEDAS = ["bitcoin", "ethereum", "solana", "chainlink"]
SIMBOLOS = {"bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "chainlink": "LINK"}

# Evita enviar alerta de medo extremo repetido
_ultimo_alerta_fg: int | None = None
# Evita enviar relatório diário mais de uma vez por hora
_ultimo_relatorio_hora: int | None = None


async def fetch_data() -> dict:
    async with httpx.AsyncClient(timeout=15) as client:
        fg_raw = (await client.get(FEAR_GREED_URL, params={"limit": 1})).json()["data"][0]
        btc_raw = (await client.get(
            COINGECKO_URL,
            params={
                "ids": ",".join(MOEDAS),
                "vs_currencies": "usd,brl",
                "include_24hr_change": "true",
                "include_24hr_vol": "true",
            },
        )).json()
    return {"fg": fg_raw, "precos": btc_raw}


def classify_fg(v: int) -> str:
    if v <= 25: return "Medo Extremo"
    if v <= 45: return "Medo"
    if v <= 55: return "Neutro"
    if v <= 75: return "Ganância"
    return "Ganância Extrema"


def signal(fg: int, btc_usd: float) -> str:
    if fg <= 25 and btc_usd <= 105000:
        return "🟢 COMPRA"
    if fg >= 75:
        return "🔴 ATENÇÃO — Realizar lucros"
    return "🟡 NEUTRO"


def send_email(subject: str, html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = RECIPIENT
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASS)
        smtp.sendmail(GMAIL_USER, RECIPIENT, msg.as_string())


def build_relatorio(d: dict, ts: str) -> tuple[str, str]:
    fg_val  = int(d["fg"]["value"])
    fg_lbl  = d["fg"]["value_classification"]
    fg_cls  = classify_fg(fg_val)
    precos  = d["precos"]
    btc_usd = precos["bitcoin"]["usd"]
    sinal   = signal(fg_val, btc_usd)

    rows = ""
    for coin in MOEDAS:
        sym    = SIMBOLOS[coin]
        usd    = precos[coin]["usd"]
        brl    = precos[coin]["brl"]
        chg    = precos[coin]["usd_24h_change"]
        icon   = "▲" if chg >= 0 else "▼"
        color  = "#22c55e" if chg >= 0 else "#ef4444"
        rows += f"""
        <tr>
          <td style="padding:8px;font-weight:800;color:#e5e5e5">{sym}</td>
          <td style="padding:8px;color:#e5e5e5">$ {usd:,.2f}</td>
          <td style="padding:8px;color:#aaa">R$ {brl:,.2f}</td>
          <td style="padding:8px;color:{color}">{icon} {chg:+.2f}%</td>
        </tr>"""

    fg_color = "#ef4444" if fg_val <= 25 else "#f59e0b" if fg_val <= 45 else "#22c55e" if fg_val >= 75 else "#aaa"
    sinal_color = "#22c55e" if "COMPRA" in sinal else "#ef4444" if "ATENÇÃO" in sinal else "#f59e0b"

    html = f"""
<div style="font-family:monospace;max-width:560px;padding:24px;
            background:#0f0f0f;color:#e5e5e5;border-radius:10px;
            border:1px solid #2a2a2a;">
  <h2 style="color:#e5e5e5;margin:0 0 4px">📊 Relatório Cripto — 21h</h2>
  <p style="color:#666;font-size:11px;margin-bottom:16px">{ts}</p>

  <div style="background:#1a1a1a;padding:14px;border-radius:8px;margin-bottom:16px;">
    <div style="font-size:11px;color:#666;margin-bottom:4px">SINAL DO DIA</div>
    <div style="font-size:20px;font-weight:800;color:{sinal_color}">{sinal}</div>
  </div>

  <div style="background:#1a1a1a;padding:14px;border-radius:8px;margin-bottom:16px;">
    <div style="font-size:11px;color:#666;margin-bottom:6px">FEAR &amp; GREED INDEX</div>
    <span style="font-size:28px;font-weight:800;color:{fg_color}">{fg_val}</span>
    <span style="color:#666;font-size:13px;margin-left:8px">{fg_lbl} ({fg_cls})</span>
  </div>

  <table style="width:100%;border-collapse:collapse;background:#1a1a1a;border-radius:8px;overflow:hidden;">
    <tr style="background:#222;">
      <th style="padding:8px;text-align:left;color:#666;font-size:10px">MOEDA</th>
      <th style="padding:8px;text-align:left;color:#666;font-size:10px">USD</th>
      <th style="padding:8px;text-align:left;color:#666;font-size:10px">BRL</th>
      <th style="padding:8px;text-align:left;color:#666;font-size:10px">24h</th>
    </tr>
    {rows}
  </table>

  <div style="margin-top:14px;padding:12px;background:#1a1a1a;border-radius:8px;font-size:11px;color:#666;">
    Gatilhos de venda: ETH $3.000 → 20% | F&amp;G &gt; 75 → 20% | F&amp;G &gt; 85 → 40% | F&amp;G &gt; 90 → resto
  </div>
  <p style="font-size:10px;color:#444;margin-top:12px;">⚠️ Não é aconselhamento financeiro.</p>
</div>"""

    subject = f"📊 Relatório 21h — BTC ${btc_usd:,.0f} | F&G {fg_val} ({fg_cls}) | {sinal}"
    return subject, html


def build_alerta_fg(d: dict, ts: str) -> tuple[str, str]:
    fg_val  = int(d["fg"]["value"])
    fg_lbl  = d["fg"]["value_classification"]
    precos  = d["precos"]
    btc_usd = precos["bitcoin"]["usd"]
    btc_brl = precos["bitcoin"]["brl"]
    chg     = precos["bitcoin"]["usd_24h_change"]
    buy     = btc_usd <= 105000
    color   = "#22c55e" if buy else "#f59e0b"
    sinal   = "🟢 COMPRA CONFIRMADA" if buy else "⚠️ MEDO EXTREMO (preço > $105k)"

    html = f"""
<div style="font-family:monospace;max-width:520px;padding:24px;
            border:2px solid {color};border-radius:10px;background:#0f0f0f;color:#e5e5e5;">
  <h2 style="color:{color};margin:0 0 4px">🚨 ALERTA — {sinal}</h2>
  <p style="color:#666;font-size:11px;margin-bottom:16px">{ts}</p>
  <p>Fear &amp; Greed: <strong style="color:{color};font-size:1.6em">{fg_val}/100</strong>
     — {fg_lbl}</p>
  <p>BTC: <strong>$ {btc_usd:,.2f}</strong> | R$ {btc_brl:,.2f}
     | {'▲' if chg>=0 else '▼'} {chg:+.2f}%</p>
  <p style="font-size:10px;color:#444;margin-top:12px">⚠️ Não é aconselhamento financeiro.</p>
</div>"""

    subject = f"🚨 ALERTA BTC — F&G {fg_val} Medo Extremo | ${btc_usd:,.0f} | {sinal}"
    return subject, html


async def loop() -> None:
    global _ultimo_alerta_fg, _ultimo_relatorio_hora
    print(f"Monitor iniciado — verificando a cada {INTERVALO_MIN} min | Relatório diário às {HORARIO}h")
    print(f"Enviando para: {RECIPIENT}\n")

    while True:
        ts  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        now = datetime.now()
        try:
            d      = await fetch_data()
            fg_val = int(d["fg"]["value"])
            btc    = d["precos"]["bitcoin"]["usd"]
            print(f"[{ts}] F&G: {fg_val} | BTC: ${btc:,.0f}", end="")

            # Alerta de medo extremo
            if fg_val <= 25 and _ultimo_alerta_fg != fg_val:
                print(" → 🚨 MEDO EXTREMO! Enviando alerta...", end="")
                subj, html = build_alerta_fg(d, ts)
                send_email(subj, html)
                _ultimo_alerta_fg = fg_val
                print(" ✅")
            elif fg_val > 25:
                _ultimo_alerta_fg = None
                print()
            else:
                print(" (alerta já enviado)")

            # Relatório diário às 21h
            if now.hour == HORARIO and _ultimo_relatorio_hora != now.day:
                print(f"  → 📊 Enviando relatório das {HORARIO}h...", end="")
                subj, html = build_relatorio(d, ts)
                send_email(subj, html)
                _ultimo_relatorio_hora = now.day
                print(" ✅")

        except Exception as e:
            print(f"\n[{ts}] Erro: {e}")

        await asyncio.sleep(INTERVALO_MIN * 60)


if __name__ == "__main__":
    asyncio.run(loop())
