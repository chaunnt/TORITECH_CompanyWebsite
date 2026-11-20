// Chụp ảnh đại diện 1200x630 (JPEG) cho trang dự án chưa có ảnh → assets/img/du-an/<ten>.jpg
// build.py tự gọi script này khi thiếu ảnh. Chụp lại tất cả: node tools/og_shots.js --force
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const root = path.join(__dirname, '..'), force = process.argv.includes('--force');
  const works = JSON.parse(fs.readFileSync(path.join(__dirname, 'projects.json'), 'utf8')).works;
  let b = null, p = null;
  for (const w of works) {
    const out = path.join(root, 'assets/img/du-an', path.basename(w.href, '.html') + '.jpg');
    if (fs.existsSync(out) && !force) continue;
    if (!b) { b = await chromium.launch(); p = await b.newPage({viewport: {width: 1200, height: 630}, deviceScaleFactor: 1}); }
    await p.goto('file://' + path.join(root, w.href));
    await p.evaluate(() => { for (const id of ['tt-top', 'tt-foot']) { const e = document.getElementById(id); if (e) e.remove(); } });
    await p.waitForTimeout(2500);
    await p.screenshot({path: out, type: 'jpeg', quality: 82});
    console.log('anh', out);
  }
  if (b) await b.close();
})();
