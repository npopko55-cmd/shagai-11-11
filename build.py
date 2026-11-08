#!/usr/bin/env python3
"""Сайт распродажи 11.11 «Шагай Дома», v3 по концепту v3-2 «Ярмарка паков» (выбран Никитой 08.11.2026).

Собирает index.html, p1…p6.html (паки), c1.html, c2.html (абонементы). Предыдущая версия лежит в v2/.
Тексты интерфейса — те же, что прошли na-pero для v2; описания паков и цены — с карточек Сони, состав — из ТЗ.
Графика ярмарки (навес, полка, флажки, лента, банты, бирка, стикер, конфетти) и вырезы фото сделаны в Higgsfield
через сессию Trandwatching, лежат в assets/fair/ и assets/cut/.
Запуск: python3 build.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
# Метка акции для аналитики (utm_campaign=l_ГГГГММ_имя). Выдаёт Никита; пока пусто — ничего не подставляется.
SALE_CAMPAIGN = ''

NB = ' '
LOGO = (ROOT / 'parts/logo.svg').read_text().replace('<svg ', '<svg class="logo__svg" ', 1)
FOOTER = (ROOT / 'parts/footer.html').read_text().replace(
    '<h2 class="footer__brand">Шагай Дома</h2>',
    '<a class="footer__brand" href="index.html" aria-label="Шагай Дома">' + LOGO + '</a>')

AUD = {
    'members': ('Только для участников клуба', 'lock'),
    'new': ('Для новых участников', 'user'),
    'all': ('Для всех', 'users'),
    'club': ('Клубный абонемент', 'star'),
}

PACKS = [
    dict(id='p1', aud='members', imgs=['p1'], pos='50% 35%',
         title='Три интенсива в одном паке',
         desc='«Стройный живот», «Антиотёчность» и «Стройные ноги». Шагательные тренировки, зарядки, самомассажи и материалы специалистов.',
         count='65 занятий и практик', term='До конца абонемента', price=990, old=1990,
         inside=[('Стройный живот', ['7 шагательных тренировок', '14 дополнительных: зарядки и пилатес', 'Меню-конструктор и рецепты из яблок и кабачков', 'Раздел заботы о теле', 'Чат программы в формате канала']),
                 ('Антиотёчность', ['7 шагательных тренировок', '4 занятия от специалиста по фейс-йоге', '7 зарядок и 3 занятия от отёков от Димы', 'Вебинар с диетологом «Худеем и избавляемся от отёков»', 'Памятка от диетолога и список анализов', '2 занятия по тейпированию лица']),
                 ('Стройные и здоровые ноги', ['7 шагательных тренировок', '7 самомассажей', '7 тренировок на зону ног', 'Вебинар с флебологом', 'Гайды «Мягкие пяточки» и «Борьба с целлюлитом»'])]),
    dict(id='p2', aud='new', imgs=['p2'], pos='50% 25%',
         title='Фитнес-пак',
         desc='Табата, зумба и интервальные тренировки. Три зажигательных направления для разнообразного домашнего кардио.',
         count='21 тренировка', term='1 месяц', price=1500, old=3000, up='fit',
         inside=[('Табата', ['7 тренировок']), ('Зумба', ['7 тренировок']), ('Интервальные тренировки', ['7 тренировок'])]),
    dict(id='p3', aud='members', imgs=['p3', 'p3b'], pos='50% 30%', rest=True,
         title='Отдых и восстановление',
         desc='Лагерь похудения «Осень 25» и «Санаторий №1». Две программы для движения, восстановления и хорошего самочувствия.',
         count='2 программы', term='До конца абонемента', price=990, old=1990,
         inside=[('Лагерь похудения «Осень 25»', ['Чат программы в формате канала']), ('Санаторий №1', ['Чат программы в формате канала'])]),
    dict(id='p4', aud='all', imgs=[], pos='50% 50%', mem_note='1m',
         title='Всё меню от «Шагай дома»',
         desc='Готовые меню на каждый день, ПП-пироги, напитки, десерты и праздничные рецепты.',
         count='19 недельных меню + подборки', term='1 месяц', price=2000, old=4000, up='menu',
         inside=[('Меню', ['19 недельных меню: на 7 дней завтраки, обеды, ужины и полдники', 'Меню ПП-пирогов', '2 меню напитков', 'Меню десертов', 'Меню ПП-куличей'])]),
    dict(id='p5', aud='all', imgs=['p5'], pos='50% 40%', mem_note='3m',
         title='Красота, здоровье и лёгкость',
         desc='Фейс-йога, женское здоровье и антисутулость с Викой. Забота о лице, теле и осанке в одном наборе.',
         count='45 занятий и практик', term='3 месяца', price=1990, old=3990, up='beauty',
         inside=[('Фейс-йога', ['7 тренировок по фейс-йоге', '2 занятия по тейпам лица', 'Лимфодренажная зарядка']),
                 ('Женское здоровье с Викой', ['17 занятий на мышцы пресса и тазового дна, рассчитано на 3 недели']),
                 ('Антисутулость с Викой', ['15 занятий и 3 вводных'])]),
    dict(id='p6', aud='new', imgs=['p6'], pos='50% 35%',
         title='Все хиты',
         desc='Любимые зарубежные и русские хиты, новые тренировки в стиле 80-х и проверенная классика.',
         count='24 тренировки', term='3 месяца', price=1990, old=3990, up='hits',
         inside=[('Тренировки под хиты', ['24 тренировки: 15 новых в стиле 80-х и 9 любимых', '57 зарубежных хитов', '48 русских хитов'])]),
]
CLUBS = [
    dict(id='c1', img='club', cut='club', tone='dark', bow='red',
         title='Клуб на 6 + 6 месяцев',
         desc='Полный доступ к тренировкам, программам и возможностям клуба на целый год по специальной цене 11.11.',
         line='12 месяцев полного доступа', term='12 месяцев', mem=3800, new=4400),
    dict(id='c2', img='club2', cut='club2', tone='red', bow='yellow',
         title='Клуб навсегда',
         desc='Полный доступ к клубу без ограничения срока. Занимайтесь дома в удобном ритме и возвращайтесь к любимым тренировкам.',
         line='Полный клубный доступ', term='Навсегда', mem=7990, new=9990),
]

T = dict(
    STUB_TOP='Черновик для согласования. Оплата пока не подключена, цены ждут подтверждения.',
    STUB_PAY='Здесь будет форма оплаты GetCourse. Пока её нет, оплатить нельзя.',
    STUB_PRICE='Старая цена и скидка ждут подтверждения',
    STUB_REST='Состав пака ещё уточняем',
    STUB_REST_LONG='Состав пака ещё уточняем. Вариант из ТЗ: «Омоложение» и «Лагерь „Осенний сезон“». Вариант с карточки: «Лагерь похудения „Осень 25“» и «Санаторий №1».',
    STUB_MENU_PHOTO='Фото для пака пока нет',
    STUB_UPSELL='Ссылка на абонемент пока не подключена',
    HEADER_BTN='Выбрать пак',
    HERO_LEAD='Впервые продаём наборы — для тех, кто хотел, но не успел или пришёл позже. Цены распродажи 10–12 ноября.',
    CLUBS_LEAD='Год в клубе или клуб навсегда, участникам клуба — дешевле.',
    NOINT_T='Пак вы проходите сами. В каналах с заданиями открыты комментарии: там можно обсуждать задания с другими участниками. Кураторы обратную связь не дают, конкурсов нет.',
    HOW_MEM_H='Если вы в клубе',
    HOW_MEM=['Паки «Три интенсива в одном паке» и «Отдых и восстановление» продаём только участникам клуба, если до конца абонемента остался месяц или больше.',
             'Доступ к этим двум пакам — до конца текущего абонемента.',
             'Паки «Всё меню от „Шагай дома“» и «Красота, здоровье и лёгкость» можно купить, даже если до конца абонемента меньше месяца.'],
    HOW_NEW_H='Если вы пока не в клубе',
    HOW_NEW=['Вам доступны четыре пака: «Фитнес-пак» и «Всё меню от „Шагай дома“» открываются на месяц, «Все хиты» и «Красота, здоровье и лёгкость» — на 3 месяца.',
             'Тренировки из паков «Фитнес-пак» и «Все хиты» есть в клубе.',
             'Можно сразу вступить в клуб: месяц стоит 1 600 ₽, 3 месяца — 3 200 ₽.'],
    MEM_COND=['Купить пак можно, если до конца абонемента остался месяц или больше.',
              'Пак открыт, пока действует текущий абонемент.',
              'Если до конца меньше месяца, после проверки почты предложим продлить абонемент по прежним ценам из личного кабинета.'],
    ALL_MEM_H='Если вы в клубе',
    ALL_MEM={'1m': 'Пак можно купить, даже если до конца абонемента меньше месяца.',
             '3m': 'Пак можно купить, даже если до конца абонемента меньше 3 месяцев.'},
    CLUB_PAGE_LEAD='Абонемент открывает весь клуб, цена 11.11 действует 10–12 ноября.',
    CLUB_PRICE_MEM='Участникам клуба',
    CLUB_PRICE_NEW='Новым участникам',
    CLUB_WHAT_H='Что есть в клубе',
    CLUB_WHAT=['25 фитнес-программ и курсов, больше 400 тренировок', 'План тренировок на каждый день недели', 'Тренировки от 5 до 40 минут',
               'Шагай.FM — фитнес-эфир нон-стоп под треки DJ', 'Шаговая аэробика под музыку: не нужно быть спортивной или уметь танцевать'],
    CLUB_WHO_NOTE='Цена для участников клуба — после проверки почты. Как устроить эту проверку на сайте, ещё уточняем.',
)
UPSELL = {
    'fit': ('Эти тренировки есть <em>у всех участников клуба</em>',
            'Пак на месяц стоит 1 500 ₽, месяц в клубе — 1 600 ₽. Там 25 программ, больше 400 шагательных тренировок, 60 рецептов и чат с куратором.'),
    'hits': ('Эти тренировки есть <em>у всех участников клуба</em>',
             'Пак на три месяца стоит 1 990 ₽, три месяца в клубе — 3 200 ₽. Там 25 программ, больше 400 шагательных тренировок, 60 рецептов и чат с куратором.'),
    'menu': ('Добавьте к меню <em>движение</em>',
             'Для стройности к питанию стоит добавить движение. В клубе 25 программ и больше 400 шагательных тренировок. Месяц в клубе — 1 600 ₽.'),
    'beauty': ('В клубе есть <em>план занятий на каждый день</em>',
               'Три месяца в клубе стоят 3 200 ₽. Там больше 400 шагательных тренировок от 5 до 40 минут, 30 тренировок для спины, 60 рецептов полезной еды и вебинары о здоровье.'),
}

ICON = {
    'lock': '<path d="M7 10V7a5 5 0 0 1 10 0v3M5 10h14v11H5z"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.6-5.5 6.5-5.5s5.5 2 6.5 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.8.8 3 2.6 3.6 5.2"/>',
    'star': '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4l-5.5 2.9 1-6.2L3 9.7l6.2-.9z"/>',
    'check': '<path d="M4 12.5l5 5L20 6.5"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    'gift': '<path d="M3 9h18v12H3zM12 9v12M3 13h18M8 9c-2 0-3-1.2-3-2.5S6.2 4 8 5.5 12 9 12 9s1.8-2 4-3.5S19 4.9 19 6.5 18 9 16 9"/>',
    'loop': '<path d="M6.5 15.5c-2 0-3.5-1.6-3.5-3.5s1.5-3.5 3.5-3.5c3.5 0 7.5 7 11 7 2 0 3.5-1.6 3.5-3.5S19.5 8.5 17.5 8.5c-3.5 0-7.5 7-11 7z"/>',
    'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    'alert': '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5M12 16.5v.5"/>',
    'chev': '<path d="M6 9l6 6 6-6"/>',
}


def icon(name, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


SHORT = re.compile(r'(^|[\s(«„])((?:[А-Яа-яЁё]{1,2})|для|без|под|при|про|что|как|или|это|его|все)\s', re.I)


def t(s):
    """Экранирует текст и ставит неразрывные пробелы после коротких слов и перед тире."""
    s = html.escape(s, quote=False)
    for _ in range(2):
        s = SHORT.sub(lambda m: m.group(1) + m.group(2) + NB, s)
    s = s.replace(' —', NB + '—').replace(' ₽', NB + '₽')
    return re.sub(r'(\d) (\d{3})', r'\1' + NB + r'\2', s)


def rub(n):
    return f'{n:,}'.replace(',', NB) + NB + '₽'


def img(path, cls, alt='', lazy=True, extra=''):
    lz = ' loading="lazy"' if lazy else ''
    return f'<img class="{cls}" src="assets/{path}" alt="{html.escape(alt)}"{lz}{extra}>'


def tag(aud):
    label, ic = AUD[aud]
    return f'<span class="tag">{icon(ic)}{t(label)}</span>'


def stub(text, cls=''):
    return f'<p class="stub {cls}">{icon("alert")}<span>{t(text)}</span></p>'


def photo(p, cls, eager=False):
    if not p['imgs']:
        return f'<div class="{cls} nophoto"><span>{t(T["STUB_MENU_PHOTO"])}</span></div>'
    return img(f'{p["imgs"][0]}.webp', cls, lazy=not eager, extra=f' style="object-position:{p["pos"]}"')


def ptag(p, big=False):
    """Цена на жёлтой бирке-ценнике (бирка — из Higgsfield, цифры — HTML)."""
    pct = round(100 - p['price'] * 100 / p['old'])
    return (f'<div class="ptag{" ptag--big" if big else ""}">{img("fair/tag.webp", "ptag__bg")}'
            f'<p class="ptag__in"><s>{rub(p["old"])}</s><b>{rub(p["price"])}</b><i>−{pct}%</i></p></div>')


def ticks(items, cls='ticks'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{icon("check")}<span>{t(x)}</span></li>' for x in items) + '</ul>'


def gbox(p, i, small=False):
    """Пак — подарочная коробка с бантом (бант из Higgsfield)."""
    href = f'{p["id"]}.html'
    bow = 'red' if i % 2 == 0 else 'yellow'
    rest = f'<p class="gbox__rest">{icon("alert")}{t(T["STUB_REST"])}</p>' if p.get('rest') and not small else ''
    return (f'<article class="gbox{" gbox--s" if small else ""}" data-aud="{p["aud"]}">{img(f"fair/bow-{bow}.webp", "gbox__bow")}'
            f'<div class="gbox__in"><a class="gbox__img" href="{href}">{photo(p, "gbox__photo")}{tag(p["aud"])}</a>'
            f'<h3 class="gbox__t"><a href="{href}">{t(p["title"])}</a></h3>{rest}'
            f'<div class="gbox__foot">{ptag(p)}<a class="btn btn--red gbox__btn" href="{href}">Что внутри</a></div></div></article>')


def cbox(c):
    """Абонемент — большая коробка с бантом и вырезанным фото."""
    bow, cut = c['bow'], c['cut']
    return (f'<article class="cbox cbox--{c["tone"]}">{img(f"fair/bow-{bow}.webp", "cbox__bow")}'
            f'<div class="cbox__in"><div class="cbox__text">{tag("club")}'
            f'<h3 class="cbox__t"><a href="{c["id"]}.html">{t(c["title"])}</a></h3><p class="cbox__line">{t(c["line"])}</p>'
            f'<p class="cbox__price">от{NB}{rub(c["mem"])}</p>'
            f'<p class="cbox__two">{rub(c["mem"])} своим · {rub(c["new"])} новым</p>'
            f'<a class="btn btn--yellow" href="{c["id"]}.html">Купить абонемент</a></div>'
            f'{img(f"cut/{cut}.webp", "cbox__cut cutout")}</div></article>')


def head(title):
    return f'''<!doctype html>
<html lang="ru" data-sale-campaign="{SALE_CAMPAIGN}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="draft">{icon("alert")}<span>{t(T["STUB_TOP"])}</span></div>
<header class="top"><div class="wrap top__in">
  <a class="logo" href="index.html" aria-label="Шагай Дома — на витрину распродажи">{LOGO}</a>
  <nav class="top__nav"><a href="index.html#packs">Паки программ</a><a href="index.html#clubs">Доступ в клуб</a><a href="index.html#how">Как это работает</a></nav>
  <a class="btn btn--red top__btn" href="index.html#packs">{t(T["HEADER_BTN"])}</a>
</div></header>
'''


def foot():
    return f'''<div class="wrap">{FOOTER}</div>
<script src="app.js"></script>
</body>
</html>
'''


def noint():
    return (f'<section class="noint"><p class="noint__h">{icon("bolt")}Пак без интерактива</p>'
            f'<p class="noint__t">{t(T["NOINT_T"])}</p></section>')


def stall(boxes):
    """Прилавок: навес и полки (из Higgsfield), коробки — HTML. Полки под рядами расставляет app.js."""
    return (f'<div class="stall">{img("fair/awning.webp", "stall__awning", lazy=False)}'
            f'<div class="stall__body"><div class="shelves" aria-hidden="true" data-plank="assets/fair/plank.webp"></div>'
            f'<div class="grid" id="grid">{boxes}</div></div></div>')


def index():
    count = lambda a: sum(1 for p in PACKS if a == 'any' or p['aud'] == a)
    chips = ''.join(
        f'<button class="chip{" is-on" if a == "any" else ""}" type="button" data-aud="{a}">{t(label)} <i>{count(a)}</i></button>'
        for a, label in [('any', 'Все предложения'), ('members', 'Только для участников клуба'), ('new', 'Для новых участников'), ('all', 'Для всех')])
    how = ''.join(f'<div class="how__col"><h3 class="how__h">{t(h)}</h3>{ticks(items)}</div>'
                  for h, items in [(T['HOW_MEM_H'], T['HOW_MEM']), (T['HOW_NEW_H'], T['HOW_NEW'])])
    return head('Распродажа 11.11 — паки программ «Шагай Дома»') + f'''
<main>
<section class="fhero"><div class="wrap">
  <div class="fbanner">
    {img("fair/bunting.webp", "fbanner__flags fbanner__flags--l", lazy=False)}
    <p class="fbanner__ribbon">{img("fair/ribbon.webp", "fbanner__bg", lazy=False)}<span>Акция 11.11 · 10–12{NB}ноября</span></p>
    {img("fair/bunting.webp", "fbanner__flags fbanner__flags--r", lazy=False)}
  </div>
  <div class="fhero__grid">
    <h1 class="fhero__h">Большая распродажа <em>любимых программ</em></h1>
    <p class="fhero__lead">{t(T["HERO_LEAD"])}</p>
    <div class="fhero__art">
      {img("fair/confetti-1.webp", "conf conf--1", lazy=False)}{img("fair/confetti-2.webp", "conf conf--2", lazy=False)}
      {img("cut/hero.webp", "cut cut--a cutout", "Участница клуба в футболке «Шагай Дома»", lazy=False)}
      {img("cut/p3b.webp", "cut cut--b cutout", "Участница клуба в футболке «Шагай Дома»", lazy=False)}
      <p class="stk stk--fav">{img("fair/sticker.webp", "stk__bg", lazy=False)}<span>Любимые программы в{NB}выгодных наборах</span></p>
      <p class="stk stk--sale">{img("fair/sticker.webp", "stk__bg", lazy=False)}<span>−50%</span></p>
    </div>
    <ul class="feats"><li>{icon("gift")}Специальные цены</li><li>{icon("loop")}Выбирай свой пакет</li><li>{icon("bolt")}Действуй 10–12 ноября</li></ul>
  </div>
</div></section>

<section class="shop" id="packs"><div class="wrap">
  <div class="chips" role="tablist">{chips}</div>
  {stub(T["STUB_PRICE"], "stub--wide")}
  {stall(''.join(gbox(p, i) for i, p in enumerate(PACKS)))}
  {noint()}
</div></section>

<section class="clubs" id="clubs"><div class="wrap">
  <h2 class="h2 h2--c">Клубные <em>абонементы</em></h2>
  <p class="lead--c">{t(T["CLUBS_LEAD"])}</p>
  <div class="clubs__row">{''.join(cbox(c) for c in CLUBS)}</div>
</div></section>

<section class="how" id="how"><div class="wrap">
  <h2 class="h2 h2--c">Как это работает</h2>
  <div class="how__row">{how}</div>
</div></section>
</main>
''' + foot()


def more(cur):
    others = [(i, p) for i, p in enumerate(PACKS) if p['id'] != cur][:4]
    return (f'<section class="more"><h2 class="h2">Другие <em>паки распродажи</em></h2>'
            f'<div class="more__row">{"".join(gbox(p, i, small=True) for i, p in others)}</div></section>')


def gallery(p):
    big = photo(p, 'pp__photo', eager=True)
    if len(p['imgs']) < 2:
        return f'<div class="pp__media">{big}</div>'
    th = ''.join(f'<button type="button" class="pp__th{" is-on" if i == 0 else ""}" data-src="assets/{n}.webp" aria-label="Фото {i + 1}">'
                 f'<img src="assets/{n}.webp" alt="" loading="lazy"></button>' for i, n in enumerate(p['imgs']))
    return f'<div class="pp__media">{big}<div class="pp__thumbs">{th}</div></div>'


def upsell(key):
    h, txt = UPSELL[key]
    return (f'<section class="cbox cbox--red up">{img("fair/bow-yellow.webp", "cbox__bow")}<div class="cbox__in">'
            f'<div class="cbox__text"><h2 class="up__h">{h}</h2><p class="up__t">{t(txt)}</p>'
            f'<a class="btn btn--yellow" href="index.html#clubs">Купить абонемент</a>{stub(T["STUB_UPSELL"], "stub--onred")}</div>'
            f'{img("cut/club.webp", "cbox__cut cutout")}</div></section>')


def pack_page(p):
    inside = ''.join(
        f'<details class="acc"{" open" if i == 0 else ""}><summary>{t(name)}{icon("chev", "ic acc__chev")}</summary>{ticks(items)}</details>'
        for i, (name, items) in enumerate(p['inside']))
    if p.get('rest'):
        inside = stub(T['STUB_REST_LONG']) + inside
    blocks = ''
    if p['aud'] == 'members':
        blocks += f'<section class="box"><h2 class="h2 h2--s">Для участников <em>клуба</em></h2>{ticks(T["MEM_COND"], "ticks ticks--big")}</section>'
    else:
        blocks += (f'<section class="box"><h2 class="h2 h2--s">Сколько <em>действует</em></h2>'
                   f'<div class="term">{icon("clock")}<b>{t(p["term"])}</b><span>{t("Доступ к тренировкам пака — " + p["term"] + ".")}</span></div></section>')
        if p.get('mem_note'):
            blocks += (f'<section class="box"><h2 class="h2 h2--s">{t(T["ALL_MEM_H"])}</h2>'
                       f'{ticks([T["ALL_MEM"][p["mem_note"]]], "ticks ticks--big")}</section>')
    up = upsell(p['up']) if p.get('up') else ''
    return head(f'{p["title"]} — распродажа 11.11 «Шагай Дома»') + f'''
<main class="wrap page">
  <nav class="crumbs"><a href="index.html">Распродажа 11.11</a><span>›</span><span>{t(p["title"])}</span></nav>
  <div class="pp">
    {gallery(p)}
    <aside class="buy gbox">{img("fair/bow-red.webp", "gbox__bow", lazy=False)}<div class="gbox__in">
      {tag(p["aud"])}
      <h1 class="buy__t">{t(p["title"])}</h1>
      <p class="buy__d">{t(p["desc"])}</p>
      <ul class="buy__meta"><li>{icon("check")}{t(p["count"])}</li><li>{icon("clock")}{t(p["term"])}</li></ul>
      {ptag(p, big=True)}
      {stub(T["STUB_PRICE"], "stub--s")}
      <a class="btn btn--red btn--big" href="#pay">Купить пак</a>
      <div class="pay" id="pay" data-widget-for="{p["id"]}">{icon("alert")}<span>{t(T["STUB_PAY"])}</span></div>
    </div></aside>
  </div>
  <section class="box box--inside"><h2 class="h2">Что <em>в паке</em></h2>{inside}</section>
  {blocks}
  {noint()}
  {up}
  {more(p["id"])}
</main>
''' + foot()


def club_page(c):
    other = [x for x in CLUBS if x['id'] != c['id']][0]
    bow, pic = c['bow'], c['img']
    return head(f'{c["title"]} — распродажа 11.11 «Шагай Дома»') + f'''
<main class="wrap page">
  <nav class="crumbs"><a href="index.html">Распродажа 11.11</a><span>›</span><span>{t(c["title"])}</span></nav>
  <div class="pp">
    <div class="pp__media">{img(f"{pic}.webp", "pp__photo", lazy=False)}</div>
    <aside class="buy gbox">{img(f"fair/bow-{bow}.webp", "gbox__bow", lazy=False)}<div class="gbox__in">
      {tag("club")}
      <h1 class="buy__t">{t(c["title"])}</h1>
      <p class="buy__d">{t(c["desc"])}</p>
      <p class="buy__lead">{t(T["CLUB_PAGE_LEAD"])}</p>
      <ul class="buy__meta"><li>{icon("check")}{t(c["line"])}</li><li>{icon("clock")}{t(c["term"])}</li></ul>
      <div class="two">
        <div class="two__o"><span>{t(T["CLUB_PRICE_MEM"])}</span><b>{rub(c["mem"])}</b></div>
        <div class="two__o"><span>{t(T["CLUB_PRICE_NEW"])}</span><b>{rub(c["new"])}</b></div>
      </div>
      {stub(T["CLUB_WHO_NOTE"], "stub--s")}
      <a class="btn btn--red btn--big" href="#pay">Купить абонемент</a>
      <div class="pay" id="pay" data-widget-for="{c["id"]}">{icon("alert")}<span>{t(T["STUB_PAY"])}</span></div>
    </div></aside>
  </div>
  <section class="box"><h2 class="h2">{t(T["CLUB_WHAT_H"])}</h2>{ticks(T["CLUB_WHAT"], "ticks ticks--big ticks--cols")}</section>
  <section class="more"><h2 class="h2">Клубные <em>абонементы</em></h2><div class="clubs__row clubs__row--one">{cbox(other)}</div></section>
  {more(c["id"])}
</main>
''' + foot()


def main():
    pages = {'index.html': index()}
    for p in PACKS:
        pages[f'{p["id"]}.html'] = pack_page(p)
    for c in CLUBS:
        pages[f'{c["id"]}.html'] = club_page(c)
    for name, src in pages.items():
        (ROOT / name).write_text(src)
    print('собрано:', ', '.join(pages))


if __name__ == '__main__':
    main()
