#!/usr/bin/env python3
"""Распродажа 11.11 «Шагай Дома», страница /v5/ — вёрстка по концептам GPT Image Sunburst (Никита, 09.11.2026):
~/Downloads/shagai-v4-ref/improve/gpt-hero.png (первый экран) и gpt-packs.png (блок паков).

Всё свёрстано кодом, из концептов ничего не вырезано. Фото — те же кадры клуба, что на v4.
Данные паков (состав, цены, фразы Маши, виджеты GetCourse) — снимок опубликованной v4 (v4_data_snapshot.py, коммит 6e118b5).
v4/, корень (v3) и v2/ не трогает. Запуск: python3 build_v5.py
"""
import html
import pathlib

import v4_data_snapshot as d

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'v5'
# фото «Все хиты» как на концепте: тренер с поднятой рукой (настоящий кадр клуба)
PHOTO = {'p6': ('hits', '50% 18%')}
t, rub, icon, AUD, PACKS, T = d.t, d.rub, d.icon, d.AUD, d.PACKS, d.T

# линейные иконки состава (как на концепте)
LI = {
    'run': '<circle cx="14" cy="4" r="2"/><path d="M7 21l3-6 3 2v5M5 12l3-3 4 1 3 3 3 1M10 15l1-5"/>',
    'waist': '<path d="M8 3c0 4 2 5 2 9s-2 5-2 9M16 3c0 4-2 5-2 9s2 5 2 9M9 12h6"/>',
    'leg': '<path d="M10 2v9l-3 9h4l2-6 1 6h3l-2-11V2"/>',
    'dumbbell': '<path d="M3 9v6M6 7v10M18 7v10M21 9v6M6 12h12"/>',
    'lotus': '<path d="M12 20c-4 0-8-3-8-7 3 0 6 2 8 5 2-3 5-5 8-5 0 4-4 7-8 7zM12 18c-2-3-2-8 0-12 2 4 2 9 0 12z"/>',
    'stack': '<path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5"/>',
    'tent': '<path d="M3 20L12 4l9 16zM12 4v16M9 20l3-6 3 6"/>',
    'leaf': '<path d="M5 19C5 10 11 5 20 4c0 9-5 15-14 15zM5 19l8-8"/>',
    'cloche': '<path d="M3 17h18M5 17a7 7 0 0 1 14 0M12 8V6M10 6h4"/>',
    'fork': '<path d="M7 3v8a2 2 0 0 0 4 0V3M9 11v10M17 3c-2 2-2 6 0 8v10"/>',
    'cup': '<path d="M5 8h12v5a5 5 0 0 1-5 5h-2a5 5 0 0 1-5-5zM17 10h2a2 2 0 0 1 0 4h-2"/>',
    'book': '<path d="M4 5c3-1 6-1 8 1 2-2 5-2 8-1v14c-3-1-6-1-8 1-2-2-5-2-8-1zM12 6v14"/>',
    'checkc': '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    'female': '<circle cx="12" cy="9" r="5"/><path d="M12 14v7M9 18h6"/>',
    'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    'play': '<circle cx="12" cy="12" r="9"/><path d="M10 8l6 4-6 4z"/>',
    'star': '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4l-5.5 2.9 1-6.2L3 9.7l6.2-.9z"/>',
}
ITEM_ICON = {
    'Антиотёк': 'run', 'Стройный живот': 'waist', 'Стройные ноги': 'leg',
    'Табата': 'dumbbell', 'Зумба': 'lotus', 'Интервальные': 'stack',
    'Лагерь «Осень 25»': 'tent', 'Санаторий № 1': 'leaf',
    '19 недельных меню': 'cloche', 'Меню ПП-пирогов': 'fork', '2 меню напитков': 'cup', 'Меню десертов': 'book', 'Меню ПП-куличей': 'checkc',
    'Фейс-йога от Валерии': 'leaf', 'Женское здоровье от Вики': 'female', 'Осанка от Вики': 'lotus', 'Зарядки 5 минут от Димы': 'bolt',
    'Все хиты': 'play', '80-е новые': 'bolt', '80-е старые': 'star',
}


def li_icon(name):
    return '<svg class="pc__ico" viewBox="0 0 24 24" aria-hidden="true">' + LI[ITEM_ICON.get(name, 'checkc')] + '</svg>'


def buy_btn(title, price, widget=None, sid=None, ghost=False):
    cls = 'pc__buy' + (' pc__buy--ghost' if ghost else '')
    data = (f' data-widget="{widget}" data-sid="{sid}" data-title="{html.escape(title)}" data-price="{rub(price)}"' if widget else '')
    return f'<button class="{cls}" type="button"{data}>' + icon('bag') + 'Купить</button>'


