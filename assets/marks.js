// Small generative marks, one per research area, drawn once into any
// <canvas class="mark" data-kind="env|reg|comp">. Colors come from the stylesheet.
(function () {
  var css = getComputedStyle(document.documentElement);
  var col = { env: css.getPropertyValue('--env').trim(), reg: css.getPropertyValue('--reg').trim(), comp: css.getPropertyValue('--comp').trim() };

  function setup(c) {
    var dpr = Math.min(devicePixelRatio || 1, 2);
    var s = c.clientWidth || 96;
    c.width = s * dpr; c.height = s * dpr;
    var ctx = c.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.lineCap = 'round';
    return { ctx: ctx, s: s };
  }

  // environment: a small branching tree growing from the bottom
  function env(c, seed) {
    var o = setup(c), ctx = o.ctx, s = o.s, rnd = rng(seed);
    ctx.strokeStyle = col.env;
    function branch(x, y, a, len, w, d) {
      var nx = x + Math.cos(a) * len, ny = y + Math.sin(a) * len;
      ctx.globalAlpha = 0.9 - d * 0.1; ctx.lineWidth = w;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(nx, ny); ctx.stroke();
      if (d >= 5) { ctx.globalAlpha = 0.9; ctx.fillStyle = col.env; ctx.beginPath(); ctx.arc(nx, ny, 1.6, 0, 7); ctx.fill(); return; }
      var n = d < 1 ? 2 : (rnd() < 0.75 ? 2 : 1);
      for (var i = 0; i < n; i++) {
        var sign = n === 1 ? (rnd() < 0.5 ? -1 : 1) : (i ? 1 : -1);
        branch(nx, ny, a + sign * (0.35 + rnd() * 0.45), len * (0.68 + rnd() * 0.12), Math.max(0.6, w * 0.7), d + 1);
      }
    }
    branch(s * 0.5, s * 0.98, -Math.PI / 2 + (rnd() - 0.5) * 0.2, s * 0.3, 2.2, 0);
  }

  // regulation: an orderly lattice with a few emphasized cells
  function reg(c, seed) {
    var o = setup(c), ctx = o.ctx, s = o.s, rnd = rng(seed);
    var n = 6, pad = s * 0.12, step = (s - 2 * pad) / (n - 1);
    ctx.strokeStyle = col.reg; ctx.fillStyle = col.reg;
    ctx.lineWidth = 0.8; ctx.globalAlpha = 0.35;
    for (var i = 0; i < n; i++) {
      ctx.beginPath(); ctx.moveTo(pad, pad + i * step); ctx.lineTo(s - pad, pad + i * step); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(pad + i * step, pad); ctx.lineTo(pad + i * step, s - pad); ctx.stroke();
    }
    for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) {
      var r = rnd();
      ctx.globalAlpha = r < 0.18 ? 0.95 : 0.55;
      ctx.beginPath(); ctx.arc(pad + i * step, pad + j * step, r < 0.18 ? 3 : 1.4, 0, 7); ctx.fill();
    }
  }

  // computational: a scatter of nodes with near-neighbour edges
  function comp(c, seed) {
    var o = setup(c), ctx = o.ctx, s = o.s, rnd = rng(seed);
    var pts = [], N = 26, R = s * 0.3;
    for (var i = 0; i < N; i++) pts.push({ x: s * 0.08 + rnd() * s * 0.84, y: s * 0.08 + rnd() * s * 0.84, r: 1.2 + rnd() * 2.2 });
    ctx.strokeStyle = col.comp; ctx.fillStyle = col.comp; ctx.lineWidth = 0.8;
    for (var i = 0; i < N; i++) for (var j = i + 1; j < N; j++) {
      var dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y, d = Math.sqrt(dx * dx + dy * dy);
      if (d < R) { ctx.globalAlpha = 0.6 * (1 - d / R); ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y); ctx.stroke(); }
    }
    ctx.globalAlpha = 0.95;
    for (var i = 0; i < N; i++) { ctx.beginPath(); ctx.arc(pts[i].x, pts[i].y, pts[i].r, 0, 7); ctx.fill(); }
  }

  function rng(seed) { var t = seed >>> 0 || 1; return function () { t = (t * 1664525 + 1013904223) >>> 0; return t / 4294967296; }; }

  var draw = { env: env, reg: reg, comp: comp };
  function all() {
    var cs = document.querySelectorAll('canvas.mark');
    for (var i = 0; i < cs.length; i++) { var k = cs[i].dataset.kind; if (draw[k]) draw[k](cs[i], 7 + i * 31 + (k.length * 101)); }
  }
  all();
  var t; addEventListener('resize', function () { clearTimeout(t); t = setTimeout(all, 150); });
})();
