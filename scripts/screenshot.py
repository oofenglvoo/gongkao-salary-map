# -*- coding: utf-8 -*-
"""用 Playwright 依次截取三级视图，验证地图渲染无报错。"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, '全国公务员收入地图.html')
OUT = os.path.join(ROOT, 'docs')


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1500, 'height': 1000})
        errs = []
        pg.on('console', lambda m: errs.append(m.type + ': ' + m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        await pg.goto('file:///' + HTML.replace('\\', '/'))
        await pg.wait_for_timeout(3000)
        await pg.screenshot(path=os.path.join(OUT, '01-全国视图.png'), full_page=True)

        await pg.evaluate('renderSichuan()')
        await pg.wait_for_timeout(2200)
        await pg.screenshot(path=os.path.join(OUT, '02-四川省视图.png'), full_page=True)

        await pg.evaluate('renderChengdu()')
        await pg.wait_for_timeout(2200)
        info = await pg.evaluate("""() => ({
            crumb: document.getElementById('crumbCur').textContent,
            hint: document.getElementById('crumbHint').textContent,
            stats: document.getElementById('statsBox').innerText.replace(/\\n/g,' | '),
            btnNat: document.getElementById('btnNat').style.display,
            btnSC: document.getElementById('btnSC').style.display,
            canvases: document.querySelectorAll('canvas').length
        })""")
        await pg.screenshot(path=os.path.join(OUT, '03-成都市视图.png'), full_page=True)
        print('info:', info)
        print('errors:', errs if errs else 'NONE')
        await b.close()
        return 1 if errs else 0


sys.exit(asyncio.run(main()))
