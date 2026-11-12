/* ============================================================
   CONFIG — edit these values to go live. Nothing else needs changing.
   ============================================================ */
const CONFIG = {
  brand: "GoodBuy Foods Global",
  whatsappNumber: "8801700000000",        // international format, digits only
  whatsappDisplay: "+880 1700-000000",
  email: "sales@goodbuyfoodsglobal.com",
  messengerPage: "goodbuyfoodsglobal",       // facebook page username for m.me links
  // n8n production webhook URLs (Webhook node → "Production URL").
  // Leave empty to run the site in demo mode (form shows success locally).
  rfqWebhook: "",                          // e.g. https://n8n.yourdomain.com/webhook/gfg-rfq
  eventsWebhook: "",                       // e.g. https://n8n.yourdomain.com/webhook/gfg-events
  supplierWebhook: "",                     // e.g. https://n8n.yourdomain.com/webhook/gfg-supplier
};

/* ---------- Helpers ---------- */
const $ = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => [...r.querySelectorAll(s)];
const store = { get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}}, set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}} };
const STILL = matchMedia("(prefers-reduced-motion: reduce)").matches;
function toast(msg){const t=$("#toast");if(!t)return;t.textContent=msg;t.hidden=false;clearTimeout(toast._t);toast._t=setTimeout(()=>t.hidden=true,2600)}
const qs = new URLSearchParams(location.search);
const utm = store.get("oc_utm") || {};
["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"].forEach(k=>{if(qs.get(k))utm[k]=qs.get(k)});
store.set("oc_utm",utm);   // keep first-touch campaign across pages
const visitorId = store.get("oc_vid") || ("v_"+Math.random().toString(36).slice(2,10)+Date.now().toString(36)); store.set("oc_vid",visitorId);

/* ---------- Visitor events → n8n (consent-gated) ---------- */
let consent = store.get("oc_consent");
function track(event, data={}){
  if(consent!=="yes" || !CONFIG.eventsWebhook) return;
  const body = JSON.stringify({event, data, visitorId, page:location.pathname+location.hash, referrer:document.referrer||null, utm, lang:navigator.language, ts:new Date().toISOString()});
  try{ if(navigator.sendBeacon) navigator.sendBeacon(CONFIG.eventsWebhook, new Blob([body],{type:"text/plain"})); else fetch(CONFIG.eventsWebhook,{method:"POST",body,keepalive:true}); }catch(e){}
}
if($("#cookie")){
  if(consent==null) $("#cookie").hidden=false;
  $("#ckYes").onclick=()=>{consent="yes";store.set("oc_consent","yes");$("#cookie").hidden=true;track("page_view")};
  $("#ckNo").onclick=()=>{consent="no";store.set("oc_consent","no");$("#cookie").hidden=true};
}
if(consent==="yes") track("page_view");

/* ---------- Brand, nav & channel links ---------- */
$$("[data-brand]").forEach(e=>e.textContent=CONFIG.brand);
$$("[data-year]").forEach(e=>e.textContent=new Date().getFullYear());
$$("[data-wa]").forEach(a=>{a.href="https://wa.me/"+CONFIG.whatsappNumber+"?text="+encodeURIComponent(a.dataset.wa);a.target="_blank";a.rel="noopener"});
$$('[data-show="whatsappDisplay"]').forEach(a=>a.textContent=CONFIG.whatsappDisplay);
$$("[data-messenger]").forEach(a=>{a.href="https://m.me/"+CONFIG.messengerPage;a.target="_blank";a.rel="noopener"});
$$('[data-show-text="messengerPage"]').forEach(s=>s.textContent=CONFIG.messengerPage);
$$("[data-mail]").forEach(a=>{a.href="mailto:"+CONFIG.email+"?subject="+encodeURIComponent("Seafood enquiry");if(!a.children.length)a.textContent=CONFIG.email});
document.addEventListener("click",e=>{const t=e.target.closest("[data-track]");if(t)track(t.dataset.track,{label:t.textContent.trim().slice(0,60)})});
const page=document.body.dataset.page;
$$("#nav a").forEach(a=>{if(a.dataset.nav===page)a.setAttribute("aria-current","page")});
if($("#menuBtn")){
  $("#menuBtn").onclick=function(){const o=$("#nav").classList.toggle("open");this.setAttribute("aria-expanded",o)};
  $$("#nav a").forEach(a=>a.addEventListener("click",()=>{$("#nav").classList.remove("open");$("#menuBtn").setAttribute("aria-expanded","false")}));
}

