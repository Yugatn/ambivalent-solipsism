window.addEventListener("error",e=>{const el=document.getElementById("validation");if(el)el.innerHTML='<span class="bad">JavaScript error:</span> '+esc(e.message||"unknown error")+'<br><span class="small muted">Проверьте консоль браузера и версию demo.js.</span>';},{passive:true});
window.addEventListener("unhandledrejection",e=>{const el=document.getElementById("validation");if(el)el.innerHTML='<span class="bad">Ошибка загрузки/вычисления:</span> '+esc(e.reason?.message||String(e.reason||"unknown rejection"));},{passive:true});

const CODE_TIPS={
 N:"Nω · число событий категории.",
 T:"Tω · объединённая длительность интервалов категории; перекрытия внутри категории не удваиваются.",
 S:"Sω · абсолютная screen-time share = Tω / T. Это не viewer exposure.",
 C:"Cω · покрытие релевантных shots. Низкое покрытие ограничивает вывод об отсутствии.",
 "ρevents":"ρevents · плотность событий: Nω / (T / 60).",
 "ρtime":"ρtime · плотность времени: Tω / (T / 60).",
 R:"Rω · повторяемость относительно числа narrative units / scenes.",
 confidence:"confidence · уверенность кодирования или интерпретации; не вероятность эффекта.",
 constructive:"Constructive · полярность кодбука, а не научный вердикт.",
 destructive:"Destructive · полярность кодбука, не доказанный вред аудитории.",
 unknown:"Unknown · данных недостаточно для утверждения отсутствия.",
 ambiguous:"Ambiguous · наблюдение есть, но уверенность ниже порога.",
 L4:"L4 · интерпретационная гипотеза. Не доказывает изменение установки у зрителя.",
 life_orientation:"life_orientation · ось сохранения/укрепления жизни ↔ сокращения жизни.",
 cognitive_orientation:"cognitive_orientation · ось развития мышления/творчества ↔ блокировки/пассивности."
};
function tip(code){const t=CODE_TIPS[code]||("Описание для "+code+" находится в текущей онтологии.");return '<button type="button" class="code-tip" data-tip="'+String(t).replace(/"/g,"&quot;")+'" aria-label="'+String(t).replace(/"/g,"&quot;")+'">?</button>'}
function initCodeTips(){
 document.querySelectorAll(".code-tip").forEach(el=>{el.addEventListener("click",e=>{e.stopPropagation();const open=el.classList.contains("tip-open");document.querySelectorAll(".code-tip.tip-open").forEach(x=>x.classList.remove("tip-open"));if(!open)el.classList.add("tip-open")});el.addEventListener("keydown",e=>{if(e.key==="Escape")el.classList.remove("tip-open")})});
 document.addEventListener("click",e=>{if(!e.target.closest(".code-tip"))document.querySelectorAll(".code-tip.tip-open").forEach(x=>x.classList.remove("tip-open"))},{passive:true});
}

