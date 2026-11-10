#!/usr/bin/env python3
"""Распродажа 11.11 «Шагай Дома», страница /v5/ — вёрстка по концептам GPT Image Sunburst (Никита, 09.11.2026):
~/Downloads/shagai-v4-ref/improve/gpt-hero.png (первый экран) и gpt-packs.png (блок паков).

Всё свёрстано кодом, из концептов ничего не вырезано. Фото — те же кадры клуба, что на v4.
Данные наборов (состав, цены, фразы Маши, виджеты GetCourse) — v4_data_snapshot.py (снимок v4 6e118b5 + правка Маши «пак» → «набор»).\nАбонементы клуба «Удвоение 6+6» и «Навсегда» — CLUBS ниже (ТЗ Сони, без виджетов).
v4/, корень (v3) и v2/ не трогает. Запуск: python3 build_v5.py
"""
import html
import pathlib

import v4_data_snapshot as d

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'v5'
# фото «Все хиты» как на концепте: тренер с поднятой рукой (настоящий кадр клуба)
# 10.11 (Мария): «Отдых» — другой кадр (две девушки в движении), «Красота» — Валерия снова на фоне цветов (исходный кадр, v2/assets/p5.webp)
PHOTO = {'p6': ('hits', '50% 18%'), 'p3': ('hits2', '50% 30%'), 'p5': ('valeria-flowers', '50% 35%')}
# кадр в окне «Подробнее» (шапка окна 4/3 на телефоне, 16/10 на десктопе): у вертикальных фото — лицо и корпус, а не поднятая рука
MPOS = {'p1': '50% 45%', 'p2': '50% 25%', 'p3': '50% 30%', 'p4': '50% 50%', 'p5': '50% 35%', 'p6': '50% 42%'}
# п.7 (Мария): пометка у Антиотёка и Лагеря
# Мария 10.11 15:07: все программы этих карточек без интерактива — одна общая спокойная пометка под списком
NOINT_NOTE = '*без интерактива в чатах'
NOINT_PACKS = {'p1', 'p3'}
# п.3: второй вариант 2 490 ₽ в окне свёрнут в одну строку (na-pero 10.11)
# 10.11 11:20 (Мария): плашка должна быть заметной и объяснять, откуда 2 490 ₽. Тексты — na-pero.
ALT_Q = 'Нет абонемента или осталось меньше 30 дней?'
ALT_A = 'Программа и полный доступ в клуб на месяц — 2 490 ₽'
ALT_OPEN, ALT_CLOSE = 'Развернуть', 'Свернуть'
CHEV = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