# Короткий бейдж аудитории на превью (подпись «Для всех» — как в фильтре)
AUD_SHORT = {'members': AUD['members'][0], 'new': AUD['new'][0], 'all': 'Для всех'}
# Условия покупки для паков с одной ценой — пояснения аудиторий из блока над фильтрами
AUD_COND = {'members': d.HOLDER, 'new': T['AUD_NEW_EXPL'], 'all': T['AUD_ALL_EXPL']}
COND_TBD = 'Условия уточняются'  # плейсхолдер, если для кнопки нет условий в материалах


def photo(p):
    img, pos = PHOTO.get(p['id'], (p['img'], p['pos']))
    return f'<img class="pc__photo" src="assets/{img}.webp" alt="" loading="lazy" style="object-position:{pos}">'


def price_row(old, price):
    pct = f'<i>−{round(100 - price * 100 / old)}%</i>' if old else ''
    return f'<p class="pc__price">' + (f'<s>{rub(old)}</s>' if old else '') + f'<b>{rub(price)}</b>{pct}</p>'


def option(cond, price_html, btn, title=''):
    """Вариант покупки в окне пака: название варианта (если есть), условия, цена, кнопка."""
    head = f'<p class="pk__optt">{t(title)}</p>' if title else ''
    return f'<div class="pk__opt">{head}<p class="pk__cond">{t(cond or COND_TBD)}</p>{price_html}{btn}</div>'


def main_price(p):
    if p.get('opts'):
        o = p['opts'][0]
        return o[2], o[3]
    return p['old'], p['price']


def card(p):
    """Превью: фото, бейдж, название, одна строка сути (лид или объём), главная цена, «Подробнее»."""
    line = p.get('lead') or p['count']
    old, price = main_price(p)
    label, ic = AUD[p['aud']]
    return f'''<article class="pc" data-aud="{p["aud"]}" id="{p["id"]}">
  <div class="pc__media">
    {photo(p)}
    <span class="pc__aud pc__aud--{p["aud"]}">{icon(ic)}{t(AUD_SHORT[p["aud"]])}</span>
  </div>
  <div class="pc__body">
    <h3 class="pc__t">{t(p["title"])}</h3>
    <p class="pc__line">{t(line)}</p>
    <div class="pc__foot">{price_row(old, price)}<button class="pc__more" type="button" data-pk="pk-{p["id"]}" aria-haspopup="dialog">Подробнее</button></div>
  </div>
</article>'''


def pack_dialog(p):
    """Окно пака: лид, описание, мета, полный состав с сутью программ, все варианты покупки с условиями."""
    rows = ''.join(f'<li>{li_icon(n)}<span class="pc__item"><b>{t(n + (" — " + q if q else ""))}</b>'
                   + (f'<small>{t(sub)}</small>' if sub else '') + '</span></li>'
                   for n, q, sub in p['items'])
    label, ic = AUD[p['aud']]
    lead = f'<p class="pc__lead">{t(p["lead"])}</p>' if p.get('lead') else ''
    about = f'<p class="pc__about">{t(p["about"])}</p>' if p.get('about') else ''
    meta = '<span>' + icon('stack') + t(p['count']) + '</span>'
    if p.get('term'):
        meta += '<span>' + icon('clock') + t(p['term']) + '</span>'
    if p.get('note'):
        meta += '<span class="pc__chip--no">' + icon('ban') + t(p['note']) + '</span>'
    opts = ''
    if p.get('opts'):
        # паки 1 и 3: 990 ₽ держателям (виджета пока нет — кнопка без действия) + 2 490 ₽ с клубом на месяц (виджет GetCourse)
        for n, o in enumerate(p['opts']):
            cap, title_o, old_o, price_o = o[:4]
            w, sid = (o[4], o[5]) if len(o) > 4 else (None, None)
            opts += option(cap, price_row(old_o, price_o), buy_btn(title_o or p['title'], price_o, w, sid, ghost=n > 0), title_o)
    else:
        opts += option(AUD_COND.get(p['aud']), price_row(p['old'], p['price']), buy_btn(p['title'], p['price'], p['widget'], p['sid']))
        if p.get('extra'):
            # «Фитнес»: клуб на месяц за 1 600 ₽ — кнопка пока без действия
            et, es, ep = p['extra']
            opts += option(es, price_row(0, ep), buy_btn(et, ep, ghost=True), et)
    return f'''<dialog class="pk" id="pk-{p["id"]}" aria-labelledby="pk-{p["id"]}-t">
  <button class="pk__x" type="button" aria-label="Закрыть">{icon("x")}</button>
  <div class="pk__in">
    <div class="pk__media">{photo(p)}<span class="pc__aud pc__aud--{p["aud"]}">{icon(ic)}{t(label)}</span></div>
    <div class="pk__body">
      <h3 class="pc__t" id="pk-{p["id"]}-t">{t(p["title"])}</h3>{lead}{about}
      <p class="pc__meta">{meta}</p>
      <p class="pc__in">Что внутри:</p>
      <ul class="pc__list">{rows}</ul>
      <div class="pk__opts">{opts}</div>
    </div>
  </div>
</dialog>'''


