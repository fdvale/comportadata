export function validar(input) {
  const r={};
  r.data=String(input.data??'').trim();
  const match=/^(\d{2})\/(\d{2})\/(\d{4})$/.exec(r.data);
  if(!match) throw new Error('Informe uma data no formato dd/mm/aaaa.');
  const [,dd,mm,yyyy]=match;
  const d=new Date(`${yyyy}-${mm}-${dd}T12:00:00Z`);
  if(!Number(yyyy)||isNaN(d.getTime())||d.getUTCDate()!==Number(dd)||d.getUTCMonth()+1!==Number(mm)) throw new Error('Informe uma data que exista no calendário.');
  for(const k of ['antecedente','comportamento','consequencia']) {
    r[k]=String(input[k]??'').trim().toLowerCase();
    if(!r[k]) throw new Error('Preencha antecedente, comportamento e consequência.');
    if(r[k].length>500) throw new Error('Use até 500 caracteres em cada descrição.');
  }
  if(String(input.frequencia??'').trim()===''||String(input.duracao??'').trim()==='') throw new Error('Preencha frequência e duração.');
  r.frequencia=Number(input.frequencia);
  r.duracao=Number(String(input.duracao).replace(',','.'));
  if(!Number.isSafeInteger(r.frequencia)||r.frequencia<0||r.frequencia>1000000) throw new Error('A frequência deve ser um inteiro de 0 a 1.000.000.');
  if(!Number.isFinite(r.duracao)||r.duracao<0||r.duracao>1000000) throw new Error('A duração deve ser um número de 0 a 1.000.000 minutos.');
  return r;
}
export function resumir(rows) {
  const count=new Map(), days=new Map();
  let frequencia=0,duracao=0;
  for(const r of rows){frequencia+=r.frequencia;duracao+=r.duracao;count.set(r.comportamento,(count.get(r.comportamento)||0)+1);days.set(r.data,(days.get(r.data)||0)+r.frequencia);}
  return {total:rows.length,frequencia,media:rows.length?duracao/rows.length:0,comportamentos:[...count].sort((a,b)=>b[1]-a[1]),dias:[...days].sort((a,b)=>a[0].split('/').reverse().join('').localeCompare(b[0].split('/').reverse().join('')))};
}
export function paraCSV(rows) {
  const cols=['data','antecedente','comportamento','consequencia','frequencia','duracao'];
  const escape=x=>{let s=String(x);if(/^[=+@\-\t\r]/.test(s))s="'"+s;return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
  return cols.join(',')+'\r\n'+rows.map(r=>cols.map(k=>escape(r[k])).join(',')).join('\r\n')+'\r\n';
}