# Абонементы клуба 11.11 (ТЗ Сони; цены «участникам клуба / новым участникам» — из v2/_build_v2.py).
# Тексты — na-pero 09.11.2026. Старых цен в материалах нет — не зачёркиваем.
# Виджетов GetCourse на эти цены в проекте нет: кнопки «Купить» без data-widget, ничего не делают.
CLUB_T = dict(
    H2='Абонементы клуба',
    LEAD='Удваиваем абонемент на 6 месяцев или даём доступ к клубу навсегда — для тех, у кого уже есть абонемент, и для новых участников.',
    WHAT_H='Что есть в клубе:',
    WHAT=['25 фитнес-программ и курсов, больше 400 тренировок', 'План тренировок на каждый день недели', 'Тренировки от 5 до 40 минут',
          'Шагай.FM — фитнес-эфир нон-стоп под треки DJ', 'Шаговая аэробика под музыку: не нужно быть спортивной или уметь танцевать'],
    MEM='Участникам клуба', NEW='Новым участникам',
)
CLUBS = [
    dict(id='c1', aud='all', img='sanatoriy', pos='50% 36%', mpos='50% 36%', title='Клуб «Удвоение\u00a06+6»',
         line='6 месяцев абонемента и ещё 6 в подарок', chips=[('clock', '12 месяцев'), ('check', 'Полный доступ к клубу')],
         about='Платите за 6 месяцев абонемента и получаете ещё 6 в подарок. Итого 12 месяцев полного доступа к тренировкам и программам клуба. Цены распродажи действуют 10–12 ноября.',
         mem=3800, new=4400, card_price=('от', 3800), new_first=True,
         # виджеты GetCourse от Ани, 10.11: (номер, id скрипта)
         mem_w=('1681432', '7018af0150b7060df01b222f88fc2208baa5ce44'), new_w=('1681429', 'c06de214a59b9c1aed42942fcfefed2906fe2b5f'), month=('Выходит от 317 ₽ за месяц', 'Всего 318₽ в месяц', 'Всего 367₽ в месяц')),  # подписи — Мария 10.11 15:08
    dict(id='c2', aud='all', img='club2', pos='50% 22%', mpos='50% 22%', title='Клуб «Навсегда»',
         line='Абонемент, который не нужно продлевать', chips=[('clock', 'Бессрочно'), ('check', 'Полный доступ к клубу')],
         about='Полный доступ к клубу без ограничения срока: можно заниматься дома в удобном ритме и возвращаться к любимым тренировкам. Цены распродажи действуют 10–12 ноября.',
         mem=7990, new=9990, card_price=('', 9990), new_first=True,
         # виджеты GetCourse от Ани, 10.11: (номер, id скрипта)
         mem_w=('1681435', '35016c1712dc0a8c01ea4b3c82c4ddc41525172f'), new_w=('1681434', 'da707c020c8ce53f881381bff3a2576cb2190bb3')),
]


# Превью ссылки в мессенджерах и meta description (текст — na-pero 10.11.2026)
SITE_URL = 'https://npopko55-cmd.github.io/shagai-11-11/v5/'
PAGE_TITLE = 'Распродажа 11.11 — программы и абонементы клуба «Шагай Дома»'
META_DESC = 'Программы клуба домашних тренировок «Шагай Дома» со скидкой 50% и абонементы «Удвоение 6+6» и «Навсегда». Цены действуют с 10 по 12 ноября.'
# Сообщение по кнопке «Купить», к которой ещё нет виджета GetCourse (990 ₽ ×2, клуб 1 600 ₽, абонементы ×4). Текст — na-pero 10.11.2026.
# Телефон — первый из подвала (отдел заботы о клиентах). Когда виджет появится, кнопке достаточно дать widget и sid.
NOTICE_T = 'Оплата этого варианта на сайте пока не подключена.'
NOTICE_P = 'Чтобы купить сейчас, позвоните в отдел заботы о клиентах:'
NOTICE_TEL = ('+79990668100', '+7\u00a0(999)\u00a0066-81-00')


def name(p):
    # 10.11 (Мария и Дима): слово «набор» убрано — название программы без приставки
    return p['title']
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
    '17 недельных меню': 'cloche', 'Меню ПП-пирогов': 'fork', '2 меню напитков': 'cup', 'Меню десертов': 'book', 'Меню ПП-куличей': 'checkc',
    'Фейс-йога от Валерии': 'leaf', 'Женское здоровье от Вики': 'female', 'Осанка от Вики': 'lotus', 'Зарядки 5 минут от Димы': 'bolt',
    'Все хиты': 'play', '80-е новые': 'bolt', '80-е старые': 'star',
}


def li_icon(name):
    return '<svg class="pc__ico" viewBox="0 0 24 24" aria-hidden="true">' + LI[ITEM_ICON.get(name, 'checkc')] + '</svg>'


def buy_btn(title, price, widget=None, sid=None, ghost=False):
    cls = 'pc__buy' + (' pc__buy--ghost' if ghost else '')
    data = f' data-title="{html.escape(title)}" data-price="{rub(price)}"'
    if widget:
        data = f' data-widget="{widget}" data-sid="{sid}"' + data
    return f'<button class="{cls}" type="button"{data}>' + icon('bag') + 'Купить</button>'


