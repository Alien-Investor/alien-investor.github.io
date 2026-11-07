#!/usr/bin/env python3
"""
update-like-buttons.py
Ersetzt alte Like-Buttons (Gefällt mir + Zähler) durch:
- Alien-SVG statt 👍
- localStorage-Flag (kein Doppelklick nach Reload)
- Kein Zähler, stattdessen Bestätigungstext
"""
import os, re, hashlib, sys

DRY_RUN = '--write' not in sys.argv
HTML_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP = {
    'blog.html', 'index.html', 'buecher.html', 'buch-direkt.html',
    'grapheneos-book.html', 'spenden.html', 'datenschutz.html',
    'impressum.html', 'template-artikel.html',
    'aktien-analysen.html', 'bitcoin-analysen.html',
    'inflation.html',  # bereits erledigt
    'eu-digital-id-bitcoin-grapheneos.html',  # bereits erledigt
}

OLD_BTN_RE = re.compile(r'<div class="like-button">.*?</script>', re.DOTALL)

def make_block(fid):
    alien = (
        f'<svg style="width:0.85em;height:1.1em;vertical-align:-0.2em;filter:drop-shadow(0 0 4px #00ffcc88);" '
        f'viewBox="-4 -14 44 51" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<line x1="10.32" y1="2.98" x2="0.6" y2="-5.2" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<circle cx="0.6" cy="-5.2" r="3" fill="#00ffcc"/>'
        f'<line x1="25.68" y1="2.98" x2="35.4" y2="-5.2" stroke="#00ffcc" stroke-width="1.5" stroke-linecap="round"/>'
        f'<circle cx="35.4" cy="-5.2" r="3" fill="#00ffcc"/>'
        f'<path fill="url(#ai-head-{fid})" stroke="#00ffcc" stroke-width="0.8" d="M1.64 16.04A16.36 16.04 0 0 1 34.36 16.04C34.36 22.24 23.25 36 18 36C12.75 36 1.64 22.24 1.64 16.04Z"/>'
        f'<path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" d="M5.41 15.84A6.55 3.52 32 0 0 9.1 22.29A6.55 3.52 32 0 0 16.51 22.78A6.55 3.52 32 0 0 12.83 16.33A6.55 3.52 32 0 0 5.41 15.84ZM19.49 22.78A6.55 3.52 -32 0 0 26.9 22.29A6.55 3.52 -32 0 0 30.59 15.84A6.55 3.52 -32 0 0 23.17 16.33A6.55 3.52 -32 0 0 19.49 22.78Z"/>'
        f'<circle cx="9.49" cy="17.35" r="0.9" fill="#00ffcc"/><circle cx="26.51" cy="17.35" r="0.9" fill="#00ffcc"/>'
        f'</svg>'
    )
    return (
        f'<div class="like-button">\n'
        f'    <button id="likeButton">{alien} Gefällt mir</button>\n'
        f'    <span id="likeMsg" style="color:#888; font-size:0.9em;"></span>\n'
        f'  </div>\n\n'
        f'  <script>\n'
        f'    (function() {{\n'
        f"      const key = 'liked_' + window.location.pathname.replace(/[^a-z0-9]/gi, '_');\n"
        f'      const btn = document.getElementById(\'likeButton\');\n'
        f'      const msg = document.getElementById(\'likeMsg\');\n'
        f'      if (localStorage.getItem(key)) {{\n'
        f'        btn.disabled = true;\n'
        f"        btn.textContent = '✓ Danke!';\n"
        f"        msg.textContent = 'Freut mich, dass dir der Artikel gefallen hat.';\n"
        f'      }}\n'
        f'      btn.addEventListener(\'click\', function() {{\n'
        f'        localStorage.setItem(key, \'1\');\n'
        f'        btn.disabled = true;\n'
        f"        btn.textContent = '✓ Danke!';\n"
        f"        msg.textContent = 'Freut mich, dass dir der Artikel gefallen hat.';\n"
        f'      }});\n'
        f'    }})();\n'
        f'  </script>'
    )

def process(filepath):
    filename = os.path.basename(filepath)
    fid = hashlib.md5(filename.encode()).hexdigest()[:6]
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    if 'Gefällt mir' not in content and 'likeCount' not in content:
        return False
    if not OLD_BTN_RE.search(content):
        return False
    new_content = OLD_BTN_RE.sub(make_block(fid), content)
    if new_content == content:
        return False
    if DRY_RUN:
        print(f'  [DRY] {filename}')
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'  ✓ {filename}')
    return True

files = sorted(f for f in os.listdir(HTML_DIR) if f.endswith('.html') and f not in SKIP)
print(f'update-like-buttons.py — {"DRY-RUN" if DRY_RUN else "SCHREIBEN"}\n')
changed = sum(process(os.path.join(HTML_DIR, f)) for f in files)
print(f'\nFertig — {changed} Dateien {"würden geändert" if DRY_RUN else "geändert"}.')
if DRY_RUN:
    print('→ python3 update-like-buttons.py --write')