def page():
    def count(a):
        return sum(1 for p in PACKS if a == 'any' or p['aud'] == a)
    chips = ''.join(
        f'<button class="chip{" is-on" if a == "any" else ""}" type="button" data-aud="{a}">{t(label)}<i>{count(a)}</i></button>'
        for a, label in [('any', 'Все предложения'), ('members', 'Для держателей абонемента'), ('new', 'Для новых пользователей'), ('all', 'Для всех')])
    legend = ''.join(
        f'<li class="lg lg--{k}"><span class="lg__ic">{icon(AUD[k][1])}</span><div><b>{t(AUD[k][0])}</b><p>{t(x)}</p></div></li>'
        for k, x in [('members', d.HOLDER), ('new', T['AUD_NEW_EXPL']), ('all', T['AUD_ALL_EXPL'])])
    steps = ''.join(f'<li><b class="steps__n">{i}</b><p>{t(s)}</p></li>' for i, s in enumerate(T['HOW'], 1))
    faq = ''.join(f'<details class="qa"><summary>{t(q)}</summary><p>{t(a)}</p></details>' for q, a in T['FAQ'])
    return f'''<!doctype html>
<html lang="ru" data-sale-campaign="{d.SALE_CAMPAIGN}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Распродажа 11.11 — паки программ «Шагай Дома»</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f6f0ff">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body id="top">
<header class="top"><div class="wrap top__in">
  <a class="logo" href="#top" aria-label="Шагай Дома">{d.LOGO}</a>
  <nav class="top__nav" aria-label="Разделы"><a href="#packs">Паки программ</a><a href="#how">Как купить</a><a href="#faq">Вопросы</a></nav>
  <a class="btn btn--sm" href="#packs">Выбрать пак</a>
</div></header>
<main>
<section class="hero"><div class="wrap hero__in">
  <div class="hero__text">
    <span class="hero__pill">Акция 11.11</span>
    <h1 class="hero__h"><span>Большая распродажа</span> <em>любимых программ</em></h1>
    <p class="hero__lead">{t(T["HERO_LEAD"])}</p>
    <a class="btn btn--lg" href="#packs">Выбрать пак</a>
    <ul class="perks"><li>{icon("gift")}<span>Специальные<br>цены</span></li><li>{icon("loop")}<span>Выбирай<br>свой пакет</span></li><li>{icon("bolt")}<span>Действуй<br>10–12 ноября</span></li></ul>
  </div>
  <div class="hero__art" aria-hidden="true">
    <span class="hero__blob"></span>
    <p class="hero__num">11<i>.</i>11</p>
    <span class="ring ring--back"></span>
    <img class="hero__cut" src="assets/hero-cut.webp" alt="">
    <span class="ring ring--front"></span>
    <p class="hero__card">Любимые программы в&nbsp;выгодных наборах</p>
  </div>
</div></section>

<section class="shop" id="packs"><div class="wrap">
  <p class="kicker"><span>Распродажа</span>Паки программ клуба «ШАГАЙ ДОМА⚡️»</p>
  <h2 class="h2">Паки программ</h2>
  <p class="shop__lead">{t(T["PACKS_LEAD"])}</p>
  <ul class="legend">{legend}</ul>
  <div class="chips">{chips}</div>
  <div class="grid">{"".join(card(p) for p in PACKS)}</div>
</div></section>

<section class="how" id="how"><div class="wrap">
  <h2 class="h2 h2--s">{t(T["HOW_H"])}</h2>
  <ol class="steps">{steps}</ol>
  <a class="btn" href="#packs">Выбрать пак</a>
</div></section>

<section class="faq" id="faq"><div class="wrap">
  <h2 class="h2 h2--s">{t(T["FAQ_H"])}</h2>
  <div class="faq__list">{faq}</div>
</div></section>
</main>
<div class="wrap">{d.FOOTER}</div>
{"".join(pack_dialog(p) for p in PACKS)}
<dialog class="paydlg" id="paydlg" aria-labelledby="paydlg-t">
  <div class="paydlg__head"><div><p class="paydlg__t" id="paydlg-t"></p><p class="paydlg__p"></p></div>
  <button class="paydlg__x" type="button" aria-label="Закрыть">{icon("x")}</button></div>
  <div class="paydlg__body"><span class="paydlg__spin" aria-hidden="true"></span></div>
</dialog>
<script src="app.js"></script>
</body>
</html>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(page())
    print('собрано: v5/index.html')