# Короткий бейдж аудитории на превью (подпись «Для всех» — как в фильтре)
AUD_SHORT = {'members': AUD['members'][0], 'new': AUD['new'][0], 'all': 'Для всех'}
# Условия покупки для паков с одной ценой — пояснения аудиторий из блока над фильтрами
AUD_COND = {'members': d.HOLDER, 'new': T['AUD_NEW_EXPL'], 'all': T['AUD_ALL_EXPL']}
COND_TBD = 'Условия уточняются'  # плейсхолдер, если для кнопки нет условий в материалах


def img_size(name):
    """Размер картинки из assets (заголовок WebP: VP8X, VP8L или VP8) — для width/height в разметке."""
    import struct
    data = (OUT / 'assets' / (name + '.webp')).read_bytes()[:40]
    kind = data[12:16]
    if kind == b'VP8X':
        return int.from_bytes(data[24:27], 'little') + 1, int.from_bytes(data[27:30], 'little') + 1
    if kind == b'VP8L':
        bits = struct.unpack('<I', data[21:25])[0]
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    w, h = struct.unpack('<HH', data[26:30])
    return w & 0x3FFF, h & 0x3FFF


def photo(p, modal=False):
    img, pos = PHOTO.get(p['id'], (p['img'], p['pos']))
    if modal:
        pos = p.get('mpos') or MPOS.get(p['id'], pos)
    w, h = img_size(img)
    return f'<img class="pc__photo" src="assets/{img}.webp" alt="" width="{w}" height="{h}" loading="lazy" decoding="async" style="object-position:{pos}">'


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


def contents(p):
    """Содержимое программы: описание, чипы, «Что внутри» с сутью программ, варианты цены с условиями и «Купить»."""
    rows = ''.join(f'<li>{li_icon(n)}<span class="pc__item"><b>{t(n + (" — " + q if q else ""))}</b>'
                   + (f'<small>{t(sub)}</small>' if sub else '')
                   + '</span></li>'
                   for n, q, sub in p['items'])
    lead = f'<p class="pc__lead">{t(p["lead"])}</p>' if p.get('lead') else ''
    about = f'<p class="pc__about">{t(p["about"])}</p>' if p.get('about') else ''
    meta = '<span>' + icon('stack') + t(p['count']) + '</span>'
    if p.get('term'):
        meta += '<span>' + icon('clock') + t(p['term']) + '</span>'
    if p.get('note'):
        meta += '<span class="pc__chip--no">' + icon('ban') + t(p['note']) + '</span>'
    opts = ''
    if p.get('opts'):
        # «Стройное тело» и «Отдых»: 990 ₽ держателям (виджета пока нет — кнопка без действия) + 2 490 ₽ с клубом на месяц (виджет GetCourse)
        for n, o in enumerate(p['opts']):
            cap, title_o, old_o, price_o = o[:4]
            w, sid = (o[4], o[5]) if len(o) > 4 else (None, None)
            opt_html = option(cap, price_row(old_o, price_o), buy_btn(title_o or name(p), price_o, w, sid, ghost=n > 0), title_o)
            # второй вариант (2 490 ₽) — свёрнут, раскрывается по тапу (Мария 09.11: «придумай как скрыть это»)
            opts += opt_html if n == 0 else (f'<details class="pk__alt"><summary><span class="pk__altq"><b>{t(ALT_Q)}</b><span>{t(ALT_A)}</span></span>'
                                                f'<span class="pk__altgo"><span class="pk__alt-o">{ALT_OPEN}</span><span class="pk__alt-c">{ALT_CLOSE}</span>{CHEV}</span>'
                                                f'</summary>{opt_html}</details>')
    else:
        opts += option(AUD_COND.get(p['aud']), price_row(p['old'], p['price']), buy_btn(name(p), p['price'], p['widget'], p['sid']))
        if p.get('extra'):
            # «Фитнес»: клуб на месяц за 1 600 ₽ — виджет 1681202 (Аня, 10.11)
            et, es, ep = p['extra'][:3]
            ew, esid = (p['extra'][3], p['extra'][4]) if len(p['extra']) > 3 else (None, None)  # виджет GetCourse, если Аня его дала
            opts += option(es, price_row(0, ep), buy_btn(et, ep, ew, esid, ghost=True), et)
    return (f'{lead}{about}\n    <p class="pc__meta">{meta}</p>\n    <p class="pc__in">Что внутри:</p>\n    <ul class="pc__list">{rows}</ul>\n'
            + (f'    <p class="pc__noint">{t(NOINT_NOTE)}</p>\n' if p['id'] in NOINT_PACKS else '')
            + f'    <div class="pc__foot"><div class="pk__opts">{opts}</div></div>')