/* ---------- Ocean animation: waves, light rays, fish, bubbles ----------
   Any <canvas class="sea" data-level="0.66"> inside a .vid section.
   The deepest wave is the page colour, so each header melts into the page. */
function initSea(cv){
  const host=cv.parentElement, ctx=cv.getContext("2d"); if(!ctx) return;
  const L=parseFloat(cv.dataset.level||"0.66"), rays=cv.dataset.rays!=="off";
  let W=0,H=0,t=0,run=true,raf=0,fish=[],bubbles=[];
  const waves=[
    {y:L,     a:14,k:1.6,s:.35, c:"rgba(190,233,244,.55)", foam:true},
    {y:L+.07, a:18,k:1.1,s:-.25,c:"rgba(120,206,229,.45)"},
    {y:L+.15, a:13,k:2.0,s:.45, c:"rgba(223,243,248,.85)"},
    {y:L+.23, a:10,k:1.4,s:-.55,c:"rgb(245,251,253)"}];
  const newBubble=any=>({x:Math.random()*W,y:any?H*(L+Math.random()*(1-L)):H+10,r:1.5+Math.random()*4,v:.25+Math.random()*.7,ph:Math.random()*6});
  function resize(){const d=Math.min(devicePixelRatio||1,2);W=host.clientWidth;H=host.clientHeight;cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0);
    fish=Array.from({length:Math.max(4,Math.round(W/190))},(_,i)=>({x:Math.random()*W,y:H*(L+.09+Math.random()*.1),v:(.35+Math.random()*.6)*(i%3?1:-1),s:6+Math.random()*8,ph:Math.random()*6}));
    bubbles=Array.from({length:Math.round(W/45)},()=>newBubble(true));}
  const wy=(w,x)=>H*w.y+Math.sin(x/W*Math.PI*2*w.k+t*w.s)*w.a+Math.sin(x/W*Math.PI*6*w.k-t*w.s*1.7)*w.a*.3;
  function drawFish(f){const dir=Math.sign(f.v)||1,sw=Math.sin(t*6+f.ph)*.35,y=f.y+Math.sin(t*1.3+f.ph)*5;
    ctx.save();ctx.translate(f.x,y);ctx.scale(dir,1);ctx.fillStyle="rgba(11,80,108,.32)";
    ctx.beginPath();ctx.ellipse(0,0,f.s*1.6,f.s*.6,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.moveTo(-f.s*1.4,0);ctx.lineTo(-f.s*2.4,-f.s*(.6+sw));ctx.lineTo(-f.s*2.4,f.s*(.6-sw));ctx.closePath();ctx.fill();
    ctx.fillStyle="rgba(255,255,255,.75)";ctx.beginPath();ctx.arc(f.s*.9,-f.s*.12,f.s*.13,0,Math.PI*2);ctx.fill();ctx.restore();}
  function frame(){
    ctx.clearRect(0,0,W,H);
    if(rays){ctx.save();ctx.globalCompositeOperation="lighter";
      for(let i=0;i<6;i++){const x=W*(.08+i*.17)+Math.sin(t*.3+i)*40,g=ctx.createLinearGradient(0,H*L,0,H);g.addColorStop(0,"rgba(255,255,255,.2)");g.addColorStop(1,"rgba(255,255,255,0)");
        ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(x-18,H*L+6);ctx.lineTo(x+18,H*L+6);ctx.lineTo(x+90+Math.sin(t*.4+i)*30,H);ctx.lineTo(x-30+Math.sin(t*.4+i)*30,H);ctx.closePath();ctx.fill();}
      ctx.restore();}
    waves.forEach((w,i)=>{ctx.fillStyle=w.c;ctx.beginPath();ctx.moveTo(0,H);for(let x=0;x<=W+10;x+=10)ctx.lineTo(x,wy(w,x));ctx.lineTo(W,H);ctx.closePath();ctx.fill();
      if(w.foam){ctx.strokeStyle="rgba(255,255,255,.95)";ctx.lineWidth=2;ctx.beginPath();for(let x=0;x<=W+10;x+=10){const y=wy(w,x);x?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke();}
      if(i===1)fish.forEach(drawFish);});
    ctx.strokeStyle="rgba(255,255,255,.9)";ctx.lineWidth=1.2;
    bubbles.forEach(b=>{ctx.beginPath();ctx.arc(b.x+Math.sin(t*2+b.ph)*3,b.y,b.r,0,Math.PI*2);ctx.stroke();});}
  function step(){t+=.016;fish.forEach(f=>{f.x+=f.v;if(f.x>W+60)f.x=-60;if(f.x<-60)f.x=W+60});
    bubbles.forEach((b,i)=>{b.y-=b.v;if(b.y<H*L-10)bubbles[i]=newBubble(false)});
    if(bubbles.length>260)bubbles.splice(0,bubbles.length-260);
    frame();if(run)raf=requestAnimationFrame(step);}
  host.addEventListener("pointermove",e=>{if(STILL)return;const r=host.getBoundingClientRect();for(let i=0;i<2;i++)bubbles.push({x:e.clientX-r.left+(Math.random()-.5)*14,y:e.clientY-r.top,r:1.5+Math.random()*3,v:.6+Math.random()*.8,ph:Math.random()*6});});
  resize();addEventListener("resize",()=>{resize();if(STILL)frame()});
  if(STILL){frame();return}
  const go=v=>{if(v&&!run){run=true;step()}else if(!v){run=false;cancelAnimationFrame(raf)}};
  new IntersectionObserver(([en])=>go(en.isIntersecting&&!document.hidden)).observe(host);
  document.addEventListener("visibilitychange",()=>go(!document.hidden));
  step();
}
$$("canvas.sea").forEach(initSea);

/* ---------- Videos: play only while visible; lightbox on tiles ---------- */
const vids=$$("video[data-auto]");
if(STILL) vids.forEach(v=>{v.removeAttribute("autoplay");v.pause()});
else{
  const io=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target;if(e.isIntersecting){if(v.preload==="none")v.preload="auto";v.play().catch(()=>{})}else v.pause()}),{threshold:.2});
  vids.forEach(v=>{v.muted=true;io.observe(v)});
}
const lb=$("#lightbox");
if(lb){
  const lv=$("video",lb), lt=$("p",lb);
  const close=()=>{lv.pause();lv.removeAttribute("src");lv.load();lb.hidden=true;document.body.style.overflow=""};
  $$("[data-play]").forEach(b=>b.addEventListener("click",()=>{lv.src=b.dataset.play;lt.textContent=b.dataset.title||"";lb.hidden=false;document.body.style.overflow="hidden";lv.play().catch(()=>{});$(".close",lb).focus();track("video_play",{video:b.dataset.title})}));
  $(".close",lb).onclick=close;lb.addEventListener("click",e=>{if(e.target===lb)close()});
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!lb.hidden)close()});
}

