import test from 'node:test';
import assert from 'node:assert/strict';
import { exemplos } from './dados.js';
import { resumir, validar, paraCSV } from './modelo.js';
test('analisa os 20 registros fictícios',()=>{
 const s=resumir(exemplos);
 assert.equal(s.total,20); assert.equal(s.frequencia,40); assert.equal(s.media,2.85);
});
test('análise vazia',()=>assert.deepEqual(resumir([]),{total:0,frequencia:0,media:0,comportamentos:[],dias:[]}));
test('cadastro rejeita dados inválidos',()=>{
 const r={...exemplos[0]};
 for(const change of [{data:'31/02/2026'},{antecedente:' '},{frequencia:2.5},{frequencia:-1},{duracao:Infinity}]) assert.throws(()=>validar({...r,...change}));
});
test('aceita vírgula e data bissexta',()=>{
 const r=validar({...exemplos[0],data:'29/02/2024',duracao:'1,5'});
 assert.equal(r.duracao,1.5); assert.equal(r.data,'29/02/2024');
});
test('novo registro altera totais sem mudar exemplos',()=>{
 const s=resumir([...exemplos,validar({...exemplos[0],frequencia:2,duracao:1.5})]);
 assert.equal(s.total,21);assert.equal(s.frequencia,42);assert.equal(exemplos.length,20);
});
test('CSV mantém seis campos e escapa vírgulas',()=>{
 const csv=paraCSV([{...exemplos[0],antecedente:'tarefa, jogo'}]);
 assert.ok(csv.startsWith('data,antecedente,comportamento,consequencia,frequencia,duracao\r\n'));
 assert.ok(csv.includes('"tarefa, jogo"'));
});
