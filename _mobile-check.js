const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    const page = await browser.newPage();
    await page.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
    page.on('console', m => { if (m.type() === 'error') console.log('CONSOLE ERROR:', m.text()); });
    await page.goto('http://127.0.0.1:8931/index.html', { waitUntil: 'networkidle0' });
    await page.waitForSelector('svg', { timeout: 15000 });

    // Measure horizontal overflow and the circle SVG's rendered size
    const m = await page.evaluate(() => {
        const doc = document.documentElement;
        const svg = document.querySelector('svg[viewBox="0 0 600 600"]') || document.querySelector('svg');
        const r = svg ? svg.getBoundingClientRect() : null;
        return {
            scrollWidth: doc.scrollWidth,
            clientWidth: doc.clientWidth,
            overflow: doc.scrollWidth - doc.clientWidth,
            svgWidth: r ? Math.round(r.width) : null,
            svgHeight: r ? Math.round(r.height) : null,
            svgRight: r ? Math.round(r.right) : null,
        };
    });
    console.log(JSON.stringify(m, null, 2));

    await page.screenshot({ path: '_mobile-check.png' });

    // Desktop sanity check too
    await page.setViewport({ width: 1440, height: 900 });
    await new Promise(r => setTimeout(r, 300));
    const d = await page.evaluate(() => {
        const svg = document.querySelector('svg[viewBox="0 0 600 600"]') || document.querySelector('svg');
        const r = svg ? svg.getBoundingClientRect() : null;
        return { svgWidth: r ? Math.round(r.width) : null };
    });
    console.log('desktop svg width:', d.svgWidth);

    await browser.close();
    process.exit(0);
})();