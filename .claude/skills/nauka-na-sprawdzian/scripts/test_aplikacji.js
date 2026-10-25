// Automatyczny test zbudowanej aplikacji. Użycie: node test_aplikacji.js plik.html
// Wymaga jsdom:  cd /tmp && npm i jsdom@24  (uruchamiaj z NODE_PATH=/tmp/node_modules)
const fs=require('fs');const {JSDOM}=require('jsdom');
const html=fs.readFileSync(process.argv[2],'utf8');
const errs=[];
const dom=new JSDOM(html,{runScripts:'dangerously',pretendToBeVisual:true,url:'https://test.local/'});
const w=dom.window;w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};w.confirm=()=>true;
w.Element.prototype.getBoundingClientRect=function(){return {left:0,top:0,width:100,height:100,right:100,bottom:100};};
w.addEventListener('error',e=>errs.push('Błąd JS: '+e.message));
setTimeout(()=>{
  const A=w.__app;if(!A){console.log('❌ Aplikacja się nie uruchomiła',errs);process.exit(2);}
  const $=s=>w.document.querySelector(s);
  // 1. Każda poprawna odpowiedź musi zostać przyjęta, każda z listy „zle” – odrzucona
  A.Q.forEach((q,i)=>{
    const id=`pytanie ${i} „${(q.q||q.b||'').slice(0,60)}”`;
    if(q.t==='in'){q.a.forEach(a=>{if(!A.judge(a,q.a,q).ok)errs.push(id+': nie przyjmuje „'+a+'”');});
      (q.zle||[]).forEach(z=>{if(A.judge(z,q.a,q).ok)errs.push(id+': przyjmuje błędne „'+z+'”');});}
    if(q.t==='num'){[].concat(q.a).forEach(a=>{const s=String(a).replace('.',',');if(!A.judgeNum(s,q).ok)errs.push(id+': nie przyjmuje liczby '+s);});}
    if(q.t==='multi')q.pola.forEach(f=>{[].concat(f.a).forEach(a=>{const r=f.num?A.judgeNum(String(a).replace('.',','),f):A.judge(a,[].concat(f.a),Object.assign({},q,f));if(!r.ok)errs.push(id+': pole „'+f.l+'” nie przyjmuje „'+a+'”');});});
  });
  // 2. Każde pytanie musi się wyrenderować
  A.Q.forEach((q,i)=>{try{w.eval(`R={mode:'test',ids:[${JSON.stringify(q._id)}],res:[]};show('quiz');renderQ();`);
    if(!$('#qText').textContent.trim()&&q.t!=='gap')errs.push(`pytanie ${i}: pusta treść`);
    if(!$('#qBody').children.length)errs.push(`pytanie ${i}: brak pola odpowiedzi`);}catch(e){errs.push(`pytanie ${i}: ${e.message}`);}});
  // 3. Pełny test „na chybił trafił” + powtórka błędów + fiszki
  try{
    w.eval("S.cur=null;S.errors=[];renderHome();");$('#goTest').click();
    for(let k=0;k<A.CFG.liczbaPytan&&!$('#quiz').hidden;k++){const b=$('#qBody');const o=b.querySelector('.opts .opt');
      if(o)o.click();else{const sp=b.querySelector('.spot img');if(sp)sp.dispatchEvent(new w.MouseEvent('click',{clientX:50,clientY:50,bubbles:true}));b.querySelectorAll('input').forEach(x=>x.value='xyz');b.querySelectorAll('.word').forEach((x,j)=>{if(j<1)x.click();});
        b.querySelectorAll('select').forEach(x=>x.value=x.options[1].value);let g=0;while(b.querySelector('.pool .opt')&&g++<50)b.querySelector('.pool .opt').click();$('#qActions button').click();}
      $('#qActions button').click();}
    if($('#result').hidden)errs.push('Test nie doszedł do ekranu wyniku');
    if(!$('#rReview').disabled){$('#rReview').click();if($('#quiz').hidden)errs.push('Powtórka błędów się nie otwiera');}
    $('[data-home]').click();if(A.CARDS.length){$('#goCards').click();if(!$('#cardsPick').hidden)$('#pickList button').click();if($('#cards').hidden&&$('#cardsDone').hidden)errs.push('Fiszki się nie otwierają');$('#cYes').click();}
  }catch(e){errs.push('Przebieg testu: '+e.message);}
  if(errs.length){console.log('❌ Problemy ('+errs.length+'):');errs.slice(0,60).forEach(e=>console.log(' - '+e));process.exit(2);}
  console.log(`✅ Test OK: ${A.Q.length} pytań i ${A.CARDS.length} fiszek – wszystko się wyświetla, poprawne odpowiedzi są przyjmowane.`);
  process.exit(0);
},400);
