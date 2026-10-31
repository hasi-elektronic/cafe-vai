#!/usr/bin/env python3
"""Baut karte.html (QR-Speisekarte) nach dem Vorbild der Goya's-Lamm-Karte.
Alle Inhalte stammen von cafevai.de (Oktober 2026). Ausgabe: <ziel>/karte.html"""
import sys, json, html, pathlib
out = pathlib.Path(sys.argv[1])
esc = lambda s: html.escape(s, quote=True)

# ---------- UI-Texte (DE / EN / TR) ----------
UI = {
 "title": ("Speisekarte", "Menu", "Menü"),
 "sub": ("Vor Ort · Freitag bis Sonntag", "Dine-in · Friday to Sunday", "Mekânda · Cuma - Pazar"),
 "search": ("Gericht oder Getränk suchen …", "Search dishes or drinks …", "Yemek veya içecek ara …"),
 "best": ("Bestseller", "Bestseller", "Çok satan"), "veg": ("vegetarisch", "vegetarian", "vejetaryen"),
 "home": ("hausgemacht", "homemade", "ev yapımı"), "u10": ("unter 10 €", "under €10", "10 € altı"),
 "sig": ("Signature", "Signature", "İmza lezzet"),
 "count": ("{v} von {t} Positionen", "{v} of {t} items", "{t} üründen {v} tanesi"),
 "hidden": ("{h} ausgeblendet", "{h} hidden", "{h} gizli"),
 "none": ("Nichts gefunden — probier einen anderen Begriff.", "Nothing found — try another word.", "Sonuç yok — başka bir kelime dene."),
 "allergen": ("Allergene und Zusatzstoffe: Bitte fragen Sie uns — wir sagen es Ihnen gern.",
              "Allergens and additives: please ask us — we are happy to tell you.",
              "Alerjenler ve katkı maddeleri: lütfen bize sorun, memnuniyetle söyleriz."),
 "menu": ("Menü", "Meal", "Menü"), "single": ("Einzeln", "Single", "Tek"),
 "small": ("Klein", "Small", "Küçük"), "large": ("Groß", "Large", "Büyük"),
 "add": ("Zur Auswahl", "Add to my list", "Listeme ekle"), "added": ("Hinzugefügt", "Added", "Eklendi"),
 "share": ("Teilen", "Share", "Paylaş"), "copied": ("Link kopiert", "Link copied", "Bağlantı kopyalandı"),
 "close": ("Schließen", "Close", "Kapat"), "sort": ("Sorte", "Variety", "Çeşit"),
 "mylist": ("Meine Auswahl", "My list", "Listem"), "pos": ("Positionen", "items", "ürün"),
 "view": ("Ansehen", "View", "Gör"), "table": ("Tisch-Nr.", "Table no.", "Masa no."),
 "total": ("Summe", "Total", "Toplam"), "show": ("Dem Service zeigen", "Show to staff", "Servise göster"),
 "send": ("An die Küche senden (Demo)", "Send to kitchen (demo)", "Mutfağa gönder (demo)"),
 "empty": ("Noch nichts ausgewählt. Tippen Sie auf + bei einem Gericht.", "Nothing selected yet. Tap + on any item.", "Henüz seçim yok. Bir ürünün yanındaki + simgesine dokunun."),
 "slipnote": ("Bitte dem Service zeigen — der Preis versteht sich laut Karte.", "Please show this to our staff.", "Lütfen servis personeline gösterin."),
 "sent": ("Demo: In der Live-Version landet diese Bestellung als Alarm auf dem Küchen-Tablet.",
          "Demo: in the live version this order triggers an alarm on the kitchen tablet.",
          "Demo: Canlı sürümde bu sipariş mutfak tabletinde alarm olarak görünür."),
 "print": ("Papierkarte drucken", "Print paper menu", "Kâğıt menüyü yazdır"),
 "back": ("Zur Website", "Back to site", "Siteye dön"),
 "open_b": ("Frühstück läuft gerade", "Breakfast is being served", "Kahvaltı şu an servis ediliyor"),
 "open_a": ("Frühstück: Sa & So 9–12:30 Uhr", "Breakfast: Sat & Sun 9–12:30", "Kahvaltı: Cts & Paz 9–12:30"),
 "foot": ("Preise und Angebot nach cafevai.de (Oktober 2026), bitte vor Ort bestätigen. Fotos: Café VAI. Demo-Entwurf von Hasi Elektronic mit GastrOptima.",
          "Prices and offer as on cafevai.de (October 2026), please confirm on site. Photos: Café VAI. Demo by Hasi Elektronic with GastrOptima.",
          "Fiyatlar ve menü cafevai.de'ye göredir (Ekim 2026), lütfen mekânda doğrulayın. Fotoğraflar: Café VAI. Hasi Elektronic ve GastrOptima demosu."),
}
def U(k, cls="", tag="span"):
    de, en, tr = UI[k]
    return f'<{tag} class="i {cls}" data-en="{esc(en)}" data-tr="{esc(tr)}">{esc(de)}</{tag}>'

