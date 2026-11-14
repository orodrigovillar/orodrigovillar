const { chromium } = require('playwright');
const fs=require('fs');
const jobs = JSON.parse(process.argv[2]);
(async () => {
  const b = await chromium.launch();
  const out=[];
  await Promise.all(jobs.map(async ([q,country])=>{
    const p = await b.newPage({ locale: 'en-US', viewport:{width:1280,height:2000} });
    const url = `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=${country}&q=${encodeURIComponent(q)}&search_type=keyword_unordered&media_type=all`;
    try{
      await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await p.waitForTimeout(7000);
      for (let i=0;i<6;i++){ await p.mouse.wheel(0,4000); await p.waitForTimeout(2000); }
      const t = await p.evaluate(()=>document.body.innerText);
      const total = (t.match(/~?([\d,\.]+K?) results/)||[])[1]||'?';
      const blocks = t.split(/\n\s*Active\s*\n\s*Library ID: /).slice(1).map(s=>{
        const id=s.split('\n')[0].trim();
        const start=(s.match(/Started running on ([A-Za-z]+ \d+, \d{4})/)||[])[1];
        const n=(s.match(/(\d+) ads use this/)||[])[1]||'1';
        const m=s.match(/See (?:ad|summary) details\s*\n\s*(.+?)\n\s*Sponsored\s*\n([\s\S]*)/);
        const adv=m?m[1].trim():'';
        let body=m?m[2]:'';
        const dom=(body.match(/\n([A-Z0-9\-]+\.[A-Z\.]{2,})\n/)||[])[1]||'';
        body=body.split(/Sorry, we're having|\n(?:Learn more|Shop now|Sign up|Download|Get offer|Order now)\n/)[0].replace(/\s+/g,' ').trim().slice(0,600);
        return {id,start,n:+n,adv,dom,body};
      });
      out.push({q,country,total,ads:blocks});
    }catch(e){ out.push({q,country,err:String(e).slice(0,200)}); }
    await p.close();
  }));
  fs.writeFileSync(process.argv[3], JSON.stringify(out,null,1));
  await b.close();
})();
