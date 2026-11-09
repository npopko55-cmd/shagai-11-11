/* Распродажа 11.11 «Шагай Дома», v4: метки, фильтры, окно оплаты с виджетом GetCourse */
(function () {
  'use strict';

  /* Метки: тот же набор ключей, что на остальных лендингах */
  var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'utm_referrer', 'gclid', 'yclid', 'fbclid', 'erid', 'from'];
  var STORE = 'shd1111_utm';
  /* Метка акции l_ГГГГММ_имя (задаётся в build_v4.py). Покупка через 11.11 должна быть видна, поэтому utm_campaign = метка. */
  var SALE = document.documentElement.getAttribute('data-sale-campaign') || '';
  var params = [];
  try {
    var q = new URLSearchParams(location.search);
    for (var i = 0; i < KEYS.length; i++) { var v = q.get(KEYS[i]); if (v) params.push([KEYS[i], v]); }
    if (params.length) sessionStorage.setItem(STORE, JSON.stringify(params));
    else params = JSON.parse(sessionStorage.getItem(STORE) || '[]');
  } catch (err) {}
  if (SALE) {
    params = params.filter(function (p) { return p[0] !== 'utm_campaign'; });
    params.push(['utm_campaign', SALE]);
  }
  if (params.length) {
    /* виджет GetCourse берёт метки из адреса страницы — кладём их туда до запуска виджета */
    try {
      var u = new URL(location.href);
      for (var k = 0; k < params.length; k++) {
        if (!u.searchParams.has(params[k][0]) || (params[k][0] === 'utm_campaign' && SALE)) u.searchParams.set(params[k][0], params[k][1]);
      }
      if (u.href !== location.href) history.replaceState(null, '', u.href);
    } catch (err) {}
  }

  /* Фильтры */
  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('.pc');
  Array.prototype.forEach.call(chips, function (chip) {
    chip.addEventListener('click', function () {
      Array.prototype.forEach.call(chips, function (x) { x.classList.toggle('is-on', x === chip); });
      Array.prototype.forEach.call(cards, function (c) {
        c.hidden = !(chip.dataset.aud === 'any' || c.dataset.aud === chip.dataset.aud);
      });
    });
  });

  /* Окно оплаты: виджет пака грузится только по нажатию «Купить пак» и остаётся загруженным */
  var dlg = document.getElementById('paydlg');
  if (!dlg) return;
  var body = dlg.querySelector('.paydlg__body');
  function close() {
    if (dlg.close) dlg.close(); else dlg.removeAttribute('open');
  }
  dlg.addEventListener('close', function () { document.documentElement.classList.remove('is-locked'); });
  dlg.querySelector('.paydlg__x').addEventListener('click', close);
  dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });

  Array.prototype.forEach.call(document.querySelectorAll('.pc__buy[data-widget]'), function (btn) {
    btn.addEventListener('click', function () {
      var sid = btn.dataset.sid;
      dlg.querySelector('.paydlg__t').textContent = btn.dataset.title;
      dlg.querySelector('.paydlg__p').textContent = btn.dataset.price;
      var slot = document.getElementById('slot-' + sid);
      if (!slot) {
        slot = document.createElement('div');
        slot.className = 'paydlg__slot';
        slot.id = 'slot-' + sid;
        body.appendChild(slot);
        var s = document.createElement('script');
        s.id = sid;
        s.src = 'https://my.walk-walk.ru/pl/lite/widget/script?id=' + btn.dataset.widget;
        s.onload = function () {
          /* скрипт GetCourse стартует по событию StartWidget<id>, если страница уже загружена */
          var ev;
          try { ev = new Event('StartWidget' + sid); } catch (err) { ev = document.createEvent('Event'); ev.initEvent('StartWidget' + sid, true, true); }
          document.dispatchEvent(ev);
        };
        slot.appendChild(s);
      }
      Array.prototype.forEach.call(body.querySelectorAll('.paydlg__slot'), function (x) { x.hidden = x !== slot; });
      document.documentElement.classList.add('is-locked');
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    });
  });
})();

/* Появление блоков при прокрутке (v9). Без JS и при reduce-motion всё видно сразу. */
(function () {
  var els = document.querySelectorAll('.rv, .pc, .qa, .shop .h2, .faq .h2, .how .h2');
  if (!('IntersectionObserver' in window) || !els.length) return;
  document.documentElement.classList.add('js');
  Array.prototype.forEach.call(els, function (el) { el.classList.add('rv'); });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  Array.prototype.forEach.call(els, function (el) { io.observe(el); });
})();