# ---------- Karte ----------
def I(id, de, en=None, tr=None, d=None, v=None, c=None, o=None, img=None, b=(), nm=None):
    return dict(id=id, name=dict(de=de, en=en or de, tr=tr or de), desc=d, vars=v, c=c, opts=o, imgs=img, badges=list(b))
D = lambda de, en, tr: dict(de=de, en=en, tr=tr)
MENU = lambda m, s: [("menu", m), ("single", s)]

CATS = [
 dict(id="fruehstueck", t=D("Frühstück","Breakfast","Kahvaltı"), img=("banner-fruehstueck-echt.webp","50% 55%"),
  note=D("Samstag und Sonntag, 9–12:30 Uhr · nur vor Ort","Saturday and Sunday, 9–12:30 · dine-in only","Cumartesi ve Pazar, 9–12:30 · yalnızca mekânda"),
  groups=[dict(t=None, items=[
   I("schnelles-fruehstueck","Schnelles Frühstück","Quick breakfast","Hızlı kahvaltı",D("mit Heißgetränk","with a hot drink","sıcak içecek ile"),c=1390),
   I("serpme","VAI Serpme Kahvaltı",None,None,D("Türkisches Frühstück zum Teilen, für 2 Personen","Turkish breakfast to share, for 2 people","2 kişilik, paylaşmalık Türk kahvaltısı"),c=3890,img=[("fruehstueck.webp","50% 72%")],b=["sig"]),
   I("weitere-person","Jede weitere Person","Each additional person","Her ilave kişi",c=1690),
   I("kinder","Kinder 7–12 Jahre","Children 7–12","Çocuk 7–12 yaş",c=890),
  ]),
  dict(t=D("Extras","Extras","Ekstralar"), items=[
   I("aufstrich","Aufstrich / Oliven","Spreads / olives","Ezme / zeytin",c=300),
   I("menemen","Menemen",c=500), I("sucuk-ei","Sucuk mit Ei","Sucuk with egg","Sucuklu yumurta",c=550),
   I("menemen-sucuk","Menemen & Sucuk",c=600),
   I("tee-kaennchen","Kännchen Tee","Pot of tea","Demlik çay",c=650),
  ])]),
 dict(id="burger", t=D("SmashBurger","SmashBurger","SmashBurger"), img=("banner-burger.webp","50% 40%"),
  note=D("Menü = Burger mit Pommes und 0,33 l Softdrink","Meal = burger with fries and 0.33 l soft drink","Menü = patates kızartması ve 0,33 l meşrubat ile"),
  groups=[dict(t=None, items=[
   I("dobis-smashburger","Dobi's SmashBurger",None,None,D("140 g Rind, Spiegelei, Pastırma, Jalapeños, Haussauce","140 g beef, fried egg, pastırma, jalapeños, house sauce","140 g dana, sahanda yumurta, pastırma, jalapeño, ev sosu"),v=MENU(1990,1190),img=[("burger.webp","50% 78%")],b=["best"]),
   I("chicken-hot-honey","Chicken Hot Honey",v=MENU(1890,1090)),
   I("cheeseburger","Cheeseburger",v=MENU(1750,950)),
   I("chickenburger","Chickenburger",v=MENU(1750,950)),
   I("hamburger","Hamburger",v=MENU(1650,850)),
   I("veggieburger","Veggieburger",v=MENU(1650,750),b=["veg"]),
  ]),
  dict(t=D("Beilagen","Sides","Yanlar"), items=[
   I("pommes","Pommes","Fries","Patates kızartması",c=450),
   I("suesskartoffel","Süßkartoffel-Pommes","Sweet potato fries","Tatlı patates kızartması",D("als Menü-Upgrade +1,50 €","as meal upgrade +€1.50","menüde +1,50 € fark"),c=550),
  ]),
  dict(t=D("Extras zum Burger","Burger extras","Burger ekstraları"), items=[
   I("spiegelei","Spiegelei","Fried egg","Sahanda yumurta",c=100), I("kaese","Käse","Cheese","Peynir",c=100),
   I("pastirma","Pastırma",c=150), I("jalapenos","Jalapeños",c=50),
   I("extra-patty","Extra Patty (70 g)",c=300),
  ])]),
 dict(id="tenders", t=D("Tenders","Tenders","Tenders"), img=("tenders-crunchy.webp","50% 50%"),
  note=D("100 % Hähnchenfilet · Menü mit Pommes, Dip und Softdrink","100 % chicken fillet · meal with fries, dip and soft drink","%100 tavuk fileto · menü: patates, sos ve meşrubat ile"),
  groups=[dict(t=None, items=[
   I("tenders-4","4 Stück","4 pieces","4 adet",v=[("single",590),("menu",1090)],o=["OG's","Natural Crunchy"],img=[("tenders-og.webp","50% 50%"),("tenders-crunchy.webp","50% 50%")]),
   I("tenders-8","8 Stück","8 pieces","8 adet",v=[("single",990),("menu",1590)],o=["OG's","Natural Crunchy"],img=[("tenders-og.webp","50% 50%"),("tenders-crunchy.webp","50% 50%")]),
   I("tenders-12","12 Stück","12 pieces","12 adet",v=[("single",1390),("menu",2090)],o=["OG's","Natural Crunchy"],img=[("tenders-og.webp","50% 50%"),("tenders-crunchy.webp","50% 50%")]),
  ])],
  foot=D("Sorten: OG's (zart, würzig paniert) oder Natural Crunchy (extra knusprig). Dips: Dobi's Sauce, Sweet & Sour, Ketchup, Mayo, Hot Honey.",
         "Varieties: OG's (tender, savoury breading) or Natural Crunchy (extra crispy). Dips: Dobi's sauce, sweet & sour, ketchup, mayo, hot honey.",
         "Çeşitler: OG's (yumuşak, baharatlı kaplama) veya Natural Crunchy (ekstra çıtır). Soslar: Dobi's sos, tatlı-ekşi, ketçap, mayonez, acı bal.")),
 dict(id="kaffee", t=D("Kaffee & Tee","Coffee & Tea","Kahve & Çay"), img=("banner-drinks-stock.webp","46% 50%"),
  note=D("Meet for coffee, stay for more.","Meet for coffee, stay for more.","Meet for coffee, stay for more."),
  groups=[dict(t=None, items=[
   I("kaffee-crema","Kaffee Crema","Filter coffee crema","Kaffee Crema",v=[("small",280),("large",480)]),
   I("espresso","Espresso",c=200), I("espresso-doppio","Espresso Doppio",c=380), I("espresso-macchiato","Espresso Macchiato",c=240),
   I("cappuccino","Cappuccino",c=380,img=[("banner-drinks-stock.webp","46% 50%")]),
   I("latte-macchiato","Latte Macchiato",c=420), I("milchkaffee","Milchkaffee","Café au lait","Sütlü kahve",c=420),
   I("kaffee-coco","Kaffee Coco",c=450), I("heisse-schokolade","Heiße Schokolade","Hot chocolate","Sıcak çikolata",c=350),
   I("tee","Teesorten","Teas","Çay çeşitleri",c=250),
   I("tuerkischer-tee","Türkischer Tee","Turkish tea","Türk çayı",c=150),
   I("tee-kanne","Türkisches Teekännchen","Turkish tea pot","Türk çay demliği",D("für bis zu 3 Personen","for up to 3 people","en fazla 3 kişilik"),c=850),
  ])]),
 dict(id="spritz", t=D("Spritz & Longdrinks","Spritz & Longdrinks","Spritz & Longdrink"), img=("kaffee.webp","50% 28%"),
  note=D("Fr · Sa · So","Fri · Sat · Sun","Cum · Cmt · Paz"),
  groups=[dict(t=D("Spritz","Spritz","Spritz"), items=[
   I("aperol","Aperol Spritz",c=750), I("lillet","Lillet",c=750), I("sarti","Sarti",c=750), I("roseano","Roseano",c=590)]),
  dict(t=D("Longdrinks","Longdrinks","Longdrink"), items=[
   I("gin-tonic","Gin & Tonic",c=750), I("jack-cola","Jack Daniel's & Cola",c=750),
   I("vodka-bull","Vodka Bull",c=750), I("vodka-lemon","Vodka Lemon",c=750), I("campari-orange","Campari Orange",c=750)])]),
 dict(id="bier", t=D("Bier","Beer","Bira"), img=None, note=D("0,33 l und 0,5 l","0.33 l and 0.5 l","0,33 l ve 0,5 l"),
  groups=[dict(t=None, items=[
   I("cluss-kellerpils","Cluss Kellerpils",d=D("0,33 l","0.33 l","0,33 l"),c=360), I("cluss-radler","Cluss Radler",d=D("0,33 l","0.33 l","0,33 l"),c=360),
   I("hefeweizen","Hefeweizen",d=D("0,5 l","0.5 l","0,5 l"),c=390), I("kristallweizen","Kristallweizen",d=D("0,5 l","0.5 l","0,5 l"),c=390),
   I("corona","Corona",c=420), I("desperados","Desperados",c=420)])]),
 dict(id="alkoholfrei", t=D("Alkoholfrei","Soft drinks","Alkolsüz"), img=None, note=D("Hausgemachtes aus der eigenen Küche","Homemade from our own kitchen","Kendi mutfağımızdan ev yapımı"),
  groups=[dict(t=None, items=[
   I("limonade","Hausgemachte Limonade","Homemade lemonade","Ev yapımı limonata",D("0,5 l","0.5 l","0,5 l"),c=490,b=["home"]),
   I("eistee","Hausgemachter Eistee","Homemade iced tea","Ev yapımı buzlu çay",D("0,5 l","0.5 l","0,5 l"),c=490,b=["home"]),
   I("cola","Coca-Cola","Coca-Cola","Coca-Cola",D("0,33 l","0.33 l","0,33 l"),c=390), I("cola-zero","Coca-Cola Zero",d=D("0,33 l","0.33 l","0,33 l"),c=390),
   I("fanta","Fanta",d=D("0,33 l","0.33 l","0,33 l"),c=390), I("sprite","Sprite",d=D("0,33 l","0.33 l","0,33 l"),c=390), I("mezzo-mix","Mezzo-Mix",d=D("0,33 l","0.33 l","0,33 l"),c=390),
   I("ensinger-still","Ensinger Still","Ensinger still","Ensinger Still",D("0,25 l · 0,5 l","0.25 l · 0.5 l","0,25 l · 0,5 l"),v=[("small",280),("large",470)]),
   I("ensinger-classic","Ensinger Classic",d=D("0,25 l · 0,5 l","0.25 l · 0.5 l","0,25 l · 0,5 l"),v=[("small",280),("large",470)]),
   I("red-bull","Red Bull",d=D("0,25 l","0.25 l","0,25 l"),c=400)])]),
]

