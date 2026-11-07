#!/usr/bin/env python3
"""
update-footer-icons.py
Ersetzt Emoji-Footer durch Custom SVG Icons in allen HTML-Artikeln.
Bereits aktualisierte Hauptseiten werden übersprungen.

Verwendung: python3 update-footer-icons.py
"""

import os
import hashlib

REPO = os.path.dirname(os.path.abspath(__file__))

SKIP = {
    "index.html", "blog.html", "buecher.html", "buch-direkt.html",
    "aktien-analysen.html", "bitcoin-analysen.html", "alien-head-test.html",
    "update-footer-icons.py", "inject-footer.py"
}

def fid(filename):
    return hashlib.md5(filename.encode()).hexdigest()[:6]

def svg_lightning():
    return (
        '<svg style="width:0.7em;height:1em;vertical-align:-0.15em;'
        'filter:drop-shadow(0 0 3px #00ffcc88);" viewBox="0 0 24 36" '
        'xmlns="http://www.w3.org/2000/svg" aria-label="Energie" role="img">'
        '<polygon points="14,2 4,20 12,20 10,34 20,16 12,16" fill="#00ffcc" '
        'opacity="0.9" stroke="#00ffcc" stroke-width="0.5" stroke-linejoin="round"/></svg>'
    )

def svg_ufo(f):
    return (
        f'<svg style="width:1.6em;height:0.8em;vertical-align:-0.1em;'
        f'filter:drop-shadow(0 0 4px #00ffcc88);" viewBox="0 0 72 36" '
        f'xmlns="http://www.w3.org/2000/svg" aria-label="UFO" role="img">'
        f'<defs>'
        f'<radialGradient id="ufo-dome-{f}" cx="50%" cy="80%" r="60%">'
        f'<stop offset="0%" stop-color="#5fffe0"/>'
        f'<stop offset="60%" stop-color="#1a3a38"/>'
        f'<stop offset="100%" stop-color="#0a1a1e"/></radialGradient>'
        f'<linearGradient id="ufo-body-{f}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="#4a5a5a"/>'
        f'<stop offset="50%" stop-color="#2a3638"/>'
        f'<stop offset="100%" stop-color="#101818"/></linearGradient></defs>'
        f'<path d="M 22 16 A 14 10 0 0 1 50 16 Z" fill="url(#ufo-dome-{f})" stroke="#00ffcc" stroke-width="0.4" opacity="0.9"/>'
        f'<ellipse cx="36" cy="18" rx="34" ry="5" fill="url(#ufo-body-{f})" stroke="#00ffcc" stroke-width="0.4"/>'
        f'<ellipse cx="36" cy="20.5" rx="26" ry="2.2" fill="#0c1416"/>'
        f'<ellipse cx="36" cy="22" rx="20" ry="3" fill="#1a2628" stroke="#00ffcc" stroke-width="0.3" opacity="0.8"/>'
        f'<circle cx="20" cy="20.5" r="1.3" fill="#fff"/>'
        f'<circle cx="27" cy="21.2" r="1.3" fill="#fff"/>'
        f'<circle cx="34" cy="21.6" r="1.3" fill="#fff"/>'
        f'<circle cx="41" cy="21.6" r="1.3" fill="#fff"/>'
        f'<circle cx="48" cy="21.2" r="1.3" fill="#fff"/>'
        f'<circle cx="55" cy="20.5" r="1.3" fill="#fff"/></svg>'
    )

def svg_alien(f):
    return (
        f'<svg style="width:0.85em;height:1.1em;vertical-align:-0.2em;'
        f'filter:drop-shadow(0 0 4px #00ffcc88);" viewBox="-4 -14 44 51" '
        f'xmlns="http://www.w3.org/2000/svg" aria-label="Alien" role="img">'
        f'<defs><radialGradient id="ai-head-{f}" cx="50%" cy="40%" r="60%">'
        f'<stop offset="0%" stop-color="#3db86a"/>'
        f'<stop offset="70%" stop-color="#1a6635"/>'
        f'<stop offset="100%" stop-color="#0a2016"/></radialGradient></defs>'
        f'<line x1="10.32" y1="2.98" x2="0.6" y2="-5.2" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<circle cx="0.6" cy="-5.2" r="3" fill="#00ffcc"/>'
        f'<line x1="25.68" y1="2.98" x2="35.4" y2="-5.2" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<circle cx="35.4" cy="-5.2" r="3" fill="#00ffcc"/>'
        f'<path fill="url(#ai-head-{f})" stroke="#00ffcc" stroke-width="0.8" '
        f'd="M1.64 16.04A16.36 16.04 0 0 1 34.36 16.04C34.36 22.24 23.25 36 18 36C12.75 36 1.64 22.24 1.64 16.04Z"/>'
        f'<path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" '
        f'd="M5.41 15.84A6.55 3.52 32 0 0 9.1 22.29A6.55 3.52 32 0 0 16.51 22.78A6.55 3.52 32 0 0 12.83 16.33'
        f'A6.55 3.52 32 0 0 5.41 15.84ZM19.49 22.78A6.55 3.52 -32 0 0 26.9 22.29A6.55 3.52 -32 0 0 30.59 15.84'
        f'A6.55 3.52 -32 0 0 23.17 16.33A6.55 3.52 -32 0 0 19.49 22.78Z"/>'
        f'<circle cx="9.49" cy="17.35" r="0.9" fill="#00ffcc"/><circle cx="26.51" cy="17.35" r="0.9" fill="#00ffcc"/></svg>'
    )

def svg_antenna():
    return (
        '<svg style="width:1em;height:1em;vertical-align:-0.15em;'
        'filter:drop-shadow(0 0 3px #00ffcc88);" viewBox="0 0 36 36" '
        'xmlns="http://www.w3.org/2000/svg" aria-label="Kontakt" role="img">'
        '<circle cx="18" cy="20" r="2" fill="#00ffcc"/>'
        '<path d="M12 18 A7 7 0 0 1 24 18" fill="none" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round"/>'
        '<path d="M8 14 A12 12 0 0 1 28 14" fill="none" stroke="#00ffcc" stroke-width="1" stroke-linecap="round" opacity="0.7"/>'
        '<path d="M4 10 A17 17 0 0 1 32 10" fill="none" stroke="#00ffcc" stroke-width="0.8" stroke-linecap="round" opacity="0.45"/>'
        '<line x1="18" y1="22" x2="18" y2="32" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round"/>'
        '<line x1="13" y1="32" x2="23" y2="32" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round"/></svg>'
    )

def patch_file(filepath):
    filename = os.path.basename(filepath)
    f = fid(filename)

    with open(filepath, 'r', encoding='utf-8') as fh:
        content = fh.read()

    original = content

    content = content.replace('🔋 Energie aufladen', f'{svg_lightning()} Energie aufladen')
    content = content.replace('👽🛸', svg_ufo(f))
    content = content.replace('👽 <strong>Haftungsausschluss:</strong>', f'{svg_alien(f)} <strong>Haftungsausschluss:</strong>')
    content = content.replace('📬 Kontakt:', f'{svg_antenna()} Kontakt:')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        return True
    return False

if __name__ == '__main__':
    updated, unchanged = [], []

    for filename in sorted(os.listdir(REPO)):
        if not filename.endswith('.html') or filename in SKIP:
            continue
        if patch_file(os.path.join(REPO, filename)):
            updated.append(filename)
        else:
            unchanged.append(filename)

    print(f"Aktualisiert: {len(updated)} Dateien")
    print(f"Keine Änderung nötig: {len(unchanged)} Dateien")
    for f in updated:
        print(f"  ✓ {f}")