/* ---------- Reefer readout (sample telemetry) ---------- */
if($("#reeferTemp")){let t=-20.1;setInterval(()=>{t=Math.max(-20.6,Math.min(-19.6,t+(Math.random()-.5)*.2));$("#reeferTemp").firstChild.nodeValue=(t<0?"−":"")+Math.abs(t).toFixed(1);$("#reeferHum").textContent=(85+Math.round(Math.random()*4))+" %"},3000)}

/* ---------- Product directory + quote basket (shared across pages) ---------- */
const CAT = window.CATALOG || {};
let basket = (store.get("oc_basket") || []).filter(id=>CAT[id]);
function syncButtons(){$$("[data-add]").forEach(b=>{const on=basket.includes(b.dataset.add);b.setAttribute("aria-pressed",on);b.textContent=on?"Added to quote":"Add to quote"})}
function renderBasket(){
  store.set("oc_basket",basket);
  $$("[data-basket-count]").forEach(e=>{e.textContent=basket.length;e.hidden=!basket.length});
  const b=$("#basket");if(b)b.innerHTML=basket.map(id=>`<span class="pill">${CAT[id].n}<button type="button" data-remove="${id}" aria-label="Remove ${CAT[id].n}">×</button></span>`).join("");
  syncButtons();
}
document.addEventListener("click",e=>{
  const a=e.target.closest("[data-add]");
  if(a){const id=a.dataset.add;if(basket.includes(id))basket=basket.filter(x=>x!==id);else{basket.push(id);toast(CAT[id].n+" added to your quote request");track("rfq_item_added",{product:id})}renderBasket()}
  const r=e.target.closest("[data-remove]");
  if(r){basket=basket.filter(x=>x!==r.dataset.remove);renderBasket()}
});
renderBasket();

