#!/usr/bin/env python3
"""Baut index.html + Rechtsseiten für die Café-VAI-Demo (GastrOptima)."""
import sys, pathlib
out = pathlib.Path(sys.argv[1])

def items(rows):
    h = ""
    for r in rows:
        name, desc, price = r[0], r[1], r[2]
        tag = f"<small>{r[3]}</small>" if len(r) > 3 else ""
        d = f"<span>{desc}</span>" if desc else ""
        h += f"<li><strong>{name}{tag}</strong>{d}<em>{price}</em></li>\n"
    return f'<ul class="items">\n{h}</ul>'

panels = []

panels.append(f'''
<article class="panel" data-label="Frühstück">
  <div class="pimg"><img src="assets/fruehstueck.webp" alt="VAI Serpme Kahvaltı – türkisches Frühstück für zwei" loading="lazy" width="620" height="827"><span class="tag">Sa &amp; So · 9–12:30 Uhr</span></div>
  <div class="ptxt">
    <div class="pnum">01</div>
    <h3>Frühstück</h3>
    <p class="sub">Nur vor Ort · samstags und sonntags</p>
    {items([
      ("Schnelles Frühstück","mit Heißgetränk","13,90 €"),
      ("VAI Serpme Kahvaltı","türkisches Frühstück · für 2 Personen","38,90 €","Signature"),
      ("Jede weitere Person","","16,90 €"),
      ("Kinder 7–12 Jahre","","8,90 €"),
    ])}
    <p class="extras"><b>Extras:</b> Menemen 5,00 · Sucuk mit Ei 5,50 · Menemen &amp; Sucuk 6,00 · Aufstrich/Oliven 3,00 · Kännchen Tee 6,50</p>
  </div>
</article>''')

panels.append(f'''
<article class="panel" data-label="SmashBurger">
  <div class="pimg"><img src="assets/burger.webp" alt="Dobi's SmashBurger mit Spiegelei und Jalapeños" loading="lazy" width="620" height="827"><span class="tag">Menü = Pommes + 0,33 l</span></div>
  <div class="ptxt">
    <div class="pnum">02</div>
    <h3>SmashBurger</h3>
    <p class="sub">Menü mit Pommes &amp; Softdrink · einzeln</p>
    {items([
      ("Dobi's SmashBurger","140 g Rind, Spiegelei, Pastırma, Jalapeños, Haussauce","19,90 € · 11,90 €","Bestseller"),
      ("Chicken Hot Honey","","18,90 € · 10,90 €"),
      ("Cheeseburger","","17,50 € · 9,50 €"),
      ("Chickenburger","","17,50 € · 9,50 €"),
      ("Hamburger","","16,50 € · 8,50 €"),
      ("Veggieburger","","16,50 € · 7,50 €"),
    ])}
    <p class="extras"><b>Dazu:</b> Pommes 4,50 · Süßkartoffel-Pommes 5,50 · Spiegelei 1,00 · Käse 1,00 · Pastırma 1,50 · Jalapeños 0,50 · Extra Patty 3,00</p>
  </div>
</article>''')

panels.append(f'''
<article class="panel" data-label="Tenders">
  <div class="pimg"><div class="duo"><img src="assets/tenders-og.webp" alt="OG's Chicken Tenders mit fünf Dips" loading="lazy" width="721" height="540"><img src="assets/tenders-crunchy.webp" alt="Natural Crunchy Tenders" loading="lazy" width="721" height="540"></div><span class="tag">100 % Hähnchenfilet</span></div>
  <div class="ptxt">
    <div class="pnum">03</div>
    <h3>Tenders</h3>
    <p class="sub">OG's (zart, würzige Panade) oder Natural Crunchy (extra knusprig)</p>
    {items([
      ("4 Stück","Menü mit Pommes, Dip &amp; Softdrink 10,90 €","5,90 €"),
      ("8 Stück","Menü 15,90 €","9,90 €"),
      ("12 Stück","Menü 20,90 €","13,90 €"),
    ])}
    <p class="extras"><b>Dips:</b> Dobi's Sauce · Sweet &amp; Sour · Ketchup · Mayo · Hot Honey</p>
  </div>
</article>''')

