# Smart Price Monitor
Sistema de monitoramento automatizado de preços com scraping modular, armazenamento em PostgreSQL, API local e dashboard interativo para análise de histórico e detecção de quedas.
---
## Visão geral
O **Smart Price Monitor** foi desenvolvido para coletar preços de produtos automaticamente, salvar os dados em banco de dados, detectar variações e exibir tudo em um dashboard interativo.
O projeto foi construído com foco em:
- arquitetura modular
- múltiplas fontes de coleta
- persistência em banco de dados
- visualização de histórico
- detecção de quedas de preço
- tolerância a falhas por fonte
---
## Funcionalidades
- Coleta automatizada de preços
- Arquitetura plugável para múltiplos scrapers
- Armazenamento em PostgreSQL
- API local para acesso aos dados
- Dashboard interativo com Streamlit
- Histórico de preços por produto
- Detecção de quedas reais e suspeitas
- Filtros por fonte, título e quantidade mínima de registros
- Separação entre fontes estáveis, experimentais e temporariamente desativadas
---
## Stack utilizada
### Backend
- Python
- PostgreSQL
- psycopg2
### Scraping
- Playwright
- Requests
- BeautifulSoup
### Visualização
- Streamlit
- Pandas
---
## Estrutura do projeto
```bash
web-scraper/
├── api.py
├── agent.py
├── dashboard.py
├── main.py
├── smart_scraper.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   └── db.py
│
├── scraper/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── price_detector.py
│   ├── scraper_loader.py
│   └── utils.py
│
├── scrapers/
│   ├── base_scraper.py
│   ├── books_scraper.py
│   ├── mercadolivre_scraper.py
│   ├── magalu_scraper.py
│   └── casasbahia_scraper.py
│
├── data/
├── logs/
├── dist/
├── build/
└── legacy/


Como o sistema funciona
1. Coleta
O agente percorre automaticamente os scrapers disponíveis e executa a coleta de dados.
2. Persistência
Os dados coletados são salvos no PostgreSQL com:
    • título
    • preço
    • link
    • fonte
    • data da coleta
3. Análise
Após salvar os dados, o sistema:
    • calcula preço médio
    • calcula preço mínimo
    • calcula preço máximo
    • compara com registros anteriores
4. Detecção de quedas
O projeto classifica quedas em:
    • quedas reais
    • quedas suspeitas
5. Visualização
O dashboard permite:
    • filtrar por fonte
    • pesquisar produtos
    • visualizar histórico
    • identificar variações
    • consultar quedas registradas

Fontes implementadas
BooksScraper
Fonte estável usada para testes, validação da arquitetura e demonstração do sistema.
MercadoLivreScraper
Fonte principal experimental. Usa Playwright local e consegue coletar dados reais, mas pode capturar conteúdo misturado do marketplace, como blocos informativos e títulos editoriais.
NewsScraper
Fonte auxiliar usada para demonstrar arquitetura multi-fonte.
MagaluScraper
Implementado como tentativa de expansão, mas temporariamente desativado devido a bloqueios por CAPTCHA e mecanismos anti-bot.
CasasbahiaScraper
Implementado como tentativa adicional, mas temporariamente desativado devido a resposta 403/bloqueio direto.

Limitações atuais
Este projeto foi construído como produto experimental funcional e case de portfólio. Algumas limitações conhecidas:
    • fontes de e-commerce modernas podem aplicar anti-bot
    • scrapers de marketplace podem capturar ruído junto com produtos reais
    • Mercado Livre pode exigir verificação ou alterar o comportamento da página
    • algumas fontes públicas podem bloquear requests simples com 403 ou CAPTCHA
    • o projeto ainda não utiliza autenticação de usuários nem arquitetura multi-tenant

Banco de dados
O sistema usa PostgreSQL com pelo menos estas tabelas:
produtos
Armazena todos os dados coletados.
Campos principais:
    • id
    • titulo
    • preco
    • link
    • fonte
    • data_coleta
quedas_detectadas
Armazena as quedas classificadas pelo detector.
Campos principais:
    • id
    • titulo
    • preco_anterior
    • preco_atual
    • fonte
    • tipo
    • link
    • data_detectada

Como rodar o projeto
1. Clonar o repositório
git clone <url-do-repositorio>
cd web-scraper
2. Criar e ativar ambiente virtual
python -m venv .venv
.venv\Scripts\activate
3. Instalar dependências
pip install -r requirements.txt
4. Instalar navegador do Playwright
playwright install chromium
5. Configurar PostgreSQL
Crie o banco:
CREATE DATABASE scraper_db;
Depois crie as tabelas necessárias.
6. Rodar o agente
python smart_scraper.py
7. Rodar o dashboard
streamlit run dashboard.py
8. Rodar a API
uvicorn api:app --reload

Exemplo de uso
Fluxo típico:
    1. o agente coleta os dados
    2. salva tudo no banco
    3. detecta quedas
    4. o dashboard mostra histórico, métricas e alertas
    5. a API pode ser usada por integrações futuras

Possíveis evoluções futuras
    • autenticação de usuários
    • alertas por e-mail ou WhatsApp
    • filtros por categoria e faixa de preço
    • exportação para CSV/Excel
    • comparação entre múltiplas lojas estáveis
    • painel administrativo
    • arquitetura SaaS multi-cliente
    • integração com agentes de IA para análise e recomendação de compra

Objetivo do projeto
Este projeto foi desenvolvido como:
    • case técnico de scraping real
    • demonstração de arquitetura modular
    • base para monitoramento de preços
    • peça de portfólio para backend, automação e dados
    • prova prática de construção de produto funcional com Python

Status
Funcional e demonstrável
Estado atual:
    • dashboard funcional
    • API funcional
    • banco funcional
    • scraping modular funcional
    • detecção de quedas funcional
    • fontes adicionais em modo experimental/desativado

Autor
Desenvolvido por Matheus Galo como projeto de portfólio e produto experimental de monitoramento de preços.