const dir=$(".directory");
if(dir){
  let cat="all";const q=$("#dirSearch");
  const apply=()=>{
    const term=q.value.trim().toLowerCase();let shown=0;
    $$(".cat",dir).forEach(sec=>{let n=0;
      $$(".item",sec).forEach(it=>{const ok=(cat==="all"||it.dataset.cat===cat)&&(!term||it.dataset.search.includes(term));it.hidden=!ok;if(ok)n++});
      sec.hidden=!n;shown+=n});
    $("#dirCount").textContent=shown+(shown===1?" product":" products");$("#dirEmpty").hidden=!!shown;
  };
  $$(".chip[data-filter]").forEach(c=>c.onclick=()=>{$$(".chip[data-filter]").forEach(x=>x.setAttribute("aria-pressed","false"));c.setAttribute("aria-pressed","true");cat=c.dataset.filter;apply();track("catalogue_filter",{filter:cat})});
  let t;q.addEventListener("input",()=>{apply();clearTimeout(t);t=setTimeout(()=>q.value.trim()&&track("catalogue_search",{q:q.value.trim().slice(0,60)}),800)});
  if(location.hash.startsWith("#p-")){const el=document.getElementById(location.hash.slice(1));if(el)el.classList.add("flash")}
}

/* ---------- Lot trace (sample data) ---------- */
function trace(code){
  code=code.trim().toUpperCase();
  const out=$("#traceOut");
  if(!/^(GFG|OCN)-\d{2}-\d{3,5}$/.test(code)){out.innerHTML=`<li class="nodot">Lot codes look like <span class="mono">GFG-26-1187</span>. Check the carton side label.</li>`;return}
  const n=parseInt(code.slice(-4),10)||1187;
  const farms=["Shyamnagar, Satkhira","Mongla, Bagerhat","Paikgachha, Khulna","Chakaria, Cox's Bazar"];
  out.innerHTML=[
    ["14 Sep · 05:40","Harvested", farms[n%4]+" · pond BD-"+(1000+n%900)+" · iced at 2.1 °C"],
    ["14 Sep · 09:15","Received at plant","Core 3.4 °C · graded 16/20 · 1,940 kg"],
    ["14 Sep · 16:30","Lab release","Nitrofurans, CAP: not detected · TPC within limit"],
    ["15 Sep · 02:10","Plate frozen","Core −18.6 °C · 6 × 1.8 kg block · glaze 10 %"],
    ["22 Sep · 11:00","Loaded","Reefer set −20 °C · seal OC"+(400000+n)],
  ].map(([t,h,d])=>`<li><time>${t}</time><b>${h}</b><br>${d}</li>`).join("")+`<li class="nodot"><span class="sample-tag">Sample trace for demonstration</span></li>`;
  track("lot_trace",{code});
}
if($("#traceForm")){$("#traceForm").onsubmit=e=>{e.preventDefault();trace($("#lot").value)};trace("GFG-26-1187")}