panels.append(f'''
<article class="panel" data-label="Kaffee &amp; Tee">
  <div class="pimg"><img src="assets/banner-drinks-stock.webp" alt="Cappuccino mit Latte Art" loading="lazy" width="1100" height="423" style="object-position:34% 50%"><span class="tag">Meet for coffee</span></div>
  <div class="ptxt">
    <div class="pnum">04</div>
    <h3>Kaffee &amp; Tee</h3>
    <p class="sub">Die Pause, für die man hergekommen ist</p>
    {items([
      ("Kaffee Crema","klein · groß","2,80 € · 4,80 €"),
      ("Espresso","Doppio 3,80 € · Macchiato 2,40 €","2,00 €"),
      ("Cappuccino","","3,80 €"),
      ("Latte Macchiato","","4,20 €"),
      ("Milchkaffee","","4,20 €"),
      ("Türkischer Tee","Kännchen (bis 3 Personen) 8,50 €","1,50 €"),
    ])}
    <p class="extras"><b>Außerdem:</b> Kaffee Coco 4,50 · Heiße Schokolade 3,50 · Teesorten 2,50</p>
  </div>
</article>''')

panels.append(f'''
<article class="panel" data-label="Drinks &amp; Bar">
  <div class="pimg"><img src="assets/kaffee.webp" alt="Barista an der Kaffeemaschine im Café VAI" loading="lazy" width="620" height="827"><span class="tag">Fr · Sa · Sa 17–22 Uhr</span></div>
  <div class="ptxt">
    <div class="pnum">05</div>
    <h3>Drinks &amp; Bar</h3>
    <p class="sub">Spritz, Longdrinks, Bier und Hausgemachtes</p>
    {items([
      ("Aperol · Lillet · Sarti","Spritz","7,50 €"),
      ("Longdrinks","Gin &amp; Tonic, Jack &amp; Cola, Vodka Bull/Lemon, Campari Orange","7,50 €"),
      ("Hausgemachte Limo / Eistee","0,5 l","4,90 €"),
      ("Weizen","0,5 l","3,90 €"),
      ("Cluss Kellerpils / Radler","0,33 l","3,60 €"),
    ])}
    <p class="extras"><b>Dazu:</b> Roseano 5,90 · Corona/Desperados 4,20 · Softdrinks 0,33 l 3,90 · Red Bull 4,00</p>
  </div>
</article>''')
panels[-1] = panels[-1].replace("Fr · Sa · Sa 17–22 Uhr", "Fr · Sa · So")

index = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Café VAI — Demo by GastrOptima · Vaihingen an der Enz</title>
<meta name="description" content="Demo-Website für Café VAI in Vaihingen an der Enz: Kaffee, Frühstück, SmashBurger, Drinks — mit Scroll-Erlebnis und GastrOptima-Bestellsystem.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0b0d0c">
<meta property="og:title" content="Café VAI — Demo by GastrOptima">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/icon-180.png">
<link rel="preload" href="assets/fraunces-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div id="bar"></div>

<header class="nav" id="nav">
  <a class="brand" href="#top" aria-label="Café VAI – nach oben"><img src="assets/logo-disc.png" alt="" width="40" height="40"><span>Café VAI<small>VAIHINGEN / ENZ</small></span><em class="demotag">Demo</em></a>
  <ul>
    <li><a href="#ueber">Über uns</a></li>
    <li><a href="#speisekarte">Speisekarte</a></li>
    <li><a href="#bestellen">Bestellen</a></li>
    <li><a href="#system">GastrOptima</a></li>
    <li><a href="#besuch">Besuch</a></li>
  </ul>
  <div class="navcta"><a class="btn btn-amber" href="karte">Karte &amp; Bestellen</a><a class="btn btn-ghost" href="#besuch">Tisch reservieren</a></div>
  <button class="burger" id="burger" aria-label="Menü"><i></i><i></i></button>
</header>
<nav class="sheet" id="sheet">
  <a href="#ueber">Über uns</a><a href="#speisekarte">Speisekarte</a><a href="#bestellen">Bestellen</a><a href="#system">GastrOptima</a><a href="karte">Karte &amp; Bestellen</a><a href="#besuch">Reservieren &amp; Zeiten</a>
</nav>

