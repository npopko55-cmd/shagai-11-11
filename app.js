/* Распродажа 11.11 «Шагай Дома», v2: фильтры витрины, галерея пака, проброс меток и метка акции */
(function () {
  'use strict';

  /* Метки: тот же набор ключей, что на остальных лендингах */
  var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'utm_referrer', 'gclid', 'yclid', 'fbclid', 'erid', 'from'];
  var STORE = 'shd1111_utm';
  /* Метка акции l_ГГГГММ_имя (задаётся в build.py). По ТЗ покупка через 11.11 должна быть видна,
     даже если берут большой абонемент, поэтому на этом сайте utm_campaign всегда = метка акции. */
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

  function withParams(href) {
    try {
      var u = new URL(href, location.href);
      if (u.origin !== location.origin && !/(^|\.)walk-walk\.ru$/.test(u.hostname)) return href;
      for (var i = 0; i < params.length; i++) {
        var k = params[i][0];
        if (!u.searchParams.has(k) || (k === 'utm_campaign' && SALE)) u.searchParams.set(k, params[i][1]);
      }
      return u.href;
    } catch (err) { return href; }
  }

  if (params.length) {
    /* адрес самой страницы тоже с метками: виджет GetCourse берёт их из location.search */
    var here = withParams(location.href);
    if (here !== location.href) history.replaceState(null, '', here);
    var links = document.querySelectorAll('a[href]');
    for (var l = 0; l < links.length; l++) {
      var h = links[l].getAttribute('href');
      if (h && h.charAt(0) !== '#' && h.indexOf('tel:') !== 0) links[l].setAttribute('href', withParams(h));
    }
  }

  /* Фильтры витрины */
  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('#grid .card');
  Array.prototype.forEach.call(chips, function (chip) {
    chip.addEventListener('click', function () {
      Array.prototype.forEach.call(chips, function (x) { x.classList.toggle('is-on', x === chip); });
      Array.prototype.forEach.call(cards, function (c) {
        c.hidden = !(chip.dataset.aud === 'any' || c.dataset.aud === chip.dataset.aud);
      });
    });
  });

  /* Галерея на странице пака */
  var big = document.querySelector('.pp__photo');
  var thumbs = document.querySelectorAll('.pp__th');
  Array.prototype.forEach.call(thumbs, function (th) {
    th.addEventListener('click', function () {
      big.src = th.dataset.src;
      Array.prototype.forEach.call(thumbs, function (x) { x.classList.toggle('is-on', x === th); });
    });
  });
})();
