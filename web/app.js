import { exemplos } from './dados.js';
import { resumir, validar, paraCSV } from './modelo.js';

let registros=exemplos.map(r=>({...r}));
const $=s=>document.querySelector(s);
const number=x=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2}).format(x);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let toastTimer;
function notify(text){$('#toast').textContent=text;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,4000);}
function render(){
 const all=location.hash==='#registros';
 const title=all?'Registros':'Visão geral';
 $('#breadcrumb').textContent=title;$('#page-title').textContent=title;
 $('#page-description').textContent=all?'Antecedentes, comportamentos e consequências em um só lugar.':'Uma leitura dos seus registros comportamentais.';
 $('#overview').hidden=all;$('#all-records').hidden=all;
 document.querySelectorAll('.nav-link').forEach(a=>{const active=a.dataset.view===(all?'registros':'visao-geral');a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 $('#records-title').textContent=all?'Todos os registros':'Registros recentes';
 $('#records-description').textContent=all?'Observações fictícias disponíveis nesta sessão':'Últimas observações do conjunto fictício';
 const s=resumir(registros);
 $('#stat-total').textContent=number(s.total);$('#stat-frequency').textContent=number(s.frequencia);$('#stat-duration').textContent=number(s.media);$('#nav-count').textContent=s.total;
 const sorted=[...registros].sort((a,b)=>b.data.split('/').reverse().join('').localeCompare(a.data.split('/').reverse().join(''))||b.id-a.id);
 const shown=all?sorted:sorted.slice(0,5);
 $('#records-body').innerHTML=shown.map(r=>`<tr><td>${esc(r.data)}</td><td>${esc(r.antecedente)}</td><td>${esc(r.comportamento)}</td><td>${esc(r.consequencia)}</td><td class="numeric">${number(r.frequencia)}</td><td class="numeric">${number(r.duracao)} min</td></tr>`).join('')||'<tr><td colspan="6" class="empty">Nenhum registro nesta sessão.</td></tr>';
 $('#table-count').textContent=`Mostrando ${shown.length} de ${registros.length} registros`;
 const max=Math.max(...s.comportamentos.map(x=>x[1]),1);
 $('#behavior-chart').innerHTML=s.comportamentos.slice(0,5).map(([label,n])=>`<div class="bar-item"><div class="bar-label"><span>${esc(label)}</span><strong>${n}</strong></div><div class="bar-track" aria-hidden="true"><div class="bar-fill" style="width:${n/max*100}%"></div></div></div>`).join('')||'<p class="empty">Adicione um registro para começar.</p>';
 timeline(s.dias);
}
function timeline(dias){
 if(!dias.length){$('#timeline').innerHTML='<p class="empty">Nenhum dado para exibir.</p>';return;}
 const w=610,h=180,left=30,right=14,top=10,bottom=28,max=Math.max(...dias.map(d=>d[1]),1);
 const x=i=>left+(w-left-right)*(dias.length===1?.5:i/(dias.length-1));
 const y=n=>h-bottom-n/max*(h-top-bottom);
 const points=dias.map(([d,n],i)=>`${x(i)},${y(n)}`).join(' ');
 const area=`${x(0)},${h-bottom} ${points} ${x(dias.length-1)},${h-bottom}`;
 const grid=[0,.5,1].map(t=>`<line x1="${left}" y1="${y(max*t)}" x2="${w-right}" y2="${y(max*t)}" stroke="#e5edef" stroke-dasharray="3 4"/><text x="${left-10}" y="${y(max*t)+4}" text-anchor="end">${number(max*t)}</text>`).join('');
 const labels=[...new Set([0,Math.floor((dias.length-1)/3),Math.floor(2*(dias.length-1)/3),dias.length-1])].map(i=>`<text x="${x(i)}" y="${h-5}" text-anchor="middle">${esc(dias[i][0].slice(0,5))}</text>`).join('');
 const dots=dias.map(([d,n],i)=>`<circle cx="${x(i)}" cy="${y(n)}" r="3.2" fill="#087e83" stroke="white" stroke-width="1.5"><title>${esc(d)}: ${n} ocorrências</title></circle>`).join('');
 $('#timeline').innerHTML=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">Frequência por data</title><desc id="chart-desc">${esc(dias.map(([d,n])=>`${d}: ${n} ocorrências`).join('; '))}</desc><defs><linearGradient id="chart-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#55aaad" stop-opacity=".25"/><stop offset="100%" stop-color="#55aaad" stop-opacity=".02"/></linearGradient></defs>${grid}<polygon points="${area}" fill="url(#chart-fill)"/><polyline points="${points}" fill="none" stroke="#087e83" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>${dots}${labels}</svg>`;
}
function openForm(){
 $('#record-form').reset();$('#form-error').textContent='';
 const d=new Date();const local=`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
 $('#record-form').elements.data.value=local;$('#record-dialog').showModal();
}
function addRecord(input){
 const record={...validar(input),id:Math.max(0,...registros.map(r=>r.id))+1};
 registros.push(record);render();notify('Registro fictício adicionado à sessão.');return record;
}
$('#new-record').addEventListener('click',openForm);
for(const id of ['#close-dialog','#cancel-dialog'])$(id).addEventListener('click',()=>$('#record-dialog').close());
$('#record-form').addEventListener('submit',e=>{
 e.preventDefault();const form=Object.fromEntries(new FormData(e.target));
 form.data=form.data.split('-').reverse().join('/');
 try{addRecord(form);$('#record-dialog').close();}catch(error){$('#form-error').textContent=error.message;}
});
$('#export-csv').addEventListener('click',()=>{
 const url=URL.createObjectURL(new Blob([paraCSV(registros)],{type:'text/csv;charset=utf-8'}));
 const a=document.createElement('a');a.href=url;a.download='registros_demo.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('CSV preparado com os registros desta sessão.');
});
window.addEventListener('hashchange',render);
render();

if(document.modelContext?.registerTool){
 const lifecycle=new AbortController();
 const definitions=[
  {name:'consultar_resumo_comportadata',description:'Consulta o resumo dos registros fictícios da sessão atual.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:()=>resumir(registros)},
  {name:'cadastrar_registro_ficticio',description:'Adiciona um registro fictício à sessão da demonstração. Os registros são descartados ao recarregar a página.',inputSchema:{type:'object',properties:{data:{type:'string',description:'dd/mm/aaaa'},antecedente:{type:'string',maxLength:500},comportamento:{type:'string',maxLength:500},consequencia:{type:'string',maxLength:500},frequencia:{type:'integer',minimum:0,maximum:1000000},duracao:{type:'number',minimum:0,maximum:1000000}},required:['data','antecedente','comportamento','consequencia','frequencia','duracao'],additionalProperties:false},annotations:{readOnlyHint:false},execute:input=>{const r=addRecord(input);return{id:r.id,total:registros.length};}}
 ];
 for(const tool of definitions){try{Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}}
 window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
}
