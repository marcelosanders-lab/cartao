"""Gera o painel HTML da leitura (o artefato publicado a cada rotina).

  python3 radar/painel.py --janela <manha|noite> --relatorio radar/relatorios/<ARQ>.md \
      --saida radar/painel.html

Nao inventa numero: sinais, precos e indicadores vem do analisar.py rodando
sobre radar/dados (as velas desta execucao); marcas e lista de sobrevivencia
vem do auditar.py; placar e perguntas vem de placar.csv e perguntas.md; o
texto critico vem do apendice do relatorio. Antes de escrever, confere que o
"Agora" de cada par no relatorio e igual ao do motor - se nao bater, o
relatorio e de outra coleta e o painel NAO e gerado.
"""
import argparse
import csv
import html
import os
import re
import sys
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import auditar as AU  # noqa: E402

BRT = timezone(timedelta(hours=-3))

GRUPOS = [  # (prefixo do sinal, chave, rotulo)
    ("COMPRA", "compra", "Compra"),
    ("REALIZAR PARCIAL", "parcial", "Realizar parcial"),
    ("VENDA", "venda", "Venda"),
    ("ABAIXO DO STOP", "venda", "Abaixo do stop"),
    ("ALVO JA ALCANCADO", "parcial", "Alvo alcançado"),
    ("SEM ENTRADA", "bloq", "Sem entrada"),
    ("NEUTRO", "neutro", "Neutro"),
    ("DADOS INSUFICIENTES", "semdados", "Sem dados"),
]
MARCAS = {
    "MORTA": "vela sem negócio ou com negócio único: o preço atual repete o fechamento",
    "LIQ": "volume abaixo de US$ 50 mil/dia na fonte",
    "REGIME": "só é compra por causa do ponto extra do regime do BTC",
    "X4H-": "cruzamento de baixa no 4h ignorado",
    "RSI-BORDA": "RSI a menos de 2 pontos do teto de sobrecompra",
    "DER-BORDA": "deriva colada num limite do portão de entrada",
}


def e(x):
    return html.escape(str(x), quote=True)


def grupo(sinal):
    for pref, chave, rot in GRUPOS:
        if sinal.startswith(pref):
            return chave, rot
    return "neutro", sinal


def br(x, casas=2, sinal=False):
    if x is None:
        return "—"
    s = f"{x:+,.{casas}f}" if sinal else f"{x:,.{casas}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".").replace("-", "−")


def preco(x):
    if x is None:
        return "—"
    s = f"{x:.8g}"
    if "e" in s:
        s = f"{x:.12f}".rstrip("0")
    inteiro, _, dec = s.partition(".")
    inteiro = f"{int(inteiro):,}".replace(",", ".") if inteiro.lstrip("-").isdigit() else inteiro
    return inteiro + ("," + dec if dec else "")


# ---------- markdown minimo (o subconjunto que os relatorios usam) ----------

def inline(t):
    t = e(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def md(texto):
    linhas = texto.splitlines()
    out, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", l)
        if m:
            n = min(len(m.group(1)) + 1, 5)
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if l.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith("|"):
                bloco.append([c.strip() for c in linhas[i].strip().strip("|").split("|")])
                i += 1
            cab, corpo = bloco[0], [b for b in bloco[1:] if not set("".join(b)) <= set("-: ")]
            out.append('<div class="rolagem"><table class="md"><thead><tr>'
                       + "".join(f"<th>{inline(c)}</th>" for c in cab) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                                 for r in corpo) + "</tbody></table></div>")
            continue
        if l.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i].lstrip("> "))
                i += 1
            out.append(f"<blockquote>{inline(' '.join(bloco))}</blockquote>")
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", l)
        if m:
            ordenada = m.group(2)[0].isdigit()
            itens = []
            while i < len(linhas):
                m2 = re.match(r"^\s*([-*]|\d+\.)\s+(.*)", linhas[i])
                if m2 and (m2.group(1)[0].isdigit()) == ordenada:
                    itens.append([m2.group(1), m2.group(2)])
                elif linhas[i].startswith("  ") and linhas[i].strip() and itens:
                    itens[-1][1] += " " + linhas[i].strip()
                else:
                    break
                i += 1
            if ordenada:
                out.append("<ol>" + "".join(
                    f'<li value="{it[0][:-1]}">{inline(it[1])}</li>' for it in itens) + "</ol>")
            else:
                out.append("<ul>" + "".join(f"<li>{inline(it[1])}</li>" for it in itens) + "</ul>")
            continue
        par = []
        while i < len(linhas) and linhas[i].strip() and not re.match(
                r"^(#{1,4}\s|\||>|\s*([-*]|\d+\.)\s)", linhas[i]):
            par.append(linhas[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(par))}</p>")
    return "\n".join(out)