<!-- ============ HERO ============ -->
<section class="hero" id="top" data-scene>
  <div class="hero-stage">
    <div class="hero-bgtext" id="bgtext" aria-hidden="true">VAI</div>
    <div class="hero-frame" id="frame">
      <div class="slide"><picture><source media="(max-width:760px)" srcset="assets/fruehstueck.webp"><img src="assets/banner-fruehstueck-echt.webp" alt="Serpme-Frühstück im Café VAI" width="1100" height="578" fetchpriority="high"></picture></div>
      <div class="slide"><picture><source media="(max-width:760px)" srcset="assets/burger.webp"><img src="assets/og-burger.jpg" alt="Dobi's SmashBurger" width="1200" height="630"></picture></div>
      <div class="slide"><img src="assets/tenders-og.webp" alt="Crispy Tenders mit Dips" width="721" height="540" style="object-position:50% 55%"></div>
      <div class="slide"><img src="assets/banner-drinks-stock.webp" alt="Cappuccino mit Latte Art" width="1100" height="423" style="object-position:45% 50%"></div>
    </div>
    <div class="hero-caps" id="caps">
      <div class="cap"><span class="eyebrow">Sa &amp; So · ab 9 Uhr</span><div class="hero-word">Früh<em>stück</em></div><p>Das VAI Serpme Kahvaltı: türkisches Frühstück, das den ganzen Tisch füllt.</p><span class="chip">für zwei Personen <b>38,90 €</b></span></div>
      <div class="cap"><span class="eyebrow">Fr · Sa · So</span><div class="hero-word">Smash<em>Burger</em></div><p>140 g Rind, Spiegelei, Pastırma, Jalapeños — Dobi's Signature.</p><span class="chip">ab <b>11,90 €</b> · Menü <b>19,90 €</b></span></div>
      <div class="cap"><span class="eyebrow">100 % Hähnchenfilet</span><div class="hero-word">Crispy <em>Tenders</em></div><p>OG's oder Natural Crunchy, mit fünf Dips zum Teilen.</p><span class="chip">4 Stück <b>5,90 €</b></span></div>
      <div class="cap"><span class="eyebrow">Meet for coffee</span><div class="hero-word">Kaffee <em>&amp; Drinks</em></div><p>Vom Espresso bis zum Aperol Spritz — bleib auf einen zweiten.</p><span class="chip">Crema ab <b>2,80 €</b> · Spritz <b>7,50 €</b></span></div>
    </div>
    <div class="count" id="count"><b>01</b> / 04</div>
    <div class="ticks" id="ticks"><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i></div>
    <div class="hero-intro" id="intro">
      <h1>Café VAI</h1>
      <p>Kaffee · Frühstück · SmashBurger · Drinks</p>
    </div>
    <div class="hint" id="hint" style="position:absolute;right:var(--pad);bottom:4vh;z-index:6"><div class="mouse"></div>Scrollen</div>
  </div>
</section>

<!-- ============ ÜBER UNS ============ -->
<section class="intro" id="ueber">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <span class="eyebrow">Über uns</span>
        <p class="fill" id="fill" style="margin-top:18px" data-text="Ein Ort zum *Durchatmen.* Kaffee am Morgen, Serpme-Frühstück am Wochenende, SmashBurger am Abend — allein, mit Freunden oder der ganzen Familie. *Meet for coffee, stay for more.*"></p>
      </div>
      <figure><img src="assets/team.webp" alt="Barista im Café VAI" loading="lazy" id="parimg" width="760" height="950"><figcaption>Stuttgarter Straße 36 · Vaihingen an der Enz</figcaption></figure>
    </div>
    <div class="facts">
      <div class="fact"><b data-count="6">6</b><span>Burger — vom Veggie bis zum Bestseller</span></div>
      <div class="fact"><b>Fr–So</b><span>vor Ort geöffnet, dienstags bis sonntags Lieferservice</span></div>
      <div class="fact"><b data-count="38.9" data-dec="2" data-suf=" €">38,90 €</b><span>Serpme-Frühstück für zwei</span></div>
      <div class="fact"><b data-count="5" data-dec="1" data-suf=" ★">5,0 ★</b><span>in den Google-Bewertungen auf der Website</span></div>
    </div>
  </div>
</section>

