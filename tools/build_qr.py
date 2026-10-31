#!/usr/bin/env python3
"""QR-Code (Fehlerkorrektur H) + druckbarer Tischaufsteller. Aufruf: build_qr.py <zielordner> <url>"""
import sys, pathlib, segno
out = pathlib.Path(sys.argv[1]); url = sys.argv[2]
qr = segno.make(url, error='h', boost_error=False)
qr.save(out / "assets" / "qr-karte.svg", scale=10, border=0, dark="#0b0d0c", light=None, xmldecl=False, svgns=True, nl=False, omitsize=True)
svg = (out / "assets" / "qr-karte.svg").read_text()
card = f'''<div class="card"><div class="in">
  <img class="logo" src="assets/logo-disc.png" alt="">
  <p class="eb">Café VAI · Vaihingen an der Enz</p>
  <h1>Speisekarte</h1>
  <p class="sub">Scannen · Stöbern · Auswahl dem Service zeigen</p>
  <div class="qr">{svg}</div>
  <p class="url">{url.replace("https://","")}</p>
  <p class="mot">Meet for coffee, stay for more.</p>
  <p class="lng">Deutsch · English · Türkçe</p>
</div></div>'''
page = f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tischaufsteller — Café VAI</title><meta name="robots" content="noindex,nofollow">
<style>
@font-face{{font-family:"Inter";src:url(assets/inter-latin-wght-normal.woff2) format("woff2");font-weight:100 900}}
@font-face{{font-family:"Fraunces";src:url(assets/fraunces-latin-wght-normal.woff2) format("woff2");font-weight:100 900}}
body{{background:#e8e2d4;color:#111;margin:0;font-family:Inter,system-ui,sans-serif}}
.bar{{position:sticky;top:0;background:#0b0d0c;color:#f3ead9;padding:12px 18px;display:flex;gap:14px;align-items:center;justify-content:space-between;font-size:.85rem;z-index:5}}
.bar button{{background:#e3a83f;border:0;border-radius:99px;padding:.7em 1.4em;font-weight:700;cursor:pointer}}
.sheet{{width:210mm;height:297mm;margin:16px auto;background:#fff;display:grid;grid-template-rows:1fr 1fr;box-shadow:0 10px 40px rgba(0,0,0,.2);position:relative}}
.card{{display:grid;place-items:center;position:relative;background:#f7f1e4;border-bottom:.3mm dashed #999}}
.card.flip{{transform:rotate(180deg)}}
.card:last-child{{border:0}}
.in{{text-align:center;width:150mm}}
.logo{{width:22mm;height:22mm;border-radius:50%;margin:0 auto 3mm;display:block}}
.eb{{font-size:8pt;letter-spacing:.22em;text-transform:uppercase;color:#1c4a46;margin:0 0 1mm;font-weight:600}}
h1{{font-family:Fraunces,Georgia,serif;font-weight:500;font-size:34pt;margin:0 0 2mm;color:#0b0d0c;line-height:1}}
.sub{{font-size:10pt;color:#333;margin:0 0 5mm}}
.qr{{width:56mm;height:56mm;margin:0 auto 3mm;padding:4mm;background:#fff;border:.4mm solid #0b0d0c;border-radius:4mm;box-sizing:content-box}}
.qr svg{{width:100%;height:100%;display:block}}
.url{{font-size:8pt;color:#555;margin:0 0 3mm;font-family:ui-monospace,monospace}}
.mot{{font-family:Fraunces,Georgia,serif;font-style:italic;font-size:13pt;color:#1c4a46;margin:0 0 1mm}}
.lng{{font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:#777;margin:0}}
.hint{{max-width:210mm;margin:10px auto;font-size:.8rem;color:#444;padding:0 10px}}
@page{{size:A4 portrait;margin:0}}
@media print{{body{{background:#fff}}.bar,.hint{{display:none}}.sheet{{margin:0;box-shadow:none}}}}
</style></head><body>
<div class="bar"><span>Café VAI · Tischaufsteller (Demo) — A4 drucken, in der Mitte falten, aufstellen</span><button onclick="print()">Drucken</button></div>
<p class="hint">Die obere Hälfte steht auf dem Kopf, damit nach dem Falten beide Seiten richtig herum lesbar sind. QR-Code: Fehlerkorrektur H (bleibt lesbar auch bei Flecken). Ziel: {url}</p>
<div class="sheet">{card.replace('class="card"','class="card flip"',1)}{card}</div>
</body></html>'''
(out / "qr.html").write_text(page, encoding="utf-8")
print("ok", url)
