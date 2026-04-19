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
      <svg style="width:0.85em;height:1.1em;vertical-align:-0.2em;filter:drop-shadow(0 0 4px #00ffcc88);" viewBox="-4 -16 44 51" xmlns="http://www.w3.org/2000/svg" aria-label="Alien" role="img"><defs><radialGradient id="ai-head-{FID}" cx="50%" cy="40%" r="60%"><stop offset="0%" stop-color="#3db86a"/><stop offset="70%" stop-color="#1a6635"/><stop offset="100%" stop-color="#0a2016"/></radialGradient></defs><line x1="13" y1="2" x2="4" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/><circle cx="4" cy="-13" r="2.8" fill="#00ffcc"/><line x1="23" y1="2" x2="32" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/><circle cx="32" cy="-13" r="2.8" fill="#00ffcc"/><path fill="url(#ai-head-{FID})" stroke="#00ffcc" stroke-width="0.8" d="M35 17c0 9.389-13.223 19-17 19-3.778 0-17-9.611-17-19S8.611 0 18 0s17 7.611 17 17z"/><path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" d="M13.503 14.845c3.124 3.124 4.39 6.923 2.828 8.485-1.562 1.562-5.361.297-8.485-2.828-3.125-3.124-4.391-6.923-2.828-8.485s5.361-.296 8.485 2.828zm8.994 0c-3.124 3.124-4.39 6.923-2.828 8.485 1.562 1.562 5.361.297 8.485-2.828 3.125-3.125 4.391-6.923 2.828-8.485-1.562-1.562-5.361-.297-8.485 2.828z"/><path fill="none" stroke="#001a0e" stroke-width="1.2" stroke-linecap="round" d="M12 27 Q18 33 24 27"/></svg> <strong>Haftungsausschluss:</strong><br><br>
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