<!-- ============ SPEISEKARTE (horizontal) ============ -->
<section class="menu-sec" id="speisekarte" data-scene>
  <div class="hmenu-stage">
    <div class="hmenu-track" id="track">
      <article class="panel lead">
        <span class="eyebrow">Speisekarte</span>
        <h2>Von früh<br>bis <em>spät.</em></h2>
        <p>Scroll weiter — die Karte läuft seitwärts. Alle Preise von Café VAI, vor Ort Fr–So.</p>
        <div class="arrow"><i></i> Weiter scrollen</div>
        <a class="btn btn-amber" href="karte" style="margin-top:22px;align-self:flex-start">Direkt zur Karte &amp; bestellen →</a>
      </article>
      {''.join(panels)}
      <div style="flex:0 0 8vw"></div>
    </div>
    <div class="hprog" id="hprog"></div>
  </div>
</section>

<!-- ============ SPOTLIGHT ============ -->
<section class="spot" id="spot">
  <div class="spot-bg" id="spotbg"><img src="assets/banner-fruehstueck-echt.webp" alt="" loading="lazy" width="1100" height="578"></div>
  <div class="spot-in"><div class="wrap">
    <span class="eyebrow">Das Wochenend-Ritual</span>
    <h2>Serpme<br><em>Kahvaltı.</em></h2>
    <p>Kleine Teller, frisches Brot, Menemen, Sucuk mit Ei, Oliven, Käse und ein Kännchen Tee — serviert, bis nichts mehr auf den Tisch passt.</p>
    <div class="price-big"><b>38,90 €</b><span>für 2 Personen · Sa &amp; So 9–12:30 Uhr</span></div>
    <a class="btn btn-amber" href="#besuch">Tisch fürs Frühstück sichern</a>
  </div></div>
</section>

<!-- ============ BESTELLEN (phone story) ============ -->
<section class="story" id="bestellen" data-scene>
  <div class="story-stage">
    <div class="wrap story-grid">
      <div>
        <span class="eyebrow">Direkt bestellen · GastrOptima Baustein 1</span>
        <h2>Vom Display<br>in die <em>Küche.</em></h2>
        <ol class="steps" id="steps">
          <li class="step on"><span class="n">01</span><div><h3>Gast wählt im Web-Menü</h3><p>Die Speisekarte ist die Bestellseite. Kein Konto, keine App, keine Installation.</p></div></li>
          <li class="step"><span class="n">02</span><div><h3>Warenkorb mit Mindestbestellwert</h3><p>Summe, Mindestbestellwert und Abholzeit sind sofort klar — ohne Rückfragen.</p></div></li>
          <li class="step"><span class="n">03</span><div><h3>Bestellung landet in WhatsApp</h3><p>Fertig formatiert, mit Name und Zeit. Die Gäste sind schon da, wo sie ohnehin schreiben.</p></div></li>
          <li class="step"><span class="n">04</span><div><h3>Küchen-Tablet schlägt Alarm</h3><p>Push-Benachrichtigung mit eigenem Ton, Bildschirm bleibt an. Nichts geht unter.</p></div></li>
        </ol>
        <div class="badges"><span class="badge"><b>0 %</b> Provision pro Bestellung</span><span class="badge">statt 13–30 % bei klassischen Lieferdiensten</span></div>
        <p style="margin-top:22px"><a class="btn btn-amber" href="karte">Jetzt selbst ausprobieren: Karte &amp; Bestellen →</a></p>
      </div>
      <div class="phone-col" style="perspective:1400px">
        <div class="phone" id="phone"><div class="screen-wrap">

          <div class="screen on" data-i="0">
            <div class="s-title">Speisekarte</div><div class="s-sub">Café VAI · Abholung &amp; Lieferung</div>
            <div class="mrow hit"><span>Dobi's Burger Signature<small>Rind, Ei, Pastırma, Jalapeños</small></span><em>ab 15,90 €</em><i class="plus">+</i></div>
            <div class="mrow"><span>Chili Cheese Burger</span><em>13,90 €</em><i class="plus">+</i></div>
            <div class="mrow"><span>Hot Honey Crispy Chicken</span><em>13,90 €</em><i class="plus">+</i></div>
            <div class="mrow"><span>Tenders · 8 Stück<small>mit Dip</small></span><em>11,90 €</em><i class="plus">+</i></div>
            <div class="mrow"><span>Süßkartoffel-Pommes</span><em>5,90 €</em><i class="plus">+</i></div>
          </div>

          <div class="screen" data-i="1">
            <div class="s-title">Dein Warenkorb</div><div class="s-sub">3 Positionen</div>
            <div class="cart-line"><span><b>2×</b> Dobi's Burger Signature</span><em>31,80 €</em></div>
            <div class="cart-line"><span><b>1×</b> Süßkartoffel-Pommes</span><em>5,90 €</em></div>
            <div class="cart-line"><span><b>1×</b> Tenders · 8 Stück</span><em>11,90 €</em></div>
            <div class="total">
              <div class="okline"><span>✓ Mindestbestellwert 25 € erreicht</span></div>
              <div><span>Abholung</span><span>heute 18:30</span></div>
              <div class="sum"><span>Summe</span><em>49,60 €</em></div>
              <span class="cta-fake">Per WhatsApp bestellen</span>
            </div>
          </div>

          <div class="screen" data-i="2">
            <div class="wa-head"><i></i><div><b>Café VAI</b><small>online</small></div></div>
            <div class="bubble"><b>Neue Bestellung</b><br>2× Dobi's Burger Signature<br>1× Süßkartoffel-Pommes<br>1× Tenders (8 Stk.)<br><b>Summe: 49,60 €</b><br>Abholung: 18:30 · Name: Demo-Gast<div class="ticks2">✓✓</div></div>
            <div class="reply">Danke! Bestellung ist da — fertig um 18:30 ✓</div>
          </div>

          <div class="screen kitchen" data-i="3">
            <div class="alarm">🔔</div>
            <div class="k-h">Neue Bestellung #014</div><div class="k-s">gerade eben · Abholung 18:30</div>
            <div class="k-card"><div><span>2× Dobi's Burger Signature</span></div><div><span>1× Süßkartoffel-Pommes</span></div><div><span>1× Tenders (8 Stk.)</span></div><div class="t"><span>Summe</span><span>49,60 €</span></div></div>
            <span class="k-btn">Annehmen</span>
          </div>

        </div></div>
      </div>
    </div>
  </div>
