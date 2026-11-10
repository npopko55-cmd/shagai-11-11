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
NOINT = {'Антиотёк': '*без интерактива в чатах', 'Лагерь «Осень 25»': '*без интерактива в чатах'}
# п.3: второй вариант 2 490 ₽ в окне свёрнут в одну строку (na-pero 10.11)
ALT_SUMMARY = 'Нет абонемента или он меньше 30 дней: 2 490 ₽'

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
    dict(id='c1', aud='all', img='sanatoriy', pos='50% 8%', mpos='50% 36%', title='Клуб «Удвоение\u00a06+6»',
         line='6 месяцев абонемента и ещё 6 в подарок', chips=[('clock', '12 месяцев'), ('check', 'Полный доступ к клубу')],
         about='Платите за 6 месяцев абонемента и получаете ещё 6 в подарок. Итого 12 месяцев полного доступа к тренировкам и программам клуба. Цены распродажи действуют 10–12 ноября.',
         mem=3800, new=4400, card_price=('от', 3800), month=('Выходит от 317 ₽ за месяц', 'Выходит по 317 ₽ за месяц', 'Выходит по 367 ₽ за месяц')),
    dict(id='c2', aud='all', img='club2', pos='50% 25%', mpos='50% 22%', title='Клуб «Навсегда»',
         line='Абонемент, который не нужно продлевать', chips=[('clock', 'Бессрочно'), ('check', 'Полный доступ к клубу')],
         about='Полный доступ к клубу без ограничения срока: можно заниматься дома в удобном ритме и возвращаться к любимым тренировкам. Цены распродажи действуют 10–12 ноября.',
         mem=7990, new=9990, card_price=('', 9990)),
]


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


def photo(p, modal=False):
    img, pos = PHOTO.get(p['id'], (p['img'], p['pos']))
    if modal:
        pos = p.get('mpos') or MPOS.get(p['id'], pos)
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
    <h3 class="pc__t">{t(name(p))}</h3>
    <p class="pc__line">{t(line)}</p>
    <div class="pc__foot">{price_row(old, price)}<button class="pc__more" type="button" data-pk="pk-{p["id"]}" aria-haspopup="dialog">Подробнее</button></div>
  </div>
</article>'''


def pack_dialog(p):
    """Окно пака: лид, описание, мета, полный состав с сутью программ, все варианты покупки с условиями."""
    rows = ''.join(f'<li>{li_icon(n)}<span class="pc__item"><b>{t(n + (" — " + q if q else ""))}</b>'
                   + (f'<small>{t(sub)}</small>' if sub else '')
                   + (f'<em class="pc__flag">{t(NOINT[n])}</em>' if n in NOINT else '') + '</span></li>'
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
            opt_html = option(cap, price_row(old_o, price_o), buy_btn(title_o or name(p), price_o, w, sid, ghost=n > 0), title_o)
            # второй вариант (2 490 ₽ с клубом на месяц) — под строкой-переключателем, покупка и виджет на месте
            opts += opt_html if n == 0 else f'<details class="pk__alt"><summary>{t(ALT_SUMMARY)}</summary>{opt_html}</details>'
    else:
        opts += option(AUD_COND.get(p['aud']), price_row(p['old'], p['price']), buy_btn(name(p), p['price'], p['widget'], p['sid']))
        if p.get('extra'):
            # «Фитнес»: клуб на месяц за 1 600 ₽ — кнопка пока без действия
            et, es, ep = p['extra']
            opts += option(es, price_row(0, ep), buy_btn(et, ep, ghost=True), et)
    return f'''<dialog class="pk" id="pk-{p["id"]}" aria-labelledby="pk-{p["id"]}-t">
  <button class="pk__x" type="button" aria-label="Закрыть">{icon("x")}</button>
  <div class="pk__in">
    <div class="pk__media">{photo(p, modal=True)}<span class="pc__aud pc__aud--{p["aud"]}">{icon(ic)}{t(label)}</span></div>
    <div class="pk__body">
      <h3 class="pc__t" id="pk-{p["id"]}-t">{t(name(p))}</h3>{lead}{about}
      <p class="pc__meta">{meta}</p>
      <p class="pc__in">Что внутри:</p>
      <ul class="pc__list">{rows}</ul>
      <div class="pk__opts">{opts}</div>
    </div>
  </div>
