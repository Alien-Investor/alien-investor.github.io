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
        f'filter:drop-shadow(0 0 4px #00ffcc88);" viewBox="-4 -16 44 51" '
        f'xmlns="http://www.w3.org/2000/svg" aria-label="Alien" role="img">'
        f'<defs><radialGradient id="ai-head-{f}" cx="50%" cy="40%" r="60%">'
        f'<stop offset="0%" stop-color="#3db86a"/>'
        f'<stop offset="70%" stop-color="#1a6635"/>'
        f'<stop offset="100%" stop-color="#0a2016"/></radialGradient></defs>'
        f'<line x1="13" y1="2" x2="4" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/>'
        f'<circle cx="4" cy="-13" r="2.8" fill="#00ffcc"/>'
        f'<line x1="23" y1="2" x2="32" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/>'
        f'<circle cx="32" cy="-13" r="2.8" fill="#00ffcc"/>'
        f'<path fill="url(#ai-head-{f})" stroke="#00ffcc" stroke-width="0.8" '
        f'd="M35 17c0 9.389-13.223 19-17 19-3.778 0-17-9.611-17-19S8.611 0 18 0s17 7.611 17 17z"/>'
        f'<path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" '
        f'd="M13.503 14.845c3.124 3.124 4.39 6.923 2.828 8.485-1.562 1.562-5.361.297-8.485-2.828'
        f'-3.125-3.124-4.391-6.923-2.828-8.485s5.361-.296 8.485 2.828zm8.994 0c-3.124 3.124'
        f'-4.39 6.923-2.828 8.485 1.562 1.562 5.361.297 8.485-2.828 3.125-3.125 4.391-6.923'
        f' 2.828-8.485-1.562-1.562-5.361-.297-8.485 2.828z"/>'
        f'<path fill="none" stroke="#001a0e" stroke-width="1.2" stroke-linecap="round" '
        f'd="M12 27 Q18 33 24 27"/></svg>'
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