def card(p):
    """10.11 (Мария): всё прямо в карточке — без короткого превью и окна «Подробнее»."""
    label, ic = AUD[p['aud']]
    return f'''<article class="pc" data-aud="{p["aud"]}" id="{p["id"]}">
  <div class="pc__media">
    {photo(p)}
    <span class="pc__aud pc__aud--{p["aud"]}">{icon(ic)}{t(label)}</span>
  </div>
  <div class="pc__body">
    <h3 class="pc__t">{t(name(p))}</h3>{contents(p)}
  </div>
</article>'''


def club_card(c):
    """Абонемент целиком на странице: описание, чипы, что есть в клубе, обе цены с цена-за-месяц и «Купить» (виджетов нет)."""
    label, ic = AUD[c['aud']]
    meta = ''.join('<span>' + icon(i) + t(x) + '</span>' for i, x in c['chips'])
    rows = ''.join(f'<li>{li_icon("")}<span class="pc__item"><b>{t(x)}</b></span></li>' for x in CLUB_T['WHAT'])
    mo = c.get('month')
    m1 = f'<p class="pc__month">{t(mo[1])}</p>' if mo else ''
    m2 = f'<p class="pc__month">{t(mo[2])}</p>' if mo else ''
    # порядок цен: «Навсегда» — сначала 9 990 ₽ для новых (Мария 09.11), 6+6 — сначала участникам
    o_mem = option(CLUB_T['MEM'], price_row(0, c['mem']) + m1, buy_btn(c['title'], c['mem'], *c.get('mem_w', (None, None)), ghost=c.get('new_first', False)))
    o_new = option(CLUB_T['NEW'], price_row(0, c['new']) + m2, buy_btn(c['title'], c['new'], *c.get('new_w', (None, None)), ghost=not c.get('new_first', False)))
    opts = (o_new + o_mem) if c.get('new_first') else (o_mem + o_new)
    return f'''<article class="pc pc--club" data-aud="{c["aud"]}" id="{c["id"]}">
  <div class="pc__media">
    {photo(c)}
    <span class="pc__aud pc__aud--{c["aud"]}">{icon(ic)}{t(label)}</span>
  </div>
  <div class="pc__body">
    <h3 class="pc__t">{t(c["title"])}</h3>
    <p class="pc__lead">{t(c["line"])}</p>
    <p class="pc__about">{t(c["about"])}</p>
    <p class="pc__meta">{meta}</p>
    <p class="pc__in">{t(CLUB_T["WHAT_H"])}</p>
    <ul class="pc__list">{rows}</ul>
    <div class="pc__foot"><div class="pk__opts">{opts}</div></div>
  </div>
</article>'''


