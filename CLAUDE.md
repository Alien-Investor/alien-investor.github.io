# CLAUDE.md — alien-investor.github.io

Projektkontext für Claude Code. Globale Regeln (Tonalität, System, Verbote) gelten via `~/.claude/CLAUDE.md`.

---

## Was ist das

GitHub Pages Website der Alien Investor Marke.
Domain: **alien-investor.org**
Remote: `https://github.com/Alien-Investor/alien-investor.github.io.git`

Statisches HTML — kein Framework, kein Build-Step, keine Dependencies.
Alle Seiten sind einzelne `.html`-Dateien direkt im Wurzelverzeichnis.

---

## Deployment

Push auf `main` → direkt live.

```bash
git add datei.html
git commit -m "Beschreibung"
git push
```

---

## Absolut verboten

**`.well-known/` niemals anfassen.**
Dieser Ordner enthält `nostr.json` — die NIP-05 Verifikationsdatei für das verifizierte Nostr-Konto. Jede Änderung bricht die Nostr-Identitätsverifikation. Der Ordner bleibt immer unberührt.

---

## Bearbeitung

Claude Code liest alle Dateien im Projekt.
Änderungen werden nur auf explizite Anweisung vorgenommen.

---

## Inhaltsstruktur (Auswahl)

| Kategorie | Dateien |
|-----------|---------|
| Einstieg | `index.html`, `blog.html`, `FAQ.html` |
| Bitcoin | `bitcoin.html`, `bitcoin-analysen.html`, `bitcoin-analyse-*.html`, `self-custody.html` |
| Aktienanalysen | `aktien-analysen.html`, `alien-analyzer.html`, `alphabet-*.html`, `amazon-*.html` |
| Privacy / GrapheneOS | `grapheneos-*.html`, `nostr-*.html`, `proton.html` |
| Tools | `btc-steuertool.html`, `charts.html`, `mission-control.html` |
| Sonstiges | `spenden.html`, `inflation.html`, `geld.html`, `vertrauen.html` |

---

## Tonalität & Stil

Vollständige Regeln: `~/projekte/alien-investor/CLAUDE.md`

Kurzfassung:
- Klar, direkt, technisch sauber, leicht rebellisch
- Kein Genderdeutsch, kein Corporate-Speak, kein Hype-Jargon
- Standard-Disclaimer auf allen Finanzseiten
- Alien-Thema sparsam als Würze, nicht als Kostüm

---

## Zweisprachigkeit DE/EN (Stand April 2026)

Die Site ist bilingual. Deutsche Originale bleiben im Wurzelverzeichnis unangetastet. Englische Versionen liegen unter `/en/`.

### Architektur

- **`/lang-switcher.js`** — in alle 93 Root-HTML-Dateien injiziert (vor `</body>`). Fügt DE|EN-Toggle in `.top-nav` ein (oder fixed-position Fallback). Speichert Sprachwahl in `localStorage('lang')`.
- **`/en/`** — Ordner mit allen englischen Übersetzungen.
- **`/en/terminology.json`** — kanonisches DE→EN Glossar (KGV→P/E ratio, Selbstverwahrung→self-custody, Namensaktie→registered share, etc.).
- **`/404.html`** — fängt fehlende `/en/*`-URLs ab mit "not yet available" und Link zur DE-Version.

### Regeln für jede EN-Datei

Jede `/en/*.html` muss haben:
```html
<html lang="en">
<link rel="canonical" href="/en/dateiname.html">
<link rel="alternate" hreflang="de" href="/dateiname.html">
<script src="/lang-switcher.js"></script>
```
- Alle internen Links als **absolute Pfade** (`/en/index.html`, nicht `index.html`)
- Alle Bildpfade als **absolute Pfade** (`/bild.jpg`, nicht `bild.jpg`) — Bilder liegen im Root
- Externe `https://`-Links unverändert lassen

### Sonderfälle

- **`/en/buecher.html`** — EN-Buchkarte zuerst, DE danach; Bildpfade absolut; nur ein Transparenz-Hinweis (EN)
- **`/en/buch-direkt.html`** — JS-Redirect zu `/buch-direkt.html#en` (die DE-Seite hat schon einen inline DE/EN-Toggle)
- **`/en/interactive-brokers.html`** und **`/en/swissquote.html`** — Redirect-Stubs (zeigen auf DE-Seiten, die selbst schon bilingual sind)

