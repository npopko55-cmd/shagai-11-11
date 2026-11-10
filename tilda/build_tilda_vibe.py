#!/usr/bin/env python3
"""Vibe-блоки (tplid 1370) для переноса /v5/ в Тильду через MCP — как на walk-walk.ru/step.

Источник — v5/index.html, v5/styles.css, v5/app.js. Картинки — только адреса Тильды из tilda/tilda-assets.json
(загружены через MCP upload_image). Сборка падает, если в блоках осталась ссылка на github или assets/.
Каждая секция — свой блок, разметка в обёртке .shd1111, все правила CSS ограничены этим классом.
CSS целиком лежит в первом блоке (шапка), скрипт — в последнем (подвал + окно оплаты).
Шапка проекта и подвал проекта на этой странице скрыты по их id (как на /step).
Запуск из корня репозитория: python3 tilda/build_tilda_vibe.py → tilda/tilda-vibe/NN-*.html
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'v5'
OUT = Path(__file__).resolve().parent / 'tilda-vibe'
SCOPE = '.shd1111'
ASSETS = json.loads((Path(__file__).resolve().parent / 'tilda-assets.json').read_text())
# шапка и подвал проекта «Шагай дома new» — те же id, что скрыты на /step
HIDE_PROJECT_PARTS = '<style>#rec953993826,#rec1696909601,#rec4977556901,#rec660132164,#rec660132671{display:none!important}</style>'

html = (SRC / 'index.html').read_text(encoding='utf-8')
css = (SRC / 'styles.css').read_text(encoding='utf-8')
js = (SRC / 'app.js').read_text(encoding='utf-8')
FONT_LINK = re.search(r'<link[^>]+fonts\.googleapis\.com/css2[^>]*>', html).group(0)

css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css += ('\n.top{position:fixed;left:0;right:0;top:0;z-index:990}'
        '\n.top-spacer{height:64px}'
        '\n@media (min-width:1060px){.top-spacer{height:84px}}'
        '\n.hero,.shop,.clubs,.how,.faq{scroll-margin-top:90px}\n')


def scope_selector(sel):
    out = []
    for part in sel.split(','):
        s = part.strip()
        if not s:
            continue
        if s.startswith(':root'):
            out.append(SCOPE)
            continue
        if s.startswith('@') or s.startswith(SCOPE) or s.startswith('html.'):
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


def strip_js_comments(text):
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
    return re.sub(r'\n{3,}', '\n\n', re.sub(r'[ \t]+\n', '\n', ''.join(out)))


# правила только для классов, которые есть в разметке (окна «Подробнее», фильтры, легенда давно убраны) + классы из JS
KNOWN = set(c for cl in re.findall(r'class="([^"]+)"', html) for c in cl.split()) | {'is-locked', 'paydlg__slot', 'top-spacer', 'shd1111'}


def prune(text):
    res, i, n = [], 0, len(text)
    while i < n:
        br = text.find('{', i)
        if br < 0:
            break
        sel = text[i:br].strip()
        if sel.startswith('@'):
            depth, j = 1, br + 1
            while j < n and depth:
                depth += {'{': 1, '}': -1}.get(text[j], 0)
                j += 1
            inner = text[br + 1:j - 1]
            if 'keyframes' in sel:
                res.append(sel + '{' + inner + '}')
            else:
                kept = prune(inner)
                if kept.strip():
                    res.append(sel + '{' + kept + '}')
            i = j
            continue
        end = text.find('}', br)
        alive = [x for x in sel.split(',') if all(c in KNOWN for c in re.findall(r'\.([\w-]+)', x))]
        if alive:
            res.append(','.join(x.strip() for x in alive) + '{' + text[br + 1:end].strip() + '}')
        i = end + 1
    return ''.join(res)


def minify(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*([{};,>])\s*', r'\1', text)
    text = re.sub(r':\s+', ':', text)
    text = text.replace(';}', '}')
    return re.sub(r'\}(?=[^}])', '}\n', text)  # одно правило на строку


css_scoped = minify(prune(scope_css(css)))

# скрипт: запуск после загрузки страницы; в редакторе Тильды не мешает (только клики и метки)
js_code = ('(function(){function shd1111(){\n' + strip_js_comments(js) + '\n}\n'
           "if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',shd1111);}else{shd1111();}})();")

body = re.search(r'<body[^>]*>(.*?)</body>', html, re.S).group(1)
body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
body = re.sub(r'<script[^>]*src="app\.js"[^>]*></script>\s*', '', body)
body = body.replace('<main>', '').replace('</main>', '')


def img(m):
    name = m.group(2)
    if name not in ASSETS:
        raise SystemExit(f'нет адреса Тильды для {name} в tilda-assets.json')
    return f'{m.group(1)}="{ASSETS[name]}"'


body = re.sub(r'(src|href)="assets/([^"]+)"', img, body)
body = body.replace('</div></header>', '</div></header><div class="top-spacer" aria-hidden="true"></div>', 1)


def cut(patt):
    m = re.search(patt, body)
    if not m:
        raise SystemExit('не нашёл: ' + patt)
    return m.start()


p = [cut(r'<header class="top"'), cut(r'<section class="hero"'), cut(r'<section class="shop"'), cut(r'<section class="clubs"'),
     cut(r'<section class="how"'), cut(r'<section class="faq"'), cut(r'<div class="wrap"><footer'), len(body)]
parts = [body[p[i]:p[i + 1]].strip() for i in range(len(p) - 1)]
names = ['шапка', 'первый экран', 'программы', 'абонементы', 'как купить', 'вопросы', 'подвал, окно оплаты и скрипт']


def wrap(chunk):
    return f'<div class="shd1111">\n{chunk}\n</div>\n'


blocks = []
for i, (nm, chunk) in enumerate(zip(names, parts)):
    code = wrap(chunk)
    if i == 0:
        code = FONT_LINK + '\n' + HIDE_PROJECT_PARTS + '\n<style>' + css_scoped + '</style>\n' + code
    if i == len(parts) - 1:
        code += '<script>\n' + js_code + '\n</script>\n'
    if re.search(r'github|assets/', code, re.I):
        raise SystemExit(f'в блоке «{nm}» осталась внешняя ссылка: ' + re.search(r'.{0,60}(github|assets/).{0,60}', code, re.I).group(0))
    blocks.append((nm, code))

OUT.mkdir(exist_ok=True)
for old in OUT.glob('*.html'):
    old.unlink()
for i, (nm, code) in enumerate(blocks, 1):
    # строки длиннее 1500 знаков (SVG логотипа и соцсетей) режем по границам тегов, а длинные пути svg — по пробелам
    def _short(line):
        if len(line) <= 1500:
            return line
        line = line.replace('><', '>\n<')
        out = []
        for ln in line.split('\n'):
            while len(ln) > 1500:
                k = ln.rfind(' ', 0, 1500)
                if k <= 0:
                    break
                out.append(ln[:k]); ln = ln[k + 1:]
            out.append(ln)
        return '\n'.join(out)
    code = '\n'.join(_short(x) for x in code.split('\n'))
    blocks[i - 1] = (nm, code)
    (OUT / f'{i:02d}-{nm}.html').write_text(code, encoding='utf-8')
    print(f'{i:02d}-{nm}: {len(code):,} знаков'.replace(',', ' '))
preview = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           '<title>Превью Vibe-блоков</title><style>body{margin:0}</style></head><body><div id="allrecords">\n'
           + '\n'.join(f'<div class="t-rec" style="background:#f6f0ff">{c}</div>' for _n, c in blocks) + '\n</div></body></html>')
(OUT.parent / '_preview_vibe.html').write_text(preview, encoding='utf-8')
print('github/assets в блоках: нет')
