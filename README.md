# Café VAI — Demo (GastrOptima)

Scroll-gesteuerte Demo-Website für Café VAI, Vaihingen an der Enz. Statisch, kein Build-Schritt.
**Demo-Entwurf**, `noindex`. Fotos/Logo stammen von cafevai.de (keine schriftliche Freigabe) — auf Wunsch sofort entfernen.

## Cloudflare Pages (GitHub → Cloudflare)
- Repo `hasi-elektronic/cafe-vai`, Branch `demo-scroll` verbinden
- Build command: *(leer)* · Output directory: `/`
- `main` bleibt die ältere Einzeldatei-Seite

## Lokal
`python3 -m http.server` im Ordner, dann `index.html` öffnen.
`tools/build.py <zielordner>` erzeugt `index.html`, Impressum, Datenschutz neu.
