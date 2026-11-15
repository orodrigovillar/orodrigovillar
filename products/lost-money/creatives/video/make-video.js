// Gera vídeo vertical 9:16 com cenas (imagem com zoom ou card em tela cheia), manchetes, legendas sincronizadas e narração.
// Uso: node make-video.js config.json   (caminhos dentro do config são relativos ao config)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const cfgPath = path.resolve(process.argv[2]); const dir = path.dirname(cfgPath);
const C = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const work = path.join(dir, '.build-' + path.basename(cfgPath, '.json')); fs.mkdirSync(work + '/ov', { recursive: true });
const FONT = fs.readFileSync(path.join(__dirname, '../anton.woff2')).toString('base64');
const DUR = C.duration;
const sh = c => execSync(c, { stdio: ['ignore', 'ignore', 'inherit'] });

// legendas: divide cada fala em blocos curtos proporcionais ao tamanho
const chunks = [];
for (const [s, e, t] of C.segments) {
  const groups = []; let g = [];
  for (const x of t.split(' ')) { g.push(x); if (g.join(' ').length > 14 || /[.…:,?]$/.test(x)) { groups.push(g.join(' ')); g = []; } }
  if (g.length) groups.push(g.join(' '));
  const tot = groups.reduce((a, b) => a + b.length, 0); let cur = s;
  for (const gr of groups) { const d = (e - s) * gr.length / tot; chunks.push([cur, cur + d, gr]); cur += d; }
}
const pts = new Set([0, DUR]);
chunks.forEach(c => { pts.add(+c[0].toFixed(2)); pts.add(+c[1].toFixed(2)); });
C.heads.forEach(h => { pts.add(h[0]); pts.add(Math.min(h[1], DUR)); });
const P = [...pts].filter(x => x <= DUR).sort((a, b) => a - b);
const hl = new RegExp(C.highlight || '(\\$[\\d,]+)', 'gi');
const css = `<style>@font-face{font-family:A;src:url(data:font/woff2;base64,${FONT})}body{margin:0;background:transparent}
.h{position:absolute;top:150px;left:30px;right:30px;text-align:center;font-family:A;font-size:100px;line-height:1.05;color:#fff;text-shadow:0 0 18px #000,0 6px 0 #000}
y{color:#ffd23f}
.c{position:absolute;top:1360px;left:60px;right:60px;text-align:center;font-family:A;font-size:96px;line-height:1.1;color:#fff;-webkit-text-stroke:5px #000;paint-order:stroke fill;text-shadow:0 8px 0 #000}
.c b{color:#ffd23f}
.src{position:absolute;top:1880px;left:0;right:0;text-align:center;font-family:Arial;font-size:26px;color:rgba(255,255,255,.8)}</style>`;

(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  let list = '';
  for (let i = 0; i < P.length - 1; i++) {
    const t = (P[i] + P[i + 1]) / 2;
    const h = (C.heads.find(x => t >= x[0] && t < x[1]) || [0, 0, ''])[2];
    const c = ((chunks.find(x => t >= x[0] && t < x[1]) || [0, 0, ''])[2]).replace(hl, '<b>$1</b>');
    await p.setContent(`${css}<div class="h">${h}</div><div class="c">${c}</div><div class="src">${C.footer || ''}</div>`);
    const f = `${work}/ov/${String(i).padStart(3, '0')}.png`; await p.screenshot({ path: f, omitBackground: true });
    list += `file '${f}'\nduration ${(P[i + 1] - P[i]).toFixed(3)}\n`;
  }
  list += `file '${work}/ov/${String(P.length - 2).padStart(3, '0')}.png'\n`;
  fs.writeFileSync(work + '/ov.txt', list);
  // cards de tela cheia
  for (const [k, sc] of C.scenes.entries()) if (sc.card) {
    await p.setContent(`${css}<div style="width:1080px;height:1920px;background:${sc.bg || 'linear-gradient(160deg,#0b3d2c,#0f7b4f)'};font-family:A;color:#fff;display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:300px;box-sizing:border-box;gap:30px">${sc.card}</div>`);
    await p.screenshot({ path: `${work}/card${k}.png` });
  }
  await b.close();
  // clipes de cena
  const clips = [];
  for (const [k, sc] of C.scenes.entries()) {
    const d = (sc.end - sc.start).toFixed(3), n = Math.round((sc.end - sc.start) * 30), out = `${work}/c${k}.mp4`;
    if (sc.card) {
      sh(`ffmpeg -y -loglevel error -loop 1 -t ${d} -i ${work}/card${k}.png -vf "scale=1080:1920,zoompan=z='1+0.0004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${n}:s=1080x1920:fps=30,format=yuv420p" -frames:v ${n} -c:v libx264 -preset veryfast -crf 20 ${out}`);
    } else {
      const img = path.resolve(dir, sc.img);
      sh(`ffmpeg -y -loglevel error -loop 1 -t ${d} -i "${img}" -filter_complex "[0]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25,eq=brightness=-0.3[bg];[b]crop=iw:iw*9/16:0:(ih-iw*9/16)*0.3,scale=2160:1215,zoompan=z='min(1+0.0009*on,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${n}:s=1080x608:fps=30[fg];[bg][fg]overlay=0:656,format=yuv420p" -r 30 -frames:v ${n} -c:v libx264 -preset veryfast -crf 20 ${out}`);
    }
    clips.push(`file '${out}'`);
  }
  fs.writeFileSync(work + '/cl.txt', clips.join('\n'));
  sh(`ffmpeg -y -loglevel error -f concat -safe 0 -i ${work}/cl.txt -c copy ${work}/bg.mp4`);
  const outPath = path.resolve(dir, C.output);
  sh(`ffmpeg -y -loglevel error -i ${work}/bg.mp4 -f concat -safe 0 -i ${work}/ov.txt -i "${path.resolve(dir, C.audio)}" -filter_complex "[1]format=rgba,fps=30[ov];[0][ov]overlay=0:0,format=yuv420p[v]" -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 160k -t ${DUR} -movflags +faststart "${outPath}"`);
  fs.rmSync(work, { recursive: true, force: true });
  console.log('ok', outPath);
})();