### Stand der Übersetzungen (April 2026)

**Fertig übersetzt (~70 Seiten):**
- Alle Bitcoin-Artikel (bitcoin.html, self-custody.html, bitcoin-analysen.html, bitcoin-analyse-*.html, bitcoin-kursanalyse-*.html, bitcoin-full-node.html, lightning-network-*.html, wie-ich-den-bitcoin-kurs-bewerte.html, bisq-*.html, Bitcoin-No-KYC.html, 21bitcoin.html)
- Alle GrapheneOS/Privacy-Artikel (grapheneos-*.html, nostr-*.html, proton.html, Alias.html, DNS.html, shelter-android-guide.html, Obtainium.html, Primal.html, Android-Zwang.html, eu-digital-id-*.html, cypherpunks-*.html, Kryptographie.html, kryptographie-freiheit.html, bitcoin_encrypt.html)
- Alle Aktienanalysen (aktien-analysen.html, alphabet-*.html, amazon-*.html, berkshire-*.html, chevron-*.html, exxon-*.html, kenon-*.html, mosaic-*.html, munich-re-*.html, rio-tinto-*.html, rollins-*.html, sandvik-*.html, sci-*.html, wheaton-*.html, rohstoff-superzyklus-2025.html)
- Broker/Depot (interactive-brokers.html, swissquote.html, us-aktien.html, namensaktien.html, direct-registration-us-aktien.html)
- Sonstiges (index.html, blog.html, FAQ.html, spenden.html, buecher.html, buch-direkt.html, geld.html, alien-analyzer.html, alien-analyzer-v2-guide.html, waehrungscrash-auf-raten.html)

**Noch nicht übersetzt (~17 Seiten):**
- `fed-bankenmacht.html`, `inflation.html`, `vertrauen.html`
- `rohstoff-superzyklus-analyse.html`
- `wasabi-wallet-research-transparent.html`, `white-noise-messenger-warum-signal-nicht-reicht-und-nostr-die-zukunft-ist.html`
- `local-ai.html`, `maple-AI.html`, `mission-control.html`, `btc-steuertool.html`, `charts.html`
- `Zapstore.html`, `GrapheneOS-Skripte.html`, `Bitbox-Einrichtung.html`, `bitbox.html`, `Liana-Wallet.html`
- `X-AGB.html`, `template-artikel.html`, `Fidus.html`
- `Roche-Aktienanalyse.html`, `Schindler-Analyse.html`, `Sika-Analyse.html`, `Ares-Capital.html`

### Live-Tools (api.alien-investor.org) — Inline-Switching

Live-Tools liegen unter `/home/alien/projekte/alien-investor/alien-analyzer-v2/` und sind ein separates Repo. Sie bekommen **kein separates `/en/`**, sondern einen inline DE|EN-Toggle (single file, `currentLang` + `i18n`-Objekt, localStorage `'alien-lang'`).

**Fertig:**
- `mission-control-v2.html` — DE|EN-Toggle in `.top-nav-right`; ~25 Strings übersetzt (Sektionslabels, Kartenbezeichnungen, Fear & Greed, Analyzer-Karte, Footer-Disclaimer)

**Ausstehend:**
- `alien-analyzer-v2.html` — ~70 JS-Strings: Alien Einordnung-Verdicts, Qualitätscheck-Labels (GUT/TEUER/STARK/MITTEL/GERING/HOCH), Metric-Hints, Tabellenköpfe (Kennzahl/Wert/Vergleich/Signal/Kontext), Statusmeldungen

### QA-Check für neue EN-Seiten

```bash
for f in en/*.html; do
  lang=$(grep -c 'lang="en"' "$f")
  canonical=$(grep -c 'rel="canonical"' "$f")
  hreflang=$(grep -c 'hreflang' "$f")
  switcher=$(grep -c 'lang-switcher' "$f")
  rel=$(grep -oP 'href="[a-z][^"]*\.html"' "$f" | grep -v http | head -3)
  echo "$f: lang=$lang can=$canonical href=$hreflang sw=$switcher | $rel"
done
```