</section>

<!-- ============ BAUSTEINE ============ -->
<section class="bs" id="system">
  <div class="wrap">
    <div class="bs-head">
      <h2>Das System<br>dahinter: <em>GastrOptima.</em></h2>
      <p>Drei Bausteine für Gastronomiebetriebe — gebaut von Menschen, die Küche und IT kennen. Diese Demo zeigt Baustein 1 mit den echten Karten- und Preisdaten von Café VAI.</p>
    </div>
    <div class="cards">
      <div class="card"><span class="st">Baustein 1 · live in dieser Demo</span><h3>Bestellsystem</h3><div class="nut">Mehr Umsatz.</div><p>Aus der Speisekarte wird ein Bestellkanal — ohne Provision an Dritte.</p><ul><li>Web-Menü ohne Konto und App</li><li>Bestellung als fertige WhatsApp-Nachricht</li><li>Küchen-Tablet mit Alarmton</li></ul></div>
      <div class="card"><span class="st">Baustein 2 · neu</span><h3>Kosten-Check</h3><div class="nut">Weniger Kosten.</div><p>Lieferantenrechnungen im Blick behalten — Preisänderungen fallen auf, bevor sie die Marge fressen.</p><ul><li>Rechnungen prüfen statt abheften</li><li>Auffällige Preissprünge sichtbar</li><li>Pilotphase läuft</li></ul></div>
      <div class="card"><span class="st">Baustein 3 · neu</span><h3>Belegvorbereitung</h3><div class="nut">Mehr Zeit.</div><p>Belege sammeln, ordnen und für den Steuerberater bereitstellen — damit der Monatsabschluss kein Wochenende kostet.</p><ul><li>Belege sauber vorsortiert</li><li>Übergabe an den Steuerberater</li><li>Ersetzt keine Steuerberatung</li></ul></div>
    </div>
    <div class="pack"><span><b>Basis</b> (1)</span>·<span><b>Plus</b> (1+2)</span>·<span><b>Premium</b> (1+2+3)</span></div>
  </div>
</section>

