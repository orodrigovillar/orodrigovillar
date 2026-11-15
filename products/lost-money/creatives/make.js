const { chromium } = require('playwright');
const ads = [
 {id:'01-name', bg:'linear-gradient(160deg,#0b3d2c,#0f7b4f)', top:'TYPE YOUR NAME.', big:'THERE MAY BE<br><span>MONEY WAITING</span><br>FOR YOU.', sub:'States hold billions in forgotten paychecks, bank accounts & insurance.', cta:'SEE WHERE TO LOOK →', foot:'Searching official databases is always free.'},
 {id:'02-parents', bg:'linear-gradient(160deg,#2a1d12,#6b4423)', top:'DID A PARENT PASS AWAY?', big:'THEY MAY HAVE LEFT<br><span>MONEY NO ONE</span><br>EVER CLAIMED.', sub:'Life insurance. Old accounts. Savings bonds. Heirs can claim.', cta:'TAKE THE 60-SECOND CHECK →', foot:'Independent guide · Not a government agency'},
 {id:'03-moved', bg:'linear-gradient(160deg,#0d1b3e,#1f4fa3)', top:'MOVED IN THE LAST 10 YEARS?', big:'YOUR LAST<br><span>PAYCHECK</span><br>MAY STILL BE OUT THERE.', sub:'When checks can\'t find you, they go to the state.', cta:'CHECK YOUR RISK FACTORS →', foot:'Official claims are always free.'},
 {id:'04-ignore', bg:'#111', top:'MOST PEOPLE SEARCH ONE WEBSITE.', big:'THAT\'S WHY<br><span>THEY FIND</span><br>NOTHING.', sub:'Other states. Maiden names. Federal programs. The 30-minute method.', cta:'GET THE PLAYBOOK · $9', foot:'60-day money-back guarantee'},
 {id:'05-bonds', bg:'linear-gradient(160deg,#3b0d0d,#9b1c1c)', top:'GRANDMA BOUGHT YOU<br>SAVINGS BONDS?', big:'MANY ARE<br><span>STILL UNCASHED</span><br>TODAY.', sub:'Matured bonds stop earning. Here\'s how to find them.', cta:'SEE HOW →', foot:'Independent guide · Not affiliated with the U.S. Treasury'},
 {id:'06-billions', bg:'linear-gradient(160deg,#1a1a2e,#3d2c8d)', top:'THIS ISN\'T A SCAM. IT\'S THE LAW.', big:'BILLIONS SIT<br><span>UNCLAIMED</span><br>IN STATE ACCOUNTS.', sub:'Companies must send lost money to the state. You have to go get it.', cta:'FIND OUT IF SOME IS YOURS →', foot:'Searching is free. We show you where.'},
];
const fs=require('fs');const FONT=fs.readFileSync(__dirname+'/anton.woff2').toString('base64');
const photo=a=>fs.existsSync(`${__dirname}/photo-${a.id}.jpg`)?`url(data:image/jpeg;base64,${fs.readFileSync(`${__dirname}/photo-${a.id}.jpg`).toString('base64')}) center/cover`:null;
const html=a=>{const ph=photo(a);const hl=a.big.replace(/<br>/g,' ').replace(/<span>/g,'<span style="color:#ffd23f">');
if(!ph) return `<style>@font-face{font-family:A;src:url(data:font/woff2;base64,${FONT})}</style><div style="width:1080px;height:1350px;background:${a.bg};font-family:A;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:70px;box-sizing:border-box;gap:40px"><div style="font-size:60px;background:#fff;color:#111;align-self:flex-start;padding:10px 22px">${a.top}</div><div style="font-size:140px;line-height:1">${hl}</div><div style="background:#22c55e;border-radius:22px;font-size:64px;text-align:center;padding:26px">${a.cta}</div></div>`;
return `<style>@font-face{font-family:A;src:url(data:font/woff2;base64,${FONT})}</style>
<div style="width:1080px;height:1350px;position:relative;overflow:hidden;font-family:A;color:#fff;background:#111">
<div style="position:absolute;left:0;right:0;top:470px;bottom:0;background:${ph}"></div>
<div style="position:absolute;left:0;right:0;top:0;height:520px;background:#111;clip-path:polygon(0 0,100% 0,100% 88%,0 100%)"></div>
<div style="position:absolute;left:56px;right:56px;top:46px">
<div style="font-size:54px;background:#ffd23f;color:#111;display:inline-block;padding:6px 20px;transform:rotate(-1.5deg)">${a.top}</div>
<div style="font-size:${hl.replace(/<[^>]+>/g,'').length>32?96:112}px;line-height:1.02;margin-top:22px;text-transform:uppercase">${hl}</div></div>
<div style="position:absolute;left:56px;right:56px;bottom:96px;background:#22c55e;border:4px solid #bbf7d0;border-radius:22px;font-size:62px;text-align:center;padding:22px;box-shadow:0 10px 0 #15803d">${a.cta}</div>
<div style="position:absolute;left:0;right:0;bottom:34px;text-align:center;font-family:Arial;font-size:26px;color:#fff;text-shadow:0 2px 6px #000">${a.foot}</div>
</div>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const a of ads){await p.setContent(html(a));await p.screenshot({path:`ad-${a.id}.png`});}
await b.close();})();
