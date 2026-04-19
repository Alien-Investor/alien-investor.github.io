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
        f'viewBox="-4 -16 44 51" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<line x1="13" y1="2" x2="4" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/>'
        f'<circle cx="4" cy="-13" r="2.8" fill="#00ffcc"/>'
        f'<line x1="23" y1="2" x2="32" y2="-12" stroke="#00ffcc" stroke-width="1.4" stroke-linecap="round"/>'
        f'<circle cx="32" cy="-13" r="2.8" fill="#00ffcc"/>'
        f'<path fill="url(#ai-head-{fid})" stroke="#00ffcc" stroke-width="0.8" d="M35 17c0 9.389-13.223 19-17 19-3.778 0-17-9.611-17-19S8.611 0 18 0s17 7.611 17 17z"/>'
        f'<path fill="#001a0e" stroke="#00ffcc" stroke-width="0.5" d="M13.503 14.845c3.124 3.124 4.39 6.923 2.828 8.485-1.562 1.562-5.361.297-8.485-2.828-3.125-3.124-4.391-6.923-2.828-8.485s5.361-.296 8.485 2.828zm8.994 0c-3.124 3.124-4.39 6.923-2.828 8.485 1.562 1.562 5.361.297 8.485-2.828 3.125-3.125 4.391-6.923 2.828-8.485-1.562-1.562-5.361-.297-8.485 2.828z"/>'
        f'<path fill="none" stroke="#001a0e" stroke-width="1.2" stroke-linecap="round" d="M12 27 Q18 33 24 27"/>'
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
