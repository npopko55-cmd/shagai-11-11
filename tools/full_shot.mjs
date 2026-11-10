// Полностраничный скрин через CDP (обычный режим браузера, прокрутка для ленивых картинок)
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [URL_, W, H, OUT] = [process.argv[2], +process.argv[3], +process.argv[4], process.argv[5]];
const port = 9800 + (W % 97);
const chrome = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, '--user-data-dir=/tmp/shd_fs_' + W, '--hide-scrollbars', '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms)); let ws, id = 0; const pend = {};
const send = (m, p = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p })); });
setTimeout(() => { console.log('таймаут'); try { chrome.kill(); } catch {} process.exit(2); }, 150000);
let t; for (let i = 0; i < 40; i++) { try { t = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); if (t.length) break; } catch {} await sleep(250); }
ws = new WebSocket(t.find(x => x.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } };
const ev = async e => (await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true })).result?.result?.value;
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: W < 700 });
await send('Page.enable'); await send('Page.navigate', { url: URL_ }); await sleep(7000);
const h = await ev(`(async () => { document.documentElement.style.scrollBehavior='auto'; for (let y = 0; y < document.documentElement.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 180)); } scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)); return document.documentElement.scrollHeight; })()`);
await send('Emulation.setDeviceMetricsOverride', { width: W, height: Math.min(h, 16000), deviceScaleFactor: 1, mobile: W < 700 }); await sleep(1200);
const s = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(OUT, Buffer.from(s.result.data, 'base64'));
console.log(OUT.split('/').pop(), W, 'x', h); chrome.kill(); process.exit(0);