def secoes(texto):
    """[(titulo, corpo)] das secoes '## ' do relatorio."""
    partes = re.split(r"^## ", texto, flags=re.M)
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1] if "\n" in p else "")
            for p in partes[1:]]


# ---------------------------- conferencia ----------------------------

def agora_do_relatorio(texto):
    out, sec = {}, None
    for l in texto.splitlines():
        if l.startswith("| Par | Sinal"):
            sec = 3
            continue
        if l.startswith("| Par | Fech"):
            sec = 2
            continue
        if not l.startswith("|"):
            sec = None
            continue
        if sec is None or l.startswith("|---"):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if c[0].endswith("_USDT") and len(c) > sec:
            try:
                out[c[0]] = float(c[sec])
            except ValueError:
                pass
    return out


# ---------------------------- grafico ----------------------------

def grafico(placar):
    seq = [r for r in placar if r["encadeia"] == "sim"]
    if not seq:
        return "<p>Placar vazio.</p>"
    pts = [(seq[0]["de"], 0.0, 0.0)]
    cp = cc = 1.0
    for r in seq:
        cp *= 1 + float(r["painel"]) / 100
        cc *= 1 + float(r["compra"]) / 100
        pts.append((r["para"], (cc - 1) * 100, (cp - 1) * 100))
    W, H, ml, mr, mt, mb = 720, 260, 44, 92, 16, 34
    vals = [v for _, a, b in pts for v in (a, b)]
    lo, hi = min(vals + [0]), max(vals + [0])
    passo = 2 if hi - lo <= 12 else 5
    lo, hi = passo * ((lo // passo)), passo * (-(-hi // passo))
    x = lambda k: ml + k * (W - ml - mr) / (len(pts) - 1)  # noqa: E731
    y = lambda v: mt + (hi - v) * (H - mt - mb) / (hi - lo)  # noqa: E731
    g = []
    v = lo
    while v <= hi + 1e-9:
        g.append(f'<line class="grade{" zero" if abs(v) < 1e-9 else ""}" x1="{ml}" x2="{W - mr}" '
                 f'y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                 f'<text class="eixo" x="{ml - 8}" y="{y(v) + 4:.1f}" text-anchor="end">'
                 f'{br(v, 0, sinal=v != 0)}%</text>')
        v += passo
    for k, (rot, _, _) in enumerate(pts):
        if k % 2 == 0 or k == len(pts) - 1:
            g.append(f'<text class="eixo" x="{x(k):.1f}" y="{H - 10}" text-anchor="middle">{e(rot)}</text>')
    lin = lambda idx: " ".join(f"{x(k):.1f},{y(p[idx]):.1f}" for k, p in enumerate(pts))  # noqa: E731
    g.append(f'<polyline class="s-painel" points="{lin(2)}"/>')
    g.append(f'<polyline class="s-compra" points="{lin(1)}"/>')
    fim = pts[-1]
    for idx, cls, rot in ((1, "s-compra", "COMPRA"), (2, "s-painel", "Painel")):
        g.append(f'<circle class="{cls} ponto" cx="{x(len(pts) - 1):.1f}" cy="{y(fim[idx]):.1f}" r="4"/>')
    ya, yb = y(fim[1]), y(fim[2])
    if abs(ya - yb) < 16:
        ya, yb = (ya - 8, yb + 8) if ya <= yb else (ya + 8, yb - 8)
    g.append(f'<text class="rotulo" x="{W - mr + 10}" y="{ya + 4:.1f}">COMPRA {br(fim[1], 2, True)}%</text>')
    g.append(f'<text class="rotulo" x="{W - mr + 10}" y="{yb + 4:.1f}">Painel {br(fim[2], 2, True)}%</text>')
    dados = ";".join(f"{rot}|{br(a, 2, True)}|{br(b, 2, True)}|{x(k):.1f}" for k, (rot, a, b) in enumerate(pts))
    return (f'<div class="grafico" data-pontos="{e(dados)}">'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Retorno acumulado das COMPRA contra o painel">'
            + "".join(g) + f'<line class="cursor" x1="0" x2="0" y1="{mt}" y2="{H - mb}" hidden/>'
            f'<rect class="alvo" x="{ml}" y="{mt}" width="{W - ml - mr}" height="{H - mt - mb}"/></svg>'
            '<div class="dica" hidden></div></div>')



# ---------------------------- sentimento ----------------------------

FAIXAS_FG = [(0, 20, "Medo extremo", "fg1"), (20, 40, "Medo", "fg2"), (40, 60, "Neutro", "fg3"),
             (60, 80, "Ganância", "fg4"), (80, 101, "Ganância extrema", "fg5")]


def sentimento_html():
    caminho = os.path.join(AQUI, "sentimento.csv")
    cab = ('<section class="senti" aria-labelledby="h-fg"><h2 id="h-fg">Medo e ganância (CoinMarketCap)</h2>')
    rodape = ('<p class="nota">Contexto, não sinal: o índice não altera nenhuma COMPRA ou VENDA do motor. '
              'Fica registrado a cada leitura para medir se ajuda (Pergunta 22).</p></section>')
    linhas = list(csv.DictReader(open(caminho, encoding="utf-8"))) if os.path.exists(caminho) else []
    if not linhas:
        return cab + '<p class="nota"><b>Não coletado.</b> <code>sentimento.py</code> nunca rodou.</p>' + rodape
    u = linhas[-1]
    quando = datetime.strptime(u["coletado_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    idade = datetime.now(timezone.utc) - quando
    hora = quando.astimezone(BRT).strftime("%d/%m %H:%M")
    if idade > timedelta(hours=3):
        return (cab + f'<p class="nota"><b>Não coletado nesta leitura.</b> O último registro é de {hora} '
                '(Brasília) e não é mostrado para não passar por dado atual.</p>' + rodape)
    if u["fonte"] == "INDISPONIVEL":
        return (cab + f'<p class="nota"><b>Indisponível nesta leitura</b> ({hora}, Brasília). '
                f'Motivo: <code>{e(u["motivo"][:240])}</code></p>' + rodape)
    v = int(u["fg_valor"])
    rot = next(r for lo, hi, r, _ in FAIXAS_FG if lo <= v < hi)
    zonas = "".join(f'<span class="{c}" style="flex:{hi - lo if hi <= 100 else 20}"></span>'
                    for lo, hi, _, c in FAIXAS_FG)
    extra = ""
    if u["btc_dom"]:
        extra = ('<div class="faixa">'
                 f'<div class="cx"><b>{br(float(u["btc_dom"]), 1)}%</b><span>Dominância do BTC</span></div>'
                 f'<div class="cx"><b>{br(float(u["eth_dom"]), 1)}%</b><span>Dominância do ETH</span></div>'
                 f'<div class="cx"><b>{br(float(u["mcap_usd"]) / 1e12, 2)} tri</b><span>Valor de mercado total, US$ '
                 f'({br(float(u["mcap_var24h"]), 2, True)}% em 24h)</span></div>'
                 f'<div class="cx"><b>{br(float(u["vol24h_usd"]) / 1e9, 1)} bi</b><span>Volume 24h, US$</span></div></div>')
    return (cab + f'<div class="fg"><div class="fg-num"><b>{v}</b><span>{e(rot)}'
            f'{" · " + e(u["fg_classe"]) if u["fg_classe"] and u["fg_classe"] != rot else ""}</span></div>'
            f'<div class="fg-escala" role="img" aria-label="Índice {v} de 100, {e(rot)}"><div class="fg-zonas">{zonas}</div>'
            f'<i style="left:{v}%"></i><div class="fg-rot"><span>0 medo</span><span>50</span><span>ganância 100</span></div></div></div>'
            f'<p class="nota">Coletado às {hora} (Brasília), fonte {e(u["fonte"])}.</p>{extra}' + rodape)

# ---------------------------- pagina ----------------------------

CSS = """
:root{--bg:#f2f4f3;--pn:#ffffff;--pn2:#e8eceb;--tx:#121719;--tx2:#4a5559;--mu:#65737a;--ln:#d5dcdd;
--ac:#0e5f74;--ok:#17804a;--okb:#e3f2e9;--av:#8a5200;--avb:#fbefd9;--cr:#b3261e;--crb:#fbe5e2;
--nb:#eceff0;--s1:#2a78d6;--s2:#eb6834;--f1:#c0392b;--f2:#e8876f;--f3:#b9bec0;--f4:#6fbf8e;--f5:#1a7f4b;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e1213;--pn:#161b1d;--pn2:#1d2427;
--tx:#e8edef;--tx2:#b6c1c5;--mu:#8e9a9f;--ln:#2a3336;--ac:#62b6cc;--ok:#52c68d;--okb:#12291d;--av:#e6a54a;
--avb:#2c2111;--cr:#ff8177;--crb:#331715;--nb:#1f2629;--s1:#3987e5;--s2:#d95926;--f1:#e0564a;--f2:#b86a56;--f3:#5b6468;--f4:#3f9467;--f5:#52c68d;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0e1213;--pn:#161b1d;--pn2:#1d2427;--tx:#e8edef;--tx2:#b6c1c5;--mu:#8e9a9f;
--ln:#2a3336;--ac:#62b6cc;--ok:#52c68d;--okb:#12291d;--av:#e6a54a;--avb:#2c2111;--cr:#ff8177;--crb:#331715;
--nb:#1f2629;--s1:#3987e5;--s2:#d95926;--f1:#e0564a;--f2:#b86a56;--f3:#5b6468;--f4:#3f9467;--f5:#52c68d;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--tx);font:15px/1.55 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
.pagina{max-width:1120px;margin:0 auto;padding-inline:16px;padding-block:28px 56px;display:grid;gap:28px}
h1,h2,h3{font-family:"IBM Plex Sans Condensed","Arial Narrow",system-ui,sans-serif;font-weight:600;
text-wrap:balance;margin:0;letter-spacing:-.005em}
h1{font-size:34px;line-height:1.1}h2{font-size:22px}h3{font-size:17px}
.num,td.n,.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums}
.cab{display:grid;gap:6px}.olho{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}
.meta{color:var(--tx2);display:flex;flex-wrap:wrap;gap:6px 18px}
.alerta{background:var(--crb);border:1px solid color-mix(in srgb,var(--cr) 35%,transparent);border-radius:10px;
padding:18px 20px;display:grid;gap:8px}
.alerta .olho{color:var(--cr);font-weight:600}.alerta h2{font-size:21px}.alerta .relatorio{max-width:80ch}.alerta .relatorio p{margin:.4em 0}
.alerta .rolagem{margin:6px 0}
.faixa{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.cx{background:var(--pn);border:1px solid var(--ln);border-radius:8px;padding:12px 14px;display:grid;gap:2px}
.cx b{font:600 26px/1.1 "IBM Plex Mono",ui-monospace,monospace}.cx span{color:var(--mu);font-size:13px}
.cx.placar{grid-column:span 2}.cx.placar b{font-size:20px}
@media (max-width:520px){.cx.placar{grid-column:1/-1}}
section{display:grid;gap:12px}
.nota{color:var(--tx2);max-width:75ch;margin:0}
.rolagem{overflow-x:auto;border:1px solid var(--ln);border-radius:8px;background:var(--pn)}
table{border-collapse:collapse;width:100%;font-size:14px}
th{font-weight:600;text-align:left;color:var(--mu);font-size:12px;letter-spacing:.04em;text-transform:uppercase;
background:var(--pn2);position:sticky;top:0}
th,td{padding:7px 8px;border-bottom:1px solid var(--ln);white-space:nowrap;vertical-align:top}
tr:last-child td{border-bottom:0}td.n{text-align:right}
#sinais td:last-child{white-space:normal;min-width:120px}
table.md td,table.md th{white-space:normal;min-width:70px}
.pilula{display:inline-block;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:600;border:1px solid transparent}
.p-compra{background:var(--okb);color:var(--ok);border-color:color-mix(in srgb,var(--ok) 30%,transparent)}
.p-venda{background:var(--crb);color:var(--cr);border-color:color-mix(in srgb,var(--cr) 30%,transparent)}
.p-parcial{background:var(--avb);color:var(--av);border-color:color-mix(in srgb,var(--av) 30%,transparent)}
.p-bloq,.p-neutro,.p-semdados{background:var(--nb);color:var(--tx2);border-color:var(--ln)}
.marca{display:inline-block;margin:0 4px 2px 0;padding:0 6px;border-radius:4px;font:600 11px/18px "IBM Plex Mono",monospace;
background:var(--avb);color:var(--av)}
.marca.grave{background:var(--crb);color:var(--cr)}
.filtros{display:flex;flex-wrap:wrap;gap:8px}
.filtros button{font:inherit;font-size:13px;padding:5px 12px;border-radius:999px;border:1px solid var(--ln);
background:var(--pn);color:var(--tx2);cursor:pointer}
.filtros button[aria-pressed="true"]{background:var(--ac);border-color:var(--ac);color:var(--bg)}
button:focus-visible,summary:focus-visible,a:focus-visible{outline:2px solid var(--ac);outline-offset:2px}
.sobre{background:var(--pn);border:1px dashed var(--ln);border-radius:10px;padding:16px 18px;display:grid;gap:10px}
.legenda{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;color:var(--tx2)}
.legenda i{display:inline-block;width:18px;height:0;border-top:2px solid var(--s1);vertical-align:middle;margin-right:6px}
.legenda i.p{border-top:2px dashed var(--s2)}
.grafico{position:relative;background:var(--pn);border:1px solid var(--ln);border-radius:8px;padding:12px}
.grafico svg{width:100%;height:auto;display:block;overflow:visible}
.grade{stroke:var(--ln);stroke-width:1}.grade.zero{stroke:var(--mu)}
.eixo{fill:var(--mu);font:11px "IBM Plex Mono",monospace}.rotulo{fill:var(--tx);font:600 12px "IBM Plex Mono",monospace}
polyline{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.s-compra{stroke:var(--s1)}.s-painel{stroke:var(--s2);stroke-dasharray:6 4}
circle.s-compra{fill:var(--s1);stroke:var(--pn);stroke-width:2;stroke-dasharray:none}
circle.s-painel{fill:var(--s2);stroke:var(--pn);stroke-width:2;stroke-dasharray:none}
.cursor{stroke:var(--mu);stroke-width:1}.alvo{fill:transparent;cursor:crosshair}
.dica{position:absolute;top:8px;background:var(--pn);border:1px solid var(--ln);border-radius:6px;padding:6px 10px;
font:12px/1.5 "IBM Plex Mono",monospace;color:var(--tx);pointer-events:none;box-shadow:0 2px 8px rgb(0 0 0/.12)}
details{background:var(--pn);border:1px solid var(--ln);border-radius:8px;padding:0 16px}
summary{cursor:pointer;padding:12px 0;font-weight:600}
details[open] summary{border-bottom:1px solid var(--ln);margin-bottom:8px}
.relatorio{max-width:80ch;padding-bottom:12px}.relatorio p,.relatorio li{color:var(--tx)}
.relatorio h2{font-size:19px;margin-top:22px}.relatorio h3{margin-top:14px}
.relatorio blockquote{margin:0;padding:8px 14px;background:var(--avb);border-radius:6px}
.relatorio .rolagem{margin:8px 0}
code{font:13px "IBM Plex Mono",monospace;background:var(--pn2);padding:0 4px;border-radius:3px}
ol.perg{margin:0;padding-left:28px;display:grid;gap:8px;max-width:80ch}ol.perg li::marker{font-family:"IBM Plex Mono",monospace;color:var(--mu)}
footer{color:var(--mu);font-size:13px;display:grid;gap:4px;border-top:1px solid var(--ln);padding-top:14px}
a{color:var(--ac)}
.senti{background:var(--pn);border:1px solid var(--ln);border-radius:10px;padding:16px 18px}
.fg{display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center}
.fg-num{display:grid}.fg-num b{font:600 44px/1 "IBM Plex Mono",monospace}.fg-num span{color:var(--tx2);font-weight:600}
.fg-escala{position:relative;flex:1 1 260px;padding-top:10px}
.fg-zonas{display:flex;gap:2px;height:10px;border-radius:5px;overflow:hidden}
.fg1{background:var(--f1)}.fg2{background:var(--f2)}.fg3{background:var(--f3)}.fg4{background:var(--f4)}.fg5{background:var(--f5)}
.fg-escala i{position:absolute;top:2px;width:4px;height:26px;margin-left:-2px;background:var(--tx);border:2px solid var(--pn);border-radius:3px;box-sizing:content-box}
.fg-rot{display:flex;justify-content:space-between;font:11px "IBM Plex Mono",monospace;color:var(--mu);margin-top:6px}
@media (prefers-reduced-motion:no-preference){.filtros button{transition:background .15s,color .15s}}
"""

JS = """
(function(){
  var bts=document.querySelectorAll('.filtros button'),linhas=document.querySelectorAll('#sinais tbody tr');
  function aplica(f){bts.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.f===f?'true':'false')});
    linhas.forEach(function(tr){tr.hidden=!(f==='todos'||tr.dataset.g===f)});
    try{localStorage.setItem('radar-filtro',f)}catch(e){}}
  bts.forEach(function(b){b.addEventListener('click',function(){aplica(b.dataset.f)})});
  var ini='todos';try{ini=localStorage.getItem('radar-filtro')||'todos'}catch(e){}
  if(!document.querySelector('.filtros button[data-f="'+ini+'"]'))ini='todos';aplica(ini);
  document.querySelectorAll('.grafico').forEach(function(g){
    var pts=g.dataset.pontos.split(';').map(function(s){var p=s.split('|');return{r:p[0],c:p[1],p:p[2],x:+p[3]}});
    var svg=g.querySelector('svg'),cur=svg.querySelector('.cursor'),dica=g.querySelector('.dica'),alvo=svg.querySelector('.alvo');
    function mostra(ev){var pt=svg.createSVGPoint();pt.x=ev.clientX;pt.y=ev.clientY;
      var loc=pt.matrixTransform(svg.getScreenCTM().inverse()),m=pts[0];
      pts.forEach(function(q){if(Math.abs(q.x-loc.x)<Math.abs(m.x-loc.x))m=q});
      cur.setAttribute('x1',m.x);cur.setAttribute('x2',m.x);cur.hidden=false;cur.removeAttribute('hidden');
      dica.innerHTML='<b>'+m.r+'</b><br>COMPRA '+m.c+'%<br>Painel '+m.p+'%';dica.hidden=false;
      var r=svg.getBoundingClientRect(),px=(m.x/720)*r.width;dica.style.left=Math.min(px+16,r.width-150)+'px'}
    function some(){cur.setAttribute('hidden','');dica.hidden=true}
    alvo.addEventListener('mousemove',mostra);alvo.addEventListener('mouseleave',some);
    alvo.addEventListener('touchstart',function(ev){mostra(ev.touches[0])},{passive:true});
  });
})();
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--janela", required=True, choices=["manha", "noite"])
    ap.add_argument("--relatorio", required=True)
    ap.add_argument("--saida", required=True)
    a = ap.parse_args()

    texto = open(a.relatorio, encoding="utf-8").read()
    dados = AU.rodar_motor(a.janela)
    res = dados["resultados"]

    rel = agora_do_relatorio(texto)
    diverge = [r["par"] for r in res
               if r["par"] in rel and r.get("preco_atual") is not None
               and abs(rel[r["par"]] - r["preco_atual"]) > 1e-12 * max(1, abs(r["preco_atual"]))]
    if not rel or diverge:
        sys.exit("ERRO: o relatorio nao e desta coleta (Agora diverge do motor em: "
                 f"{', '.join(diverge) or 'nenhum par lido'}). Painel nao gerado.")

    cab = re.search(r"^# Radar de cripto - (.+?) \(horario de Brasilia\)", texto, re.M)
    quando = cab.group(1) if cab else "?"
    tit = re.search(r"^\*\*(Leitura[^*]+)\*\*", texto, re.M)
    base_nome = os.path.basename(a.relatorio)
    extra = "-extra-" in base_nome
    rotulo_janela = ("Leitura extra" if extra else
                     "Leitura das 22h" if a.janela == "noite" else "Leitura das 11h")

    secs = secoes(texto)
    grave = next(((t, c) for t, c in secs if "problema mais grave" in t.lower()), None)
    if grave:
        alerta = (f'<div class="alerta" role="note"><span class="olho">Problema mais grave desta leitura</span>'
                  f'<h2>{inline(grave[0].split(":", 1)[-1].strip().capitalize())}</h2>'
                  f'<div class="relatorio">{md(grave[1])}</div></div>')
    else:
        alerta = ('<div class="alerta" role="note"><span class="olho">Falha da rotina</span>'
                  '<h2>O relatório não tem a seção "O problema mais grave"</h2>'
                  '<p>O roteiro exige que o apêndice abra por ela. Sem ela, a auditoria desta leitura '
                  'não foi feita ou foi feita fora do formato.</p></div>')

    # contagens e marcas
    cont = {}
    linhas, sobrev = [], []
    for r in res:
        chave, rot = grupo(r["sinal"])
        cont[chave] = cont.get(chave, 0) + 1
        marcas = AU.marcar(r) if chave == "compra" else []
        if chave == "compra" and AU.sobrevive(r, marcas):
            sobrev.append(r)
        chips = "".join(
            f'<span class="marca{" grave" if m in ("MORTA", "LIQ") else ""}" title="{e(MARCAS[m])}">{e(m)}</span>'
            for m in marcas)
        linhas.append(
            f'<tr data-g="{chave}"><td><b>{e(r["par"].replace("_USDT", ""))}</b></td>'
            f'<td><span class="pilula p-{chave}">{e(r["sinal"].capitalize())}</span></td>'
            f'<td class="n">{preco(r.get("preco_atual"))}</td>'
            f'<td class="n">{br(r.get("deriva_atr"), 2, True) if r.get("deriva_atr") is not None else "—"}</td>'
            f'<td class="n">{br(r.get("rsi"), 0)}</td>'
            f'<td class="n">{preco(r.get("stop"))}</td><td class="n">{preco(r.get("alvo"))}</td>'
            f'<td class="n">{br(r.get("rr_real"), 2) + ":1" if r.get("rr_real") else "—"}</td>'
            f'<td class="n">{br(r.get("vol_usd_medio"), 0)}</td><td>{chips or ""}</td></tr>')

    placar = list(csv.DictReader(open(os.path.join(AQUI, "placar.csv"), encoding="utf-8")))
    seq = [r for r in placar if r["encadeia"] == "sim"]
    cp = cc = 1.0
    for r in seq:
        cp *= 1 + float(r["painel"]) / 100
        cc *= 1 + float(r["compra"]) / 100
    v24 = [r for r in placar if r["janela"] == "24h"]
    venc = sum(float(r["compra"]) > float(r["painel"]) for r in v24)

    faixa = "".join(
        f'<div class="cx"><b>{cont.get(k, 0)}</b><span>{rot}</span></div>'
        for k, rot in (("compra", "Compra"), ("parcial", "Realizar parcial"), ("venda", "Venda"),
                       ("bloq", "Sem entrada"), ("neutro", "Neutro")))
    faixa += (f'<div class="cx placar"><b>{br((cc - cp) * 100, 2, True)} pp</b>'
              f'<span>COMPRA {br((cc - 1) * 100, 2, True)}% contra painel {br((cp - 1) * 100, 2, True)}% '
              f'em {len(seq)} janelas; venceu {venc} de {len(v24)} janelas de 24h</span></div>')

    sob = "".join(
        f'<tr><td><b>{e(r["par"].replace("_USDT", ""))}</b></td><td class="n">{preco(r["preco_atual"])}</td>'
        f'<td class="n">{preco(r["stop"])}</td><td class="n">{preco(r["alvo"])}</td>'
        f'<td class="n">{br(r["rsi"], 0)}</td><td class="n">{br(r["deriva_atr"], 2, True)}</td>'
        f'<td class="n">{br(r["vol_usd_medio"], 0)}</td></tr>'
        for r in sorted(sobrev, key=lambda x: -x["vol_usd_medio"]))
    sob_html = (f'<div class="rolagem"><table><thead><tr><th>Par</th><th>Agora</th><th>Stop</th><th>Alvo</th>'
                f'<th>RSI</th><th>Deriva ATR</th><th>Volume US$/dia</th></tr></thead><tbody>{sob}</tbody></table></div>'
                if sobrev else '<p class="nota"><b>Nenhuma COMPRA sobrevive aos filtros nesta leitura.</b></p>')

    filtros = [("todos", "Todos")] + [(k, r) for k, r in (
        ("compra", "Compra"), ("parcial", "Realizar parcial"), ("venda", "Venda"),
        ("bloq", "Sem entrada"), ("neutro", "Neutro")) if cont.get(k)]
    bts = "".join(f'<button type="button" data-f="{k}" aria-pressed="false">{r}'
                  f'{" " + str(cont.get(k, 0)) if k != "todos" else ""}</button>' for k, r in filtros)

    perg_txt = open(os.path.join(AQUI, "perguntas.md"), encoding="utf-8").read()
    perg = re.findall(r"^(\d+)\.\s+(.*(?:\n {3,}.*)*)", perg_txt, re.M)
    perg_html = "<ol class=\"perg\">" + "".join(
        f'<li value="{n}">{inline(" ".join(t.split()))}</li>' for n, t in perg) + "</ol>"
    atual = re.search(r"Última atualização: (.+?)\.", perg_txt)

    leg_marcas = "".join(f'<li><span class="marca{" grave" if k in ("MORTA", "LIQ") else ""}">{k}</span> {e(v)}</li>'
                         for k, v in MARCAS.items())
    gerado = datetime.now(BRT).strftime("%d/%m/%Y %H:%M")

    pagina = f"""<title>Radar Cripto</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
<main class="pagina">
<header class="cab"><span class="olho">{e(rotulo_janela)} · {e(quando)} (Brasília)</span>
<h1>Radar Cripto</h1>
<div class="meta"><span>Regime do BTC: <b>{e(dados["regime"].upper())}</b></span><span>Fonte: Crypto.com Exchange</span>
<span>{len(res)} pares</span><span class="mono">{e(base_nome)}</span></div>
{f'<p class="nota">{inline(tit.group(1))}</p>' if tit else ''}</header>
{alerta}
<div class="faixa">{faixa}</div>
{sentimento_html()}

<section class="sobre" aria-labelledby="h-sob"><h2 id="h-sob">Lista de sobrevivência</h2>
<p class="nota"><b>Não é sinal do motor.</b> É o que sobra das {cont.get("compra", 0)} COMPRA depois de descontar
liquidez baixa, vela morta, dependência do regime do BTC, cruzamento contrário no 4h e RSI ou deriva no limite,
e com RSI abaixo de 75. Os cortes foram escolhidos sem backtest. O stop recalcula a cada fechamento e pode descer.</p>
{sob_html}</section>

<section aria-labelledby="h-sin"><h2 id="h-sin">Sinais do motor</h2>
<div class="filtros" role="group" aria-label="Filtrar por sinal">{bts}</div>
<div class="rolagem"><table id="sinais"><thead><tr><th>Par</th><th>Sinal</th><th>Agora</th><th>Deriva ATR</th>
<th>RSI 1d</th><th>Stop</th><th>Alvo</th><th>R:R agora</th><th>Volume US$/dia</th><th>Marcas</th></tr></thead>
<tbody>{"".join(linhas)}</tbody></table></div>
<ul class="legenda" style="list-style:none;padding:0;margin:0">{leg_marcas}</ul></section>

<section aria-labelledby="h-pl"><h2 id="h-pl">Placar: COMPRA contra o painel</h2>
<p class="nota">Retorno acumulado, encadeando só as leituras agendadas. O painel é a média dos 28 pares: comprar tudo.
Se a linha azul fica abaixo da laranja, a lista de COMPRA está escolhendo pior que o acaso.</p>
<div class="legenda"><span><i></i>COMPRA</span><span><i class="p"></i>Painel</span></div>
{grafico(placar)}
<details><summary>Tabela do placar ({len(placar)} janelas)</summary><div class="rolagem" style="margin-bottom:12px"><table>
<thead><tr><th>Tipo</th><th>De</th><th>Para</th><th>Painel</th><th>COMPRA</th><th>Diferença</th><th>n</th></tr></thead><tbody>
{"".join(f'<tr><td>{"janela" if r["janela"] == "seq" else "24h"}</td><td>{e(r["de"])}</td><td>{e(r["para"])}</td>'
         f'<td class="n">{br(float(r["painel"]), 2, True)}%</td><td class="n">{br(float(r["compra"]), 2, True)}%</td>'
         f'<td class="n">{br(float(r["compra"]) - float(r["painel"]), 2, True)}</td><td class="n">{e(r["n"])}</td></tr>'
         for r in placar)}</tbody></table></div></details></section>

<section aria-labelledby="h-pg"><h2 id="h-pg">Perguntas esperando sua resposta</h2>
<p class="nota">Nenhuma foi implementada. O número entre parênteses conta quantos relatórios ela atravessou sem resposta.
{('Contadores de ' + e(atual.group(1)) + '.') if atual else ''}</p>
{perg_html}</section>

<details><summary>Relatório completo desta leitura</summary><div class="relatorio">{md(texto)}</div></details>

<footer><span>Gerado em {gerado} (Brasília) por <code>radar/painel.py</code> a partir de <code>{e(base_nome)}</code>.</span>
<span>Preços, indicadores e sinais saíram de <code>analisar.py</code> rodando sobre as velas desta coleta; o painel confere
o preço atual de cada par contra o relatório antes de ser gerado.</span>
<span>Sinais mecânicos, sem backtest, sobre uma fonte de preços parcial. Não é recomendação de investimento.</span></footer>
</main>
<script>{JS}</script>
"""
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(pagina)
    print(f"painel escrito em {a.saida} ({len(pagina) // 1024} KB): {cont.get('compra', 0)} COMPRA, "
          f"{len(sobrev)} sobreviventes, alerta {'ok' if grave else 'AUSENTE'}")


if __name__ == "__main__":
    main()