const C=["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10"], palette=["#58d6ff","#ff647c","#ffb454","#72e0a5","#bd8cff","#67a8ff","#ff77b7","#ff8d5c","#6ee7d0","#aab4c8"];let data=null,selected="ALL",selectedSet=new Set(),metric="share",wheelMode="absolute",passport=null;
const C_MIN=0.95, VERSIONS={ontology:"0.3.0",model:"demo-0.6",schema:"input-0.1",measurement:"CM-0.6",attitudes:"attitudes-0.1"};
const $=s=>document.querySelector(s),fmt=(x,d=1)=>Number(x).toFixed(d);
function duration(e){return Math.max(0,Number(e.end)-Number(e.start))}
function validate(d){const errors=[];const T=Number(d?.work?.duration_seconds);if(!d||typeof d!=="object")errors.push("JSON должен быть объектом.");if(!d?.work?.id||!d?.work?.title)errors.push("work.id и work.title обязательны.");if(!(Number(d?.work?.duration_seconds)>0))errors.push("work.duration_seconds должен быть > 0.");if(!Array.isArray(d?.events))errors.push("events должен быть массивом.");(d?.events||[]).forEach((e,i)=>{if(!e.id)errors.push("events["+i+"]: отсутствует id");if(!C.includes(e.class))errors.push("events["+i+"]: неизвестный class "+e.class);if(!(Number(e.end)>Number(e.start)&&Number(e.start)>=0&&Number(e.end)<=T))errors.push("events["+i+"]: interval must satisfy 0 ≤ start < end ≤ duration");if(e.confidence!==undefined&&!(Number(e.confidence)>=0&&Number(e.confidence)<=1))errors.push("events["+i+"].confidence: must be 0..1");if(!["present","absent","unknown","ambiguous","not_applicable"].includes(e.status))errors.push("events["+i+"]: некорректный status")});if(!(Number(d?.coverage?.temporal)>=0&&Number(d?.coverage?.temporal)<=1))errors.push("coverage.temporal должен быть 0..1");return errors}
function unionLength(es){const a=es.map(e=>[Number(e.start),Number(e.end)]).sort((x,y)=>x[0]-y[0]);let total=0,s=null,e=null;for(const p of a){if(s===null){s=p[0];e=p[1]}else if(p[0]<=e)e=Math.max(e,p[1]);else{total+=e-s;s=p[0];e=p[1]}}return s===null?0:total+e-s}
function effectiveStatus(row){if(row.N<=0)return row.coverage>=C_MIN?"absent":"unknown";if(row.mean_confidence<0.5)return "ambiguous";return "present"}
function metrics(){const T=data.work.duration_seconds;const shotTotal=Number(data.work.shot_count)||0;const sceneTotal=Number(data.work.scene_count)||0;const rows=Object.fromEntries(C.map(c=>{const es=data.events.filter(e=>e.class===c&&e.status==="present"),t=unionLength(es),n=es.reduce((a,e)=>a+(Number(e.membership??e.p??1)||0),0);return[c,{N:n,T:t,share:t/T,event_density:n/(T/60),covered_time_density:t/(T/60),coverage:shotTotal?new Set(es.map(e=>e.shot_id).filter(Boolean)).size/shotTotal:data.coverage.temporal,repeatability:sceneTotal?n/sceneTotal:0,mean_confidence:es.length?es.reduce((a,e)=>a+(Number(e.confidence??1)||0),0)/es.length:1}]}));Object.values(rows).forEach(x=>x.status=effectiveStatus(x));return rows}
function contextStats(){const es=data.events.filter(e=>e.status==="present");const dur=es.map(e=>duration(e));const below=es.filter(e=>duration(e)*1000<(data.analysis_parameters?.perceptual_min_ms??120)).length;const byContext={};for(const e of es){for(const [k,v] of Object.entries(e.context_observed||{})){if(k==="scene_id"||k==="shot_id")continue;if(!byContext[k])byContext[k]={};byContext[k][v]=(byContext[k][v]||0)+1}}return{presentEvents:es.length,sceneCount:Number(data.work.scene_count)||new Set(es.map(e=>e.scene_id).filter(Boolean)).size,shotCount:Number(data.work.shot_count)||new Set(es.map(e=>e.shot_id).filter(Boolean)).size,subPerceptual:below,minMs:data.analysis_parameters?.perceptual_min_ms??120,context:byContext};}
const DEMO_ATTITUDES=[["A01",720,795,.86,"уважение достоинства и границ другого человека","наблюдаемый диалог и реакция персонажей"],["A04",720,795,.82,"совместное решение задач","совместное решение конфликта"],["A19",1450,1510,.9,"ответственное выполнение работы","добросовестное выполнение работы"],["A21",1450,1510,.8,"дисциплина и контроль поведения","дисциплина персонажа"],["A03",1780,1870,.88,"помощь и взаимопомощь","помощь другому персонажу"],["A17",1780,1870,.84,"поддержка близкого","поддержка близкого"],["A33",2360,2440,.91,"положительная или нормализующая рамка алкоголя","положительная рамка употребления алкоголя"],["A71",2360,2440,.72,"потребление как социальный статус","потребление связано со статусом"],["A39",2700,2860,.86,"агрессия как допустимое решение","агрессивное разрешение конфликта"],["A47",2700,2860,.78,"месть как ответ","месть представлена как ответ"],["A16",3140,3200,.75,"уважение границ и согласие","согласие и личные границы"],["A40",3480,3575,.7,"обобщённая враждебность к незнакомым","враждебность к незнакомцам"],["A38",3820,3940,.79,"опасный риск как привлекательный","риск представлен как привлекательный"],["A20",4200,4305,.86,"профессиональная ответственность","профессиональная ответственность"],["A11",4510,4580,.9,"укрепление семейной связи","поддержание семейной связи"],["A12",4510,4580,.83,"уважение родителей и старших","уважение старшего родственника"],["A28",4820,4900,.76,"положительная рамка здорового питания","позитивная рамка здорового питания"],["A62",5120,5200,.65,"эмоциональное подавление","эмоциональное подавление как социальная норма"]].map(x=>({id:x[0],start:x[1],end:x[2],confidence:x[3],basis:x[5],label:x[4]}));
function attitudeRows(){
 const T=data.work.duration_seconds;
 const obs=Array.isArray(data.attitude_observations)?data.attitude_observations:DEMO_ATTITUDES;
 const by={};
 for(const o of obs){if(!by[o.category])by[o.category]=[];by[o.category].push(o)}
 const ontology=data.attitude_ontology||window.ATTITUDE_ONTOLOGY||{items:[]};
 return (ontology.items||[]).map(item=>{const es=by[item.id]||[], t=unionLength(es), share=t/T, conf=es.length?es.reduce((a,e)=>a+Number(e.confidence??1),0)/es.length:null; return {...item,N:es.length,T:t,share,confidence:conf,status:es.length?(conf<.5?"ambiguous":"hypothesis"):"unknown",observations:es}}); 
}
function renderAttitudeEvidence(row){
 const el=document.getElementById("attitudeEvidence");
 if(!el)return;
 if(!row){el.innerHTML="<div class='muted small'>Выберите установку в таблице для просмотра evidence trace.</div>";return;}
 let html="<h3>"+esc(row.label)+" · "+fmt(row.share*100,3)+"%</h3><div class='small muted'>L4-гипотеза · "+esc(row.definition)+"</div>";
 if(!row.observations.length) html+="<div class='muted'>Нет кодированных наблюдений.</div>";
 row.observations.forEach(o=>{html+="<div class='evidence-item'><b>"+esc(o.id||o.category||"observation")+"</b> · "+fmt(o.start,1)+"–"+fmt(o.end,1)+" s · duration "+fmt(o.end-o.start,1)+" s · confidence "+fmt(o.confidence,2)+"<br><span>"+esc(o.basis||"Основание не указано")+"</span><br><span class='small muted'>L3 context: "+esc(JSON.stringify(o.context_observed||{}))+"</span></div>";});
 el.innerHTML=html;
}
function renderSceneAnalysis(){
 const el=$("#sceneAnalysis"); if(!el||!data)return;
 const threshold=Number(data.analysis_parameters?.perceptual_min_ms??120);
 const scenes=Number(data.work.scene_count)||new Set(data.events.map(e=>e.scene_id).filter(Boolean)).size;
 const shots=Number(data.work.shot_count)||new Set(data.events.map(e=>e.shot_id).filter(Boolean)).size;
 const observedScenes=[...new Set(data.events.map(e=>e.scene_id).filter(Boolean))];
 const events=data.events.filter(e=>e.status==="present");
 const shortEvents=events.filter(e=>duration(e)*1000<threshold);
 const sceneRows=observedScenes.map(id=>{const es=events.filter(e=>e.scene_id===id);const start=Math.min(...es.map(e=>Number(e.start))),end=Math.max(...es.map(e=>Number(e.end)));return{id,start,end,duration:end-start,events:es.length,shots:new Set(es.map(e=>e.shot_id).filter(Boolean)).size};});
 el.innerHTML='<div class="grid"><div class="card"><div class="muted">Нарративных сцен</div><div class="metric">'+scenes+'</div><div class="small">единицы для Rω</div></div><div class="card"><div class="muted">Планов</div><div class="metric">'+shots+'</div><div class="small">единицы для Cω</div></div><div class="card"><div class="muted">Сцен с событиями</div><div class="metric">'+observedScenes.length+'</div><div class="small">по текущему Content Map</div></div><div class="card"><div class="muted">Событий ниже порога</div><div class="metric">'+shortEvents.length+'</div><div class="small">'+threshold+' ms · assumption</div></div></div><div class="notice small"><b>Параметр:</b> '+threshold+' ms. Он не называется «законом восприятия» и не доказывает отсутствие психофизиологического отклика. Для чувствительности сравните 120 и 240 ms.</div><div class="table-scroll"><table class="table"><tr><th>Сцена</th><th>Интервал</th><th>Длительность</th><th>События</th><th>Shots</th></tr>'+sceneRows.map(x=>'<tr><td><b>'+esc(x.id)+'</b></td><td>'+fmt(x.start,1)+'–'+fmt(x.end,1)+' s</td><td>'+fmt(x.duration,1)+' s</td><td>'+x.events+'</td><td>'+x.shots+'</td></tr>').join('')+'</table></div>';
}
function attitudePolarity(id){const g=Object.entries((data.attitude_ontology||window.ATTITUDE_ONTOLOGY||{}).groups||{}).find(([k,v])=>v.includes(id))?.[0]||"other";return ["risk_destructive","prejudice_stigma","mental_health_self_harm","antisocial","commercial_body_image"].includes(g)?"destructive":["prosocial","family_social","work_civic","health_constructive"].includes(g)?"constructive":"other"}
function renderCodeReference(){
 const el=$("#codeReference"); if(!el)return;
 const ontology=data?.attitude_ontology||window.ATTITUDE_ONTOLOGY||{items:[]};
 const items=ontology.items||[];
 const groups=(ontology.groups||{});
 const groupOf=id=>Object.entries(groups).find(([,ids])=>ids.includes(id))?.[0]||"other";
 const pol=id=>attitudeMeta().polarity[id]||"uncertain";
 el.innerHTML='<div class="code-reference-grid">'+items.map(x=>'<button class="code-reference-item" type="button" data-code="'+esc(x.id)+'"><b>'+esc(x.id)+'</b><span>'+esc(x.label||x.name||"")+'</span><i>'+pol(x.id)+'</i></button>').join("")+'</div>';
 el.querySelectorAll("[data-code]").forEach(b=>b.addEventListener("click",()=>{const id=b.dataset.code, row=attitudeRows().find(x=>x.id===id); if(row){renderAttitudeEvidence(row); document.querySelector(".attitude-row[data-attitude-id='"+id+"']")?.scrollIntoView({behavior:"smooth",block:"center"});}}));
}
function attitudeMeta(){
 const ont=data.attitude_ontology||window.ATTITUDE_ONTOLOGY||{items:[],groups:{}};
 const groups=ont.groups||{};
 const domainMap={
  prosocial:["social_relations","Просоциальные отношения"],
  family_social:["family_social","Семья и близкие"],
  work_civic:["work_civic","Труд, обучение и гражданские нормы"],
  health_constructive:["health_constructive","Здоровье и сохранение жизни"],
  risk_destructive:["risk_destructive","Риск, здоровье и поведенческие зависимости"],
  prejudice_stigma:["prejudice_stigma","Предубеждение, стигма и враждебность"],
  mental_health_self_harm:["mental_health_self_harm","Психическое здоровье и самоповреждение"],
  antisocial:["antisocial","Антисоциальные стратегии"],
  commercial_body_image:["commercial_body_image","Потребление, статус и образ тела"]
 };
 const polarity={};
 Object.entries(groups).forEach(([g,ids])=>ids.forEach(id=>polarity[id]=
   ["prosocial","family_social","work_civic","health_constructive"].includes(g)?"constructive":
   ["risk_destructive","prejudice_stigma","mental_health_self_harm","antisocial","commercial_body_image"].includes(g)?"destructive":"uncertain"));
 return {groups,domainMap,polarity};
}
function attitudeRows(){
 const T=data.work.duration_seconds, obs=Array.isArray(data.attitude_observations)?data.attitude_observations:DEMO_ATTITUDES;
 const by={}; for(const o of obs){if(!by[o.category])by[o.category]=[];by[o.category].push(o)}
 const meta=attitudeMeta();
 return (data.attitude_ontology?.items||window.ATTITUDE_ONTOLOGY?.items||[]).map(item=>{
   const es=by[item.id]||[], t=unionLength(es), conf=es.length?es.reduce((a,e)=>a+Number(e.confidence??1),0)/es.length:null;
   const group=Object.entries(meta.groups).find(([,ids])=>ids.includes(item.id))?.[0]||"other";
   const domain=meta.domainMap[group]?.[0]||"other";
   const polarity=meta.polarity[item.id]||"uncertain";
   const status=es.length?(conf<.5?"ambiguous":"hypothesis"):"unknown";
   return {...item,N:es.length,T:t,share:t/T,confidence:conf,status,group,domain,polarity,observations:es};
 });
}
function axisForAttitude(row){
 const cognitive={constructive:["A22","A77","A78","A79","A80","A81"],destructive:["A82","A83","A84","A85"]};
 const life={preserve:["A27","A28","A29","A30","A31","A32","A89","A91"],shorten:["A33","A34","A35","A36","A38","A59","A60","A88","A90"]};
 if(cognitive.constructive.includes(row.id))return ["cognitive_orientation","development"];
 if(cognitive.destructive.includes(row.id))return ["cognitive_orientation","blocking/passivity"];
 if(life.preserve.includes(row.id))return ["life_orientation","preservation/strengthening"];
 if(life.shorten.includes(row.id))return ["life_orientation","shortening"];
 return [null,null];
}
function renderAttitudeAxes(rows){
 const sum=(axis,val)=>rows.filter(r=>axisForAttitude(r)[0]===axis&&axisForAttitude(r)[1]===val).reduce((a,r)=>a+r.T,0);
 const pct=x=>fmt(x/data.work.duration_seconds*100,3);
 $("#attitudeAxes").innerHTML='<div class="card"><b>life_orientation</b><div class="small">Сохранение/укрепление: <b>'+pct(sum("life_orientation","preservation/strengthening"))+'%</b> · сокращение: <b>'+pct(sum("life_orientation","shortening"))+'%</b></div></div><div class="card"><b>cognitive_orientation</b><div class="small">Развитие мышления/творчества: <b>'+pct(sum("cognitive_orientation","development"))+'%</b> · блокировка/пассивность: <b>'+pct(sum("cognitive_orientation","blocking/passivity"))+'%</b></div></div>';
}
function renderAttitudes(){
 const rows=attitudeRows(), meta=attitudeMeta(), q=window.__attitudeFilter||{}, domain=q.domain||"ALL", polarity=q.polarity||"ALL", search=(q.search||"").trim().toLowerCase();
 const filtered=rows.filter(r=>(domain==="ALL"||r.domain===domain)&&(polarity==="ALL"||r.polarity===polarity)&&(!search||(r.label+" "+r.id+" "+r.definition).toLowerCase().includes(search)));
 const present=rows.filter(x=>x.N>0), constructive=present.filter(x=>x.polarity==="constructive").length, destructive=present.filter(x=>x.polarity==="destructive").length, unknown=rows.filter(x=>x.status==="unknown").length;
 $("#attitudeSummary").innerHTML='<div class="card"><div class="muted">L4-гипотез</div><div class="metric">'+rows.length+'</div><div class="small">кодбук attitudes-0.1</div></div><div class="card"><div class="muted">Constructive</div><div class="metric">'+constructive+'</div><div class="small">аналитическая полярность</div></div><div class="card"><div class="muted">Destructive</div><div class="metric">'+destructive+'</div><div class="small">аналитическая полярность</div></div><div class="card"><div class="muted">Unknown</div><div class="metric">'+unknown+'</div><div class="small">нет кодированного evidence</div></div>';
 renderAttitudeAxes(rows);
 let out='<div class="table-scroll"><table class="table"><tr><th>Domain</th><th>Program</th><th>Attitude hypothesis</th><th>Polarity</th><th>Status</th><th>N</th><th>Tω</th><th>Sω%</th><th>Cω</th><th>ρevents</th><th>ρtime</th><th>Rω</th><th>confidence</th></tr>';
 filtered.forEach(x=>{
   const cov=data.work.shot_count?new Set(x.observations.map(o=>o.shot_id).filter(Boolean)).size/data.work.shot_count:data.coverage.temporal;
   const rho=x.N/(data.work.duration_seconds/60), rhot=x.T/(data.work.duration_seconds/60), R=data.work.scene_count?x.N/data.work.scene_count:0;
   const groupLabel=meta.domainMap[x.group]?.[1]||"Другая область";
   const sameDomain=filtered.filter(y=>y.domain===x.domain).reduce((a,y)=>a+y.share,0);
   const selectedComp=sameDomain?x.share/sameDomain:0;
   const trace=x.observations.map(o=>'<div class="evidence-item"><b>'+esc(o.id||x.id)+'</b> · '+fmt(o.start,1)+'–'+fmt(o.end,1)+' s · scene '+esc(o.scene_id??"—")+' · shot '+esc(o.shot_id??"—")+' · event '+esc(o.event_id??o.id??"—")+'<br><span class="small">L3 observed_context: '+esc(JSON.stringify(o.context_observed||{}))+'</span><br><span class="small">L4 interpretation: '+esc(o.basis||x.definition)+'</span> · confidence '+fmt(o.confidence??x.confidence??0,2)+'</div>').join("");
   out+='<tr class="attitude-row" data-attitude-id="'+x.id+'"><td>'+esc(groupLabel)+'</td><td>'+esc(x.domain)+'</td><td><b>'+esc(x.label)+'</b><div class="small">'+esc(x.id)+'</div></td><td><span class="badge">'+x.polarity+'</span></td><td>'+esc(x.status)+'</td><td>'+x.N+'</td><td>'+fmt(x.T,1)+' s</td><td><b>'+fmt(x.share*100,3)+'%</b></td><td>'+fmt(cov*100,2)+'%</td><td>'+fmt(rho,3)+'/min</td><td>'+fmt(rhot,3)+' s/min</td><td>'+fmt(R,3)+'</td><td>'+(x.confidence===null?"—":fmt(x.confidence,2))+'</td></tr>';
   out+='<tr class="attitude-detail" id="attitude-detail-'+x.id+'" hidden><td colspan="13"><div class="card"><b>'+esc(x.label)+'</b><div class="small">Absolute Sω='+fmt(x.share*100,3)+'% · selected-area composition Pω^Ω*='+fmt(selectedComp*100,3)+'% · evidence count='+x.observations.length+'</div><div class="small">Uncertainty: measurement / annotation / segmentation / grouping; CI95 не оценивается для synthetic demo.</div><div style="margin-top:8px"><b>Evidence Trace</b>'+(trace||'<div class="muted small">Нет наблюдений.</div>')+'</div></div></td></tr>';
 });
 out+='</table></div><div class="notice small"><b>Граница интерпретации:</b> L4 — гипотеза, а не доказанный эффект аудитории. Constructive/Destructive — метаданные кодбука. Единого harm score нет. Процент Sω — доля времени контента, не viewer exposure.</div>';
 $("#attitudeProfile").innerHTML=out;
 document.querySelectorAll(".attitude-row").forEach(row=>row.addEventListener("click",()=>{const id=row.dataset.attitudeId,d=$("#attitude-detail-"+id);if(d)d.hidden=!d.hidden;renderAttitudeEvidence(rows.find(x=>x.id===id));}));
}
function aggregateArea(m,area){const T=data.work.duration_seconds;const cats=area.filter(c=>m[c]);const union=unionLength(data.events.filter(e=>cats.includes(e.class)&&e.status==="present"));const denom=cats.reduce((a,c)=>a+m[c].share,0);const probs=cats.map(c=>denom?m[c].share/denom:0);const H=probs.reduce((a,p)=>a+(p>0?-p*Math.log(p):0),0),Hn=cats.length>1?H/Math.log(cats.length):0;return{N:cats.reduce((a,c)=>a+m[c].N,0),T:union,S:union/T,internal_composition:Object.fromEntries(cats.map((c,i)=>[c,probs[i]])),diversity_index:H,diversity_index_norm:Hn}}