def page():
    jump = ''.join(f'<a href="#{p["id"]}">{t(p["title"])}</a>' for p in PACKS) + '<a class="jump__club" href="#clubs">Абонементы</a>'
    steps = ''.join(f'<li><b class="steps__n">{i}</b><p>{t(s)}</p></li>' for i, s in enumerate(T['HOW'], 1))
    faq = ''.join(f'<details class="qa"><summary>{t(q)}</summary><p>{t(a)}</p></details>' for q, a in T['FAQ'])
    return f'''<!doctype html>
<html lang="ru" data-sale-campaign="{d.SALE_CAMPAIGN}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{PAGE_TITLE}</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f6f0ff">
<meta name="description" content="{html.escape(META_DESC)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Шагай Дома">
<meta property="og:title" content="{html.escape(PAGE_TITLE)}">
<meta property="og:description" content="{html.escape(META_DESC)}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}assets/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="styles.css">
</head>
<body id="top">
<header class="top"><div class="wrap top__in">
  <a class="logo" href="#top" aria-label="Шагай Дома">{d.LOGO}</a>
  <nav class="top__nav" aria-label="Разделы"><a href="#packs">Программы</a><a href="#clubs">Абонементы</a><a href="#how">Как купить</a><a href="#faq">Вопросы</a></nav>
  <a class="btn btn--sm" href="#packs">Выбрать программы</a>
</div></header>
<main>
<section class="hero"><div class="wrap hero__in">
  <div class="hero__text">
    <span class="hero__pill">Акция 11.11</span>
    <h1 class="hero__h"><span>Большая распродажа</span> <em>любимых программ</em></h1>
    <p class="hero__lead">{t(T["HERO_LEAD"])}</p>
    <a class="btn btn--lg" href="#packs">Выбрать программы</a>
    <ul class="perks"><li>{icon("gift")}<span>Специальные<br>цены</span></li><li>{icon("loop")}<span>Выбирай<br>программы</span></li><li>{icon("bolt")}<span>Действуй<br>10–12 ноября</span></li></ul>
  </div>
  <div class="hero__art" aria-hidden="true">
    <span class="hero__blob"></span>
    <p class="hero__num">11<i>.</i>11</p>
    <span class="ring ring--back"></span>
    <img class="hero__cut" src="assets/hero-cut.webp" alt="" width="{img_size("hero-cut")[0]}" height="{img_size("hero-cut")[1]}" fetchpriority="high">
    <span class="ring ring--front"></span>
    <p class="hero__card">Любимые программы клуба со&nbsp;скидкой</p>
  </div>
</div></section>

<section class="shop" id="packs"><div class="wrap">
  <h2 class="sr-only">Программы распродажи</h2>
  <nav class="jump" aria-label="Разделы страницы">{jump}</nav>
  <div class="grid grid--packs">{"".join(card(p) for p in PACKS)}</div>
</div></section>

<section class="clubs" id="clubs"><div class="wrap">
  <h2 class="h2 h2--s">{t(CLUB_T["H2"])}</h2>
  <p class="shop__lead">{t(CLUB_T["LEAD"])}</p>
  <div class="grid grid--clubs">{"".join(club_card(c) for c in CLUBS)}</div>
</div></section>

<section class="how" id="how"><div class="wrap">
  <h2 class="h2 h2--s">{t(T["HOW_H"])}</h2>
  <ol class="steps">{steps}</ol>
  <a class="btn" href="#packs">Выбрать программы</a>
</div></section>

<section class="faq" id="faq"><div class="wrap">
  <h2 class="h2 h2--s">{t(T["FAQ_H"])}</h2>
  <div class="faq__list">{faq}</div>
</div></section>
</main>
<div class="wrap">{d.FOOTER}</div>
<dialog class="paydlg" id="paydlg" aria-labelledby="paydlg-t">
  <div class="paydlg__head"><div><p class="paydlg__t" id="paydlg-t"></p><p class="paydlg__p"></p></div>
  <button class="paydlg__x" type="button" aria-label="Закрыть">{icon("x")}</button></div>
  <div class="paydlg__body"><span class="paydlg__spin" aria-hidden="true"></span><div class="paydlg__slot paydlg__note" id="slot-note" hidden><p><b>{t(NOTICE_T)}</b></p><p>{t(NOTICE_P)} <a href="tel:{NOTICE_TEL[0]}">{NOTICE_TEL[1]}</a></p></div></div>
</dialog>
<script src="app.js"></script>
</body>
</html>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(page())
    print('собрано: v5/index.html')
