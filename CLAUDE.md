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

**Repository-Sichtbarkeit: Dieses Repo muss immer `private` bleiben.**
Niemals auf `public` setzen — weder direkt noch über GitHub-Einstellungen.
Nur `btc-steuertool` ist als public vorgesehen.

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
