import os
import smtplib
import httpx
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("btc-signal")

FEAR_GREED_URL = "https://api.alternative.me/fng/"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT") or GMAIL_USER


def _classify_fear_greed(value: int) -> str:
    if value <= 25:
        return "Medo Extremo"
    if value <= 45:
        return "Medo"
    if value <= 55:
        return "Neutro"
    if value <= 75:
        return "Ganância"
    return "Ganância Extrema"


def _send_gmail(subject: str, html_body: str) -> None:
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise ValueError(
            "Variáveis GMAIL_USER e GMAIL_APP_PASSWORD não configuradas. "
            "Veja o README ou claude_desktop_config.json."
        )
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_RECIPIENT
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.sendmail(GMAIL_USER, ALERT_RECIPIENT, msg.as_string())


async def _fetch_market_data() -> dict:
    async with httpx.AsyncClient(timeout=15) as client:
        fg_resp = await client.get(FEAR_GREED_URL, params={"limit": 1})
        fg_resp.raise_for_status()
        fg_raw = fg_resp.json()["data"][0]

        btc_resp = await client.get(
            COINGECKO_URL,
            params={
                "ids": "bitcoin",
                "vs_currencies": "usd,brl",
                "include_24hr_change": "true",
            },
        )
        btc_resp.raise_for_status()
        btc_raw = btc_resp.json()["bitcoin"]

    return {
        "fg_value": int(fg_raw["value"]),
        "fg_label": fg_raw["value_classification"],
        "price_usd": btc_raw["usd"],
        "price_brl": btc_raw["brl"],
        "change_24h": btc_raw["usd_24h_change"],
    }


@mcp.tool()
async def check_btc_signal() -> str:
    """Consulta Fear & Greed Index e preço do BTC para gerar sinal de compra ou atenção."""
    d = await _fetch_market_data()
    fg_value = d["fg_value"]
    price_usd = d["price_usd"]
    change_24h = d["change_24h"]

    if fg_value <= 25 and price_usd <= 105000:
        signal = "🟢 COMPRA"
        explanation = (
            "Mercado em medo extremo com preço abaixo de $105.000. "
            "Historicamente um bom momento para acumular BTC."
        )
    elif fg_value >= 75:
        signal = "🔴 ATENÇÃO"
        explanation = (
            "Mercado em ganância extrema. "
            "Risco elevado — considere realizar lucros ou aguardar correção."
        )
    else:
        signal = "🟡 NEUTRO"
        explanation = "Sem sinal claro no momento. Aguarde condições mais favoráveis."

    change_icon = "▲" if change_24h >= 0 else "▼"

    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊  SINAL BTC — CHECK_BTC_SIGNAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SINAL: {signal}
{explanation}

FEAR & GREED INDEX
  Valor        : {fg_value} / 100
  Classificação: {d['fg_label']} ({_classify_fear_greed(fg_value)})

PREÇO DO BITCOIN
  USD  : $ {price_usd:,.2f}
  BRL  : R$ {d['price_brl']:,.2f}
  24h  : {change_icon} {change_24h:+.2f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


@mcp.tool()
async def send_fear_alert() -> str:
    """
    Verifica o Fear & Greed Index agora. Se estiver em Medo Extremo (≤ 25),
    envia um e-mail de alerta de compra via Gmail automaticamente.
    """
    d = await _fetch_market_data()
    fg_value = d["fg_value"]
    price_usd = d["price_usd"]
    change_24h = d["change_24h"]
    change_icon = "▲" if change_24h >= 0 else "▼"
    classification = _classify_fear_greed(fg_value)

    if fg_value > 25:
        return (
            f"⚪ Sem alerta. Fear & Greed atual: {fg_value} ({classification}). "
            f"E-mail só é enviado quando o índice estiver ≤ 25 (Medo Extremo)."
        )

    buy_signal = price_usd <= 105000
    signal_label = "🟢 COMPRA CONFIRMADA" if buy_signal else "⚠️ MEDO EXTREMO (preço acima de $105k)"
    signal_color = "#22c55e" if buy_signal else "#f59e0b"

    html = f"""
<div style="font-family:monospace;max-width:520px;padding:24px;
            border:2px solid {signal_color};border-radius:10px;background:#0f0f0f;color:#e5e5e5;">
  <h2 style="color:{signal_color};margin-top:0;">
    🚨 ALERTA BTC — {signal_label}
  </h2>
  <p style="color:#888;font-size:12px;margin-top:-10px;">
    Fear &amp; Greed Index entrou em Medo Extremo
  </p>
  <hr style="border-color:#333;">

  <h3 style="color:#aaa;">FEAR &amp; GREED INDEX</h3>
  <p>
    Valor: <strong style="color:{signal_color};font-size:1.4em;">{fg_value} / 100</strong><br>
    Classificação: <strong>{d['fg_label']} ({classification})</strong>
  </p>

  <h3 style="color:#aaa;">PREÇO DO BITCOIN</h3>
  <table style="width:100%;border-collapse:collapse;color:#e5e5e5;">
    <tr><td>USD</td><td><strong>$ {price_usd:,.2f}</strong></td></tr>
    <tr><td>BRL</td><td><strong>R$ {d['price_brl']:,.2f}</strong></td></tr>
    <tr><td>Variação 24h</td><td>{change_icon} {change_24h:+.2f}%</td></tr>
  </table>

  <hr style="border-color:#333;">
  <p style="font-size:12px;color:#888;">
    ⚠️ Não é aconselhamento financeiro. Faça sua própria análise antes de investir.
  </p>
</div>
"""

    subject = f"🚨 BTC ALERTA — Fear & Greed {fg_value} (Medo Extremo) | $ {price_usd:,.0f}"
    _send_gmail(subject, html)

    return (
        f"✅ E-mail de alerta enviado para {ALERT_RECIPIENT}!\n\n"
        f"  Fear & Greed : {fg_value} / 100 ({classification})\n"
        f"  BTC USD      : $ {price_usd:,.2f}\n"
        f"  Sinal        : {signal_label}"
    )


if __name__ == "__main__":
    mcp.run()
