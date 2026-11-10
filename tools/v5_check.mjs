// v5 (10.11): кнопки с виджетом открывают форму GetCourse, кнопки без виджета — сообщение с телефоном. Формы не заполняются.
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [URL_, W, H, SHOT] = [process.argv[2], +process.argv[3], +process.argv[4], process.argv[5]];
const port = 9600 + (W % 97);
const chrome = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, '--user-data-dir=/tmp/shd_v5c_' + W, '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = {}; const errors = [];
const send = (m, p = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p })); });
setTimeout(() => { console.log(JSON.stringify({ W, error: 'таймаут теста' })); try { chrome.kill(); } catch {} process.exit(2); }, 220000);
let t; for (let i = 0; i < 40; i++) { try { t = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); if (t.length) break; } catch {} await sleep(250); }
ws = new WebSocket(t.find(x => x.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; }
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + (m.params.exceptionDetails.exception?.description || '').slice(0, 120));
  if (m.method === 'Network.loadingFailed' || (m.method === 'Network.responseReceived' && m.params.response.status >= 400)) errors.push('сеть: ' + (m.params.response?.status || m.params.errorText) + ' ' + (m.params.response?.url || '').slice(0, 90)); };
await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: W < 700 ? 2 : 1, mobile: W < 700 });
await send('Page.enable'); await send('Page.navigate', { url: URL_ }); await sleep(7000);
const ev = async e => (await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true })).result?.result?.value;
const out = await ev(`(async () => {
  const dlg = document.getElementById('paydlg'), note = document.getElementById('slot-note'), o = { vw: innerWidth, hscroll: document.documentElement.scrollWidth > innerWidth };
  o.fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')).filter((x, i, a) => a.indexOf(x) === i).join(',');
  o.google = performance.getEntriesByType('resource').filter(r => /googleapis|gstatic/.test(r.name)).length + ' запросов к Google';
  o.jump = getComputedStyle(document.querySelector('.jump')).display + ', ссылок ' + document.querySelectorAll('.jump a').length + ', цели есть: ' + [...document.querySelectorAll('.jump a')].every(a => document.querySelector(a.getAttribute('href')));
  const wait = ms => new Promise(r => setTimeout(r, ms));
  o.note = [];
  for (const btn of document.querySelectorAll('.pc__buy:not([data-widget])')) { btn.click(); await wait(250);
    const ok = dlg.open && !note.hidden && note.offsetHeight > 40 && !!note.querySelector('a[href^="tel:"]') && [...dlg.querySelectorAll('.paydlg__slot')].filter(x => !x.hidden).length === 1 && document.documentElement.classList.contains('is-locked');
    o.note.push((ok ? 'ok' : 'ПРОБЛЕМА') + ' · ' + dlg.querySelector('.paydlg__t').textContent.slice(0, 34) + ' · ' + dlg.querySelector('.paydlg__p').textContent); dlg.close(); await wait(80); }
  o.forms = [];
  for (const btn of document.querySelectorAll('.pc__buy[data-widget]')) { btn.click(); let h = 0;
    for (let i = 0; i < 50; i++) { await wait(400); const f = document.querySelector('#slot-' + btn.dataset.sid + ' iframe'); h = f ? parseInt(f.style.height) || 0 : 0; if (h > 50) break; }
    o.forms.push((h > 50 && note.hidden ? 'ok' : 'ПРОБЛЕМА') + ' · ' + btn.dataset.widget + ' · ' + btn.dataset.price + ' · форма ' + h + 'px'); dlg.close(); await wait(80); }
  // после формы снова сообщение: слоты не должны накладываться
  const b = document.querySelector('.pc__buy:not([data-widget])'); b.click(); await wait(250);
  o.afterForm = (!note.hidden && [...dlg.querySelectorAll('.paydlg__slot')].filter(x => !x.hidden).length === 1) ? 'ok' : 'ПРОБЛЕМА';
  o.unlocked = (dlg.close(), await wait(100), !document.documentElement.classList.contains('is-locked'));
  return o; })()`);
if (SHOT) { await ev(`document.querySelector('.pc__buy:not([data-widget])').scrollIntoView({block:'center', behavior:'instant'}); document.querySelector('.pc__buy:not([data-widget])').click()`); await sleep(600); const s = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(SHOT, Buffer.from(s.result.data, 'base64')); }
out.errors = errors; console.log(JSON.stringify(out, null, 1)); chrome.kill(); process.exit(0);
