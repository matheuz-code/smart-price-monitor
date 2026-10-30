"""Demonstração local independente de banco, credenciais e serviços externos."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

PRODUCTS = [
    {"produto": "Notebook Exemplo 14", "loja": "Loja fictícia A", "preco": 2800.0},
    {"produto": "Notebook Exemplo 14", "loja": "Loja fictícia B", "preco": 2650.0},
    {"produto": "Mouse Exemplo", "loja": "Loja fictícia A", "preco": 89.9},
    {"produto": "Mouse Exemplo", "loja": "Loja fictícia B", "preco": 79.9},
]


def comparar(query=''):
    rows = [dict(p) for p in PRODUCTS if query.casefold() in p['produto'].casefold()]
    for row in rows:
        row['menor_preco'] = min(p['preco'] for p in PRODUCTS if p['produto'] == row['produto'])
    return sorted(rows, key=lambda p: (p['produto'], p['preco']))


HTML = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Smart Price Monitor | Demonstração</title><style>body{font:17px system-ui;background:#101a2c;color:#eef3ff;max-width:900px;margin:48px auto;padding:24px}h1{font-size:36px}input{padding:14px;width:90%;font:inherit;border-radius:8px}article{background:#1c2b43;padding:20px;margin-top:15px;border-radius:12px}small{color:#c3d3e9}.notice{background:#624c13;padding:16px;border-radius:8px}</style>
<h1>Smart Price Monitor</h1><p>Pesquise um produto e compare os valores entre lojas.</p>
<p class="notice">Demonstração com dados inteiramente fictícios. Nenhum preço ou loja representa uma oferta real. Nenhuma API externa é consultada.</p>
<label for="q">Pesquisar produto</label><p><input id="q" placeholder="Notebook ou mouse" type="search"></p><main id="results" aria-live="polite"></main>
<script>const q=document.getElementById('q'),r=document.getElementById('results');let latest=0;async function render(){const version=++latest;try{const data=await(await fetch('/api/produtos?q='+encodeURIComponent(q.value))).json();if(version!==latest)return;r.replaceChildren();if(!data.produtos.length){r.textContent='Nenhum produto encontrado.';return}for(const p of data.produtos){const a=document.createElement('article'),h=document.createElement('h2'),v=document.createElement('p'),s=document.createElement('small');h.textContent=p.produto;v.textContent=p.loja+' — '+p.preco.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});s.textContent=p.preco===p.menor_preco?'Menor preço nesta demonstração':'Diferença para o menor preço: '+(p.preco-p.menor_preco).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});a.append(h,v,s);r.append(a)}}catch{r.textContent='Não foi possível carregar os dados.'}}q.addEventListener('input',render);render();</script></html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == '/api/produtos':
            data = {'demonstracao': True, 'produtos': comparar(parse_qs(url.query).get('q', [''])[0])}
            body = json.dumps(data, ensure_ascii=False).encode()
            content_type = 'application/json; charset=utf-8'
        elif url.path == '/':
            body, content_type = HTML.encode(), 'text/html; charset=utf-8'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    print(f'Demo fictícia em http://127.0.0.1:{args.port}', flush=True)
    HTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
