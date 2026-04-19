#!/usr/bin/env python3
"""
replace-article-icons.py

Ersetzt Marken-Emojis in h1/h2/h3 und <a>-Tags durch inline SVG-Icons.
Nur diese 5 Emojis werden angefasst:
  🛸 → UFO SVG      (referenziert Footer-Defs url(#ufo-dome-{FID}))
  👽 → Alien SVG    (referenziert Footer-Defs url(#ai-head-{FID}))
  ⚡ → Blitz SVG    (self-contained)
  📡 → Schüssel SVG (self-contained)
  📊 → Candlestick  (self-contained)

Alle anderen Emojis im Fließtext bleiben unangetastet.

Benutzung:
  python3 replace-article-icons.py          # Dry-Run: zeigt was sich ändert
  python3 replace-article-icons.py --write  # Schreibt Änderungen
"""

import os
import re
import sys
import hashlib

DRY_RUN = '--write' not in sys.argv
HTML_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP = {
    'blog.html', 'index.html', 'buecher.html', 'buch-direkt.html',
    'grapheneos-book.html', 'spenden.html', 'datenschutz.html',
    'impressum.html', 'template-artikel.html',
    'aktien-analysen.html', 'bitcoin-analysen.html',
}

BRAND_EMOJIS = {'🛸', '👽', '⚡', '📡', '📊'}

# ── SVG-Bausteine ─────────────────────────────────────────────────────────────

def ufo_svg(fid, link=False):
    """UFO — referenziert Gradienten aus dem Footer (ufo-dome-{fid})."""
    if link:
        s = 'width:1.4em;height:0.7em;vertical-align:-0.05em;filter:drop-shadow(0 0 3px #00ffcc88);'
        aria = 'aria-hidden="true"'
    else:
        s = 'width:1.6em;height:0.8em;vertical-align:-0.1em;filter:drop-shadow(0 0 4px #00ffcc88);'
        aria = 'aria-label="UFO" role="img"'
    d, b = f'ufo-dome-{fid}', f'ufo-body-{fid}'
    return (
        f'<svg style="{s}" viewBox="0 0 72 36" xmlns="http://www.w3.org/2000/svg" {aria}>'
        f'<path d="M 22 16 A 14 10 0 0 1 50 16 Z" fill="url(#{d})" stroke="#00ffcc" stroke-width="0.4" opacity="0.9"/>'
        f'<ellipse cx="36" cy="18" rx="34" ry="5" fill="url(#{b})" stroke="#00ffcc" stroke-width="0.4"/>'
        f'<ellipse cx="36" cy="20.5" rx="26" ry="2.2" fill="#0c1416"/>'
        f'<ellipse cx="36" cy="22" rx="20" ry="3" fill="#1a2628" stroke="#00ffcc" stroke-width="0.3" opacity="0.8"/>'
        f'<circle cx="20" cy="20.5" r="1.3" fill="#fff"/>'
        f'<circle cx="27" cy="21.2" r="1.3" fill="#fff"/>'
        f'<circle cx="34" cy="21.6" r="1.3" fill="#fff"/>'
        f'<circle cx="41" cy="21.6" r="1.3" fill="#fff"/>'
        f'<circle cx="48" cy="21.2" r="1.3" fill="#fff"/>'
        f'<circle cx="55" cy="20.5" r="1.3" fill="#fff"/>'
        f'</svg>'
    )