def eur(c): return f"{c//100},{c%100:02d} €"
def price_html(it):
    if it["vars"]:
        pills = "".join(
            f'<button type="button" class="vp{" on" if i == 0 else ""}" data-v="{k}" aria-pressed="{"true" if i == 0 else "false"}"><small>{U(k)}</small><b>{eur(c)}</b></button>'
            for i, (k, c) in enumerate(it["vars"]))
        return f'<span class="pv vsel">{pills}</span>'
    return f'<span class="pv"><span class="pp"><b>{eur(it["c"])}</b></span></span>'
def minc(it): return min(c for _, c in it["vars"]) if it["vars"] else it["c"]
def tag(it, k): return k in it["badges"]

# Daten fürs Skript (ohne Duplikate im HTML)
DATA = {"cats": [], "ui": {k: dict(de=v[0], en=v[1], tr=v[2]) for k, v in UI.items()}}
total = 0
body = []
tabs = []
for ci, cat in enumerate(CATS):
    DATA["cats"].append(dict(id=cat["id"], t=cat["t"]))
    tabs.append(f'<a href="#{cat["id"]}" data-c="{cat["id"]}"><span class="i" data-en="{esc(cat["t"]["en"])}" data-tr="{esc(cat["t"]["tr"])}">{esc(cat["t"]["de"])}</span></a>')
    ghtml = ""
    for g in cat["groups"]:
        lis = ""
        for it in g["items"]:
            total += 1
            it["c"] = it["c"] if it["c"] is not None else None
            it["cat"] = cat["id"]
            has_detail = bool(it["desc"] or it["imgs"] or it["vars"] or it["opts"])
            n = it["name"]
            name = f'<span class="i nm" data-en="{esc(n["en"])}" data-tr="{esc(n["tr"])}">{esc(n["de"])}</span>'
            desc = ""
            if it["desc"]:
                dd = it["desc"]; desc = f'<span class="i ds" data-en="{esc(dd["en"])}" data-tr="{esc(dd["tr"])}">{esc(dd["de"])}</span>'
            badges = "".join(f'<em class="bd b-{k}">{U(k)}</em>' for k in it["badges"])
            thumb = ""
            if it["imgs"]:
                f, pos = it["imgs"][0]
                thumb = f'<span class="th"><img src="assets/{f}" alt="" loading="lazy" style="object-position:{pos}"></span>'
            big = " big" if (it["imgs"] and not it["opts"] and it["badges"]) or it["id"] in ("tenders-8",) else ""
            lis += (f'<li class="it{big}" data-id="{it["id"]}" data-p="{minc(it)}" data-b="{" ".join(it["badges"])}">'
                    f'<button class="open" type="button" data-open="{it["id"]}" aria-label="{esc(n["de"])}">{thumb}'
                    f'<span class="tx"><span class="l1">{name}{badges}</span>{desc}</span></button>'
                    f'{price_html(it)}'
                    f'<button class="add" type="button" data-add="{it["id"]}" aria-label="+"><span>+</span></button></li>\n')
            DATA.setdefault("items", {})[it["id"]] = dict(id=it["id"], name=n, desc=it["desc"], vars=it["vars"], c=it["c"], opts=it["opts"], imgs=it["imgs"], badges=it["badges"], cat=cat["id"])
        gt = ""
        if g["t"]:
            gt = f'<h3 class="gt"><span class="i" data-en="{esc(g["t"]["en"])}" data-tr="{esc(g["t"]["tr"])}">{esc(g["t"]["de"])}</span></h3>'
        ghtml += f'<div class="grp">{gt}<ul class="list">\n{lis}</ul></div>\n'
    hero = ""
    if cat["img"]:
        f, pos = cat["img"]
        hero = f'<div class="catimg"><img src="assets/{f}" alt="" loading="lazy" style="object-position:{pos}"></div>'
    note = f'<p class="cnote"><span class="i" data-en="{esc(cat["note"]["en"])}" data-tr="{esc(cat["note"]["tr"])}">{esc(cat["note"]["de"])}</span></p>' if cat.get("note") else ""
    live = '<span class="live" id="bfstatus"></span>' if cat["id"] == "fruehstueck" else ""
    ft = ""
    if cat.get("foot"):
        fo = cat["foot"]; ft = f'<p class="gfoot"><span class="i" data-en="{esc(fo["en"])}" data-tr="{esc(fo["tr"])}">{esc(fo["de"])}</span></p>'
    body.append(f'<div class="cat" id="{cat["id"]}" data-c="{cat["id"]}">{hero}<header class="ch"><span class="no">{ci+1:02d}</span><h2><span class="i" data-en="{esc(cat["t"]["en"])}" data-tr="{esc(cat["t"]["tr"])}">{esc(cat["t"]["de"])}</span></h2>{live}</header>{note}{ghtml}{ft}</div>')

