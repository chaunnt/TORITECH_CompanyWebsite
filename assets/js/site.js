/* TORITECH – site interactions: menu, chia sẻ MXH, in, xuất MP4, cookie, form liên hệ */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var CFG = window.TORI_CFG || {};

  function toast(msg, ms) {
    var t = $('#toast'); if (!t) { t = document.createElement('div'); t.id = 'toast'; t.setAttribute('role', 'status'); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show'); clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, ms || 2600);
  }
  window.toriToast = toast;

  /* ---------- menu ---------- */
  var nav = $('.site-nav'), btn = $('.nav-toggle');
  if (btn && nav) btn.addEventListener('click', function () { var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); });
  $$('.has-sub > button').forEach(function (b) {
    b.addEventListener('click', function (e) { e.stopPropagation(); var li = b.parentNode, o = li.classList.toggle('open'); b.setAttribute('aria-expanded', o ? 'true' : 'false'); });
  });
  document.addEventListener('click', function (e) { $$('.has-sub.open').forEach(function (li) { if (!li.contains(e.target)) { li.classList.remove('open'); li.querySelector('button').setAttribute('aria-expanded', 'false'); } }); });
  var hdr = $('.site-header'); if (hdr) { var onS = function () { hdr.classList.toggle('scrolled', window.scrollY > 8); }; window.addEventListener('scroll', onS, { passive: true }); onS(); }

  /* ---------- reveal on scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12 });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else $$('.reveal').forEach(function (el) { el.classList.add('in'); });

  /* ---------- share ---------- */
  function pageUrl() { return location.href.split('#')[0]; }
  function shareLinks(url, title) {
    var u = encodeURIComponent(url), t = encodeURIComponent(title);
    return {
      facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + u,
      linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + u,
      x: 'https://twitter.com/intent/tweet?url=' + u + '&text=' + t,
      telegram: 'https://t.me/share/url?url=' + u + '&text=' + t,
      email: 'mailto:?subject=' + t + '&body=' + t + '%0A' + u
    };
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) { } ta.remove(); return Promise.resolve();
  }
  var sheet = $('#share-sheet');
  function openShare(url, title) {
    if (!sheet) return;
    var L = shareLinks(url, title);
    $$('[data-net]', sheet).forEach(function (a) { var n = a.getAttribute('data-net'); if (L[n]) a.href = L[n]; });
    $('#share-url', sheet).value = url;
    var nat = $('[data-share-native]', sheet); if (nat) nat.hidden = !navigator.share;
    sheet.hidden = false; requestAnimationFrame(function () { sheet.classList.add('open'); });
    sheet._url = url; sheet._title = title;
    var f = $('.sheet-panel', sheet); f && f.focus();
  }
  function closeShare() { if (!sheet) return; sheet.classList.remove('open'); setTimeout(function () { sheet.hidden = true; }, 200); }
  $$('[data-share]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = b.getAttribute('data-share-url') ? new URL(b.getAttribute('data-share-url'), location.href).href : pageUrl();
      openShare(url, b.getAttribute('data-share-title') || document.title);
    });
  });
  if (sheet) {
    sheet.addEventListener('click', function (e) { if (e.target === sheet || e.target.closest('[data-close]')) closeShare(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !sheet.hidden) closeShare(); });
    $$('[data-net]', sheet).forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (a.getAttribute('data-net') === 'email') return;
        e.preventDefault(); window.open(a.href, 'share', 'width=640,height=560,noopener');
      });
    });
    var cp = $('[data-copy]', sheet); cp && cp.addEventListener('click', function () { copy(sheet._url).then(function () { toast('Đã sao chép liên kết'); }); });
    var zl = $('[data-zalo]', sheet); zl && zl.addEventListener('click', function () {
      if (navigator.share) { navigator.share({ title: sheet._title, url: sheet._url }).catch(function () { }); }
      else copy(sheet._url).then(function () { toast('Đã sao chép liên kết – dán vào Zalo để chia sẻ', 3600); });
    });
    var nat = $('[data-share-native]', sheet); nat && nat.addEventListener('click', function () { navigator.share({ title: sheet._title, url: sheet._url }).catch(function () { }); });
  }

  /* ---------- print ---------- */
  $$('[data-print]').forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });

  /* ---------- MP4 export ---------- */
  var vm = $('#video-modal');
  var lastVideo = null;
  function vmShow(state) { if (!vm) return; vm.hidden = false; vm.setAttribute('data-state', state); requestAnimationFrame(function () { vm.classList.add('open'); }); }
  function vmHide() { if (!vm) return; vm.classList.remove('open'); setTimeout(function () { vm.hidden = true; }, 200); }
  $$('[data-video]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!window.ToriScenes) return;
      var keys = b.getAttribute('data-video').split(',');
      var name = b.getAttribute('data-video-name') || ('toritech-' + keys.join('-'));
      var title = b.getAttribute('data-video-title') || document.title;
      vmShow('rec');
      var bar = $('.vm-bar i', vm), pct = $('.vm-pct', vm);
      var job = ToriScenes.record(ToriScenes.segmentsFor(keys, keys.length > 2 ? 3.8 : 4.6), {
        title: title, url: pageUrl(),
        onProgress: function (k) { if (bar) bar.style.width = (k * 100).toFixed(1) + '%'; if (pct) pct.textContent = Math.round(k * 100) + '%'; }
      });
      vm._job = job;
      job.then(function (r) {
        var file = name + '.' + r.ext;
        lastVideo = { blob: r.blob, file: file, type: r.type };
        var url = URL.createObjectURL(r.blob);
        var v = $('video', vm); if (v) { v.src = url; }
        var a = $('[data-dl]', vm); if (a) { a.href = url; a.download = file; a.textContent = 'Tải video (' + r.ext.toUpperCase() + ', ' + (r.blob.size / 1048576).toFixed(1) + ' MB)'; }
        var note = $('.vm-note', vm);
        if (note) note.textContent = r.ext === 'mp4' ? 'Video MP4 1280×720 – sẵn sàng đăng Facebook, Zalo, LinkedIn, YouTube.' : 'Trình duyệt này chưa ghi được MP4 nên đã xuất WebM. Mở trang bằng Chrome/Edge bản mới hoặc Safari để có MP4.';
        var sh = $('[data-share-video]', vm);
        if (sh) { var f = new File([r.blob], file, { type: r.type }); sh.hidden = !(navigator.canShare && navigator.canShare({ files: [f] })); }
        vmShow('done');
      }).catch(function (err) {
        if (err && err.message === 'cancelled') { vmHide(); return; }
        var e = $('.vm-err', vm); if (e) e.textContent = (err && err.message) || 'Không ghi được video.'; vmShow('err');
      });
    });
  });
  if (vm) {
    vm.addEventListener('click', function (e) {
      if (e.target.closest('[data-cancel]')) { if (vm._job && vm._job.cancel) vm._job.cancel(); vmHide(); }
      else if (e.target === vm || e.target.closest('[data-close]')) { if (vm.getAttribute('data-state') !== 'rec') vmHide(); }
    });
    var sv = $('[data-share-video]', vm);
    sv && sv.addEventListener('click', function () {
      if (!lastVideo) return; var f = new File([lastVideo.blob], lastVideo.file, { type: lastVideo.type });
      navigator.share({ files: [f], title: document.title, text: document.title + ' – ' + pageUrl() }).catch(function () { });
    });
  }

  /* ---------- cookie consent ---------- */
  var ck = $('#cookie-banner'), KEY = 'tori-cookie-v1';
  function getC() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setC(v) { try { localStorage.setItem(KEY, v); } catch (e) { } }
  if (ck && !getC()) ck.hidden = false;
  $$('[data-cookie]').forEach(function (b) { b.addEventListener('click', function () { setC(b.getAttribute('data-cookie')); ck.hidden = true; toast('Đã lưu lựa chọn cookie'); }); });
  $$('[data-cookie-reset]').forEach(function (b) { b.addEventListener('click', function () { try { localStorage.removeItem(KEY); } catch (e) { } if (ck) ck.hidden = false; }); });

  /* ---------- contact form (không có máy chủ: soạn sẵn nội dung, gửi qua Zalo/Email) ---------- */
  var form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form), lines = [
        'Yêu cầu tư vấn – TORITECH',
        'Họ tên: ' + d.get('name'), 'Đơn vị: ' + (d.get('org') || '-'), 'Điện thoại: ' + d.get('phone'), 'Email: ' + (d.get('email') || '-'),
        'Nhu cầu: ' + d.get('topic'), 'Nội dung: ' + (d.get('msg') || '-')
      ], body = lines.join('\n');
      var via = (e.submitter && e.submitter.value) || 'zalo';
      if (via === 'email' && CFG.email) { location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent('Yêu cầu tư vấn – ' + d.get('topic')) + '&body=' + encodeURIComponent(body); return; }
      copy(body).then(function () {
        toast('Đã sao chép nội dung yêu cầu. Dán vào Zalo để gửi cho TORITECH.', 4200);
        setTimeout(function () { window.open('https://zalo.me/' + (CFG.zalo || ''), '_blank', 'noopener'); }, 600);
      });
    });
  }

  var y = $('[data-year]'); if (y) y.textContent = new Date().getFullYear();
})();