<!-- ============ BESUCH ============ -->
<section class="visit" id="besuch">
  <div class="wrap">
    <span class="eyebrow">Besuch</span>
    <h2 style="margin-top:14px">Komm vorbei.<br><em>Wir halten dir einen Platz frei.</em></h2>
    <div class="visit-grid">
      <div class="box">
        <h3>Zeiten &amp; Anfahrt</h3>
        <div class="status" id="status"><i></i><span id="statustxt">…</span></div>
        <table class="hours" id="hours">
          <tr data-d="1"><td>Montag</td><td>Ruhetag</td></tr>
          <tr data-d="2"><td>Dienstag</td><td>Lieferservice</td></tr>
          <tr data-d="3"><td>Mittwoch</td><td>Lieferservice</td></tr>
          <tr data-d="4"><td>Donnerstag</td><td>Lieferservice</td></tr>
          <tr data-d="5"><td>Freitag</td><td>11–14 · 17–22 Uhr</td></tr>
          <tr data-d="6"><td>Samstag</td><td>9–14 · 17–22 Uhr</td></tr>
          <tr data-d="0"><td>Sonntag</td><td>9–20 Uhr</td></tr>
        </table>
        <p class="note">Café VAI · Stuttgarter Straße 36, 71665 Vaihingen an der Enz<br>Tel. +49 7042 1204640 · WhatsApp +49 179 1564135</p>
        <p style="margin-top:18px"><a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&amp;query=Caf%C3%A9+VAI+Stuttgarter+Stra%C3%9Fe+36+Vaihingen+an+der+Enz" target="_blank" rel="noopener">Route planen ↗</a></p>
        <div class="revs">
          <div class="rev"><span class="s">★★★★★</span>Burger, Pommes, freundliches Team — Gäste schwärmen besonders von den Süßkartoffel-Pommes.</div>
        </div>
      </div>
      <div class="box" id="res">
        <h3>Tisch reservieren</h3>
        <div class="fld"><label>Tag</label><div class="chips" id="days"><button class="on" data-d="5">Freitag</button><button data-d="6">Samstag</button><button data-d="0">Sonntag</button></div></div>
        <div class="fld"><label>Uhrzeit</label><div class="chips" id="times"></div></div>
        <div class="fld"><label>Personen</label><div class="stepper"><button id="minus" aria-label="weniger">−</button><output id="pers">2 Pers.</output><button id="plus" aria-label="mehr">+</button></div></div>
        <button class="btn btn-amber" id="resbtn">Reservierung anfragen</button>
        <p class="note">Ab 8 Personen bitte anrufen oder per WhatsApp schreiben.</p>
        <div class="toast" id="toast"></div>
      </div>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Meet for coffee.<br><em style="color:var(--amber)">Stay for more.</em></h2>
    <p>So fühlt sich eine Website an, die so gut ist wie der Laden. Gebaut mit GastrOptima.</p>
    <div class="row"><a class="btn btn-amber" href="#besuch">Tisch reservieren</a><a class="btn btn-ghost" href="#bestellen">Bestellung ansehen</a></div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="fgrid">
      <div><div class="fbrand"><img src="assets/logo-disc.png" alt="" width="56" height="56"><b>Café VAI</b></div><p>Kaffee · Frühstück · SmashBurger · Drinks<br>in Vaihingen an der Enz.</p></div>
      <div><h4>Kontakt</h4><ul><li>Stuttgarter Straße 36</li><li>71665 Vaihingen an der Enz</li><li><a href="tel:+4970421204640">+49 7042 1204640</a></li><li><a href="mailto:vayvay@cafevai.de">vayvay@cafevai.de</a></li></ul></div>
      <div><h4>Folgen</h4><ul><li><a href="https://instagram.com/cafe_vai" target="_blank" rel="noopener">Instagram @cafe_vai</a></li><li><a href="#besuch">Reservieren</a></li><li><a href="#bestellen">Bestellen</a></li><li><a href="karte">Karte &amp; Bestellen</a></li><li><a href="qr.html">Tischaufsteller</a></li></ul></div>
      <div><h4>Rechtliches</h4><ul><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li></ul></div>
    </div>
    <div class="legal"><span>Demo-Entwurf · nicht die offizielle Website von Café VAI</span><span>Gebaut von <a href="https://www.hasi-elektronic.de" target="_blank" rel="noopener">Hasi Elektronic</a> mit <a href="https://gastroptima.de" target="_blank" rel="noopener">GastrOptima</a></span></div>
  </div>