chips = "".join(f'<button class="chip" type="button" data-f="{k}">{U(k)}</button>' for k in ("best", "veg", "home", "u10"))

shared = f'''<div class="cartbar" id="cartbar" hidden><button type="button" id="cartopen"><span class="cn" id="cartn">0</span><span><b>{U("mylist")}</b><small id="carttot"></small></span><span class="go">{U("view")} →</span></button></div>

<dialog id="dlg"><div class="dwrap"><button class="x" type="button" data-close aria-label="{esc(UI['close'][0])}">×</button>
  <div class="dimg" id="dimg"></div>
  <div class="dbody"><div class="dbd" id="dbd"></div><h2 id="dname"></h2><p class="dd" id="ddesc"></p>
   <div class="opts" id="dopts"></div><div class="vars" id="dvars"></div>
   <div class="dprice" id="dprice"></div><p class="allergen sm">{U("allergen")}</p>
   <div class="dact"><button class="btn btn-amber" type="button" id="dadd">{U("add")}</button><button class="btn btn-ghost" type="button" id="dshare">{U("share")}</button></div></div></div></dialog>

<dialog id="cdlg"><div class="dwrap"><button class="x" type="button" data-close aria-label="{esc(UI['close'][0])}">×</button>
  <div class="dbody"><h2>{U("mylist")}</h2><ul class="clist" id="clist"></ul><p class="cempty" id="cempty">{U("empty")}</p>
   <label class="tbl"><span>{U("table")}</span><input id="tbl" inputmode="numeric" maxlength="3" placeholder="–"></label>
   <div class="ctotal"><span>{U("total")}</span><b id="ctot">0,00 €</b></div>
   <div class="dact"><button class="btn btn-amber" type="button" id="cshow">{U("show")}</button><button class="btn btn-ghost" type="button" id="csend">{U("send")}</button></div>
   <p class="toast" id="ctoast"></p></div></div></dialog>

<dialog id="sdlg" class="slip"><div class="dwrap"><button class="x" type="button" data-close aria-label="{esc(UI['close'][0])}">×</button>
  <div class="dbody"><div class="stbl" id="stbl"></div><ul class="slist" id="slist"></ul><div class="ctotal big"><span>{U("total")}</span><b id="stot"></b></div><p class="snote">{U("slipnote")}</p><p class="stime" id="stime"></p></div></div></dialog>

'''
toastg = '<div class="toastg" id="toastg" role="status"></div>'
data_script = '<script type="application/json" id="kdata">' + json.dumps(DATA, ensure_ascii=False) + '</script>'

page = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Speisekarte — Café VAI</title>
<meta name="description" content="Digitale Speisekarte von Café VAI in Vaihingen an der Enz: Frühstück, SmashBurger, Tenders, Kaffee, Drinks.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0b0d0c">
<meta property="og:title" content="Speisekarte — Café VAI">
<meta property="og:image" content="assets/og-burger.jpg">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="karte.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="kp">
<div id="bar"></div>
<header class="top"><a class="back" href="index.html#speisekarte" aria-label="{esc(UI['back'][0])}">←</a>
  <a class="tlogo" href="index.html"><img src="assets/logo-disc.png" alt="" width="36" height="36"><b>Café VAI</b><em class="demotag">Demo</em></a>
  <div class="lang" role="group" aria-label="Sprache"><button data-l="de" class="on">DE</button><button data-l="en">EN</button><button data-l="tr">TR</button></div></header>

<main>
<section class="hero-k">
  <img src="assets/og-burger.jpg" alt="" width="1200" height="630" fetchpriority="high">
  <div class="inner">
    <span class="eyebrow">{U("sub")}</span>
    <h1>{U("title")}</h1>
    <p class="allergen">{U("allergen")}</p>
    <p class="bf" id="bfchip"><i></i><span id="bftxt"></span></p>
  </div>
