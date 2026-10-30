export const catalog=Object.freeze([
 {product:'Notebook Exemplo 14',supplier:'Loja fictícia A',cents:280000,category:'Informática'},
 {product:'Notebook Exemplo 14',supplier:'Loja fictícia B',cents:265000,category:'Informática'},
 {product:'Mouse Exemplo',supplier:'Loja fictícia A',cents:8990,category:'Acessórios'},
 {product:'Mouse Exemplo',supplier:'Loja fictícia B',cents:7990,category:'Acessórios'},
 {product:'Teclado Exemplo',supplier:'Loja fictícia A',cents:15990,category:'Acessórios'},
 {product:'Teclado Exemplo',supplier:'Loja fictícia B',cents:13990,category:'Acessórios'},
]);
export const normalize=s=>String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
export function compare(query='',direction='asc',category='Todas'){
 if(!['asc','desc'].includes(direction))throw Error('Ordenação inválida.');
 const q=normalize(query);return catalog.filter(p=>normalize(p.product).includes(q)&&(category==='Todas'||p.category===category)).map(p=>{const minimum=Math.min(...catalog.filter(x=>x.product===p.product).map(x=>x.cents));return {...p,minimum,difference:p.cents-minimum};}).sort((a,b)=>direction==='asc'?a.cents-b.cents:b.cents-a.cents);
}
export const money=n=>(n/100).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
