#!/usr/bin/env python3
"""Отдельная страница /packs/: только блок паков из v4 (фильтры, 6 карточек, окно оплаты с виджетами GetCourse).

Без шапки, первого экрана и подвала. Карточки, тексты, цены и виджеты берутся из build_v4.py без изменений,
styles.css, app.js и картинки — копии из v4/. Запуск: python3 build_packs.py
"""
import pathlib
import shutil

import build_v4 as v4

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'packs'


def page():
    def count(a):
        return sum(1 for p in v4.PACKS if a == 'any' or p['aud'] == a)
    chips = ''.join(
        f'<button class="chip{" is-on" if a == "any" else ""}" type="button" data-aud="{a}">{v4.t(label)}<i>{count(a)}</i></button>'
        for a, label in [('any', 'Все предложения'), ('members', 'Только для участников клуба'), ('new', 'Для новых участников'), ('all', 'Для всех')])
    return f'''<!doctype html>
<html lang="ru" data-sale-campaign="{v4.SALE_CAMPAIGN}">
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
<body>
<main>
<section class="wrap shop" id="packs">
  <div class="chips">{chips}</div>
  <div class="grid">{"".join(v4.card(p) for p in v4.PACKS)}</div>
  <p class="noint">{v4.icon("bolt")}<span><b>Пак без интерактива.</b> {v4.t(v4.T["NOINT_T"])}</span></p>
</section>
</main>
<dialog class="paydlg" id="paydlg" aria-labelledby="paydlg-t">
  <div class="paydlg__head"><div><p class="paydlg__t" id="paydlg-t"></p><p class="paydlg__p"></p></div>
  <button class="paydlg__x" type="button" aria-label="Закрыть">{v4.icon("x")}</button></div>
  <div class="paydlg__body"><span class="paydlg__spin" aria-hidden="true"></span></div>
</dialog>
<script src="app.js"></script>
</body>
</html>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for name in ('styles.css', 'app.js'):
        shutil.copyfile(v4.OUT / name, OUT / name)
    shutil.copytree(v4.OUT / 'assets', OUT / 'assets', dirs_exist_ok=True)
    (OUT / 'index.html').write_text(page())
    print('собрано: packs/index.html')