</section>

<div class="filter" id="filter">
  <label class="srch"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  <input id="q" type="search" autocomplete="off" placeholder="{esc(UI['search'][0])}" data-ph-en="{esc(UI['search'][1])}" data-ph-tr="{esc(UI['search'][2])}"></label>
  <div class="chips" id="chips">{chips}</div>
  <p class="kcount" id="kcnt" aria-live="polite"></p>
</div>

<div class="cats">
{chr(10).join(body)}
<p class="none" id="none" hidden>{U("none")}</p>
</div>
<footer class="kfoot"><p>{U("foot")}</p><div class="fl"><a class="btn btn-amber" href="index.html#besuch">Tisch reservieren</a><button class="btn btn-ghost" id="printbtn" type="button">{U("print")}</button></div></footer>
</main>

<nav class="tabs" id="tabs" aria-label="Kategorien">{"".join(tabs)}</nav>

{shared}
<div class="rosette">Demo · GastrOptima</div>
{toastg}
{data_script}
<script src="karte.js" defer></script>
</body>
</html>
'''
(out / "karte.html").write_text(page, encoding="utf-8")
json.dump(dict(tabs="".join(tabs), chips=chips, body="\n".join(body), shared=shared, toastg=toastg, data=data_script,
               allergen=U("allergen"), bf='<p class="bf" id="bfchip"><i></i><span id="bftxt"></span></p>',
               none=U("none"), foot=U("foot"), printlbl=U("print"), search_ph=UI["search"], total=total),
          open(pathlib.Path(__file__).parent / "parts.json", "w"), ensure_ascii=False)
print("karte.html", len(page), "bytes,", total, "Positionen")
