"""
Monitora Fear & Greed a cada hora e envia e-mail quando entrar em Medo Extremo.
Uso: python monitor.py
     GMAIL_USER=seu@gmail.com GMAIL_APP_PASSWORD=xxxx INTERVALO_MIN=60 python monitor.py
"""

import asyncio
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx

FEAR_GREED_URL = "https://api.alternative.me/fng/"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT", GMAIL_USER)
INTERVALO_MIN = int(os.environ.get("INTERVALO_MIN", "60"))

# Evita re-enviar o mesmo alerta várias vezes seguidas
_ultimo_alerta_fg: int | None = None


async def fetch_data() -> dict:
    async with httpx.AsyncClient(timeout=15) as client:
        fg = (await client.get(FEAR_GREED_URL, params={"limit": 1})).json()["data"][0]
        btc = (await client.get(
            COINGECKO_URL,
            params={"ids": "bitcoin", "vs_currencies": "usd,brl", "include_24hr_change": "true"},
        )).json()["bitcoin"]
    return {
        "fg_value": int(fg["value"]),
        "fg_label": fg["value_classification"],
        "price_usd": btc["usd"],
        "price_brl": btc["brl"],
        "change_24h": btc["usd_24h_change"],
    }


def send_email(d: dict) -> None:
    fg_value = d["fg_value"]
    price_usd = d["price_usd"]
    change_24h = d["change_24h"]
    change_icon = "▲" if change_24h >= 0 else "▼"
    buy = fg_value <= 25 and price_usd <= 105000
    signal_label = "🟢 COMPRA CONFIRMADA" if buy else "⚠️ MEDO EXTREMO"
    color = "#22c55e" if buy else "#f59e0b"

    html = f"""
<div style="font-family:monospace;max-width:520px;padding:24px;
            border:2px solid {color};border-radius:10px;background:#0f0f0f;color:#e5e5e5;">
  <h2 style="color:{color};margin-top:0;">🚨 ALERTA BTC — {signal_label}</h2>
  <p style="color:#888;font-size:12px;">Fear &amp; Greed entrou em Medo Extremo</p>
  <hr style="border-color:#333;">
  <p>Fear &amp; Greed: <strong style="color:{color};font-size:1.4em;">{fg_value} / 100</strong>
     — {d['fg_label']}</p>
  <table style="width:100%;color:#e5e5e5;">
    <tr><td>BTC USD</td><td><strong>$ {price_usd:,.2f}</strong></td></tr>
    <tr><td>BTC BRL</td><td><strong>R$ {d['price_brl']:,.2f}</strong></td></tr>
    <tr><td>Variação 24h</td><td>{change_icon} {change_24h:+.2f}%</td></tr>
  </table>
  <hr style="border-color:#333;">
  <p style="font-size:11px;color:#888;">⚠️ Não é aconselhamento financeiro.</p>
</div>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 BTC — Fear & Greed {fg_value} (Medo Extremo) | $ {price_usd:,.0f}"
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_RECIPIENT
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.sendmail(GMAIL_USER, ALERT_RECIPIENT, msg.as_string())

    print(f"  ✅ E-mail enviado para {ALERT_RECIPIENT}")


async def loop() -> None:
    global _ultimo_alerta_fg
    print(f"Monitor iniciado — verificando a cada {INTERVALO_MIN} minuto(s). Ctrl+C para parar.\n")

    while True:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            d = await fetch_data()
            fg = d["fg_value"]
            print(f"[{ts}] Fear & Greed: {fg} | BTC: $ {d['price_usd']:,.0f}", end="")

            if fg <= 25:
                # Só reenvia se o valor mudou desde o último alerta
                if _ultimo_alerta_fg != fg:
                    print(f" → 🚨 MEDO EXTREMO! Enviando alerta...")
                    send_email(d)
                    _ultimo_alerta_fg = fg
                else:
                    print(" → 🚨 Medo Extremo (alerta já enviado para este valor)")
            else:
                _ultimo_alerta_fg = None
                print()

        except Exception as e:
            print(f"\n[{ts}] Erro: {e}")

        await asyncio.sleep(INTERVALO_MIN * 60)


if __name__ == "__main__":
    asyncio.run(loop())