def alien_svg(fid, link=False):
    """Alien-Kopf — referenziert Gradient aus dem Footer (ai-head-{fid})."""
    if link:
        s = 'width:0.75em;height:0.95em;vertical-align:-0.15em;filter:drop-shadow(0 0 3px #00ffcc88);'
        aria = 'aria-hidden="true"'
    else:
        s = 'width:0.85em;height:1.1em;vertical-align:-0.2em;filter:drop-shadow(0 0 4px #00ffcc88);'
        aria = 'aria-label="Alien" role="img"'
    g = f'ai-head-{fid}'
    return (
        f'<svg style="{s}" viewBox="-4 -16 44 51" xmlns="http://www.w3.org/2000/svg" {aria}>'
        f'<line x1="13" y1="2" x2="4" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/>'
        f'<circle cx="4" cy="-13" r="2.8" fill="#00ffcc"/>'
        f'<line x1="23" y1="2" x2="32" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/>'
        f'<circle cx="32" cy="-13" r="2.8" fill="#00ffcc"/>'
        f'<path fill="url(#{g})" stroke="#00ffcc" stroke-width="0.8" d="M35 17c0 9.389-13.223 19-17 19-3.778 0-17-9.611-17-19S8.611 0 18 0s17 7.611 17 17z"/>'
        f'<path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" d="M13.503 14.845c3.124 3.124 4.39 6.923 2.828 8.485-1.562 1.562-5.361.297-8.485-2.828-3.125-3.124-4.391-6.923-2.828-8.485s5.361-.296 8.485 2.828zm8.994 0c-3.124 3.124-4.39 6.923-2.828 8.485 1.562 1.562 5.361.297 8.485-2.828 3.125-3.125 4.391-6.923 2.828-8.485-1.562-1.562-5.361-.297-8.485 2.828z"/>'
        f'<path fill="none" stroke="#001a0e" stroke-width="1.2" stroke-linecap="round" d="M12 27 Q18 33 24 27"/>'
        f'</svg>'
    )


def lightning_svg(link=False):
    if link:
        s = 'width:0.6em;height:0.85em;vertical-align:-0.1em;filter:drop-shadow(0 0 2px #00ffcc88);'
        aria = 'aria-hidden="true"'
    else:
        s = 'width:0.7em;height:1em;vertical-align:-0.15em;filter:drop-shadow(0 0 3px #00ffcc88);'
        aria = 'aria-label="Blitz" role="img"'
    return (
        f'<svg style="{s}" viewBox="0 0 24 36" xmlns="http://www.w3.org/2000/svg" {aria}>'
        f'<polygon points="14,2 4,20 12,20 10,34 20,16 12,16" fill="#00ffcc" opacity="0.9" stroke="#00ffcc" stroke-width="0.5" stroke-linejoin="round"/>'
        f'</svg>'
    )


def satellite_svg(link=False):
    if link:
        s = 'width:0.9em;height:0.9em;vertical-align:-0.12em;filter:drop-shadow(0 0 2px #00ffcc88);'
        aria = 'aria-hidden="true"'
    else:
        s = 'width:1em;height:1em;vertical-align:-0.15em;filter:drop-shadow(0 0 3px #00ffcc88);'
        aria = 'aria-label="Satellitenschüssel" role="img"'
    return (
        f'<svg style="{s}" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" {aria}>'
        f'<path d="M4 24 A16 16 0 0 1 20 8" fill="#00ffcc" fill-opacity="0.06" stroke="#00ffcc" stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="20" cy="8" r="2.8" fill="#00ffcc"/>'
        f'<line x1="20" y1="8" x2="28" y2="4" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M15 13 A6 6 0 0 1 21 7" fill="none" stroke="#00ffcc" stroke-width="1.2" stroke-linecap="round" opacity="0.7"/>'
        f'<path d="M12 16 A9 9 0 0 1 21 7" fill="none" stroke="#00ffcc" stroke-width="0.9" stroke-linecap="round" opacity="0.45"/>'
        f'</svg>'
    )


def candlestick_svg(link=False):
    if link:
        s = 'width:0.9em;height:0.9em;vertical-align:-0.12em;filter:drop-shadow(0 0 2px #00ffcc88);'
        aria = 'aria-hidden="true"'
    else:
        s = 'width:1em;height:1em;vertical-align:-0.15em;filter:drop-shadow(0 0 3px #00ffcc88);'
        aria = 'aria-label="Aktienanalyse" role="img"'
    return (
        f'<svg style="{s}" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" {aria}>'
        f'<line x1="7" y1="3" x2="7" y2="7" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<rect x="4" y="7" width="6" height="9" rx="1" fill="#00ffcc"/>'
        f'<line x1="7" y1="16" x2="7" y2="21" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<line x1="16" y1="7" x2="16" y2="11" stroke="#00cc88" stroke-width="1.5" stroke-linecap="round"/>'
        f'<rect x="13" y="11" width="6" height="12" rx="1" fill="none" stroke="#00cc88" stroke-width="1.5"/>'
        f'<line x1="16" y1="23" x2="16" y2="27" stroke="#00cc88" stroke-width="1.5" stroke-linecap="round"/>'
        f'<line x1="25" y1="4" x2="25" y2="9" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<rect x="22" y="9" width="6" height="11" rx="1" fill="#00ffcc"/>'
        f'<line x1="25" y1="20" x2="25" y2="26" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'</svg>'
    )


