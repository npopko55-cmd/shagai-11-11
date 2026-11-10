#!/usr/bin/env python3
"""Блоки T123 для переноса страницы распродажи 11.11 (/v5/) в Тильду.

Источник — v5/index.html, v5/styles.css, v5/app.js (собраны build_v5.py). Запуск из корня репозитория:
    python3 tilda/build_tilda.py                         # картинки с GitHub Pages /v5/assets
    python3 tilda/build_tilda.py --img-base https://static.tildacdn.com/...   # после загрузки картинок в Тильду

Приёмы те же, что в antiotek/build-tilda-standalone.py:
- разметка каждого блока обёрнута в .shd1111, все правила CSS ограничены этим классом (не задевают шапку и футер Тильды);
- CSS отдаётся строкой base64 (Тильда переформатирует текст блока и ломает стили);
- кириллица в разметке — HTML-сущности &#NNNN;, в скрипте — \\uXXXX (иначе Тильда превращает её в «РЁР°…»);
- скрипт — последним блоком, запускается после загрузки страницы;
- шапка: в T123 position:sticky не работает (родитель — блок высотой с шапку), поэтому fixed + распорка.
Лимит Тильды ~30 000 знаков на блок; режем по секциям и окнам, внутри элементов не режем.
"""
import argparse
import base64
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'v5'
OUT = Path(__file__).resolve().parent
HAND = OUT / 'ДЛЯ ТИЛЬДЫ'
LIMIT = 30000
SCOPE = '.shd1111'
IMG_BASE_DEFAULT = 'https://npopko55-cmd.github.io/shagai-11-11/v5/assets'

ap = argparse.ArgumentParser()
ap.add_argument('--img-base', default=IMG_BASE_DEFAULT, help='адрес папки с картинками (без / на конце)')
args = ap.parse_args()
IMG_BASE = args.img_base.rstrip('/')

html = (SRC / 'index.html').read_text(encoding='utf-8')
css = (SRC / 'styles.css').read_text(encoding='utf-8')
js = (SRC / 'app.js').read_text(encoding='utf-8')
FONT_LINK = re.search(r'<link[^>]+fonts\.googleapis\.com/css2[^>]*>', html).group(0)

# ---------- CSS: изоляция в .shd1111, правки под Тильду, base64 ----------
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
# шапка: fixed вместо sticky (+ распорка в разметке), см. докстринг
css += ('\n.top{position:fixed;left:0;right:0;top:0;z-index:990}'
        '\n.top-spacer{height:64px}'
        '\n@media (min-width:1060px){.top-spacer{height:84px}}'
        '\n.hero,.shop,.clubs,.how,.faq{scroll-margin-top:90px}'
        '\n.shop--cont{padding-top:0}.shop--cont .grid{margin-top:18px}'
        '\n@media (min-width:640px){.shop--cont .grid{margin-top:20px}}@media (min-width:1060px){.shop--cont .grid{margin-top:24px}}\n')


def scope_selector(sel):
    out = []
    for part in sel.split(','):
        s = part.strip()
        if not s:
            continue
        if s.startswith(':root') or s.startswith('@') or s.startswith(SCOPE):
            out.append(s)
            continue
        if s.startswith('html.'):          # html.is-locked — класс вешается на <html>, оставляем глобальным
            out.append(s)
            continue
        head = re.split(r'[\s:\[.#>+~]', s, maxsplit=1)[0]
        if head in ('html', 'body'):
            rest = s[len(head):].strip()
            out.append(f'{SCOPE} {rest}'.strip() if rest else SCOPE)
        else:
            out.append(f'{SCOPE} {s}')
    return ', '.join(out)


def scope_css(text):
    res, i, n = [], 0, len(text)
    while i < n:
        br = text.find('{', i)
        if br < 0:
            res.append(text[i:])
            break
        sel = text[i:br]
        st = sel.strip()
        if st.startswith('@'):
            depth, j = 1, br + 1
            while j < n and depth:
                depth += {'{': 1, '}': -1}.get(text[j], 0)
                j += 1
            inner = text[br + 1:j - 1]
            res.append(sel + '{' + (inner if 'keyframes' in st else scope_css(inner)) + '}')
            i = j
            continue
        end = text.find('}', br)
        res.append(scope_selector(sel) + '{' + text[br + 1:end] + '}')
        i = end + 1
    return ''.join(res)


def css_capsule(part):
    b64 = base64.b64encode(part.encode('utf-8')).decode('ascii')
    return ('<script>(function(){var d="' + b64 + '";var b=atob(d),a=new Uint8Array(b.length),i=0;'
            'for(;i<b.length;i++){a[i]=b.charCodeAt(i);}'
            "var t=(typeof TextDecoder!=='undefined')?new TextDecoder('utf-8').decode(a):decodeURIComponent(escape(b));"
            "var s=document.createElement('style');s.appendChild(document.createTextNode(t));"
            '(document.head||document.documentElement).appendChild(s);})();</script>\n')


def split_rules(text, limit):
    """Режем CSS по границам верхнеуровневых правил (и @media целиком)."""
    parts, cur, depth, start = [], '', 0, 0
    for i, ch in enumerate(text):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                rule = text[start:i + 1]
                if len(cur) + len(rule) > limit and cur:
                    parts.append(cur)
                    cur = ''
                cur += rule
                start = i + 1
    cur += text[start:]
    if cur.strip():
        parts.append(cur)
    return parts


css_scoped = scope_css(css)
css_scoped = re.sub(r'\n\s*\n', '\n', css_scoped)
CSS_CHUNK = (LIMIT - 3000) * 3 // 4

