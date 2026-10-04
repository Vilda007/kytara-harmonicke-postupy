const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generatePDFs() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // Load the JSON data to get all keys
    const data = JSON.parse(fs.readFileSync('chords.json', 'utf8'));
    const allKeys = data.keys;

    // Set print options for A4 Landscape
    await page.setViewport({ width: 1123, height: 794 }); // A4 landscape px at 96dpi

    console.log(`Starting PDF generation for ${allKeys.length} keys...`);

    for (const key of allKeys) {
        const url = `file://${path.resolve('index.html')}?key=${encodeURIComponent(key.symbol)}&type=${key.type}`;

        try {
            await page.goto(url, { waitUntil: 'networkidle0' });

            const fileName = `harmonic-prog-guitar-${key.type === 'major' ? 'all-keys' : 'all-minor-keys'}-${key.type === 'major' ? '' : 'minor'}_${key.symbol}.pdf`;
            // Note: for the final production we can group them into one PDF,
            // but for now we'll generate per-key to verify.

            await page.pdf({
                path: fileName,
                format: 'A4',
                landscape: true,
                printBackground: true,
                margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
            });
            console.log(`✅ Generated: ${fileName}`);
        } catch (err) {
            console.error(`❌ Failed to generate PDF for ${key.symbol}:`, err);
        }
    }

    await browser.close();
    console.log('PDF generation complete.');
}

generatePDFs().catch(err => {
    console.error('Fatal error during PDF generation:', err);
    process.exit(1);
});
