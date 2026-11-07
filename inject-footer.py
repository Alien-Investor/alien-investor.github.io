#!/usr/bin/env python3
"""
inject-footer.py
Ersetzt den kompletten <footer>...</footer>-Block in allen Artikel-HTML-Dateien
durch ein aktuelles Template. Nützlich wenn sich der Footer-Inhalt ändert.

Verwendung:
  python3 inject-footer.py           # Dry-run (zeigt nur was geändert würde)
  python3 inject-footer.py --write   # Schreibt Änderungen

Das Template steht unten als FOOTER_TEMPLATE. Platzhalter {FID} wird pro Datei
durch einen MD5-Hash des Dateinamens ersetzt (für eindeutige SVG-Gradient-IDs).
"""

import os
import re
import hashlib
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
DRY_RUN = "--write" not in sys.argv

# Stillgelegt am 22.10.2026: Die Vorlage unten stammt vom April 2026 und kennt weder den PGP-Link noch den
# Impressum-Link noch den Affiliate-Hinweis. Ein Lauf würde sie auf allen Artikeln löschen und dazu die
# Tool-Kopien mit veröffentlichtem SHA-256 verändern. Footer neuer Artikel aus der Referenzdatei
# (digitaler-euro-cbdc-kontrolle.html) übernehmen, Pflichtangaben mit ~/Skripte/website-recht/recht_einbauen.py prüfen.
if "--trotzdem" not in sys.argv:
    sys.exit("inject-footer.py ist stillgelegt (veraltete Vorlage, siehe Kommentar im Skript).")

SKIP = {
    "index.html", "blog.html", "buecher.html", "buch-direkt.html",
    "aktien-analysen.html", "bitcoin-analysen.html", "alien-head-test.html",
    "update-footer-icons.py", "inject-footer.py"
}

def fid(filename):
    return hashlib.md5(filename.encode()).hexdigest()[:6]

# ── Footer-Template ────────────────────────────────────────────────────────────
# Ändere hier den Footer-Inhalt. {FID} wird automatisch pro Datei ersetzt.
FOOTER_TEMPLATE = """\
  <footer>
    <p><svg style="width:1em;height:1em;vertical-align:-0.15em;filter:drop-shadow(0 0 3px #00ffcc88);" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg" aria-label="Kontakt" role="img"><circle cx="18" cy="20" r="2" fill="#00ffcc"/><path d="M12 18 A7 7 0 0 1 24 18" fill="none" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round"/><path d="M8 14 A12 12 0 0 1 28 14" fill="none" stroke="#00ffcc" stroke-width="1" stroke-linecap="round" opacity="0.7"/><path d="M4 10 A17 17 0 0 1 32 10" fill="none" stroke="#00ffcc" stroke-width="0.8" stroke-linecap="round" opacity="0.45"/><line x1="18" y1="22" x2="18" y2="32" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round"/><line x1="13" y1="32" x2="23" y2="32" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round"/></svg> Kontakt: <a href="mailto:kontakt@alien-investor.org">kontakt@alien-investor.org</a></p>

    <p style="margin-top: 20px;">
      <svg style="width:0.85em;height:1.1em;vertical-align:-0.2em;filter:drop-shadow(0 0 4px #00ffcc88);" viewBox="-4 -14 44 51" xmlns="http://www.w3.org/2000/svg" aria-label="Alien" role="img"><defs><radialGradient id="ai-head-{FID}" cx="50%" cy="40%" r="60%"><stop offset="0%" stop-color="#3db86a"/><stop offset="70%" stop-color="#1a6635"/><stop offset="100%" stop-color="#0a2016"/></radialGradient></defs><line x1="10.32" y1="2.98" x2="0.6" y2="-5.2" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/><circle cx="0.6" cy="-5.2" r="3" fill="#00ffcc"/><line x1="25.68" y1="2.98" x2="35.4" y2="-5.2" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/><circle cx="35.4" cy="-5.2" r="3" fill="#00ffcc"/><path fill="url(#ai-head-{FID})" stroke="#00ffcc" stroke-width="0.8" d="M1.64 16.04A16.36 16.04 0 0 1 34.36 16.04C34.36 22.24 23.25 36 18 36C12.75 36 1.64 22.24 1.64 16.04Z"/><path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" d="M5.41 15.84A6.55 3.52 32 0 0 9.1 22.29A6.55 3.52 32 0 0 16.51 22.78A6.55 3.52 32 0 0 12.83 16.33A6.55 3.52 32 0 0 5.41 15.84ZM19.49 22.78A6.55 3.52 -32 0 0 26.9 22.29A6.55 3.52 -32 0 0 30.59 15.84A6.55 3.52 -32 0 0 23.17 16.33A6.55 3.52 -32 0 0 19.49 22.78Z"/><circle cx="9.49" cy="17.35" r="0.9" fill="#00ffcc"/><circle cx="26.51" cy="17.35" r="0.9" fill="#00ffcc"/></svg> <strong>Haftungsausschluss:</strong><br><br>
      Dieser Artikel stellt keine Finanz-, Steuer- oder Rechtsberatung dar.<br>
      Ich teile hier meine persönliche Alien-Meinung – unabhängig, rebellisch und frei.<br>
      Investieren ist mit Risiken verbunden. Denke selbst, vertraue niemandem und handle auf eigene Verantwortung.
    </p>
  </footer>"""

FOOTER_RE = re.compile(r'<footer>.*?</footer>', re.DOTALL)

def patch_file(filepath):
    filename = os.path.basename(filepath)
    f = fid(filename)

    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()

    new_footer = FOOTER_TEMPLATE.replace('{FID}', f)
    new_content = FOOTER_RE.sub(new_footer, content)

    if new_content == content:
        return 'unchanged'

    if not DRY_RUN:
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        return 'updated'
    return 'would-update'

if __name__ == '__main__':
    if DRY_RUN:
        print("DRY-RUN — keine Dateien werden geändert. Mit --write ausführen um zu schreiben.\n")

    updated, unchanged, no_footer = [], [], []

    for filename in sorted(os.listdir(REPO)):
        if not filename.endswith('.html') or filename in SKIP:
            continue
        result = patch_file(os.path.join(REPO, filename))
        if result == 'unchanged':
            unchanged.append(filename)
        elif result in ('updated', 'would-update'):
            updated.append(filename)
        else:
            no_footer.append(filename)

    verb = "Würde aktualisieren" if DRY_RUN else "Aktualisiert"
    print(f"{verb}: {len(updated)} Dateien")
    print(f"Keine Änderung nötig: {len(unchanged)} Dateien")
    if no_footer:
        print(f"Kein <footer> gefunden: {len(no_footer)} Dateien")
    for f in updated:
        print(f"  {'~' if DRY_RUN else '✓'} {f}")