function esc(s){return String(s).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]))}
function drawBars(m){const W=760,H=300,p=45,max=Math.max(...C.map(c=>m[c][metric==="share"?"share":"N"]),.001),bar=(W-70)/10-8;let svg='<svg viewBox="0 0 760 300" class="chart">';C.forEach((c,i)=>{const v=m[c][metric==="share"?"share":"N"],h=(H-70)*v/max,x=p+i*((W-70)/10),y=H-35-h;svg+=`<rect data-class="${c}" tabindex="0" role="button" aria-label="${esc(c+" · "+fmt(v*100,2)+"%")}" x="${x}" y="${y}" width="${bar}" height="${h}" rx="5" fill="${palette[i]}" opacity="${selected==="ALL"||selected===c?1:.25}"/><text x="${x+bar/2}" y="${H-15}" fill="#9aa7ba" font-size="12" text-anchor="middle">${c}</text><text x="${x+bar/2}" y="${Math.max(18,y-5)}" fill="#e9eef8" font-size="11" text-anchor="middle">${metric==="share"?fmt(v*100)+"%":v}</text>`});return svg+"</svg>"}
function drawTimeline(){
 const W=760,p=42,T=data.work.duration_seconds,laneH=34,top=34,bottom=28;
 const visible=data.events.filter(e=>e.status==="present"&&(selected==="ALL"||e.class===selected));
 const laneClasses=selected==="ALL"?C:C.filter(c=>visible.some(e=>e.class===c));
 const H=Math.max(260,top+laneClasses.length*laneH+bottom);
 const scale=W-p-20;
 let svg='<svg viewBox="0 0 '+W+' '+H+'" class="chart timeline-chart" role="img" aria-labelledby="timelineTitle timelineDesc">';
 svg+='<title id="timelineTitle">Timeline событий</title><desc id="timelineDesc">Дорожки категорий, границы сцен и кликабельные события.</desc>';
 laneClasses.forEach((c,i)=>{
   const y=top+i*laneH;
   svg+='<line x1="'+p+'" y1="'+(y+18)+'" x2="'+(W-20)+'" y2="'+(y+18)+'" stroke="#263247"/>';
   svg+='<text x="6" y="'+(y+13)+'" fill="#e9eef8" font-size="11" font-weight="600">'+esc(c)+'</text>';
   svg+='<text x="6" y="'+(y+27)+'" fill="#718096" font-size="9">'+esc(data.ontology.classes[c]||"")+'</text>';
 });
 const sceneMap=new Map();
 visible.forEach(e=>{const sid=e.scene_id??e.context_observed?.scene_id;if(sid&&!sceneMap.has(String(sid)))sceneMap.set(String(sid),e.start)});
 [...sceneMap.entries()].sort((a,b)=>a[1]-b[1]).forEach(([sid,t])=>{
   const x=p+(t/T)*scale;
   svg+='<line x1="'+x+'" y1="10" x2="'+x+'" y2="'+(H-bottom)+'" stroke="#56657a" stroke-dasharray="3 4" opacity=".7"/>';
   svg+='<text x="'+(x+3)+'" y="20" fill="#8e9aad" font-size="9">'+esc(sid)+'</text>';
 });
 visible.forEach(e=>{
   const li=laneClasses.indexOf(e.class); if(li<0)return;
   const y=top+li*laneH;
   const x=p+(e.start/T)*scale,w=Math.max(5,(duration(e)/T)*scale);
   const active=selected==="ALL"||selected===e.class;
   const selectedEvent=window.__selectedEventId===String(e.id);
   svg+='<rect data-event-id="'+esc(e.id)+'" tabindex="0" role="button" aria-label="Событие '+esc(e.id)+', '+esc(e.class)+', '+fmt(e.start,2)+'–'+fmt(e.end,2)+' секунд" x="'+x+'" y="'+(y+4)+'" width="'+w+'" height="18" rx="4" fill="'+palette[C.indexOf(e.class)]+'" opacity="'+(selectedEvent?1:(active?.88:.35))+'" stroke="'+(selectedEvent?"#ffffff":"none")+'" stroke-width="'+(selectedEvent?2:0)+'"/>';
   if(w>34)svg+='<text x="'+(x+4)+'" y="'+(y+17)+'" font-size="9" fill="#061018">'+esc(e.id)+'</text>';
 });
 for(let k=0;k<=6;k++){
   const x=p+k*scale/6;
   svg+='<line x1="'+x+'" y1="'+(H-bottom)+'" x2="'+x+'" y2="'+(H-bottom+4)+'" stroke="#56657a"/>';
   svg+='<text x="'+x+'" y="'+(H-6)+'" fill="#8e9aad" font-size="10" text-anchor="middle">'+Math.round(T*k/6/60)+'m</text>';
 }
 return svg+"</svg>";
}
function drawDensity(){const bins=12,T=data.work.duration_seconds,b=T/bins,W=760,H=280,p=45;const counts=Array(bins).fill(0);data.events.forEach(e=>{if(e.status==="present"&&(selected==="ALL"||e.class===selected))counts[Math.min(bins-1,Math.floor(e.start/b))]++});const mx=Math.max(...counts,1),bw=(W-p-20)/bins-5;let svg='<svg viewBox="0 0 760 280" class="chart">';counts.forEach((n,i)=>{const h=190*n/mx,x=p+i*(bw+5),y=220-h;svg+=`<rect x="${x}" y="${y}" width="${bw}" height="${h}" rx="4" fill="#78e6b2"/><text x="${x+bw/2}" y="${y-5}" fill="#e9eef8" font-size="11" text-anchor="middle">${fmt(n/(b/60),2)}</text>`});return svg+"</svg>"}
function drawWheel(m){
 const cx=180,cy=180,r=42;
 const area=selectedSet.size?C.filter(c=>selectedSet.has(c)):C;
 const max=wheelMode==="absolute"?Math.max(...C.map(c=>m[c].share),.0001):Math.max(...area.map(c=>m[c].share),.0001);
 let svg='<svg viewBox="0 0 360 360" class="chart accessible-wheel" role="img" aria-labelledby="wheelTitle wheelDesc"><title id="wheelTitle">Content Wheel</title><desc id="wheelDesc">Радиальное сравнение screen-time share категорий C1–C10. Нажмите сегмент для подробностей.</desc>';
 C.forEach((c,i)=>{
   const a0=(i*36-90)*Math.PI/180,a1=((i+1)*36-90)*Math.PI/180,rr=42+(m[c].share/max)*108,x1=cx+rr*Math.cos(a0),y1=cy+rr*Math.sin(a0),x2=cx+rr*Math.cos(a1),y2=cy+rr*Math.sin(a1),ix1=cx+r*Math.cos(a0),iy1=cy+r*Math.sin(a0),ix2=cx+r*Math.cos(a1),iy2=cy+r*Math.sin(a1);
   const label=c+" · "+fmt(m[c].share*100,2)+"% · N="+fmt(m[c].N,2)+" · "+m[c].status;
   svg+='<path tabindex="0" role="button" aria-label="'+esc(label)+'" data-wheel-class="'+c+'" d="M'+ix1+' '+iy1+' L'+x1+' '+y1+' A'+rr+' '+rr+' 0 0 1 '+x2+' '+y2+' L'+ix2+' '+iy2+' A'+r+' '+r+' 0 0 0 '+ix1+' '+iy1+'Z" fill="'+palette[i]+'" opacity="'+(selected==="ALL"||selected===c?0.9:0.18)+'"/><text x="'+(cx+(rr+12)*Math.cos((a0+a1)/2))+'" y="'+(cy+(rr+12)*Math.sin((a0+a1)/2))+'" fill="#e9eef8" font-size="10" text-anchor="middle">'+c+'</text>';
 });
 svg+='<circle cx="'+cx+'" cy="'+cy+'" r="'+(r-2)+'" fill="#080b12"/><text x="'+cx+'" y="'+(cy-5)+'" fill="#e9eef8" font-size="12" text-anchor="middle">screen_time</text><text x="'+cx+'" y="'+(cy+13)+'" fill="#8e9aad" font-size="10" text-anchor="middle">share</text></svg>';
 return svg;
}
function renderInspector(eventId){
 const e=data.events.find(x=>String(x.id)===String(eventId)), el=$("#inspectorContent"); if(!el||!e)return;
 const m=metrics()[e.class]||{};
 const obs=e.context_observed||e.observed_context||{};
 const interp=e.interpretation||e.interpreted_context||null;
 const dur=Math.max(0,(e.end||0)-(e.start||0));
 el.innerHTML='<div class="inspector-head"><b>'+esc(String(e.id))+'</b><span>'+esc(String(e.class||"unknown"))+'</span></div>'+
 '<div class="inspector-grid"><div><small>Timestamp</small><b>'+fmt(e.start,3)+'–'+fmt(e.end,3)+' s</b></div><div><small>Δt</small><b>'+fmt(dur,3)+' s</b></div><div><small>Nω</small><b>'+fmt(m.N,2)+'</b></div><div><small>Sω</small><b>'+fmt(m.share*100,3)+'%</b></div><div><small>Confidence</small><b>'+fmt(e.confidence,3)+'</b></div><div><small>Status</small><b>'+esc(String(e.status||"unknown"))+'</b></div></div>'+
 '<div class="inspector-section"><b>Scene / Shot</b><br>Scene: '+esc(String(e.scene_id??e.scene??"unknown"))+' · Shot: '+esc(String(e.shot_id??e.shot??"unknown"))+'</div>'+
 '<div class="inspector-section"><b>L0–L2 · наблюдение</b><br>'+esc(String(e.description||e.label||"Событие зафиксировано в Content Map."))+'</div>'+
 '<div class="inspector-section"><b>L3 · observed_context</b><pre class="trace-json">'+esc(JSON.stringify(obs,null,2))+'</pre></div>'+
 '<div class="inspector-section"><b>L4 · interpretation</b><br>'+esc(interp?typeof interp==="string"?interp:JSON.stringify(interp,null,2):"Не задана")+'</div>';
}
function selectEvent(eventId){
 const e=data.events.find(x=>String(x.id)===String(eventId)); if(!e)return;
 selected=e.class; selectedSet=new Set([e.class]); openProgramGroups.add(e.class); window.__selectedEventId=String(eventId); window.__selectedSceneId=String(e.scene_id??e.context_observed?.scene_id??""); window.__selectedShotId=String(e.shot_id??e.context_observed?.shot_id??""); renderEvidenceNavigator(e);
 renderInspector(eventId);
 render();
 requestAnimationFrame(()=>{renderEvidenceTrace(eventId);document.getElementById("calculationTrace")?.scrollIntoView({behavior:"smooth",block:"center"});});
}
function renderEvidenceNavigator(e){
 const out=$("#evidenceNavigator"); if(!out)return;
 const scene=e.scene_id??e.context_observed?.scene_id??"unknown";
 const shot=e.shot_id??e.context_observed?.shot_id??"unknown";
 const phrase=e.phrase??e.quote??e.transcript_fragment??null;
 const sceneEvents=data.events.filter(x=>String(x.scene_id??x.context_observed?.scene_id??"")===String(scene)&&x.status==="present");
 const shotEvents=sceneEvents.filter(x=>String(x.shot_id??x.context_observed?.shot_id??"")===String(shot));
 const candidates=e.evidence_candidates||[];
 let candidateHtml=phrase?'<div class="evidence-candidate"><b>Phrase candidate</b><p>'+esc(String(phrase))+'</p><span class="muted small">candidate · source='+esc(String(e.media_source??"Content Map"))+'</span></div>':'<div class="evidence-candidate muted small">Phrase candidate: пока отсутствует.</div>';
 if(candidates.length) candidateHtml='<div class="candidate-list">'+candidates.map((c,n)=>'<div class="evidence-candidate"><b>Candidate '+(n+1)+'</b><p>'+esc(String(c.text??c.phrase??""))+'</p><span class="muted small">'+esc(String(c.review_status??"candidate"))+' · '+esc(String(c.start??e.start))+'–'+esc(String(c.end??e.end))+' s · confidence '+fmt(c.confidence,3)+'</span></div>').join("")+'</div>';
 out.innerHTML='<div class="evidence-path"><span>Scene '+esc(String(scene))+' · '+sceneEvents.length+' events</span><span>→</span><span>Shot '+esc(String(shot))+' · '+shotEvents.length+' events</span><span>→</span><span>Event '+esc(String(e.id))+'</span><span>→</span><span>Phrase</span></div>'+candidateHtml+'<div class="small muted">Timestamp: '+fmt(e.start,3)+'–'+fmt(e.end,3)+' s · confidence: '+fmt(e.confidence,3)+'</div>';
}function renderEvidenceTrace(eventId){
 const e=data.events.find(x=>String(x.id)===String(eventId)),out=$("#traceContent");if(!out||!e)return;
 const obs=e.context_observed||e.observed_context||{},interp=e.interpretation||e.interpreted_context||null;
 const scene=e.scene_id??e.scene??obs.scene_id??"unknown",shot=e.shot_id??e.shot??obs.shot_id??"unknown",dur=Math.max(0,(e.end||0)-(e.start||0));
 const sameScene=data.events.filter(x=>String(x.scene_id??x.context_observed?.scene_id??"")===String(scene)&&x.status==="present");
 const sameShot=sameScene.filter(x=>String(x.shot_id??x.context_observed?.shot_id??"")===String(shot));
 out.innerHTML="<h3>"+esc(String(e.id))+" · "+esc(String(e.class||"unknown"))+"</h3>"+
 "<div class=\"trace-chain\" role=\"navigation\" aria-label=\"Цепочка доказательности\"><span class=\"trace-node active\">Scene "+esc(String(scene))+"</span><span>→</span><span class=\"trace-node active\">Shot "+esc(String(shot))+"</span><span>→</span><span class=\"trace-node active\">Event "+esc(String(e.id))+"</span><span>→</span><span class=\"trace-node\">L0–L2</span><span>→</span><span class=\"trace-node\">L3</span><span>→</span><span class=\"trace-node\">L4</span></div>"+
 "<div class=\"trace-grid\"><div><b>Timestamp</b><br>"+fmt(e.start,3)+"–"+fmt(e.end,3)+" s<br>Δt = "+fmt(dur,3)+" s</div><div><b>Scene</b><br>"+esc(String(scene))+"<br><span class=\"muted small\">Событий в сцене: "+sameScene.length+"</span></div><div><b>Shot</b><br>"+esc(String(shot))+"<br><span class=\"muted small\">Событий в shot: "+sameShot.length+"</span></div></div>"+
 "<h4>L0–L2 · наблюдаемое событие</h4><p>"+esc(String(e.description||e.label||"Событие зафиксировано в Content Map."))+"</p>"+
 "<h4>L3 · observed_context</h4><pre class=\"trace-json\">"+esc(JSON.stringify(obs,null,2))+"</pre>"+
 "<h4>L4 · interpretation</h4><p>"+(interp?esc(typeof interp==="string"?interp:JSON.stringify(interp,null,2)):"<span class=\"muted\">Интерпретация не задана.</span>")+"</p>"+
 "<p><b>Confidence:</b> "+fmt(e.confidence,3)+" · <b>Status:</b> "+esc(String(e.status||"unknown"))+"<br><span class=\"muted\">Confidence не является вероятностью причинного эффекта.</span></p>";
}
function renderStatus(){const m=metrics();const rows=C.map(c=>{const es=data.events.filter(e=>e.class===c),statuses=[...new Set(es.map(e=>e.status))];let state=m[c].status;if(statuses.includes("not_applicable")&&!es.length)state="not_applicable";return[c,state,statuses.join(", ")||"no event",m[c].mean_confidence]});$("#statusTable").innerHTML='<table class="table"><tr><th>Class</th><th>Result</th><th>Raw statuses</th><th>Confidence</th></tr>'+rows.map(r=>`<tr><td>${r[0]}</td><td><span class="status status-${r[1]}">${r[1]}</span></td><td>${esc(r[2])}</td><td>${fmt(r[3],2)}</td></tr>`).join("")+'</table>'}
function buildReportText(m,area,areaAgg){
 const lines=[];
 lines.push("СИНЕМА КАТАРСИС — ИССЛЕДОВАТЕЛЬСКИЙ ОТЧЁТ");
 lines.push("Произведение: "+(data.work.title||"Без названия"));
 lines.push("Длительность: "+data.work.duration_seconds+" с");
 lines.push("Статус данных: "+(data.work.data_status||"unknown"));
 lines.push("");
 lines.push("ОГРАНИЧЕНИЯ: screen_time_share ≠ viewer_exposure; контентный анализ не устанавливает audience effect или причинный вред.");
 lines.push("");
 lines.push("ОБЩИЕ МЕТРИКИ");
 lines.push("Сцены: "+data.work.scene_count+"; shots: "+data.work.shot_count+"; events: "+data.events.length);
 lines.push("Temporal coverage: "+fmt(data.coverage.temporal*100,2)+"%");
 lines.push("C_min: "+(C_MIN*100)+"%");
 lines.push("");
 lines.push("КАТЕГОРИИ");
 C.forEach(c=>{const x=m[c];lines.push(c+" | "+data.ontology.classes[c]+" | status="+x.status+" | N="+fmt(x.N,2)+" | T="+fmt(x.T,3)+" s | S="+fmt(x.share*100,3)+"% | C="+fmt(x.coverage*100,2)+"% | rho_events="+fmt(x.event_density,3)+"/min | rho_time="+fmt(x.covered_time_density,3)+" s/min | R="+fmt(x.repeatability,3)+" | confidence="+fmt(x.mean_confidence,3));});
 lines.push("");
 lines.push("ВЫБРАННАЯ ОБЛАСТЬ Ω*");
 lines.push(area.join(", "));
 lines.push("Union time: "+fmt(areaAgg.T,3)+" s; absolute share: "+fmt(areaAgg.S*100,3)+"%; normalized entropy: "+fmt(areaAgg.diversity_index_norm,4));
 return lines.join("\\n");
}
function downloadBlob(content,name,type){
 const blob=new Blob([content],{type});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
function exportSpreadsheet(m){
 const rows=[["Cinema Catharsis","Category","Label","Status","Nω","Tω (s)","Sω (%)","Cω (%)","ρevents (/min)","ρtime (s/min)","Rω","Confidence"]];
 C.forEach(c=>{const x=m[c];rows.push(["Cinema Catharsis",c,data.ontology.classes[c],x.status,x.N,x.T,x.share*100,x.coverage*100,x.event_density,x.covered_time_density,x.repeatability,x.mean_confidence])});
 const csv=rows.map(row=>row.map(v=>'"'+String(v??"").replaceAll('"','""')+'"').join(";")).join("\\r\\n");
 const tsv=rows.map(row=>row.map(v=>String(v??"").replaceAll("\\t"," ")).join("\\t")).join("\\r\\n");
 downloadBlob("\\uFEFF"+csv,"cinema-catharsis-report.csv","text/csv;charset=utf-8");
 downloadBlob("\\uFEFF"+tsv,"cinema-catharsis-report.tsv","text/tab-separated-values;charset=utf-8");
}
function setupReporting(){
 const b=$("#reportBtn"),s=$("#sheetBtn"),t=$("#reportOutput");
 if(b)b.onclick=()=>{const m=metrics(),area=selectedSet.size?[...selectedSet]:(selected==="ALL"?C:[selected]),a=aggregateArea(m,area);t.hidden=false;t.textContent=buildReportText(m,area,a);t.focus()};
 if(s)s.onclick=()=>exportSpreadsheet(metrics());
}
function populateCreatorSelect(){
 const sel=$("#creatorSelect"); if(!sel)return;
 const people=data?.creators||data?.people||[]; sel.innerHTML='<option value="">— выбрать —</option>';
 people.forEach(p=>{const o=document.createElement("option");o.value=p.person_id||p.id||p.name;o.textContent=(p.canonical_name||p.name||p.person_id)+" · "+(p.role||"");sel.appendChild(o)});
 sel.onchange=renderCreatorProfile;
}
function selectCreatorWork(workId){
 window.__selectedWorkId=String(workId);
 const people=data?.creators||data?.people||[];
 const person=people.find(p=>String(p.person_id||p.id||p.name)===String($("#creatorSelect")?.value));
 const w=(person?.works||[]).find(x=>String(x.work_id||x.id||x.title)===String(workId));
 const out=$("#creatorWorkDetail"); if(!out||!w)return;
 const currentId=String(data?.work?.id??"");
 const loaded=currentId===String(w.work_id||w.id);
 const events=loaded?data.events.filter(e=>!e.work_id||String(e.work_id)===currentId):[];
 out.hidden=false;
 out.innerHTML='<div class="work-detail-head"><div><h3>'+esc(String(w.title||w.work_id))+'</h3><div class="muted small">'+esc(String(w.year??"—"))+' · '+esc(String(w.role||"—"))+'</div></div><span class="status-pill">'+(loaded?"Content Map загружен":"Content Map не загружен")+'</span></div>'+
 '<p class="small">'+(loaded?'Показаны события текущего Content Map. Evidence Trace и Timeline относятся к этому произведению.':'Для этого произведения в текущем демо нет отдельного Content Map. Система не подставляет данные из другого произведения.')+'</p>'+
 (loaded?'<div class="creator-kpis"><div><span class="muted small">Событий</span><b>'+events.length+'</b></div><div><span class="muted small">Duration</span><b>'+fmt(data.work.duration_seconds,1)+' s</b></div><div><span class="muted small">Ontology</span><b>'+esc(String(data.metadata?.ontology_version??"—"))+'</b></div></div><button type="button" class="secondary" onclick="document.getElementById(\'calculationTrace\')?.scrollIntoView({behavior:\'smooth\',block:\'center\'})">Открыть Evidence Trace</button>':'<div class="muted small">Следующий этап pipeline: загрузка отдельного Content Map по work_id.</div>');
}
function renderCreatorProfile(){
 const sel=$("#creatorSelect"),summary=$("#creatorSummary"),table=$("#creatorTable"),detail=$("#creatorWorkDetail");if(!sel||!summary||!table)return;
 const people=data?.creators||data?.people||[];const id=sel.value;
 if(!id){summary.innerHTML='<div class="muted">Выберите персону после загрузки корпуса.</div>';table.innerHTML="";if(detail)detail.hidden=true;return;}
 const p=people.find(x=>String(x.person_id||x.id||x.name)===String(id));if(!p)return;
 const works=p.works||[];
 summary.innerHTML='<div class="creator-kpis"><div><span class="muted small">Известно произведений</span><b>'+esc(String(p.works_total_known??"—"))+'</b></div><div><span class="muted small">Проанализировано</span><b>'+esc(String(p.works_analyzed??works.filter(w=>w.analyzed).length))+'</b></div><div><span class="muted small">Роль</span><b>'+esc(String(p.role||"—"))+'</b></div></div>';
 const rows=Object.entries(p.program_profile||{}).map(([code,v])=>({code,...v})).sort((a,b)=>(b.screen_time_share??0)-(a.screen_time_share??0));
 const programTable='<h3>Агрегированный профиль программ</h3><div class="table-wrap"><table><thead><tr><th>Программа</th><th>Произведений</th><th>Nω</th><th>Tω, сек</th><th>Sω</th><th>Rω</th></tr></thead><tbody>'+rows.map(v=>'<tr><td><b>'+esc(v.code)+'</b></td><td>'+esc(String(v.works_present??0))+'</td><td>'+esc(String(v.event_count??0))+'</td><td>'+fmt(v.duration_sec??0,2)+'</td><td>'+fmt((v.screen_time_share??0)*100,2)+'%</td><td>'+fmt((v.recurrence??0)*100,2)+'%</td></tr>').join("")+'</tbody></table></div>';
 const workTable='<h3>Корпус произведений</h3><div class="table-wrap"><table><thead><tr><th>Произведение</th><th>Год</th><th>Роль</th><th>Анализ</th><th>Программы</th><th></th></tr></thead><tbody>'+works.map(w=>'<tr><td><b>'+esc(String(w.title||w.work_id))+'</b></td><td>'+esc(String(w.year??"—"))+'</td><td>'+esc(String(w.role||"—"))+'</td><td>'+((w.analyzed)?'<span class="good">analyzed</span>':'<span class="muted">not analyzed</span>')+'</td><td>'+esc((w.programs||[]).join(", "))+'</td><td><button type="button" class="secondary work-open" data-work-id="'+esc(w.work_id||w.id||w.title)+'">Открыть</button></td></tr>').join("")+'</tbody></table></div>';
 table.innerHTML=programTable+workTable;
 table.querySelectorAll(".work-open").forEach(btn=>btn.addEventListener("click",()=>selectCreatorWork(btn.dataset.workId)));
}
function checkChartHealth(){
 const ids=["bars","timeline","density","wheel"];
 const state=ids.map(id=>{const el=$("#"+id);return {id,exists:!!el,svg:!!el?.querySelector("svg"),error:!!el?.querySelector(".chart-error")};});
 const failed=state.filter(x=>!x.exists||!x.svg||x.error);
 const host=$("#chartHealth");
 if(host) host.innerHTML=failed.length?'<span class="bad">Визуализация: '+failed.length+'/'+ids.length+' блоков требуют проверки.</span>':'<span class="good">Визуализация: 4/4 диаграммы построены.</span>';
 return state;
}
function renderChartsOnly(){
 if(!data)return;
 let m;
 try{m=metrics()}catch(err){
  ["bars","timeline","density","wheel"].forEach(id=>{const el=$("#"+id);if(el)el.innerHTML='<div class="chart-error"><b>Не удалось рассчитать данные для графика</b><br><span>'+esc(err.message||String(err))+'</span></div>';});
  return;
 }
 const renderOne=(id,fn)=>{const el=$("#"+id);if(!el)return;try{el.innerHTML=fn();}catch(err){el.innerHTML='<div class="chart-error"><b>Ошибка построения</b><br><span>'+esc(err.message||String(err))+'</span></div>';}};
 renderOne("bars",()=>drawBars(m));
 renderOne("timeline",()=>drawTimeline());
 renderOne("density",()=>drawDensity());
 renderOne("wheel",()=>drawWheel(m));
}
function render(){
 const m=metrics();
 const area=selectedSet.size?[...selectedSet]:(selected==="ALL"?C:[selected]);
 renderChartsOnly();
 const areaAgg=aggregateArea(m,area);
 // Charts must render independently from optional dashboard/report UI.
 try{
  const keyArea=area, keyAgg=areaAgg;
  $("#keyMetrics").innerHTML='<div class="card"><div class="muted">Coverage '+tip("C")+'</div><div class="metric">'+fmt(data.coverage.temporal*100,1)+'%</div><div class="small">Ccov = Tprocessed / T · C_min='+(C_MIN*100)+'%</div></div><div class="card"><div class="muted">События '+tip("N")+'</div><div class="metric">'+data.events.length+'</div><div class="small">Количество L1/L2 событий в Content Map</div></div><div class="card"><div class="muted">Сцены / shots</div><div class="metric">'+data.work.scene_count+' / '+data.work.shot_count+'</div><div class="small">единицы нарративной и монтажной сегментации</div></div><div class="card"><div class="muted">Ω* union '+tip("S")+'</div><div class="metric">'+fmt(keyAgg.S*100,2)+'%</div><div class="small">'+keyArea.join(", ")+' · объединённое время; перекрытия не удваиваются</div></div><div class="card"><div class="muted">Средняя confidence '+tip("confidence")+'</div><div class="metric">'+fmt(C.reduce((s,c)=>s+m[c].mean_confidence,0)/C.length,2)+'</div><div class="small">уверенность кодирования/интерпретации, не вероятность эффекта</div></div><div class="card"><div class="muted">Data status</div><div class="metric">'+esc(data.work.data_status||"unknown")+'</div><div class="small">Synthetic demo ≠ audience study</div></div>';
 }catch(err){ $("#keyMetrics").innerHTML='<div class="card"><div class="bad">Сводный блок временно недоступен.</div><div class="small">'+esc(err.message||String(err))+'</div></div>'; }
 $("#reportOutput").hidden=true;
 setupReporting();
 const cov=data.coverage.temporal;
 $("#coverageBanner").innerHTML='<div class="coverage '+(cov>=C_MIN?"coverage-ok":"coverage-low")+'">Coverage: <b>'+fmt(cov*100)+'%</b> · C_min='+(C_MIN*100)+'% · '+(cov>=C_MIN?"absence may be reported as absent":"absence must be reported as unknown")+'</div>';
 $("#metrics").innerHTML=C.map(c=>'<div class="card"><div class="muted">'+c+' · '+data.ontology.classes[c]+'</div><div class="metric">'+fmt(m[c].share*100)+'%</div><div class="small">Nω='+fmt(m[c].N,2)+' · Tω='+fmt(m[c].T,1)+'s · Sω='+fmt(m[c].share*100,2)+'%</div><div class="small">Cω='+fmt(m[c].coverage*100,2)+'% shots · ρevents='+fmt(m[c].event_density,3)+'/мин · ρtime='+fmt(m[c].covered_time_density,3)+'с/мин · Rω='+fmt(m[c].repeatability,3)+'</div><div class="small">confidence='+fmt(m[c].mean_confidence,2)+' · status=<span class="status status-'+m[c].status+'">'+m[c].status+'</span></div></div>').join("");
 // Cross-view synchronization: charts are rendered only by renderChartsOnly().
 const bars=$("#bars");
 if(bars) bars.querySelectorAll("[data-class]").forEach(el=>{
   const activate=()=>{const c=el.dataset.class;if(!c)return;selected=c;selectedSet=new Set([c]);render();document.getElementById("selectedInspector")?.scrollIntoView({behavior:"smooth",block:"nearest"});};
   el.addEventListener("click",activate);
   el.addEventListener("keydown",ev=>{if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();activate();}});
 });
 const tl=$("#timeline");
 if(tl) tl.querySelectorAll("[data-event-id]").forEach(el=>{
   el.addEventListener("click",()=>selectEvent(el.getAttribute("data-event-id")));
   el.addEventListener("keydown",ev=>{if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();renderEvidenceTrace(el.getAttribute("data-event-id"));}});
 });
 const wh=$("#wheel");
 if(wh) wh.querySelectorAll("[data-wheel-class]").forEach(el=>{
   const open=()=>{selected=el.getAttribute("data-wheel-class");selectedSet=new Set([selected]);render();};
   el.addEventListener("click",open);
   el.addEventListener("keydown",ev=>{if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();open();}});
 });
 renderProgramGroups(m);
 requestAnimationFrame(checkChartHealth);
 const traceEl=$("#traceContent");
 if(traceEl){
  const tc=selected==="ALL"?C[0]:selected, x=m[tc], ev=data.events.filter(e=>e.class===tc&&e.status==="present");
  const intervals=ev.map(e=>[e.start,e.end]).sort((a,b)=>a[0]-b[0]);
  const merged=[]; intervals.forEach(([a,b])=>{const last=merged[merged.length-1];if(last&&a<=last[1])last[1]=Math.max(last[1],b);else merged.push([a,b]);});
  const union=merged.reduce((s,[a,b])=>s+b-a,0);
  traceEl.innerHTML='<h3>'+esc(tc)+' — '+esc(data.ontology.classes[tc])+'</h3><div class="trace-grid"><div><b>Nω</b><br>'+fmt(x.N,2)+' = Σ pᵢ,ω</div><div><b>Tω</b><br>'+fmt(union,3)+' s = μ(⋃ intervals)</div><div><b>Sω</b><br>'+fmt(x.share*100,3)+'% = '+fmt(union,3)+' / '+fmt(data.work.duration_seconds,3)+'</div></div><h4>Исходные интервалы</h4><div class="trace-intervals">'+(intervals.length?intervals.map((v,i)=>'<div><b>E'+(i+1)+'</b> · '+fmt(v[0],3)+'–'+fmt(v[1],3)+' s · '+fmt(v[1]-v[0],3)+' s</div>').join(""):'<div class="muted">Нет событий.</div>')+'</div><p class="small muted">Объединённые интервалы: '+merged.map(v=>fmt(v[0],2)+'–'+fmt(v[1],2)+' s').join(', ')+' · '+fmt(union,3)+' s. Перекрытия внутри категории учтены один раз.</p>';
 }

 document.querySelectorAll("[data-wheel-class]").forEach(p=>{const show=()=>{const c=p.dataset.wheelClass;const x=m[c];p.setAttribute("aria-label",c+" · "+fmt(x.share*100,2)+"% · N="+fmt(x.N,2)+" · T="+fmt(x.T,1)+" s · C="+fmt(x.coverage*100,1)+"% · confidence "+fmt(x.mean_confidence,2)+" · "+x.status)};p.addEventListener("focus",show);p.addEventListener("click",()=>{selectedSet=new Set([p.dataset.wheelClass]);selected=p.dataset.wheelClass;controls();render()})});
 $("#editorList").innerHTML=data.events.map((e,i)=>'<div class="editor-row"><b>'+esc(e.id)+'</b><span>'+e.class+'</span><input data-i="'+i+'" data-k="start" type="number" step="0.1" value="'+e.start+'"><input data-i="'+i+'" data-k="end" type="number" step="0.1" value="'+e.end+'"><input data-i="'+i+'" data-k="confidence" type="number" min="0" max="1" step="0.01" value="'+(e.confidence??1)+'"><button data-del="'+i+'">×</button></div>').join("");
 $("#selected").textContent=area.length===C.length?"Вся онтология":area.map(c=>c+" — "+data.ontology.classes[c]).join(", ");
 $("#passport").innerHTML='<table class="table"><tr><th>Параметр</th><th>Значение</th></tr><tr><td>Ω*</td><td>'+area.join(", ")+'</td></tr><tr><td>Area union time</td><td>'+fmt(areaAgg.T,1)+' s · '+fmt(areaAgg.S*100,2)+'%</td></tr><tr><td>HΩ* normalized</td><td>'+fmt(areaAgg.diversity_index_norm,3)+'</td></tr><tr><td>Runtime</td><td>'+Math.floor(data.work.duration_seconds/60)+' мин '+data.work.duration_seconds%60+' с</td></tr><tr><td>Scenes</td><td>'+data.work.scene_count+'</td></tr><tr><td>Shots</td><td>'+data.work.shot_count+'</td></tr><tr><td>Events</td><td>'+data.events.length+'</td></tr><tr><td>Temporal coverage</td><td>'+fmt(cov*100,2)+'%</td></tr><tr><td>Modalities</td><td>vision '+fmt((data.coverage.modalities?.vision??0)*100,1)+'%, audio '+fmt((data.coverage.modalities?.audio??0)*100,1)+'%, text '+fmt((data.coverage.modalities?.text??0)*100,1)+'%</td></tr><tr><td>Data status</td><td>'+esc(data.work.data_status)+'</td></tr></table>';
 const cs=contextStats();
 renderSceneAnalysis();
 renderAttitudes();renderCodeReference();initCodeTips();$("#contextMetrics").innerHTML='<div class="card"><div class="muted">Сцены</div><div class="metric">'+cs.sceneCount+'</div><div class="small">N_units для Rω</div></div><div class="card"><div class="muted">Планы / shots</div><div class="metric">'+cs.shotCount+'</div><div class="small">знаменатель Cω</div></div><div class="card"><div class="muted">Сверхкраткие события</div><div class="metric">'+cs.subPerceptual+'</div><div class="small">&lt; '+cs.minMs+' ms; параметрический флаг</div></div><div class="card"><div class="muted">Оси L3</div><div class="metric">'+Object.keys(cs.context).length+'</div><div class="small">наблюдаемый контекст</div></div>';
 const dp=data.destructive_programs||{}, pa=data.psychological_attitudes||{};
 const destructiveList=Object.entries(dp.definitions||{}).map(([k,v])=>{const x=m[k]||{N:0,T:0,share:0,status:"absent"};return '<li><b>'+esc(k)+'</b> — '+esc(v)+'<br><span class="small">N='+fmt(x.N,2)+' · T='+fmt(x.T,1)+'s · S='+fmt(x.share*100,2)+'% · status='+x.status+'</span></li>';}).join("");
 const contextTable=Object.entries(cs.context).map(([k,v])=>'<tr><td>'+esc(k)+'</td><td>'+Object.entries(v).map(([x,n])=>esc(x)+': '+n).join(" · ")+'</td></tr>').join("");
 const attitudeList=(pa.items||[]).map(x=>'<li><b>'+esc(x.label)+'</b> · confidence='+fmt(x.confidence,2)+' · '+esc(x.status)+'<br><span class="small">basis: '+esc(x.basis)+'</span></li>').join("");
 $("#contextDetail").innerHTML='<div class="grid"><div class="card"><b>Деструктивные программы</b><div class="small">'+esc(dp.note||"Нет отдельной таксономии")+'</div><ul>'+destructiveList+'</ul></div><div class="card"><b>Психологические установки / L4</b><div class="small">'+esc(pa.note||"Интерпретационный слой отсутствует")+'</div><ul>'+attitudeList+'</ul></div></div><div class="panel" style="margin-top:10px"><b>Распределение наблюдаемого контекста L3</b><table class="table"><tr><th>Ось</th><th>Наблюдаемые значения</th></tr>'+contextTable+'</table></div><div class="notice small"><b>О временном пороге.</b> Для разных задач восприятия описаны разные временные окна. Поэтому '+cs.minMs+' ms в этом демо — только <b>assumption</b> для sensitivity analysis, а не универсальный «закон психофизиологического отклика».</div>';
 renderStatus();
 passport={work:data.work,selected_category:selected,metrics:m,coverage:data.coverage,analysis_parameters:data.analysis_parameters,scene_count:data.work.scene_count,shot_count:data.work.shot_count,destructive_programs:data.destructive_programs,psychological_attitudes:data.psychological_attitudes,versions:VERSIONS,C_min:C_MIN,epistemic_note:"Content analysis does not establish viewer exposure, effect, harm, or causality.",generated_at:new Date().toISOString(),analysis_hash:"sha256:demo-generated",analysis_scope:area,aggregate_area:areaAgg};
}
let openProgramGroups=new Set();
function renderProgramGroups(m){
 const el=$("#programGroups"); if(!el)return;
 const active=selectedSet.size?selectedSet:C;
 el.innerHTML=C.map(c=>{
   const rows=data.events.filter(e=>e.class===c&&e.status==="present");
   const share=m[c].share, isOpen=openProgramGroups.has(c);
   const items=rows.map(e=>'<li><button type="button" class="program-event" data-event-id="'+esc(e.id)+'"><b>'+esc(e.id)+'</b><span>'+fmt(e.start,1)+'–'+fmt(e.end,1)+' s</span><span>confidence '+fmt(e.confidence??1,2)+'</span></button></li>').join("");
   return '<div class="program-group '+(isOpen?'open':'')+'"><button type="button" class="program-group-header" aria-expanded="'+isOpen+'" data-program-group="'+c+'"><span class="class-code">'+c+'</span><span class="class-name">'+esc(data.ontology.classes[c])+'</span><span class="class-metric">'+fmt(share*100,2)+'%</span><span aria-hidden="true">'+(isOpen?'▾':'▸')+'</span></button><div class="program-sublist" '+(isOpen?'':'hidden')+'><div class="small muted">Nω='+fmt(m[c].N,2)+' · Tω='+fmt(m[c].T,1)+' s · Cω='+fmt(m[c].coverage*100,1)+'% · status='+m[c].status+'</div><ul>'+items+'</ul></div></div>';
 }).join("");
 el.querySelectorAll("[data-program-group]").forEach(b=>b.addEventListener("click",()=>{const c=b.dataset.programGroup;openProgramGroups.has(c)?openProgramGroups.delete(c):openProgramGroups.add(c);renderProgramGroups(m)}));
 el.querySelectorAll("[data-event-id]").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();const id=b.dataset.eventId;selectEvent(id)}));
}
function controls(){const el=$("#controls");el.innerHTML='<button data-c="ALL">Вся онтология</button>'+C.map(c=>`<button data-c="${c}">${c}</button>`).join("")+'<button data-c="CLEAR">Сбросить</button>';el.onclick=e=>{const b=e.target.closest("button");if(!b)return;const c=b.dataset.c;if(c==="ALL"){selected="ALL";selectedSet=new Set(C)}else if(c==="CLEAR"){selected="ALL";selectedSet=new Set(C)}else{selectedSet.has(c)?selectedSet.delete(c):selectedSet.add(c);selected=selectedSet.size===1?[...selectedSet][0]:"ALL"}el.querySelectorAll("button").forEach(x=>x.classList.remove("active"));if(selectedSet.size===C.length)el.querySelector("[data-c=ALL]").classList.add("active");else for(const x of selectedSet)el.querySelector(`[data-c="${x}"]`)?.classList.add("active");render()}}
function normalizeInput(d){if(d&&d.film){return {work:{id:"imported-"+Date.now(),title:d.film.title,duration_seconds:d.film.duration_sec,data_status:"preliminary",analysis_version:VERSIONS.measurement},ontology:{classes:Object.fromEntries(C.map(c=>[c,c]))},events:(d.events||[]).map((e,i)=>({id:e.id||"E"+String(i+1).padStart(3,"0"),start:e.start,end:e.end,class:e.category,program:"imported",status:"present",confidence:e.confidence,context_observed:e.context_observed||{},membership:e.membership??e.p??1})),coverage:d.coverage||{temporal:1,modalities:{}},validation:d.validation||{status:"not_validated"}}}return d}
function setupAttitudeFilters(){const sel=$("#attitudeDomainFilter");if(!sel)return;const meta=attitudeMeta();const seen=new Map();Object.entries(meta.domainMap).forEach(([k,v])=>seen.set(v[0],v[1]));sel.innerHTML='<option value="ALL">All domains</option>'+[...seen].map(([k,v])=>'<option value="'+k+'">'+esc(v)+'</option>').join("");const apply=()=>{window.__attitudeFilter={domain:sel.value,polarity:$("#attitudePolarityFilter")?.value||"ALL",search:$("#attitudeSearch")?.value||""};renderAttitudes()};sel.onchange=apply;$("#attitudePolarityFilter").onchange=apply;$("#attitudeSearch").oninput=apply;}
function load(d){d=normalizeInput(d);const errors=validate(d);$("#validation").innerHTML=errors.length?`<span class="bad">Schema check: ${errors.length} error(s)</span><br>${errors.map(esc).join("<br>")}`:`<span class="good">Schema check: базовая валидация пройдена.</span> · ${esc(d.work.title)} · ${esc(d.work.data_status)}`;if(errors.length)return;data=d;selected="ALL";selectedSet=new Set(C);setupAttitudeFilters();controls();render();populateCreatorSelect();renderCreatorProfile()}
function loadDemo(){Promise.all([fetch("data/demo_content.json").then(r=>r.json()),fetch("data/attitude_ontology.json").then(r=>r.json())]).then(([d,o])=>{window.ATTITUDE_ONTOLOGY=o;d.attitude_ontology=o;load(d)}).catch(()=>$("#validation").textContent="Не удалось загрузить Demo JSON. Откройте через GitHub Pages или HTTP-сервер.")}
const importPanel=document.querySelector("#sourceInput"),dropzone=document.querySelector("#dropzone");
["dragenter","dragover"].forEach(ev=>dropzone?.addEventListener(ev,e=>{e.preventDefault();dropzone.classList.add("drop-active")}));
["dragleave","drop"].forEach(ev=>dropzone?.addEventListener(ev,e=>{e.preventDefault();dropzone.classList.remove("drop-active")}));
dropzone?.addEventListener("drop",e=>{const f=e.dataTransfer.files[0];if(!f)return;const reader=new FileReader();reader.onload=()=>{try{load(JSON.parse(reader.result))}catch(err){$("#validation").innerHTML='<span class="bad">Некорректный JSON.</span>'}};reader.readAsText(f)});
document.querySelectorAll("[data-source-tab]").forEach(tab=>tab.addEventListener("click",()=>{
 const name=tab.dataset.sourceTab;
 document.querySelectorAll("[data-source-tab]").forEach(x=>{x.classList.toggle("active",x===tab);x.setAttribute("aria-selected",x===tab?"true":"false")});
 document.querySelectorAll("[data-source-pane]").forEach(p=>{const active=p.dataset.sourcePane===name;p.hidden=!active;p.classList.toggle("active",active)});
}));
$("#creatorSelect")?.addEventListener("change",renderCreatorProfile);
$("#loadDemoSource")?.addEventListener("click",loadDemo);
$("#contentMapFile")?.addEventListener("change",e=>{const f=e.target.files[0];if(!f)return;const reader=new FileReader();reader.onload=()=>{try{load(JSON.parse(reader.result))}catch(err){$("#validation").innerHTML='<span class="bad">Некорректный JSON.</span>'}};reader.readAsText(f)});
$("#fileInput").addEventListener("change",e=>{const f=e.target.files[0];if(!f)return;const reader=new FileReader();reader.onload=()=>{try{load(JSON.parse(reader.result))}catch(err){$("#validation").innerHTML='<span class="bad">Некорректный JSON.</span>'}};reader.readAsText(f)});
$("#resetBtn").addEventListener("click",loadDemo);$("#editorList").addEventListener("change",e=>{const el=e.target;if(el.dataset.i===undefined)return;const i=Number(el.dataset.i),k=el.dataset.k;data.events[i][k]=Number(el.value);const errors=validate(data);if(errors.length){$("#validation").innerHTML=`<span class="bad">Ошибка после изменения:</span><br>${errors.map(esc).join("<br>")}`;return}$("#validation").innerHTML="<span class=\"good\">Изменение применено.</span>";render()});$("#editorList").addEventListener("click",e=>{const b=e.target.closest("[data-del]");if(!b)return;data.events.splice(Number(b.dataset.del),1);render()});$("#addEventBtn").addEventListener("click",()=>{const i=data.events.length+1;data.events.push({id:"E"+String(i).padStart(3,"0"),start:0,end:1,class:C[0],program:"manual",status:"present",confidence:1,context_observed:{}});render()});
$("#wheelMode")?.addEventListener("change",e=>{wheelMode=e.target.value;render()});
$("#perceptualThreshold")?.addEventListener("change",e=>{if(!data)return;data.analysis_parameters=data.analysis_parameters||{};data.analysis_parameters.perceptual_min_ms=Math.max(1,Number(e.target.value)||120);render()});
$("#threshold120")?.addEventListener("click",()=>{if(!data)return;data.analysis_parameters=data.analysis_parameters||{};data.analysis_parameters.perceptual_min_ms=120;$("#perceptualThreshold").value=120;render()});
$("#threshold240")?.addEventListener("click",()=>{if(!data)return;data.analysis_parameters=data.analysis_parameters||{};data.analysis_parameters.perceptual_min_ms=240;$("#perceptualThreshold").value=240;render()});
$("#exportBtn").addEventListener("click",()=>{if(!passport)return;const blob=new Blob([JSON.stringify(passport,null,2)],{type:"application/json"}),a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="content-passport-demo.json";a.click();URL.revokeObjectURL(a.href)});
loadDemo();