/* ---------- Reefer load planner ---------- */
if($("#calc")){
  const CONT={"40":{vol:67.5,payload:29000,name:"40′ RHC"},"20":{vol:28.3,payload:27000,name:"20′ RF"}};
  const PACK={block:{net:10.8,gross:11.8,vol:.0305},iqf:{net:10,gross:11,vol:.031},bulk:{net:20,gross:21,vol:.05},fish:{net:20,gross:21.5,vol:.052}};
  const calc=()=>{const c=CONT[$("#cContainer").value],p=PACK[$("#cPack").value];
    const cartons=Math.min(Math.floor(c.vol*.88/p.vol),Math.floor(c.payload/p.gross)),net=cartons*p.net/1000;
    $("#oCartons").textContent=cartons.toLocaleString("en-US");$("#oNet").textContent=net.toFixed(1);$("#oPallets").textContent=$("#cContainer").value==="40"?"20":"10";
    return {container:c.name,pack:$("#cPack").selectedOptions[0].text,cartons,netMT:+net.toFixed(1)}};
  ["#cContainer","#cPack"].forEach(s=>$(s).addEventListener("change",()=>track("load_planner",calc())));
  calc();
  $("#calcToRfq").onclick=()=>{const r=calc(),d=store.get("oc_draft")||{};
    d.details=(d.details?d.details+"\n":"")+`Load plan: ${r.container}, ${r.pack}, ~${r.cartons} cartons / ${r.netMT} MT net.`;
    store.set("oc_draft",d);location.href="contact.html#rfq"};
}

/* ---------- RFQ submit → n8n ---------- */
const form=$("#rfqForm");
if(form){
  const status=$("#rfqStatus");
  const draft=store.get("oc_draft");
  draft && Object.entries(draft).forEach(([k,v])=>{const el=form.elements[k];if(el&&el.type!=="checkbox"&&!el.value)el.value=v});
  form.addEventListener("input",()=>{const d={};["company","name","email","whatsapp","country","port","details"].forEach(k=>d[k]=form.elements[k].value);store.set("oc_draft",d)});
  let started=false;form.addEventListener("focusin",()=>{if(!started){started=true;track("rfq_started")}});
  const showStatus=(m,err)=>{status.textContent=m;status.hidden=false;status.classList.toggle("err",!!err)};
  form.addEventListener("submit",async e=>{
    e.preventDefault();status.hidden=true;
    const missing=["company","name","email","country"].filter(k=>!form.elements[k].value.trim());
    if(missing.length){showStatus("Please fill in "+missing.join(", ")+".",true);form.elements[missing[0]].focus();return}
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.elements.email.value.trim())){showStatus("That email address looks incomplete. Check it and try again.",true);form.elements.email.focus();return}
    if(!form.elements.consent.checked){showStatus("Tick the consent box so we can store your request and reply.",true);return}
    if(form.elements.website.value)return; // honeypot
    const fd=Object.fromEntries(new FormData(form));delete fd.website;
    const payload={...fd,consent:true,products:basket.map(id=>({id,name:CAT[id].n,hs:CAT[id].hs,category:CAT[id].c})),
      source:"website",visitorId,utm,page:location.href,submittedAt:new Date().toISOString()};
    const btn=$("#rfqSubmit");btn.disabled=true;btn.textContent="Sending…";
    try{
      let j;
      if(!CONFIG.rfqWebhook){await new Promise(r=>setTimeout(r,600));j={ref:"DEMO-"+Date.now().toString().slice(-6),demo:true}}
      else{const res=await fetch(CONFIG.rfqWebhook,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});if(!res.ok)throw new Error("HTTP "+res.status);j=await res.json().catch(()=>({}))}
      showStatus(`Request received. Your reference is ${j.ref||"—"}. Check your inbox for the confirmation${form.elements.whatsapp.value?" and WhatsApp":""}.${j.demo?" (Demo mode: connect the n8n webhook in CONFIG to go live.)":""}`);
      basket=[];renderBasket();store.set("oc_draft",null);form.reset();
    }catch(err){showStatus("We couldn't send your request just now. Message us on WhatsApp or email "+CONFIG.email+" and we'll reply today.",true)}
    finally{btn.disabled=false;btn.textContent="Send quote request"}
  });
}

