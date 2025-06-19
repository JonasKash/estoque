# Sistema de Consulta de Estoque

Sistema web para consulta de estoque baseado em planilhas Excel, com interface React e backend Python/Flask.

## 🚀 Como Executar

### 1. Instalar Dependências

**Backend (Python):**
```bash
pip install -r requirements.txt
```

**Frontend (Node.js):**
```bash
npm install
```

### 2. Executar o Sistema

**Terminal 1 - Backend:**
```bash
python main.py
```
O servidor Flask será iniciado em `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
npm run dev
```
O servidor de desenvolvimento será iniciado em `http://localhost:5173`

### 3. Testar o Sistema

**Teste da API:**
```bash
python test_api.py
```

**Acesse no navegador:**
- Frontend: http://localhost:5173
- API: http://localhost:5000

## 📁 Estrutura do Projeto

```
App/
├── main.py              # Backend Flask
├── test_api.py          # Script de teste
├── requirements.txt     # Dependências Python
├── package.json         # Dependências Node.js
├── planilhas/          # Planilhas Excel do estoque
├── src/
│   ├── App.jsx         # Componente principal React
│   └── components/     # Componentes UI
└── README.md           # Este arquivo
```

## 🔧 Endpoints da API

- `GET /` - Informações da API
- `GET /health` - Status do sistema
- `GET /stats` - Estatísticas do estoque
- `POST /search` - Busca no estoque

## 📊 Funcionalidades

- ✅ Carregamento automático de planilhas Excel
- ✅ Busca por número da peça, descrição ou localização
- ✅ Estatísticas em tempo real
- ✅ Interface moderna e responsiva
- ✅ Tratamento de erros robusto

## 🐛 Solução de Problemas

### Erro "Failed to fetch"
- Certifique-se de que o backend está rodando (`python main.py`)
- Verifique se a porta 5000 está livre
- Execute `python test_api.py` para diagnosticar

### Erro ao carregar planilhas
- Verifique se as planilhas estão na pasta `planilhas/`
- As planilhas devem ter as colunas: `Numero da Peca`, `Descricao`, `Quantidade`, `Localizacao`

### CORS errors
- O backend já está configurado com CORS
- Se persistir, verifique se está acessando a URL correta

## 📝 Exemplos de Uso

1. **Buscar por descrição:** "filtro de óleo"
2. **Buscar por número:** "A 0001808909"
3. **Buscar por localização:** "estrado 5"

## 🔄 Atualização de Dados

Para atualizar os dados:
1. Adicione novas planilhas na pasta `planilhas/`
2. Reinicie o backend (`python main.py`)
3. Os dados serão carregados automaticamente

## 📞 Suporte

Se encontrar problemas:
1. Execute `python test_api.py` para diagnosticar
2. Verifique os logs no terminal do backend
3. Confirme se todas as dependências estão instaladas 