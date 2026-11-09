#!/usr/bin/env python3
"""Распродажа 11.11 «Шагай Дома», v4 — одна карточка пака по референсу Димы (светлый фон, фиолетово-розовая гамма).

Собирает v4/index.html. Корень (v3) и v2/ не трогает.
Состав, названия и цены — из ТЗ Никиты 09.11.2026 (~/Downloads/shagai-v4-ref/TASK.md).
Новые строки (MEM_SHORT, STUB_BTN, STUB_NOTE) — через na-pero; остальные тексты утверждены в v2.
Оплата: виджеты GetCourse для паков 2, 4, 5, 6 открываются в модальном окне (app.js грузит их по клику).
Запуск: python3 build_v4.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'v4'
# Метка акции для аналитики (utm_campaign=l_ГГГГММ_имя). Выдаёт Никита; пока пусто — ничего не подставляется.
SALE_CAMPAIGN = ''

NB = ' '
LOGO = (ROOT / 'parts/logo.svg').read_text().replace('<svg ', '<svg class="logo__svg" ', 1)
FOOTER = (ROOT / 'parts/footer.html').read_text().replace(
    '<h2 class="footer__brand">Шагай Дома</h2>',
    '<a class="footer__brand" href="#top" aria-label="Шагай Дома">' + LOGO + '</a>')

AUD = {
    'members': ('Для держателей абонемента', 'lock'),
    'new': ('Для новых пользователей', 'user'),
    'all': ('Для держателей абонемента и новых пользователей', 'users'),
}

# Названия, аудитории, состав и варианты цены — по официальной странице паков Маши в GetCourse (Никита, 09.11.2026).
# items: (название, количество или '', пояснение или '')
# opts: варианты цены (подпись, пояснение, старая цена или 0, цена) — у паков 1 и 3; виджетов к ним пока нет
# note: строка про доступ в клуб в строке метаданных
OPT_MEMBERS = 'Для держателей абонемента, если осталось больше месяца'
OPT_NOSUB = 'Для тех, у кого абонемент заканчивается или его нет'
PACKS = [
    dict(id='p1', aud='members', img='p1', pos='50% 42%', sticker='3 программы в одном паке',
         title='Стройное тело', count='65 занятий и практик',
         items=[('Антиотёк', '23 занятия', ''), ('Стройный живот', '21 занятие', ''), ('Стройные ноги', '21 занятие', '')],
         opts=[(OPT_MEMBERS, '', 1990, 990), ('Абонемент на месяц + пакет В1', OPT_NOSUB, 0, 1500)]),
    dict(id='p2', aud='new', img='p2', pos='50% 22%',
         title='Фитнес', count='21 тренировка', term='1 месяц', note='Без полного доступа к клубу',
         items=[('Табата', '7 тренировок', ''), ('Зумба', '7 тренировок', ''), ('Интервальные', '7 тренировок', '')],
         old=3000, price=1500, widget='1680785', sid='e398c503c771b44edda3a589317a0cd11d810c57'),
    dict(id='p3', aud='members', img='p3', pos='50% 32%',
         title='Отдых и восстановление', count='2 программы',
         items=[('Лагерь «Осень 25»', '', 'Лёгкость, движение и хорошее настроение'), ('Санаторий № 1', '', 'Восстановление, здоровье и энергия')],
         opts=[(OPT_MEMBERS, '', 1990, 990), ('Абонемент на месяц + пакет В3', OPT_NOSUB, 0, 1500)]),
    dict(id='p4', aud='all', img='menu', pos='50% 50%',
         title='Все меню', count='19 недельных меню + подборки', term='1 месяц', note='Без доступа в клуб',
         items=[('19 недельных меню', '', 'завтраки, обеды, ужины, полдники'), ('Меню ПП-пирогов', '', ''), ('2 меню напитков', '', ''),
                ('Меню десертов', '', ''), ('Меню ПП-куличей', '', '')],
         old=4000, price=2000, widget='1680793', sid='4cc3a15ee284859f267e9b5b068cf31f5c5e535f'),
    dict(id='p5', aud='all', img='p5', pos='50% 38%',
         title='Красота, здоровье и лёгкость', count='4 программы', term='3 месяца',
         items=[('Фейс-йога от Валерии', '10 занятий', 'Упругая кожа и свежий вид'), ('Женское здоровье от Вики', '17 занятий', 'Забота о себе изнутри'),
                ('Осанка от Вики', '18 занятий', 'Прямая спина и лёгкость в теле'), ('Зарядки 5 минут от Димы', '', 'Больше энергии каждый день')],
         old=3990, price=1990, widget='1680796', sid='01cbca3dda7044eb1882b2b467f12b47d554f5a6'),
    dict(id='p6', aud='new', img='p6', pos='50% 30%',
         title='Все хиты', count='24 тренировки', term='3 месяца', note='Без доступа в клуб',
         items=[('Все хиты', '', 'Любимые тренировки'), ('80-е новые', '', 'Новые яркие программы'), ('80-е старые', '', 'Классика, которая всегда вдохновляет')],
         old=3990, price=1990, widget='1680798', sid='d89e2099d1223c0a436a9a2a6b46943046202e04'),
]

T = dict(
    HERO_LEAD='Впервые продаём наборы — для тех, кто хотел, но не успел или пришёл позже. Цены распродажи 10–12 ноября.',
    NOINT_T='Пак вы проходите сами. В каналах с заданиями открыты комментарии: там можно обсуждать задания с другими участниками. Кураторы обратную связь не дают, конкурсов нет.',
    MEM_SHORT='Меньше месяца до конца абонемента — предложим продлить по прежним ценам.',
    STUB_BTN='Купить пока нельзя',
    STUB_NOTE='Оплату для участников клуба ещё не подключили.',
)

ICON = {
    'lock': '<path d="M7 10V7a5 5 0 0 1 10 0v3M5 10h14v11H5z"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.6-5.5 6.5-5.5s5.5 2 6.5 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.8.8 3 2.6 3.6 5.2"/>',
    'check': '<path d="M4 12.5l5 5L20 6.5"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    'stack': '<path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5"/>',
    'gift': '<path d="M3 9h18v12H3zM12 9v12M3 13h18M8 9c-2 0-3-1.2-3-2.5S6.2 4 8 5.5 12 9 12 9s1.8-2 4-3.5S19 4.9 19 6.5 18 9 16 9"/>',
    'loop': '<path d="M6.5 15.5c-2 0-3.5-1.6-3.5-3.5s1.5-3.5 3.5-3.5c3.5 0 7.5 7 11 7 2 0 3.5-1.6 3.5-3.5S19.5 8.5 17.5 8.5c-3.5 0-7.5 7-11 7z"/>',
    'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    'bag': '<path d="M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2"/>',
    'x': '<path d="M6 6l12 12M18 6L6 18"/>',
    'ban': '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
}


def icon(name, cls='ic'):
    return '<svg class="' + cls + '" viewBox="0 0 24 24" aria-hidden="true">' + ICON[name] + '</svg>'


SHORT = re.compile(r'(^|[\s(«„])((?:[А-Яа-яЁё]{1,2})|для|без|под|при|про|что|как|или|это|его|все)\s', re.I)


def t(s):
    s = html.escape(s, quote=False)
    for _ in range(2):
        s = SHORT.sub(lambda m: m.group(1) + m.group(2) + NB, s)
    s = s.replace(' —', NB + '—').replace(' ₽', NB + '₽').replace(' + ', NB + '+ ')
    return re.sub(r'(\d) (\d{3})', r'\1' + NB + r'\2', s)


def rub(n):
    return f'{n:,}'.replace(',', NB) + NB + '₽'


def card(p):
    label, ic = AUD[p['aud']]
    rows = []
    for name, qty, sub in p['items']:
        li = '<li>' + icon('check') + '<span class="pc__name">' + t(name)
        if sub:
            li += '<small>' + t(sub) + '</small>'
        li += '</span>'
        if qty:
            li += '<b class="pc__qty">' + t(qty) + '</b>'
        rows.append(li + '</li>')
    sticker = '<span class="pc__sticker">' + t(p['sticker']) + '</span>' if p.get('sticker') else ''
    meta = '<span>' + icon('stack') + t(p['count']) + '</span>'
    if p.get('term'):
        meta += '<span>' + icon('clock') + t(p['term']) + '</span>'
    if p.get('note'):
        meta += '<span>' + icon('ban') + t(p['note']) + '</span>'
    stub_btn = '<button class="pc__buy pc__buy--off" type="button" disabled>' + t(T['STUB_BTN']) + '</button>'
    if p.get('opts'):
        # два варианта цены по странице Маши: подпись, цена, кнопка-заглушка (виджетов пока нет)
        foot = ''
        for label_o, sub_o, old_o, price_o in p['opts']:
            price_html = (f'<s>{rub(old_o)}</s>' if old_o else '') + f'<b>{rub(price_o)}</b>'
            if old_o:
                price_html += f'<i>−{round(100 - price_o * 100 / old_o)}%</i>'
            foot += (f'<div class="pc__opt"><p class="pc__optl">{t(label_o)}' + (f'<small>{t(sub_o)}</small>' if sub_o else '') + '</p>'
                     f'<p class="pc__price">{price_html}</p>{stub_btn}</div>')
    else:
        pct = round(100 - p['price'] * 100 / p['old'])
        if p.get('widget'):
            buy = (f'<button class="pc__buy" type="button" data-widget="{p["widget"]}" data-sid="{p["sid"]}" '
                   f'data-title="{html.escape(p["title"])}" data-price="{rub(p["price"])}">' + icon('bag') + 'Купить пак</button>')
        else:
            buy = stub_btn
        foot = f'<p class="pc__price"><s>{rub(p["old"])}</s><b>{rub(p["price"])}</b><i>−{pct}%</i></p>{buy}'
    return f'''<article class="pc" data-aud="{p["aud"]}" id="{p["id"]}">
  <div class="pc__media">
    <img class="pc__photo" src="assets/{p["img"]}.webp" alt="" loading="lazy" style="object-position:{p["pos"]}">
    <span class="pc__aud pc__aud--{p["aud"]}">{icon(ic)}{t(label)}</span>{sticker}
  </div>
  <div class="pc__body">
    <h3 class="pc__t">{t(p["title"])}</h3>
    <p class="pc__meta">{meta}</p>
    <ul class="pc__list">{"".join(rows)}</ul>
    <div class="pc__foot">
      {foot}
    </div>
  </div>
</article>'''


def page():
    def count(a):
        return sum(1 for p in PACKS if a == 'any' or p['aud'] == a)
    chips = ''.join(
        f'<button class="chip{" is-on" if a == "any" else ""}" type="button" data-aud="{a}">{t(label)}<i>{count(a)}</i></button>'
        for a, label in [('any', 'Все предложения'), ('members', 'Для держателей абонемента'), ('new', 'Для новых пользователей'), ('all', 'Для всех')])
    return f'''<!doctype html>
<html lang="ru" data-sale-campaign="{SALE_CAMPAIGN}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Распродажа 11.11 — паки программ «Шагай Дома»</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f7f4fc">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<style>.shop{{padding-bottom:24px}}</style>
</head>
<body id="top">
<main>
<section class="wrap shop" id="packs">
  <div class="chips">{chips}</div>
  <div class="grid">{"".join(card(p) for p in PACKS)}</div>
  <p class="noint">{icon("bolt")}<span><b>Пак без интерактива.</b> {t(T["NOINT_T"])}</span></p>
</section>
</main>
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
    print('собрано: v4/index.html')