/* ---------- Supplier application → n8n ---------- */
const sf=$("#supplierForm");
if(sf){
  const st=$("#supplierStatus"),show=(m,err)=>{st.textContent=m;st.hidden=false;st.classList.toggle("err",!!err)};
  sf.addEventListener("submit",async e=>{
    e.preventDefault();st.hidden=true;
    const miss=["company","name","phone","email"].filter(k=>!sf.elements[k].value.trim());
    if(miss.length){show("Please fill in "+miss.join(", ")+".",true);sf.elements[miss[0]].focus();return}
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(sf.elements.email.value.trim())){show("That email address looks incomplete. Check it and try again.",true);return}
    if(!sf.elements.consent.checked){show("Tick the confirmation box to submit your application.",true);return}
    if(sf.elements.website.value)return;
    const fd=new FormData(sf),data=Object.fromEntries(fd);delete data.website;
    data.categories=fd.getAll("categories");data.approvals=fd.getAll("approvals");
    Object.assign(data,{source:"website",visitorId,utm,submittedAt:new Date().toISOString()});
    const btn=$("#supplierSubmit");btn.disabled=true;btn.textContent="Submitting…";
    try{
      let j;
      if(!CONFIG.supplierWebhook){await new Promise(r=>setTimeout(r,600));j={ref:"SUP-DEMO-"+Date.now().toString().slice(-5),demo:true}}
      else{const res=await fetch(CONFIG.supplierWebhook,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});if(!res.ok)throw new Error();j=await res.json().catch(()=>({}))}
      show(`Application received (reference ${j.ref||"—"}). We will review it and call you within 3 working days.${j.demo?" (Demo mode: connect the n8n webhook in CONFIG to go live.)":""}`);
      sf.reset();track("supplier_applied",{district:data.district});
    }catch(err){show("We couldn't submit your application just now. Please WhatsApp or email us instead.",true)}
    finally{btn.disabled=false;btn.textContent="Submit application"}
  });
}

/* ---------- Landed cost & margin calculator ---------- */
if($("#landed")){
  const v=id=>parseFloat($(id).value)||0, usd=n=>(n<0?"−$":"$")+Math.abs(Math.round(n)).toLocaleString("en-US");
  const calc=()=>{
    const kg=v("#lKg"),fob=v("#lFob")*kg,cfr=fob+v("#lFreight"),ins=cfr*.003,cif=cfr+ins,duty=cif*v("#lDuty")/100;
    const landed=cif+duty+v("#lLocal"),perKg=kg?landed/kg:0,rev=v("#lSell")*kg,profit=rev-landed,m=rev?profit/rev*100:0;
    $("#lLanded").textContent=perKg?perKg.toFixed(2):"—";$("#lMargin").textContent=rev?m.toFixed(1)+" %":"—";$("#lProfit").textContent=rev?usd(profit):"—";
    $("#lMargin").style.color=m<0?"var(--coral-ink)":"";
    return {fob:v("#lFob"),kg,landed:+perKg.toFixed(2),margin:+m.toFixed(1),sell:v("#lSell")};
  };
  $$("#landed input").forEach(i=>i.addEventListener("input",calc));calc();
  let tracked=false;$("#landed").addEventListener("change",()=>{if(!tracked){tracked=true;track("landed_cost_calc",calc())}});
  $("#landedToRfq").onclick=()=>{const r=calc(),d=store.get("oc_draft")||{};
    d.details=(d.details?d.details+"\n":"")+`Target: landed US$${r.landed}/kg (FOB US$${r.fob}/kg, ${r.kg} kg), selling at US$${r.sell}/kg for ${r.margin}% gross margin.`;
    store.set("oc_draft",d);location.href="contact.html#rfq"};
}

/* ---------- Preselect service package from ?package= ---------- */
(function(){const sel=$("#servicePackage");if(!sel)return;const pk=qs.get("package");if(pk&&[...sel.options].some(o=>o.value===pk))sel.value=pk})();
