// Home-page hero: a branching structure that grows in from the right edge of
// the page (root system, river delta, or phylogeny, depending on your eye)
// and then holds. Tips take the three research-area colors from the stylesheet.
(function () {
  var c = document.getElementById('net');
  if (!c) return;
  var ctx = c.getContext('2d');
  var css = getComputedStyle(document.documentElement);
  var tipColors = [css.getPropertyValue('--env').trim(), css.getPropertyValue('--reg').trim(), css.getPropertyValue('--comp').trim()];
  var branchColor = css.getPropertyValue('--branch').trim() || '#5f7a6a';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W, H, dpr, growers, tips, raf;

  function size() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = c.clientWidth; H = c.clientHeight;
    c.width = W * dpr; c.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.lineCap = 'round';
  }

  function grower(x, y, angle, len, width, depth) {
    return { x: x, y: y, a: angle, left: len, w: width, d: depth, wobble: (Math.random() - 0.5) * (depth < 2 ? 0.015 : 0.04) };
  }

  function seed() {
    ctx.clearRect(0, 0, W, H);
    growers = []; tips = [];
    // trunks enter from the right edge and lower-right corner, heading left/up
    var trunks = 3 + Math.floor(W / 500);
    for (var i = 0; i < trunks; i++) {
      var fromBottom = Math.random() < 0.45;
      var x = fromBottom ? W * (0.45 + Math.random() * 0.5) : W + 4;
      var y = fromBottom ? H + 4 : H * (0.15 + Math.random() * 0.8);
      var a = fromBottom ? -Math.PI / 2 + (Math.random() - 0.5) * 0.6 : Math.PI + (Math.random() - 0.5) * 0.5;
      growers.push(grower(x, y, a, 140 + Math.random() * 160, 2.1, 0));
    }
  }

  function stepGrowers(speed) {
    var next = [];
    for (var i = 0; i < growers.length; i++) {
      var g = growers[i];
      var adv = Math.min(speed, g.left);
      g.a += g.wobble + (Math.random() - 0.5) * (g.d < 2 ? 0.05 : 0.12);
      var nx = g.x + Math.cos(g.a) * adv, ny = g.y + Math.sin(g.a) * adv;
      ctx.strokeStyle = branchColor;
      ctx.globalAlpha = 0.55 - g.d * 0.045;
      ctx.lineWidth = g.w;
      ctx.beginPath(); ctx.moveTo(g.x, g.y); ctx.lineTo(nx, ny); ctx.stroke();
      g.x = nx; g.y = ny; g.left -= adv;
      var out = g.x < -20 || g.x > W + 20 || g.y < -20 || g.y > H + 20;
      if (g.left > 0.5 && !out) { next.push(g); continue; }
      if (out || g.d >= 7) { tips.push({ x: g.x, y: g.y, k: Math.floor(Math.random() * 3), r: 1.8 + Math.random() * 2 }); continue; }
      var kids = g.d < 2 ? 2 : (Math.random() < (g.d < 4 ? 0.7 : 0.45) ? 2 : 1);
      var spread = 0.45 + Math.random() * 0.5;
      for (var k = 0; k < kids; k++) {
        var sign = kids === 1 ? (Math.random() < 0.5 ? -1 : 1) : (k === 0 ? -1 : 1);
        next.push(grower(g.x, g.y, g.a + sign * spread * (0.5 + Math.random() * 0.7),
          g.left * 0 + (70 + Math.random() * 110) * Math.pow(0.82, g.d), Math.max(0.5, g.w * 0.72), g.d + 1));
      }
      if (kids === 1 || Math.random() < 0.35) tips.push({ x: g.x, y: g.y, k: Math.floor(Math.random() * 3), r: 1.4 + Math.random() * 1.6 });
    }
    growers = next;
  }

  function drawTips() {
    ctx.globalAlpha = 0.9;
    for (var i = 0; i < tips.length; i++) {
      var t = tips[i];
      ctx.fillStyle = tipColors[t.k];
      ctx.beginPath(); ctx.arc(t.x, t.y, t.r, 0, Math.PI * 2); ctx.fill();
    }
    tips = [];
  }

  function frame() {
    stepGrowers(2.2);
    drawTips();
    if (growers.length) raf = requestAnimationFrame(frame);
  }

  function start() {
    cancelAnimationFrame(raf);
    size(); seed();
    if (reduce) { while (growers.length) { stepGrowers(6); drawTips(); } }
    else raf = requestAnimationFrame(frame);
  }

  start();
  var t; addEventListener('resize', function () { clearTimeout(t); t = setTimeout(start, 150); });
})();