</footer>

<div class="rosette">Demo · GastrOptima</div>
<div class="dock" id="dock"><a class="d-karte" href="karte">Karte &amp; Bestellen</a><a class="d-res" href="#besuch">Reservieren</a><a class="d-tel" href="tel:+4970421204640" aria-label="Anrufen">☎</a></div>
<script src="script.js" defer></script>
</body>
</html>
'''
(out / "index.html").write_text(index, encoding="utf-8")

def legal(title, body):
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Café VAI Demo</title><meta name="robots" content="noindex,nofollow"><link rel="icon" href="assets/favicon.png"><link rel="stylesheet" href="style.css"></head>
<body><header class="nav solid"><a class="brand" href="index.html"><img src="assets/logo-disc.png" alt="" width="40" height="40"><span>Café VAI<small>DEMO</small></span></a><a class="btn btn-ghost" href="index.html">← Zurück</a></header>
<main class="doc"><h1>{title}</h1>{body}</main></body></html>'''

imp = '''
<p><b>Dies ist ein Demo-Entwurf</b> und nicht die offizielle Website von Café VAI. Er zeigt, wie eine Website mit dem Bestellsystem GastrOptima aussehen kann. Er ist für Suchmaschinen gesperrt.</p>
<h2>Anbieter dieser Demo</h2>
<p>Hasi Elektronic · Hamdi Güncavdı<br>Grabenstraße 18, 71665 Vaihingen an der Enz<br>Tel. 07042 / 16391 · info@hasi-elektronic.de<br>USt-IdNr.: DE367591246</p>
<h2>Herkunft der Inhalte</h2>
<p>Name, Speisekarte, Preise, Zeiten und Fotos stammen von der öffentlichen Website <a href="https://cafevai.de">cafevai.de</a> (Café VAI, Stuttgarter Straße 36, 71665 Vaihingen an der Enz). Die Rechte an Fotos, Logo und Texten liegen bei den jeweiligen Inhabern. Wir entfernen sie auf Wunsch umgehend.</p>
<p>Die Bestellungen, Reservierungen und der Warenkorb in dieser Demo sind <b>nur Vorführung</b>: Es werden keine Bestellungen oder Reservierungen übermittelt. Alle Preise bitte direkt beim Café bestätigen.</p>
<h2>Hinweis</h2>
<p>Rechtstexte sind Vorlagen und vor einem Echtbetrieb rechtlich zu prüfen.</p>'''
dat = '''
<p>Diese Demo erhebt <b>keine personenbezogenen Daten</b>. Es gibt keine Cookies, kein Tracking, keine Analyse-Werkzeuge und keine Einbindung von Drittanbietern (Schriften werden lokal geladen).</p>
<h2>Eingaben im Formular</h2>
<p>Die Reservierungs- und Bestell-Elemente sind reine Vorführung. Eingaben werden nicht gesendet und nicht gespeichert.</p>
<h2>Hosting</h2>
<p>Die Seite wird bei Cloudflare, Inc. gehostet. Dabei werden technisch notwendige Verbindungsdaten (z. B. IP-Adresse) kurzzeitig in Server-Logs verarbeitet (Art. 6 Abs. 1 lit. f DSGVO).</p>
<h2>Externe Links</h2>
<p>Links zu Google Maps und Instagram führen erst beim Anklicken zu den Diensten. Dort gelten deren Datenschutzbestimmungen.</p>
<h2>Verantwortlich &amp; Rechte</h2>
<p>Hasi Elektronic, Grabenstraße 18, 71665 Vaihingen an der Enz, info@hasi-elektronic.de. Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung und Widerspruch sowie auf Beschwerde bei einer Aufsichtsbehörde.</p>
<p>Rechtstexte sind Vorlagen und vor einem Echtbetrieb rechtlich zu prüfen.</p>'''
(out / "impressum.html").write_text(legal("Impressum", imp), encoding="utf-8")
(out / "datenschutz.html").write_text(legal("Datenschutz", dat), encoding="utf-8")
(out / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
(out / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n")
print("ok")
