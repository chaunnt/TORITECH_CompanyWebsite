/* TORITECH – 2.5D isometric scene engine (Canvas 2D, no dependencies)
 * Mỗi giải pháp có một "cảnh" với 2 trạng thái: problem (vấn đề) → solution (giải pháp).
 * Cảnh được vẽ lại mỗi khung hình nên có thể ghi trực tiếp thành video (MediaRecorder).
 */
(function (W) {
  'use strict';
  var FONT = "'Be Vietnam Pro', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";
  var C = {
    ink: '#0b1426', navy: '#10203d', slate: '#334155', ground: '#1a2b4a', ground2: '#1e3256',
    road: '#26344f', line: '#e2e8f0', cyan: '#22d3ee', teal: '#14b8a6', blue: '#3b82f6',
    amber: '#f59e0b', red: '#ef4444', green: '#22c55e', white: '#f8fafc', violet: '#8b5cf6',
    building: '#cbd5e1', glass: '#7dd3fc'
  };

  /* ---------- colour helpers ---------- */
  function hexToRgb(h) { h = h.replace('#', ''); if (h.length === 3) h = h.split('').map(function (c) { return c + c; }).join(''); var n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function shade(h, f) { var c = hexToRgb(h); return 'rgb(' + c.map(function (v) { return Math.max(0, Math.min(255, Math.round(v * f))); }).join(',') + ')'; }
  function rgba(h, a) { var c = hexToRgb(h); return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }
  function ease(x) { x = Math.max(0, Math.min(1, x)); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function lerp(a, b, k) { return a + (b - a) * k; }

  /* ---------- isometric graphics context ---------- */
  function G(ctx, rx, ry, rw, rh, opts) {
    opts = opts || {};
    var gw = opts.grid || 10;
    var s = Math.min(rw / (gw * 2 + 3), rh / (gw + 6)) * (opts.zoom || 1);
    this.ctx = ctx; this.s = s; this.gw = gw;
    this.ox = rx + rw / 2;
    this.oy = ry + rh * 0.56 - (gw / 2) * s;
    this.rx = rx; this.ry = ry; this.rw = rw; this.rh = rh;
    this.q = [];
  }
  G.prototype.p = function (x, y, z) { return [this.ox + (x - y) * this.s, this.oy + (x + y) * this.s * 0.5 - (z || 0) * this.s]; };
  G.prototype.poly = function (pts, fill, stroke, lw) {
    var c = this.ctx; c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (var i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
    c.closePath(); if (fill) { c.fillStyle = fill; c.fill(); }
    if (stroke) { c.strokeStyle = stroke; c.lineWidth = lw || 1; c.stroke(); }
  };
  G.prototype.queue = function (depth, fn) { this.q.push([depth, fn]); };
  G.prototype.flush = function () { this.q.sort(function (a, b) { return a[0] - b[0]; }); for (var i = 0; i < this.q.length; i++) this.q[i][1](); this.q = []; };
  G.prototype.alpha = function (a, fn) { if (a <= 0.003) return; var c = this.ctx, o = c.globalAlpha; c.globalAlpha = o * Math.min(1, a); fn(); c.globalAlpha = o; };
  G.prototype.tile = function (x, y, w, d, fill, z, stroke) {
    z = z || 0; this.poly([this.p(x, y, z), this.p(x + w, y, z), this.p(x + w, y + d, z), this.p(x, y + d, z)], fill, stroke, 1);
  };
  G.prototype.box = function (x, y, z, w, d, h, col, o) {
    o = o || {};
    var P = this.p.bind(this);
    var edge = o.edge || 'rgba(255,255,255,.10)';
    this.poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)], shade(col, o.rf || .78), edge);
    this.poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], shade(col, o.lf || .6), edge);
    this.poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)], o.top || shade(col, 1.08), edge);
    if (o.windows) {
      var c = this.ctx, rows = o.windows[0], cols = o.windows[1], wc = o.wcol || rgba(C.glass, .55);
      for (var r = 0; r < rows; r++) for (var k = 0; k < cols; k++) {
        var wx = x + w, wy = y + (k + .25) / cols * d, wz = z + (r + .3) / rows * h, ww = d / cols * .5, wh = h / rows * .45;
        this.poly([P(wx, wy, wz), P(wx, wy + ww, wz), P(wx, wy + ww, wz + wh), P(wx, wy, wz + wh)], wc);
        var lx = x + (k + .25) / cols * w;
        this.poly([P(lx, y + d, wz), P(lx + w / cols * .5, y + d, wz), P(lx + w / cols * .5, y + d, wz + wh), P(lx, y + d, wz + wh)], wc);
      }
      c = null;
    }
  };
  G.prototype.text = function (x, y, z, str, o) {
    o = o || {}; var c = this.ctx, p = this.p(x, y, z), fs = Math.max(9, (o.size || .42) * this.s);
    c.font = (o.weight || 600) + ' ' + fs + 'px ' + FONT; c.textAlign = 'center'; c.textBaseline = 'middle';
    if (o.bg) {
      var m = c.measureText(str), pw = m.width + fs * 1.1, ph = fs * 1.75, bx = p[0] - pw / 2, by = p[1] - ph / 2;
      c.fillStyle = o.bg; roundRect(c, bx, by, pw, ph, ph / 2); c.fill();
      if (o.border) { c.strokeStyle = o.border; c.lineWidth = 1; c.stroke(); }
      if (o.tail) { c.beginPath(); c.moveTo(p[0] - fs * .35, by + ph); c.lineTo(p[0], by + ph + fs * .5); c.lineTo(p[0] + fs * .35, by + ph); c.fillStyle = o.bg; c.fill(); }
    }
    c.fillStyle = o.color || C.white; c.fillText(str, p[0], p[1] + 0.5);
  };
  G.prototype.line = function (a, b, col, lw, dash, off) {
    var c = this.ctx, p1 = this.p(a[0], a[1], a[2]), p2 = this.p(b[0], b[1], b[2]);
    c.save(); c.strokeStyle = col; c.lineWidth = (lw || .06) * this.s; c.lineCap = 'round';
    if (dash) { c.setLineDash([dash * this.s, dash * this.s]); c.lineDashOffset = -(off || 0) * this.s; }
    c.beginPath(); c.moveTo(p1[0], p1[1]); c.lineTo(p2[0], p2[1]); c.stroke(); c.restore();
  };
  G.prototype.dot = function (x, y, z, r, col, glow) {
    var c = this.ctx, p = this.p(x, y, z);
    if (glow) { var gr = c.createRadialGradient(p[0], p[1], 0, p[0], p[1], r * this.s * 3); gr.addColorStop(0, rgba(col, .55)); gr.addColorStop(1, rgba(col, 0)); c.fillStyle = gr; c.beginPath(); c.arc(p[0], p[1], r * this.s * 3, 0, 7); c.fill(); }
    c.fillStyle = col; c.beginPath(); c.arc(p[0], p[1], r * this.s, 0, 7); c.fill();
  };
  G.prototype.ring = function (x, y, z, r, col, lw, fill) {
    var c = this.ctx, p = this.p(x, y, z);
    c.save(); c.beginPath(); c.ellipse(p[0], p[1], r * this.s * 1.414, r * this.s * .707, 0, 0, 7);
    if (fill) { c.fillStyle = fill; c.fill(); }
    if (col) { c.strokeStyle = col; c.lineWidth = (lw || .05) * this.s; c.stroke(); }
    c.restore();
  };
  G.prototype.person = function (x, y, col, bob) {
    var b = bob || 0; this.box(x - .15, y - .15, b, .3, .3, .55, col); this.dot(x, y, .8 + b, .17, '#f1c9a5');
  };
  G.prototype.car = function (x, y, col, dir) {
    if (dir === 'y') { this.box(x - .3, y - .55, .08, .6, 1.1, .32, col); this.box(x - .25, y - .25, .4, .5, .55, .25, col, { top: rgba(C.glass, .9) }); }
    else { this.box(x - .55, y - .3, .08, 1.1, .6, .32, col); this.box(x - .25, y - .25, .4, .55, .5, .25, col, { top: rgba(C.glass, .9) }); }
  };
  G.prototype.hud = function (x, y, w, h, title, rows, accent, a) {
    var c = this.ctx, s = this.s;
    this.alpha(a === undefined ? 1 : a, function () {
      c.save(); c.fillStyle = 'rgba(8,15,30,.82)'; c.strokeStyle = rgba(accent, .7); c.lineWidth = 1.2;
      roundRect(c, x, y, w, h, 10); c.fill(); c.stroke();
      var fs = Math.max(10, s * .38); c.font = '700 ' + fs + 'px ' + FONT; c.fillStyle = accent; c.textAlign = 'left'; c.textBaseline = 'top';
      c.fillText(title, x + 12, y + 10);
      c.font = '500 ' + (fs * .92) + 'px ' + FONT;
      for (var i = 0; i < rows.length; i++) { c.fillStyle = rows[i][1] || '#cbd5e1'; c.fillText(rows[i][0], x + 12, y + 14 + fs * 1.55 * (i + 1)); }
      c.restore();
    });
  };
  function roundRect(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }

  function ground(g, alt) {
    var n = g.gw;
    for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) g.tile(i, j, 1, 1, (i + j) % 2 ? C.ground : (alt || C.ground2), 0, 'rgba(255,255,255,.035)');
    // plinth edge
    var P = g.p.bind(g);
    g.poly([P(n, 0, 0), P(n, n, 0), P(n, n, -.5), P(n, 0, -.5)], '#0d1a33');
    g.poly([P(0, n, 0), P(n, n, 0), P(n, n, -.5), P(0, n, -.5)], '#091327');
  }

  /* =====================================================================
   * SCENES. draw(g, t, m) — t: giây, m: 0 = vấn đề, 1 = giải pháp
   * ===================================================================*/
  var S = {};

  /* 1. AI Camera Vision & VMS */
  S.vision = {
    title: 'AI Camera Vision & VMS',
    problem: 'Camera rời rạc, người trực phải dán mắt vào màn hình – sự cố bị bỏ sót.',
    solution: 'AI nhận diện thời gian thực, VMS gom mọi luồng về một nơi, cảnh báo tức thì.',
    draw: function (g, t, m) {
      ground(g);
      // road
      g.tile(0, 4, 10, 2.2, C.road);
      for (var k = 0; k < 10; k++) g.tile(k + .15, 5.05, .5, .1, rgba(C.line, .55));
      // inspection hall
      g.queue(8.5, function () { g.box(1, 7, 0, 3.2, 2.4, 1.7, '#94a3b8', { windows: [2, 4] }); g.box(1, 7, 1.7, 3.2, 2.4, .12, '#475569'); g.text(2.6, 8.2, 2.3, 'TRẠM ĐĂNG KIỂM', { size: .34, bg: 'rgba(15,23,42,.85)' }); });
      // cameras
      var cams = [[2, 3.4], [6.3, 3.4], [8.6, 6.8]];
      cams.forEach(function (cp, i) {
        g.queue(cp[0] + cp[1], function () {
          g.box(cp[0] - .05, cp[1] - .05, 0, .1, .1, 2.2, '#64748b');
          var live = m > .5 || i !== 1;
          g.box(cp[0] - .2, cp[1] - .1, 2.2, .45, .22, .2, live ? '#e2e8f0' : '#6b7280');
          g.dot(cp[0] + .25, cp[1] + .12, 2.3, .06, m > .5 ? C.green : (i === 1 ? C.red : C.amber), true);
        });
      });
      // FOV cones (solution)
      g.alpha(m, function () {
        cams.forEach(function (cp, i) {
          var sw = Math.sin(t * .8 + i) * .9, cx = cp[0] + sw, cy = (cp[1] < 5 ? 5.1 : 5.0);
          var a = g.p(cp[0], cp[1], 2.2), L = g.p(cx - 1.3, cy - .9, 0), R = g.p(cx + 1.3, cy + .9, 0), Rr = g.p(cx + 1.3, cy - .9, 0), Ll = g.p(cx - 1.3, cy + .9, 0);
          var ctx = g.ctx, gr = ctx.createLinearGradient(a[0], a[1], (L[0] + R[0]) / 2, (L[1] + R[1]) / 2);
          gr.addColorStop(0, rgba(C.cyan, .42)); gr.addColorStop(1, rgba(C.cyan, .05));
          g.poly([a, L, Ll, R, Rr], gr);
          g.tile(cx - 1.3, cy - .9, 2.6, 1.8, rgba(C.cyan, .07), .01, rgba(C.cyan, .35));
        });
      });
      // cars
      var cols = ['#f97316', '#e2e8f0', '#3b82f6', '#a3e635', '#f43f5e'];
      for (var c = 0; c < 5; c++) {
        (function (c) {
          var lane = c % 2 ? 4.55 : 5.6, sp = .9 + c * .12, x = ((t * sp + c * 2.6) % 13) - 1.5;
          if (x < -.6 || x > 10.4) return;
          g.queue(x + lane + .3, function () {
            g.car(x, lane, cols[c]);
            var p = g.p(x, lane, .9);
            // solution: bounding box + label
            g.alpha(m, function () {
              var ctx = g.ctx, bw = g.s * 2.1, bh = g.s * 1.35;
              ctx.save(); ctx.strokeStyle = C.cyan; ctx.lineWidth = 1.6; ctx.setLineDash([]);
              var bx = p[0] - bw / 2, by = p[1] - bh * .45, L = bw * .22;
              ctx.beginPath();
              ctx.moveTo(bx, by + L); ctx.lineTo(bx, by); ctx.lineTo(bx + L, by);
              ctx.moveTo(bx + bw - L, by); ctx.lineTo(bx + bw, by); ctx.lineTo(bx + bw, by + L);
              ctx.moveTo(bx, by + bh - L); ctx.lineTo(bx, by + bh); ctx.lineTo(bx + L, by + bh);
              ctx.moveTo(bx + bw - L, by + bh); ctx.lineTo(bx + bw, by + bh); ctx.lineTo(bx + bw, by + bh - L);
              ctx.stroke(); ctx.restore();
              g.text(x, lane, 1.75, (c % 2 ? 'Xe tải' : 'Ô tô') + ' · 5' + (c + 1) + 'A-•••.•• · ' + (96 + c % 4) + '%', { size: .28, bg: rgba(C.cyan, .92), color: '#06202a' });
            });
            // problem: missed vehicles
            if (c % 2 === 0) g.alpha(1 - m, function () { g.text(x, lane, 1.5, '?', { size: .5, bg: rgba(C.red, .9), weight: 800 }); });
          });
        })(c);
      }
      // problem: guard watching wall of screens
      g.alpha(1 - m, function () {
        g.queue(16.5, function () {
          for (var r = 0; r < 2; r++) for (var q = 0; q < 3; q++) {
            var flick = (Math.sin(t * 6 + r * 3 + q * 5) > .6);
            g.box(8.9, 7.6 + q * .55, .6 + r * .5, .1, .5, .42, flick ? '#94a3b8' : '#1f2937');
          }
          g.person(8.2, 8.3, '#475569', Math.sin(t * 2) * .02);
          g.text(8.2, 8.3, 1.55, 'Zzz…', { size: .3, bg: 'rgba(71,85,105,.9)' });
        });
      });
      g.flush();
      // HUD
      var W0 = g.rw, hx = g.rx + W0 - Math.min(250, W0 * .34) - 10, hw = Math.min(250, W0 * .34);
      g.hud(hx, g.ry + 10, hw, g.s * 3.1, 'VMS · Giám sát tập trung', [
        ['● 24/24 luồng camera trực tuyến', '#86efac'],
        ['Sự kiện hôm nay: ' + (120 + Math.floor(t * 3) % 40), '#e2e8f0'],
        ['Cảnh báo: xe dừng sai vị trí', '#fcd34d']
      ], C.cyan, m);
      g.hud(g.rx + 10, g.ry + 10, Math.min(250, W0 * .34), g.s * 3.1, 'Hiện trạng', [
        ['1/3 camera mất tín hiệu', '#fca5a5'],
        ['Không có cảnh báo tự động', '#fca5a5'],
        ['Tra lại video mất hàng giờ', '#fcd34d']
      ], C.red, 1 - m);
    }
  };

  /* 2. Booking & dispatch at scale */
  S.booking = {
    title: 'Nền tảng đặt lịch quy mô lớn',
    problem: 'Mọi người cùng đến một lúc: xe xếp hàng dài, máy chủ quá tải, không ai biết phải chờ bao lâu.',
    solution: 'Mỗi người có khung giờ riêng, được nhắc lịch đa kênh, hệ thống chia tải nên không nghẽn.',
    draw: function (g, t, m) {
      ground(g);
      g.tile(0, 5.2, 7.2, 1.3, C.road);            // access road
      g.tile(6.2, 1.2, 1.3, 4.0, C.road);
      // inspection center
      g.queue(7.2, function () {
        g.box(6.6, 1.3, 0, 3.0, 3.2, 1.9, '#cbd5e1', { windows: [2, 3] });
        g.box(6.6, 1.3, 1.9, 3.0, 3.2, .14, '#334155');
        g.text(8.1, 2.9, 2.6, 'TRUNG TÂM DỊCH VỤ', { size: .32, bg: 'rgba(15,23,42,.85)' });
      });
      // server(s)
      g.queue(3.6, function () {
        var hot = 1 - m;
        for (var i = 0; i < 3; i++) {
          var on = i === 0 || m > .3;
          if (!on) continue;
          var col = hot > .5 ? '#7f1d1d' : '#1e293b';
          g.box(.8 + i * .75, 1.2, 0, .6, .6, 1.5, col);
          for (var l = 0; l < 5; l++) g.dot(.8 + i * .75 + .62, 1.5, .25 + l * .26, .04, hot > .5 ? (Math.sin(t * 9 + l) > 0 ? C.red : C.amber) : (Math.sin(t * 4 + l + i) > -.3 ? C.green : C.teal));
        }
        g.alpha(hot, function () { g.text(1.1, 1.5, 2.25, '503 · Quá tải', { size: .32, bg: rgba(C.red, .92), tail: true }); });
        g.alpha(m, function () { g.text(1.9, 1.5, 2.25, 'Bộ đếm slot · 42/60', { size: .3, bg: rgba(C.teal, .92), color: '#03201c', tail: true }); });
      });
      // problem: long queue
      var cols = ['#f97316', '#e2e8f0', '#3b82f6', '#a3e635', '#f43f5e', '#eab308', '#94a3b8', '#06b6d4', '#fb7185', '#c084fc'];
      g.alpha(1 - m, function () {
        for (var i = 0; i < 9; i++) (function (i) {
          var x = 5.6 - i * 1.25 + Math.sin(t * 3 + i) * .03;
          g.queue(x + 5.85, function () { g.car(x, 5.85, cols[i]); if (i % 3 === 1) g.text(x, 5.85, 1.3, '!', { size: .4, bg: rgba(C.amber, .9), color: '#1c1917', weight: 800 }); });
        })(i);
        g.queue(20, function () { g.text(2.6, 7.8, 1.3, '⏱ Chờ 4–6 giờ', { size: .42, bg: rgba(C.red, .92), weight: 700 }); });
      });
      // solution: spaced cars flowing
      g.alpha(m, function () {
        for (var i = 0; i < 3; i++) (function (i) {
          var u = ((t * .16 + i / 3) % 1), x, y, dir;
          if (u < .65) { x = -0.5 + u / .65 * 7.3; y = 5.85; dir = 'x'; } else { x = 6.85; y = 5.85 - (u - .65) / .35 * 3.6; dir = 'y'; }
          g.queue(x + y, function () { g.car(x, y, cols[i * 3], dir); });
        })(i);
        // phones with reminders
        [[1.5, 8.2], [3.2, 8.8], [4.8, 8.1]].forEach(function (p, i) {
          g.queue(p[0] + p[1], function () {
            g.box(p[0] - .2, p[1] - .05, 0, .4, .1, .75, '#0f172a', { top: '#334155' });
            g.box(p[0] - .17, p[1] + .05, .05, .34, .005, .65, '#0ea5e9');
            if (Math.sin(t * 2 + i * 2) > -.2) g.text(p[0], p[1], 1.25, ['Nhắc lịch 08:30 ✓', 'Mã QR đã gửi ✓', 'Đổi giờ thành công ✓'][i], { size: .27, bg: rgba(C.green, .92), color: '#052e16', tail: true });
          });
        });
      });
      g.flush();
      // floating slot board (screen-space HUD)
      var c = g.ctx, n = 12, cw = Math.min(46, g.rw * .06), ch = cw * .55, bx = g.rx + g.rw - (cw + 5) * 4 - 16, by = g.ry + 14;
      g.alpha(m, function () {
        c.save(); c.fillStyle = 'rgba(8,15,30,.82)'; c.strokeStyle = rgba(C.teal, .7); roundRect(c, bx - 10, by - 6, (cw + 5) * 4 + 16, (ch + 5) * 3 + 38, 10); c.fill(); c.stroke();
        c.font = '700 ' + Math.max(10, g.s * .36) + 'px ' + FONT; c.fillStyle = C.teal; c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText('Khung giờ hôm nay', bx, by);
        for (var i = 0; i < n; i++) {
          var r = Math.floor(i / 4), k = i % 4, lit = (Math.floor(t * 2) % (n + 3)) >= i;
          c.fillStyle = lit ? rgba(C.teal, .85) : 'rgba(51,65,85,.8)'; roundRect(c, bx + k * (cw + 5), by + 22 + r * (ch + 5), cw, ch, 4); c.fill();
          c.fillStyle = lit ? '#032621' : '#94a3b8'; c.font = '600 ' + Math.max(8, ch * .45) + 'px ' + FONT; c.textAlign = 'center'; c.textBaseline = 'middle';
          c.fillText((7 + Math.floor(i / 2)) + ':' + (i % 2 ? '30' : '00'), bx + k * (cw + 5) + cw / 2, by + 22 + r * (ch + 5) + ch / 2);
        }
        c.restore();
      });
    }
  };

  /* 3. MCP & AI Agent ecosystem */
  S.mcp = {
    title: 'Hệ sinh thái MCP & AI Agent',
    problem: 'Nhân viên chạy qua lại giữa ERP, CRM, kế toán, thuế, cổng dịch vụ công – sao chép thủ công, dễ sai.',
    solution: 'AI Agent kết nối an toàn qua MCP: phân quyền chi tiết, ghi nhật ký mọi lệnh, việc quan trọng có người duyệt.',
    draw: function (g, t, m) {
      ground(g);
      var cx = 4.6, cy = 4.6, R = 3.4;
      var nodes = ['ERP', 'CRM', 'Kế toán', 'Thuế', 'Kho vận', 'Dịch vụ công'].map(function (n, i) {
        var a = -Math.PI / 2 + i / 6 * Math.PI * 2; return { n: n, x: cx + Math.cos(a) * R, y: cy + Math.sin(a) * R, col: [C.blue, C.violet, C.teal, C.amber, '#64748b', '#e11d48'][i] };
      });
      // links (drawn under boxes)
      nodes.forEach(function (nd, i) {
        g.alpha(m, function () {
          g.line([cx, cy, .5], [nd.x, nd.y, .5], rgba(C.cyan, .55), .07);
          var u = (t * .45 + i / 6) % 1, v = 1 - ((t * .3 + i / 4) % 1);
          g.dot(lerp(cx, nd.x, u), lerp(cy, nd.y, u), .5, .09, C.cyan, true);
          g.dot(lerp(cx, nd.x, v), lerp(cy, nd.y, v), .5, .07, '#a5f3fc', true);
        });
        g.alpha(1 - m, function () {
          var j = (i + 2) % 6; g.line([nd.x, nd.y, .3], [nodes[j].x, nodes[j].y, .3], rgba(C.red, .6), .05, .2, t * .6);
        });
      });
      nodes.forEach(function (nd, i) {
        g.queue(nd.x + nd.y, function () {
          g.box(nd.x - .55, nd.y - .55, 0, 1.1, 1.1, .9, nd.col);
          g.text(nd.x, nd.y, 1.45, nd.n, { size: .32, bg: 'rgba(15,23,42,.88)' });
          g.alpha(m, function () { g.text(lerp(cx, nd.x, .5), lerp(cy, nd.y, .5), .95, '🔒', { size: .3, bg: 'rgba(15,23,42,.8)' }); });
        });
      });
      // AI core
      g.alpha(m, function () {
        g.queue(cx + cy, function () {
          g.ring(cx, cy, .05, 1.35 + Math.sin(t * 2) * .08, rgba(C.cyan, .6), .06, rgba(C.cyan, .08));
          g.box(cx - .6, cy - .6, 0, 1.2, 1.2, .35, '#0e7490');
          var fl = Math.sin(t * 2.2) * .12;
          g.box(cx - .4, cy - .4, .55 + fl, .8, .8, .8, '#22d3ee', { top: '#a5f3fc' });
          g.dot(cx, cy, 1.8 + fl, .12, C.white, true);
          g.text(cx, cy, 2.45 + fl, 'AI Agent · MCP', { size: .36, bg: rgba(C.cyan, .95), color: '#062029', weight: 700 });
        });
        // audit log stack
        g.queue(17.5, function () {
          var n = 3 + Math.floor((t * 1.2) % 6);
          for (var i = 0; i < n; i++) g.box(8.6, 8.6, i * .12, .9, .7, .1, i === n - 1 ? C.cyan : '#334155');
          g.text(9.05, 8.95, n * .12 + .55, 'Audit log', { size: .28, bg: 'rgba(15,23,42,.88)' });
        });
        // human in the loop
        g.queue(9.8, function () {
          g.person(1.0, 8.8, '#0ea5e9');
          if ((t % 4) > 1.5) g.text(1.0, 8.8, 1.5, 'Duyệt lệnh ghi ✓', { size: .28, bg: rgba(C.green, .92), color: '#052e16', tail: true });
        });
      });
      // problem: employee running between systems with paper
      g.alpha(1 - m, function () {
        var seg = (t * .5) % 6, i0 = Math.floor(seg), f = ease(seg - i0), a = nodes[i0], b = nodes[(i0 + 3) % 6];
        var px = lerp(a.x, b.x, f), py = lerp(a.y, b.y, f);
        g.queue(px + py + .1, function () {
          g.person(px, py, '#f59e0b', Math.abs(Math.sin(t * 10)) * .08);
          g.box(px + .1, py - .1, .6, .3, .05, .38, '#f8fafc');
          g.text(px, py, 1.6, 'Copy · Paste · Gõ lại', { size: .28, bg: rgba(C.red, .9) });
        });
      });
      g.flush();
      g.hud(g.rx + 10, g.ry + 10, Math.min(260, g.rw * .36), g.s * 3.1, 'Kiểm soát MCP', [
        ['RBAC theo vai trò · OAuth / API key', '#a5f3fc'],
        ['Không dùng dữ liệu để huấn luyện AI', '#86efac'],
        ['Lệnh ghi/xoá cần người duyệt', '#fcd34d']
      ], C.cyan, m);
      g.hud(g.rx + 10, g.ry + 10, Math.min(260, g.rw * .36), g.s * 3.1, 'Hiện trạng', [
        ['10–15 phút / đơn vị / kỳ', '#fca5a5'],
        ['Đăng nhập từng cổng, từng mã', '#fca5a5'],
        ['Không ai biết ai đã sửa gì', '#fcd34d']
      ], C.red, 1 - m);
    }
  };

  /* 4. Trust & Governance */
  S.trust = {
    title: 'Bảo mật & Tuân thủ',
    problem: 'Dữ liệu hình ảnh, CCCD, biển số nằm rải rác – không phân quyền, không nhật ký, rủi ro rò rỉ.',
    solution: 'Nhiều lớp bảo vệ: lưu trữ tại Việt Nam, mã hoá, phân quyền RBAC, nhật ký kiểm toán, triển khai On-Premise.',
    draw: function (g, t, m) {
      ground(g);
      var cx = 4.5, cy = 4.5;
      var layers = [['Lưu trữ tại Việt Nam · On-Premise / Private Cloud', '#1d4ed8'], ['Mã hoá khi truyền & khi lưu', '#0891b2'], ['Phân quyền RBAC · xác thực OAuth', '#0d9488'], ['Nhật ký kiểm toán · giám sát 24/7', '#7c3aed']];
      layers.forEach(function (L, i) {
        var k = ease(m * 1.6 - i * .2), sz = 4.2 - i * .75, z = i * .45 * k;
        if (k <= 0) return;
        g.queue(i * .01, function () {
          g.alpha(k, function () {
            g.box(cx - sz / 2, cy - sz / 2, z, sz, sz, .22, L[1]);
          });
        });
        g.queue(30 + i, function () {
          g.alpha(k, function () { var lp = sz / 2; g.text(cx + lp + .2, cy + lp + .2, z + .3, L[0], { size: .29, bg: 'rgba(15,23,42,.88)', border: rgba(L[1], .9) }); });
        });
      });
      // data cube
      var hz = 1.95 * ease(m) + .2;
      g.queue(1, function () {
        g.box(cx - .45, cy - .45, hz, .9, .9, .9, '#f8fafc', { top: '#ffffff' });
        g.text(cx, cy, hz + 1.45, 'Dữ liệu khách hàng', { size: .3, bg: 'rgba(15,23,42,.9)' });
      });
      // leaking particles (problem) / contained (solution)
      for (var i = 0; i < 18; i++) {
        var a = i / 18 * 6.283 + t * .4, u = (t * .35 + i * .137) % 1;
        var rLeak = .6 + u * 5, rIn = 1.1 + Math.sin(t * 2 + i) * .25;
        var r = lerp(rLeak, rIn, ease(m)), z = lerp(hz + .4 + u * .5, hz + .5 + Math.sin(t * 3 + i) * .3, ease(m));
        (function (r, a, z, i, u) {
          g.queue(40, function () { g.alpha(lerp(1 - u, .9, m), function () { g.dot(cx + Math.cos(a) * r, cy + Math.sin(a) * r, z, .07, m > .5 ? C.cyan : C.red, true); }); });
        })(r, a, z, i, u);
      }
      g.flush();
      // shield dome
      g.alpha(ease(m), function () {
        var c = g.ctx, p = g.p(cx, cy, hz + .4), R = g.s * 2.2;
        var gr = c.createRadialGradient(p[0], p[1] - R * .4, R * .1, p[0], p[1], R * 1.2); gr.addColorStop(0, rgba(C.cyan, .02)); gr.addColorStop(1, rgba(C.cyan, .2));
        c.save(); c.beginPath(); c.ellipse(p[0], p[1], R, R * .95, 0, Math.PI, 0); c.ellipse(p[0], p[1], R, R * .35, 0, 0, Math.PI); c.fillStyle = gr; c.fill();
        c.strokeStyle = rgba(C.cyan, .5); c.lineWidth = 1.5; c.stroke(); c.restore();
      });
      g.alpha(1 - m, function () { g.text(cx, cy, 3.6, '⚠ Rò rỉ dữ liệu', { size: .42, bg: rgba(C.red, .92), weight: 700 }); });
    }
  };

  /* 5. Digital clerk – traffic violation notices (AI Agent) */
  S.notice = {
    title: 'AI Agent văn thư số',
    problem: 'Hàng nghìn bộ hồ sơ phải gấp, ghi địa chỉ, gửi bưu cục – chậm và nhiều thư bị hoàn.',
    solution: 'Scan cả tập, AI Agent đọc – phân loại – gửi thông báo qua app ngân hàng, ví điện tử trong cùng ngày.',
    draw: function (g, t, m) {
      ground(g);
      // desk & paper stacks
      g.queue(7, function () {
        g.box(1.3, 3.6, 0, 2.4, 1.4, .6, '#78716c');
        var h = lerp(1.6, .35 + .25 * Math.abs(Math.sin(t)), ease(m));
        g.box(1.6, 3.8, .6, .8, .6, h, '#f8fafc', { top: '#ffffff' });
        g.box(2.6, 3.9, .6, .7, .55, h * .8, '#e2e8f0');
        g.text(2.4, 4.3, .9 + h + .4, lerp(1248, 0, ease(m)) > 1 ? Math.round(lerp(1248, 60, ease(m))) + ' bộ hồ sơ' : 'Đã xử lý', { size: .3, bg: 'rgba(15,23,42,.88)' });
        g.person(2.5, 5.6, '#64748b', 0);
      });
      // problem: post truck & envelopes
      g.alpha(1 - m, function () {
        var x = 5 + ((t * .35) % 5);
        g.queue(x + 7.5, function () { g.box(x - .7, 7.2, .08, 1.4, .7, .7, '#f59e0b'); g.box(x + .7, 7.25, .08, .45, .6, .5, '#fbbf24', { top: rgba(C.glass, .8) }); g.text(x, 7.55, 1.3, 'Bưu cục · 3–7 ngày', { size: .3, bg: rgba(C.red, .9) }); });
        g.queue(19, function () { g.text(8.3, 3.2, 1.2, '✉ Chuyển hoàn', { size: .34, bg: rgba(C.amber, .92), color: '#1c1917' }); });
      });
      // solution: scanner, AI, phones
      g.alpha(m, function () {
        g.queue(6.9, function () { g.box(4.1, 2.6, 0, 1.1, .9, .8, '#334155'); g.box(4.1, 2.6, .8, 1.1, .9, .08, '#22d3ee'); g.text(4.65, 3.05, 1.35, 'Scan', { size: .28, bg: 'rgba(15,23,42,.88)' }); });
        g.queue(10.5, function () { var fl = Math.sin(t * 2) * .1; g.box(5.0, 5.0, .4 + fl, .9, .9, .9, '#22d3ee', { top: '#a5f3fc' }); g.text(5.45, 5.45, 1.95 + fl, 'AI Agent', { size: .32, bg: rgba(C.cyan, .95), color: '#062029' }); });
        var phones = [[8.2, 2.6, 'App ngân hàng'], [8.6, 4.9, 'Ví điện tử'], [8.0, 7.2, 'ePass / VETC']];
        phones.forEach(function (p, i) {
          g.line([5.45, 5.45, 1.0], [p[0], p[1], .5], rgba(C.cyan, .4), .05, .18, t * 1.5);
          var u = (t * .5 + i / 3) % 1;
          g.queue(20 + i, function () { g.dot(lerp(5.45, p[0], u), lerp(5.45, p[1], u), lerp(1, .6, u), .09, C.cyan, true); });
          g.queue(p[0] + p[1], function () {
            g.box(p[0] - .2, p[1] - .05, 0, .4, .1, .75, '#0f172a', { top: '#334155' }); g.box(p[0] - .17, p[1] + .05, .05, .34, .005, .65, '#0ea5e9');
            g.text(p[0], p[1], 1.25, p[2] + ' ✓', { size: .26, bg: rgba(C.green, .92), color: '#052e16', tail: true });
          });
        });
        g.line([2.6, 4.3, 1], [4.6, 3.05, .9], rgba(C.cyan, .45), .05, .18, t * 1.5);
        g.line([4.6, 3.05, .9], [5.45, 5.45, 1], rgba(C.cyan, .45), .05, .18, t * 1.5);
      });
      g.flush();
    }
  };

  /* 0. Hero – platform overview */
  S.hero = {
    title: 'TORITECH Platform',
    problem: 'Ba bài toán vận hành tách rời nhau.',
    solution: 'Một nền tảng: thị giác máy tính, đặt lịch quy mô lớn và AI Agent qua MCP.',
    draw: function (g, t, m) {
      ground(g, '#1b2f52');
      var isl = [[1.2, 1.2, 'AI Vision & VMS', C.cyan], [5.9, 1.6, 'Đặt lịch & Điều phối', C.teal], [3.4, 5.9, 'MCP & AI Agent', C.violet]];
      // links
      [[0, 1], [1, 2], [2, 0]].forEach(function (e, i) {
        var a = isl[e[0]], b = isl[e[1]];
        g.line([a[0] + 1.4, a[1] + 1.4, .6], [b[0] + 1.4, b[1] + 1.4, .6], rgba(C.cyan, .35), .06, .25, t);
        var u = (t * .35 + i / 3) % 1; g.dot(lerp(a[0] + 1.4, b[0] + 1.4, u), lerp(a[1] + 1.4, b[1] + 1.4, u), .6, .1, C.cyan, true);
      });
      isl.forEach(function (I, i) {
        var bob = Math.sin(t * 1.2 + i * 2) * .08;
        g.queue(I[0] + I[1] + 1, function () {
          g.box(I[0], I[1], .1 + bob, 2.8, 2.8, .35, '#1e3a8a', { top: '#25428f' });
          g.tile(I[0] + .2, I[1] + .2, 2.4, 2.4, rgba(I[3], .18), .46 + bob, rgba(I[3], .6));
          var X = I[0] + 1.4, Y = I[1] + 1.4, Z = .45 + bob;
          if (i === 0) {
            g.box(X + .4, Y - .9, Z, .08, .08, 1.5, '#94a3b8'); g.box(X + .2, Y - 1.0, Z + 1.5, .45, .22, .2, '#e2e8f0');
            g.car(X - .3, Y + .5, '#f97316'); g.alpha(.9, function () { g.ring(X - .3, Y + .5, Z, .8 + .1 * Math.sin(t * 3), C.cyan, .05); });
          } else if (i === 1) {
            g.box(X - .9, Y - .9, Z, 1.5, 1.2, 1.0, '#cbd5e1', { windows: [2, 2] });
            for (var k = 0; k < 4; k++) g.box(X + .7, Y - .8 + k * .45, Z, .35, .35, .12 + ((Math.floor(t * 2) + k) % 4 === 0 ? .5 : .1), k % 2 ? C.teal : '#5eead4');
          } else {
            var fl = Math.sin(t * 2) * .1;
            g.box(X - .4, Y - .4, Z + .3 + fl, .8, .8, .8, '#a78bfa', { top: '#ddd6fe' });
            for (var k2 = 0; k2 < 4; k2++) { var a = k2 / 4 * 6.283 + t * .6; g.box(X + Math.cos(a) * 1.0 - .15, Y + Math.sin(a) * 1.0 - .15, Z, .3, .3, .3, ['#3b82f6', '#14b8a6', '#f59e0b', '#e11d48'][k2]); }
          }
          g.text(X, Y, Z + 2.25, I[2], { size: .36, bg: 'rgba(8,15,30,.88)', border: rgba(I[3], .9), weight: 700 });
        });
      });
      g.flush();
    }
  };

  /* =====================================================================
   * PLAYER – gắn cảnh vào <canvas data-scene="...">
   * ===================================================================*/
  var reduce = W.matchMedia && W.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function Player(canvas) {
    this.cv = canvas; this.key = canvas.getAttribute('data-scene'); this.scene = S[this.key];
    this.mode = canvas.getAttribute('data-mode') === 'problem' ? 0 : 1; this.m = this.mode; this.t = 0; this.last = 0;
    this.auto = canvas.hasAttribute('data-auto'); this.visible = false; this.playing = !reduce;
    var self = this;
    this.resize(); W.addEventListener('resize', function () { self.resize(); });
    if ('IntersectionObserver' in W) new IntersectionObserver(function (es) { self.visible = es[0].isIntersecting; if (self.visible) self.kick(); }, { threshold: .05 }).observe(canvas);
    else this.visible = true;
    this.render();
    if (this.auto) { this.mode = 0; this.m = 0; this.autoT = 0; }
  }
  Player.prototype.resize = function () {
    var r = this.cv.getBoundingClientRect(), d = Math.min(2, W.devicePixelRatio || 1);
    this.w = Math.max(280, r.width); this.h = Math.max(200, r.height);
    this.cv.width = Math.round(this.w * d); this.cv.height = Math.round(this.h * d); this.d = d; this.render();
  };
  Player.prototype.setMode = function (m) { this.mode = m; this.auto = false; this.kick(); this.render(); };
  Player.prototype.kick = function () { var self = this; if (this.raf) return; this.last = performance.now(); this.raf = requestAnimationFrame(function f(now) { self.raf = null; if (!self.visible) return; var dt = Math.min(.05, (now - self.last) / 1000); self.last = now; self.step(dt); self.render(); if (self.playing || Math.abs(self.m - self.mode) > .001) self.raf = requestAnimationFrame(f); }); };
  Player.prototype.step = function (dt) {
    if (this.playing) this.t += dt;
    if (this.auto) { this.autoT += dt; var cyc = this.autoT % 10; this.mode = cyc < 4.5 ? 0 : 1; }
    this.m += (this.mode - this.m) * Math.min(1, dt * 3.2);
    var root = this.cv.closest('[data-scene-root]');
    if (root) { root.setAttribute('data-state', this.mode ? 'solution' : 'problem'); }
  };
  Player.prototype.render = function () {
    var c = this.cv.getContext('2d'); c.setTransform(this.d, 0, 0, this.d, 0, 0); c.clearRect(0, 0, this.w, this.h);
    var g = new G(c, 0, 0, this.w, this.h); this.scene.draw(g, this.t, ease(this.m));
  };

  /* =====================================================================
   * RECORDER – xuất video MP4 (hoặc WebM nếu trình duyệt không hỗ trợ MP4)
   * ===================================================================*/
  function pickMime() {
    var list = ['video/mp4;codecs=avc1.42E01E,mp4a.40.2', 'video/mp4;codecs=avc1.42E01E', 'video/mp4;codecs=avc1', 'video/mp4', 'video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm'];
    if (!W.MediaRecorder) return null;
    for (var i = 0; i < list.length; i++) if (MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(list[i])) return list[i];
    return '';
  }
  function wrap(c, text, x, y, maxW, lh) {
    var words = text.split(' '), line = '', lines = [];
    for (var i = 0; i < words.length; i++) { var test = line ? line + ' ' + words[i] : words[i]; if (c.measureText(test).width > maxW && line) { lines.push(line); line = words[i]; } else line = test; }
    lines.push(line); for (var j = 0; j < lines.length; j++) c.fillText(lines[j], x, y + j * lh); return lines.length;
  }
  /* segments: [{scene, mode:'problem'|'solution', dur}] */
  function record(segments, opts) {
    opts = opts || {};
    var WID = 1280, HEI = 720, FPS = 30;
    var cv = document.createElement('canvas'); cv.width = WID; cv.height = HEI;
    var c = cv.getContext('2d');
    var mime = pickMime();
    if (mime === null || !cv.captureStream) return Promise.reject(new Error('Trình duyệt không hỗ trợ ghi video (MediaRecorder). Hãy dùng Chrome, Edge hoặc Safari bản mới.'));
    var stream = cv.captureStream(FPS), rec = new MediaRecorder(stream, mime ? { mimeType: mime, videoBitsPerSecond: 6e6 } : { videoBitsPerSecond: 6e6 });
    var chunks = []; rec.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
    var total = segments.reduce(function (a, s) { return a + s.dur; }, 0) + 2.2;
    var cancelled = false, start = 0;
    var url = opts.url || location.href.split('#')[0];
    function frame(now) {
      if (cancelled) return;
      if (!start) start = now;
      var el = (now - start) / 1000;
      // background
      var gr = c.createLinearGradient(0, 0, 0, HEI); gr.addColorStop(0, '#071022'); gr.addColorStop(1, '#0f2246'); c.fillStyle = gr; c.fillRect(0, 0, WID, HEI);
      if (el < 2.2) { // intro card
        var k = ease(Math.min(1, el / .6));
        c.globalAlpha = k; c.fillStyle = '#22d3ee'; c.font = '800 64px ' + FONT; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('TORITECH', WID / 2, HEI / 2 - 40);
        c.fillStyle = '#e2e8f0'; c.font = '500 26px ' + FONT; c.fillText(opts.title || 'Hạ tầng thị giác máy tính & hệ sinh thái AI Agent', WID / 2, HEI / 2 + 24);
        c.fillStyle = '#94a3b8'; c.font = '400 18px ' + FONT; c.fillText(url.replace(/^https?:\/\//, ''), WID / 2, HEI / 2 + 70); c.globalAlpha = 1;
      } else {
        var acc = 2.2, seg = segments[segments.length - 1], segT = 0, idx = segments.length - 1;
        for (var i = 0; i < segments.length; i++) { if (el < acc + segments[i].dur) { seg = segments[i]; segT = el - acc; idx = i; break; } acc += segments[i].dur; }
        var sc = S[seg.scene], prev = segments[idx - 1];
        var target = seg.mode === 'solution' ? 1 : 0, from = prev && prev.scene === seg.scene ? (prev.mode === 'solution' ? 1 : 0) : target;
        var m = lerp(from, target, ease(segT / .9));
        var g = new G(c, 40, 96, WID - 80, HEI - 96 - 150, { zoom: 1.22 }); sc.draw(g, el, ease(m));
        // header
        c.fillStyle = 'rgba(7,16,34,.92)'; c.fillRect(0, 0, WID, 80);
        c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillStyle = '#22d3ee'; c.font = '800 26px ' + FONT; c.fillText('TORITECH', 36, 40);
        c.fillStyle = '#e2e8f0'; c.font = '600 22px ' + FONT; c.fillText(sc.title, 210, 40);
        var tag = seg.mode === 'solution' ? 'GIẢI PHÁP' : 'VẤN ĐỀ', tc = seg.mode === 'solution' ? '#14b8a6' : '#ef4444';
        c.font = '700 16px ' + FONT; var tw = c.measureText(tag).width + 28; c.fillStyle = tc; roundRect(c, WID - tw - 36, 24, tw, 32, 16); c.fill();
        c.fillStyle = '#fff'; c.textAlign = 'center'; c.fillText(tag, WID - tw / 2 - 36, 41);
        // caption
        c.fillStyle = 'rgba(7,16,34,.9)'; c.fillRect(0, HEI - 140, WID, 140);
        c.fillStyle = tc; c.fillRect(0, HEI - 140, 6, 140);
        c.textAlign = 'left'; c.textBaseline = 'top'; c.fillStyle = '#f8fafc'; c.font = '600 28px ' + FONT;
        wrap(c, seg.mode === 'solution' ? sc.solution : sc.problem, 40, HEI - 118, WID - 80, 40);
        c.fillStyle = '#94a3b8'; c.font = '400 16px ' + FONT; c.fillText(url.replace(/^https?:\/\//, ''), 40, HEI - 30);
        // progress
        c.fillStyle = '#22d3ee'; c.fillRect(0, HEI - 4, WID * Math.min(1, el / total), 4);
      }
      if (opts.onProgress) opts.onProgress(Math.min(1, el / total));
      if (el >= total) { rec.stop(); return; }
      requestAnimationFrame(frame);
    }
    var p = new Promise(function (res, rej) {
      rec.onstop = function () {
        stream.getTracks().forEach(function (tr) { tr.stop(); });
        if (cancelled) return rej(new Error('cancelled'));
        var type = (rec.mimeType || mime || 'video/webm').split(';')[0];
        res({ blob: new Blob(chunks, { type: type }), ext: type.indexOf('mp4') >= 0 ? 'mp4' : 'webm', type: type });
      };
      rec.onerror = function (e) { rej(e.error || new Error('Lỗi ghi video')); };
    });
    rec.start(250); requestAnimationFrame(frame);
    p.cancel = function () { cancelled = true; try { rec.stop(); } catch (e) { } };
    return p;
  }

  function segmentsFor(keys, dur) { var out = []; dur = dur || 4.5; keys.forEach(function (k) { if (k === 'hero') { out.push({ scene: k, mode: 'solution', dur: dur }); return; } out.push({ scene: k, mode: 'problem', dur: dur }); out.push({ scene: k, mode: 'solution', dur: dur + .5 }); }); return out; }

  W.ToriScenes = { scenes: S, G: G, Player: Player, record: record, segmentsFor: segmentsFor, mime: pickMime };

  function boot() {
    var players = [];
    document.querySelectorAll('canvas[data-scene]').forEach(function (cv) { if (S[cv.getAttribute('data-scene')]) { var p = new Player(cv); cv._player = p; players.push(p); } });
    document.querySelectorAll('[data-scene-toggle]').forEach(function (b) {
      b.addEventListener('click', function () {
        var root = b.closest('[data-scene-root]'), cv = root && root.querySelector('canvas[data-scene]'); if (!cv || !cv._player) return;
        cv._player.setMode(b.getAttribute('data-scene-toggle') === 'solution' ? 1 : 0);
        root.querySelectorAll('[data-scene-toggle]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      });
    });
    W.addEventListener('beforeprint', function () {
      players.forEach(function (p) { try { var img = new Image(); img.src = p.cv.toDataURL('image/png'); img.className = 'print-snapshot'; p.cv.insertAdjacentElement('afterend', img); } catch (e) { } });
    });
    W.addEventListener('afterprint', function () { document.querySelectorAll('.print-snapshot').forEach(function (i) { i.remove(); }); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