# ── Ersetzungs-Logik ──────────────────────────────────────────────────────────

def replace_emojis_in_text(text, fid, link=False):
    """Ersetzt Marken-Emojis in einem Textstück (kein HTML, rein Text)."""
    text = text.replace('🛸', ufo_svg(fid, link=link))
    text = text.replace('👽', alien_svg(fid, link=link))
    text = text.replace('⚡', lightning_svg(link=link))
    text = text.replace('📡', satellite_svg(link=link))
    text = text.replace('📊', candlestick_svg(link=link))
    return text


def patch_tag_content(tag_html, fid, link=False):
    """
    Ersetzt Emojis nur in Text-Knoten innerhalb eines Tags.
    HTML-Attribute und Kind-Tags bleiben unverändert.
    """
    # Aufteilen in Sub-Tags und Text-Knoten
    parts = re.split(r'(<[^>]+>)', tag_html)
    result = []
    for part in parts:
        if part.startswith('<'):
            result.append(part)  # Tag unverändert
        else:
            result.append(replace_emojis_in_text(part, fid, link=link))
    return ''.join(result)


def has_brand_emoji(text):
    return any(e in text for e in BRAND_EMOJIS)


def process_file(filepath):
    filename = os.path.basename(filepath)
    fid = hashlib.md5(filename.encode()).hexdigest()[:6]

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    changed_lines = []

    # h1 / h2 / h3
    def replace_heading(m):
        full = m.group(0)
        if not has_brand_emoji(full):
            return full
        patched = patch_tag_content(full, fid, link=False)
        if patched != full:
            changed_lines.append(('H', full.strip()[:80]))
        return patched

    content = re.sub(
        r'<h[123](?:[^>]*)>.*?</h[123]>',
        replace_heading,
        content,
        flags=re.DOTALL
    )

    # <a ...>...</a>
    def replace_link(m):
        full = m.group(0)
        if not has_brand_emoji(full):
            return full
        patched = patch_tag_content(full, fid, link=True)
        if patched != full:
            changed_lines.append(('A', full.strip()[:80]))
        return patched

    content = re.sub(
        r'<a(?:\s[^>]*)?>.*?</a>',
        replace_link,
        content,
        flags=re.DOTALL
    )

    if content == original:
        return False

    if DRY_RUN:
        print(f'\n[DRY] {filename}  (fid={fid})')
        for kind, line in changed_lines:
            print(f'  {kind}: {line}')
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓ {filename}  ({len(changed_lines)} Ersetzungen)')

    return True


# ── Haupt-Loop ────────────────────────────────────────────────────────────────

def main():
    files = sorted(
        f for f in os.listdir(HTML_DIR)
        if f.endswith('.html') and f not in SKIP
    )

    mode = 'DRY-RUN' if DRY_RUN else 'SCHREIBEN'
    print(f'replace-article-icons.py — Modus: {mode}')
    print(f'Verzeichnis: {HTML_DIR}')
    print(f'Dateien: {len(files)}\n')

    changed = 0
    for fname in files:
        path = os.path.join(HTML_DIR, fname)
        if process_file(path):
            changed += 1

    print(f'\n{"[DRY] " if DRY_RUN else ""}Fertig — {changed} von {len(files)} Dateien geändert.')
    if DRY_RUN:
        print('→ Mit --write anwenden: python3 replace-article-icons.py --write')


if __name__ == '__main__':
    main()
