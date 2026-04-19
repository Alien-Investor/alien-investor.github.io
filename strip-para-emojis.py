#!/usr/bin/env python3
"""
strip-para-emojis.py

Entfernt dekorative Emojis am Anfang von <p>- und <h3>-Tags.
Damit sind gemeint: Emojis die als "Bullet"-Ersatz am Zeilenanfang stehen.

Was passiert:
  - <p>💡 Text…</p>  →  <p>Text…</p>
  - <h3>📋 Nächster Schritt</h3>  →  <h3>Nächster Schritt</h3>
  - <h1>⚠ Titel</h1>  →  <h1>Titel</h1>  (verbleibende Emojis in Headings)

Was NICHT angefasst wird:
  - Emojis mitten in Sätzen
  - Bereits ersetzte SVG-Icons
  - <p> mit mehreren Emojis die inhaltlich wichtig sind (nur Anfang!)
  - Fußzeilen, footer, nav

Benutzung:
  python3 strip-para-emojis.py          # Dry-Run
  python3 strip-para-emojis.py --write  # Schreibt Änderungen
"""

import os
import re
import sys

DRY_RUN = '--write' not in sys.argv
HTML_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP = {
    'blog.html', 'index.html', 'buecher.html', 'buch-direkt.html',
    'grapheneos-book.html', 'spenden.html', 'datenschutz.html',
    'impressum.html', 'template-artikel.html',
}

# Breites Emoji-Spektrum: Misc Symbols, Emoticons, Transport, Dingbats, etc.
EMOJI_PAT = re.compile(
    r'^(?:'
    r'[\U0001F300-\U0001FAFF]'   # Misc Symbols + Emoticons + Transport + Supplemental
    r'|[\U00002600-\U000027BF]'  # Misc Technical, Dingbats
    r'|[\U00002300-\U000023FF]'  # Misc Technical (Uhr etc.)
    r'|[\uFE00-\uFE0F]'          # Variation Selectors
    r'|[\u200D]'                  # Zero-Width Joiner
    r')+\s*'                      # beliebig viele, gefolgt von Whitespace
)


def strip_leading_emoji(text):
    """Entfernt Emojis + Whitespace vom Anfang eines Textstücks."""
    return EMOJI_PAT.sub('', text)


def patch_tag(tag_html):
    """
    Entfernt führende Emojis aus dem ersten Text-Knoten eines Tags.
    HTML-Attribute und Kind-Tags bleiben unverändert.
    """
    parts = re.split(r'(<[^>]+>)', tag_html)
    patched = list(parts)
    for i, part in enumerate(parts):
        if part.startswith('<'):
            continue
        stripped = part.lstrip()
        if not stripped:
            continue
        # Nur wenn das erste nicht-leere Textstück mit Emoji beginnt
        new_part = strip_leading_emoji(part.lstrip())
        if new_part != part.lstrip():
            patched[i] = new_part
        break  # Nur ersten Text-Knoten anfassen
    return ''.join(patched)


def has_leading_emoji(tag_html):
    parts = re.split(r'(<[^>]+>)', tag_html)
    for part in parts:
        if part.startswith('<'):
            continue
        stripped = part.lstrip()
        if not stripped:
            continue
        return bool(EMOJI_PAT.match(stripped))
    return False


# Matching-Pattern für Ziel-Tags
# p, h1, h2, h3 — aber NICHT wenn sie bereits SVG enthalten am Anfang
TAG_RE = re.compile(r'<(p|h[123])(?:[^>]*)>.*?</\1>', re.DOTALL)


def process_file(filepath):
    filename = os.path.basename(filepath)

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = []

    def replace_tag(m):
        full = m.group(0)
        tag = m.group(1)

        # h1/h2/h3: nur wenn kein SVG bereits am Anfang (brand-emoji schon ersetzt)
        if tag in ('h1', 'h2', 'h3'):
            # Wenn bereits ein SVG-Icon drin ist, überspringen
            inner_start = full.index('>') + 1
            inner = full[inner_start:].lstrip()
            if inner.startswith('<svg'):
                return full

        if not has_leading_emoji(full):
            return full

        patched = patch_tag(full)
        if patched != full:
            # Leerzeichen nach öffnendem Tag normalisieren
            patched = re.sub(r'(<(?:p|h[123])[^>]*>)\s+', r'\1', patched)
            changed.append((tag.upper(), full.strip()[:80]))
        return patched

    content = TAG_RE.sub(replace_tag, content)

    if content == original:
        return False

    if DRY_RUN:
        print(f'\n[DRY] {filename}')
        for tag, line in changed:
            print(f'  {tag}: {line}')
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓ {filename}  ({len(changed)} Emojis entfernt)')

    return True


def main():
    files = sorted(
        f for f in os.listdir(HTML_DIR)
        if f.endswith('.html') and f not in SKIP
    )

    mode = 'DRY-RUN' if DRY_RUN else 'SCHREIBEN'
    print(f'strip-para-emojis.py — Modus: {mode}')
    print(f'Dateien: {len(files)}\n')

    changed = 0
    for fname in files:
        if process_file(os.path.join(HTML_DIR, fname)):
            changed += 1

    print(f'\n{"[DRY] " if DRY_RUN else ""}Fertig — {changed} Dateien geändert.')
    if DRY_RUN:
        print('→ python3 strip-para-emojis.py --write')


if __name__ == '__main__':
    main()
