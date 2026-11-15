const { chromium } = require('playwright'); const fs=require('fs');
const FONT=fs.readFileSync('anton.woff2').toString('base64');
const DUR=42.8;
// speech segments [start,end,text]
const seg=[[0,3.4,"An 88-year-old woman in Florida kept getting letters…"],[3.72,5.6,"saying she had unclaimed money."],[6.28,8.0,"She was sure it was a scam."],[8.35,9.85,"She even called the police."],[10.35,12.1,"But when a detective looked into it…"],[12.45,15.94,"he found a real notice from the state, buried in her junk mail."],[16.33,22.63,"About $108,000. Stock from a company she worked for over 30 years ago."],[23.13,24.81,"And here's what nobody tells you:"],[25.1,31.8,"states are holding about $70 billion just like this. About 1 in 7 Americans has some."],[32.35,39.27,"Most people never find theirs… because they only search one place. Tap below and take the 60-second check."],[39.68,41.76,"Some of it could have your name on it."]];
// headline per time range
const heads=[[0,6.28,'SHE GOT LETTERS ABOUT<br><y>UNCLAIMED MONEY</y>'],[6.28,10.35,'SHE WAS SURE<br><y>IT WAS A SCAM</y>'],[10.35,16.33,'THEN A DETECTIVE<br><y>READ THE LETTER</y>'],[16.33,23.13,'IT WAS REAL:<br><y>$108,000</y>'],[23.13,32.35,''],[32.35,DUR,'IS THERE MONEY<br><y>IN YOUR NAME?</y>']];
// caption chunks
const chunks=[];
for(const [s,e,t] of seg){const w=t.split(' ');const groups=[];let g=[];for(const x of w){g.push(x);if(g.join(' ').length>14||/[.…:,]$/.test(x)){groups.push(g.join(' '));g=[];}} if(g.length)groups.push(g.join(' '));
 const tot=groups.reduce((a,b)=>a+b.length,0);let cur=s;for(const gr of groups){const d=(e-s)*gr.length/tot;chunks.push([cur,cur+d,gr]);cur+=d;}}
// timeline boundaries
const pts=new Set([0,DUR]);chunks.forEach(c=>{pts.add(+c[0].toFixed(2));pts.add(+c[1].toFixed(2))});heads.forEach(h=>{pts.add(h[0]);pts.add(h[1])});
const P=[...pts].sort((a,b)=>a-b);
const css=`<style>@font-face{font-family:A;src:url(data:font/woff2;base64,${FONT})}body{margin:0;background:transparent}
.h{position:absolute;top:150px;left:0;right:0;text-align:center;font-family:A;font-size:104px;line-height:1.05;color:#fff;text-shadow:0 0 18px #000,0 6px 0 #000}
y{color:#ffd23f}
.c{position:absolute;top:1360px;left:60px;right:60px;text-align:center;font-family:A;font-size:96px;line-height:1.1;color:#fff;-webkit-text-stroke:5px #000;paint-order:stroke fill;text-shadow:0 8px 0 #000}
.c b{color:#ffd23f}
.src{position:absolute;top:1880px;left:0;right:0;text-align:center;font-family:Arial;font-size:26px;color:rgba(255,255,255,.75)}</style>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
let list='';fs.mkdirSync('ov',{recursive:true});
for(let i=0;i<P.length-1;i++){const t=(P[i]+P[i+1])/2;
 const h=(heads.find(x=>t>=x[0]&&t<x[1])||[0,0,''])[2];
 let c=(chunks.find(x=>t>=x[0]&&t<x[1])||[0,0,''])[2];
 c=c.replace(/(\$[\d,]+(?: billion)?|scam\.|police\.|real notice|1 in 7|60-second check)/gi,'<b>$1</b>');
 await p.setContent(`${css}<div class="h">${h}</div><div class="c">${c}</div><div class="src">Story as reported by FOX 13 Tampa, Sept. 2025 · Images are dramatizations</div>`);
 const f=`ov/${String(i).padStart(3,'0')}.png`;await p.screenshot({path:f,omitBackground:true});
 list+=`file '${f}'\nduration ${(P[i+1]-P[i]).toFixed(3)}\n`;}
list+=`file 'ov/${String(P.length-2).padStart(3,'0')}.png'\n`;
fs.writeFileSync('ov.txt',list);
// stat card + CTA card full frames
await p.setContent(`${css}<div style="width:1080px;height:1920px;background:linear-gradient(160deg,#0b3d2c,#0f7b4f);font-family:A;color:#fff;display:flex;flex-direction:column;justify-content:flex-start;padding-top:330px;box-sizing:border-box;align-items:center;text-align:center;gap:34px">
<div style="font-size:90px">STATES ARE HOLDING</div><div style="font-size:230px;color:#ffd23f;line-height:1">$70 BILLION</div><div style="font-size:90px">IN UNCLAIMED MONEY</div>
<div style="font-size:70px;background:#fff;color:#111;padding:14px 34px;margin-top:40px">1 IN 7 AMERICANS HAS SOME</div><div style="font-family:Arial;font-size:30px;opacity:.8">Source: NAUPA</div></div>`);
await p.screenshot({path:'stat.png'});
await b.close();})();
