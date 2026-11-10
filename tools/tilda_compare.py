#!/usr/bin/env python3
"""Сверка опубликованной страницы Тильды с блоками из tilda/tilda-vibe (после publish_page).

Сравнение игнорирует пробелы, переносы и неразрывные пробелы: Тильда схлопывает переносы,
а неразрывные пробелы могут потеряться при передаче кода через MCP.
Запуск из корня репозитория: python3 tools/tilda_compare.py [URL]
"""
import glob
import re
import sys
import urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else 'https://walk-walk.ru/rasprodazha-11-11'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
live = urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8')


def sq(s):
    s = re.sub(r'(\.\d*[1-9])0+(?!\d)', r'\1', s)  # 15.930 и 15.93 — одно число (так легло в Тильду при первой выкладке)
    return re.sub(r'[ \t\r\n ]+', '', s)


L, bad = sq(live), 0
for f in sorted(glob.glob('tilda/tilda-vibe/*.html')):
    ok = sq(open(f, encoding='utf-8').read()) in L
    bad += not ok
    print(('СОВПАДАЕТ  ' if ok else 'РАЗНИЦА    ') + f.split('/')[-1])
print('ссылок на github на странице:', len(re.findall('github', live, re.I)))
print('кнопок с виджетом GetCourse:', len(re.findall(r'data-widget="\d+"', live)))
sys.exit(1 if bad else 0)
