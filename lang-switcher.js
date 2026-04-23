(function () {
  var path = window.location.pathname;
  var isEn = path.indexOf('/en/') === 0;
  var file = (isEn ? path.slice(4) : path).split('/').pop() || 'index.html';
  var deUrl = '/' + file;
  var enUrl = '/en/' + file;

  var css = document.createElement('style');
  css.textContent =
    '.lang-toggle{display:flex;align-items:center;gap:6px;font-size:0.85em;white-space:nowrap}' +
    '.lang-toggle a{color:#00ffcc;text-decoration:none;padding:2px 8px;border-radius:3px;transition:color .2s,text-shadow .2s}' +
    '.lang-toggle a:hover{color:#fff;text-shadow:0 0 8px #00ffcc}' +
    '.lang-cur{color:#fff;background:rgba(0,255,204,.15);padding:2px 8px;border-radius:3px;cursor:default;font-weight:bold}' +
    '.lang-sep{color:#444;user-select:none}';
  document.head.appendChild(css);

  function makeToggle() {
    var el = document.createElement('div');
    el.className = 'lang-toggle';
    if (isEn) {
      el.innerHTML =
        '<a href="' + deUrl + '" onclick="localStorage.setItem(\'lang\',\'de\')">DE</a>' +
        '<span class="lang-sep">|</span>' +
        '<span class="lang-cur">EN</span>';
    } else {
      el.innerHTML =
        '<span class="lang-cur">DE</span>' +
        '<span class="lang-sep">|</span>' +
        '<a href="' + enUrl + '" onclick="localStorage.setItem(\'lang\',\'en\')">EN</a>';
    }
    return el;
  }

  function inject() {
    var nav = document.querySelector('.top-nav');
    if (nav) {
      nav.style.display = 'flex';
      nav.style.justifyContent = 'space-between';
      nav.style.alignItems = 'center';
      nav.appendChild(makeToggle());
    } else {
      var wrap = document.createElement('div');
      wrap.style.cssText = 'position:fixed;top:14px;right:18px;z-index:9999;';
      wrap.appendChild(makeToggle());
      document.body.appendChild(wrap);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