</dialog>'''


def club_card(c):
    """Превью абонемента: как у наборов — фото, «Для всех», название, строка, цена «от», «Подробнее»."""
    label, ic = AUD[c['aud']]
    return f'''<article class="pc pc--club" data-aud="{c["aud"]}" id="{c["id"]}">
  <div class="pc__media">
    {photo(c)}
    <span class="pc__aud pc__aud--{c["aud"]}">{icon(ic)}{t(AUD_SHORT[c["aud"]])}</span>
  </div>
  <div class="pc__body">
    <h3 class="pc__t">{t(c["title"])}</h3>
    <p class="pc__line">{t(c["line"])}</p>
    <div class="pc__foot"><p class="pc__price"><b>{("<small>" + c["card_price"][0] + "</small>&nbsp;") if c["card_price"][0] else ""}{rub(c["card_price"][1])}</b></p>{('<p class="pc__month">' + t(c["month"][0]) + '</p>') if c.get("month") else ""}<button class="pc__more" type="button" data-pk="pk-{c["id"]}" aria-haspopup="dialog">Подробнее</button></div>
  </div>
</article>'''


def club_dialog(c):
    """Окно абонемента: описание, что есть в клубе, две цены (участникам клуба / новым участникам). Виджетов нет — кнопки без действия."""
    label, ic = AUD[c['aud']]
    meta = ''.join('<span>' + icon(i) + t(x) + '</span>' for i, x in c['chips'])
    rows = ''.join(f'<li>{li_icon("")}<span class="pc__item"><b>{t(x)}</b></span></li>' for x in CLUB_T['WHAT'])
    mo = c.get('month')
    m1 = f'<p class="pc__month">{t(mo[1])}</p>' if mo else ''
    m2 = f'<p class="pc__month">{t(mo[2])}</p>' if mo else ''
    opts = (option(CLUB_T['MEM'], price_row(0, c['mem']) + m1, buy_btn(c['title'], c['mem']))
            + option(CLUB_T['NEW'], price_row(0, c['new']) + m2, buy_btn(c['title'], c['new'], ghost=True)))
    return f'''<dialog class="pk" id="pk-{c["id"]}" aria-labelledby="pk-{c["id"]}-t">
  <button class="pk__x" type="button" aria-label="Закрыть">{icon("x")}</button>
  <div class="pk__in">
    <div class="pk__media">{photo(c, modal=True)}<span class="pc__aud pc__aud--{c["aud"]}">{icon(ic)}{t(label)}</span></div>
    <div class="pk__body">
      <h3 class="pc__t" id="pk-{c["id"]}-t">{t(c["title"])}</h3>
      <p class="pc__about">{t(c["about"])}</p>
      <p class="pc__meta">{meta}</p>
      <p class="pc__in">{t(CLUB_T["WHAT_H"])}</p>
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
<title>Распродажа 11.11 — программы и абонементы клуба «Шагай Дома»</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f6f0ff">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
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
    <img class="hero__cut" src="assets/hero-cut.webp" alt="">
    <span class="ring ring--front"></span>
    <p class="hero__card">Любимые программы клуба со&nbsp;скидкой</p>
  </div>
</div></section>

<section class="shop" id="packs"><div class="wrap">
  <h2 class="sr-only">Программы распродажи</h2>
  <div class="chips">{chips}</div>
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
{"".join(pack_dialog(p) for p in PACKS)}{"".join(club_dialog(c) for c in CLUBS)}
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
