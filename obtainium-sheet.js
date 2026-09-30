// Obtainium-Blatt: aufklappbare Einrichtungshilfe je App (<details class="ob-sheet">).
// Die Werte stehen als normales HTML in <code data-copy> (lesbar auch ohne JavaScript);
// dieses Skript bringt den Stil mit und hängt an jeden Wert einen Kopier-Knopf.
// Einbinden: <script src="/obtainium-sheet.js" defer></script> — ein Baustein für alle App-Seiten (DE/EN über <html lang>).
(function () {
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = en ? { copy: 'Copy', done: 'Copied', fail: 'Select manually' }
             : { copy: 'Kopieren', done: 'Kopiert', fail: 'Bitte markieren' };

  var css =
    '.ob-sheet{border:1px solid #00ffcc;background:#050505;border-radius:8px;margin:1.5em 0;box-shadow:0 0 10px rgba(0,255,204,0.1);}' +
    '.ob-sheet>summary{cursor:pointer;padding:0.9em 1.2em;color:#00ffcc;font-weight:bold;list-style-position:inside;}' +
    '.ob-sheet[open]>summary{border-bottom:1px solid #1a3a33;}' +
    '.ob-sheet .ob-body{padding:0.4em 1.2em 1.1em 1.2em;}' +
    '.ob-sheet ol{padding-left:1.3em;} .ob-sheet li{margin-bottom:0.9em;}' +
    '.ob-sheet .ob-menu{color:#ccc;}' +
    '.ob-sheet .ob-val{display:flex;gap:0.5em;align-items:stretch;margin-top:0.3em;}' +
    '.ob-sheet .ob-val code{flex:1;display:block;padding:0.45em 0.6em;font-size:0.85em;}' +
    '.ob-sheet .ob-copy{background:#000;color:#00ffcc;border:1px solid #00ffcc;border-radius:6px;padding:0 0.8em;cursor:pointer;font-size:0.85em;white-space:nowrap;}' +
    '.ob-sheet .ob-copy:hover{background:#00ffcc;color:#000;}' +
    '.ob-sheet .ob-open{display:inline-block;margin:0.4em 0 0.2em 0;padding:0.6em 1.2em;border:1px solid #00ffcc;border-radius:8px;font-weight:bold;}' +
    '.ob-sheet .ob-open:hover{background:#00ffcc;color:#000;box-shadow:0 0 15px #00ffcc;text-shadow:none;}' +
    '.ob-sheet .ob-note{color:#aaa;font-size:0.9em;}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (ok, fail) {
      var ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? ok() : fail(); } catch (e) { fail(e); } finally { ta.remove(); }
    });
  }

  function init() {
    document.querySelectorAll('.ob-sheet code[data-copy]').forEach(function (code) {
      var wrap = document.createElement('span'); wrap.className = 'ob-val';
      code.parentNode.insertBefore(wrap, code); wrap.appendChild(code);
      var b = document.createElement('button'); b.type = 'button'; b.className = 'ob-copy'; b.textContent = T.copy;
      b.addEventListener('click', function () {
        copy(code.textContent.trim()).then(function () { b.textContent = T.done; },
                                           function () { b.textContent = T.fail; })
          .then(function () { setTimeout(function () { b.textContent = T.copy; }, 1800); });
      });
      wrap.appendChild(b);
    });
    // Sprungmarke (z. B. apps.html → alien-pass.html#obtainium): Blatt gleich aufgeklappt zeigen
    function openFromHash() {
      var id = decodeURIComponent((location.hash || '').slice(1)); if (!id) return;
      var d = document.getElementById(id);
      if (d && d.classList.contains('ob-sheet')) { d.open = true; d.scrollIntoView(); }
    }
    openFromHash(); window.addEventListener('hashchange', openFromHash);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