# ---------- JS: без комментариев, кириллица → \uXXXX, запуск после загрузки ----------


def js_for_tilda(text):
    out, i, n, quote = [], 0, len(text), None
    while i < n:
        c = text[i]
        if quote:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(text[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in '\'"`':
            quote = c; out.append(c); i += 1; continue
        if c == '/' and i + 1 < n and text[i + 1] == '/':
            j = text.find('\n', i); i = n if j == -1 else j; continue
        if c == '/' and i + 1 < n and text[i + 1] == '*':
            j = text.find('*/', i + 2); i = n if j == -1 else j + 2; continue
        out.append(c); i += 1
    code = re.sub(r'[ \t]+\n', '\n', ''.join(out))
    code = re.sub(r'\n{3,}', '\n\n', code)
    return ''.join(ch if ord(ch) < 128 else '\\u%04x' % ord(ch) for ch in code)


js_wrapped = ('(function(){function shd1111(){\n' + js_for_tilda(js) + '\n}\n'
              "if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',shd1111);}else{shd1111();}})();")

# ---------- Разметка ----------
body = re.search(r'<body[^>]*>(.*?)</body>', html, re.S).group(1)
body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
body = re.sub(r'<script[^>]*src="app\.js"[^>]*></script>\s*', '', body)
body = body.replace('<main>', '').replace('</main>', '')
used = sorted(set(re.findall(r'assets/([\w.-]+)', body)))
body = re.sub(r'(src|href)="assets/([^"]+)"', lambda m: f'{m.group(1)}="{IMG_BASE}/{m.group(2)}"', body)
body = body.replace('</div></header>', '</div></header><div class="top-spacer" aria-hidden="true"></div>', 1)


def to_entities(text):
    return ''.join(c if ord(c) < 128 else f'&#{ord(c)};' for c in text)


def wrap(chunk):
    return f'<div class="shd1111">\n{to_entities(chunk.strip())}\n</div>\n'


def pos(patt):
    m = re.search(patt, body)
    if not m:
        raise SystemExit('не нашёл: ' + patt)
    return m.start()


p_shop = pos(r'<section class="shop"')
p_clubs = pos(r'<section class="clubs"')
p_how = pos(r'<section class="how"')
p_dlg = pos(r'<dialog')
blocks = [('шапка и первый экран', body[:p_shop])]
# программы: карточки целиком, блок не больше лимита; продолжение сетки — отдельная секция .shop--cont
shop = body[p_shop:p_clubs]
cards = re.findall(r'<article class="pc".*?</article>', shop, re.S)
head_html = shop[:shop.index('<article')]
tail_html = '</div>\n</div></section>\n'
cont_head = '<section class="shop shop--cont"><div class="wrap">\n  <div class="grid grid--packs">'
# по 3 карточки в блоке: ряд на десктопе (3 колонки) не рвётся между блоками
groups = [cards[i:i + 3] for i in range(0, len(cards), 3)]
for gi, g in enumerate(groups, 1):
    h = head_html if gi == 1 else cont_head
    if len(wrap(h + ''.join(g) + tail_html)) > LIMIT - 500:
        raise SystemExit(f'программы, часть {gi}: больше лимита Тильды — нужен другой разрез')
for gi, g in enumerate(groups, 1):
    h = head_html if gi == 1 else cont_head
    blocks.append((f'программы, часть {gi}' if len(groups) > 1 else 'программы', h + ''.join(g) + tail_html))
blocks.append(('абонементы', body[p_clubs:p_how]))
blocks.append(('как купить, вопросы, подвал, окно оплаты', body[p_how:]))

files = []
for i, part in enumerate(split_rules(css_scoped, CSS_CHUNK), 1):
    files.append((f'стили, часть {i}', (FONT_LINK + '\n' if i == 1 else '') + css_capsule(part)))
for title, chunk in blocks:
    files.append((title, wrap(chunk)))
files.append(('скрипт, вставлять последним', '<script>\n' + js_wrapped + '\n</script>\n'))

# ---------- Запись ----------
HAND.mkdir(exist_ok=True)
for old in HAND.glob('*.html'):
    old.unlink()
report = []
for i, (title, content) in enumerate(files, 1):
    name = f'{i:02d} — {title}.html'
    (HAND / name).write_text(content, encoding='utf-8')
    nonascii = sum(1 for c in content if ord(c) > 127)
    flag = 'OK' if len(content) < LIMIT and nonascii == 0 else '!! ПРОБЛЕМА'
    report.append(f'{name}: {len(content):,} знаков, не-ASCII {nonascii} — {flag}'.replace(',', ' '))

# картинки — копия для загрузки в Тильду
assets_out = OUT / 'assets'
assets_out.mkdir(exist_ok=True)
for a in used:
    shutil.copy2(SRC / 'assets' / a, assets_out / a)

# превью «как в Тильде»: каждый блок в обёртке t-rec/t123, поля body обнулены
preview = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           '<title>Превью блоков Тильды — распродажа 11.11</title><style>body{margin:0}</style></head><body>\n'
           + '\n'.join(f'<div class="t-rec"><div class="t123"><div class="t-container_100"><div class="t-width t-width_100">{c}</div></div></div></div>'
                       for _t, c in files)
           + '\n</body></html>')
(OUT / '_preview.html').write_text(preview, encoding='utf-8')

print('\n'.join(report))
print('картинки:', ', '.join(used))
print('адрес картинок:', IMG_BASE)
