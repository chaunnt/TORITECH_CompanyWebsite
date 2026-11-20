// Tạo ảnh xem trước 1200x630 cho các trang showcase: node tools/og_shots.js [--force]
// Chạy trước `python3 tools/build.py` khi có trang showcase mới.
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const root = path.join(__dirname, '..'), force = process.argv.includes('--force');
  const works = JSON.parse(fs.readFileSync(path.join(__dirname, 'showcase.json'), 'utf8')).works;
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1200, height: 630}, deviceScaleFactor: 1});
  for (const w of works) {
    const out = path.join(root, 'assets/img/showcase', path.basename(w.href, '.html') + '.png');
    if (fs.existsSync(out) && !force) continue;
    await p.goto('file://' + path.join(root, w.href));
    await p.waitForTimeout(2500);
    await p.screenshot({path: out});
    console.log('og', out);
  }
  await b.close();
})();
