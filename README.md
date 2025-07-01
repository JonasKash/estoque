# Sistema de Consulta de Estoque

Sistema web para consulta de estoque baseado em planilhas Excel, com interface React e backend Python/Flask. **Agora com assistente de IA para análise inteligente das planilhas!**

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

**Teste do Chat e Análise:**
```bash
python test_chat.py
```

**Acesse no navegador:**
- Frontend: http://localhost:5173
- API: http://localhost:5000

## 🤖 Assistente de IA - Chat Inteligente

O sistema agora inclui um **assistente de IA** que pode analisar as planilhas de estoque e responder perguntas inteligentes:

### 📍 Como Usar o Chat
1. Clique no balão de chat no canto inferior direito da tela
2. Digite suas perguntas em linguagem natural
3. O assistente analisará as planilhas e responderá com insights

### 🔍 Tipos de Análise Disponíveis

#### 📊 Análise de Mudanças
- **Pergunta:** "Mostre as mudanças no estoque"
- **O que faz:** Compara planilhas de diferentes datas
- **Retorna:** Novos itens, itens removidos, mudanças de quantidade

#### 📋 Histórico de Peças
- **Pergunta:** "Histórico da peça A 0001808909"
- **O que faz:** Analisa o histórico completo de uma peça específica
- **Retorna:** Evolução de quantidade, mudanças de localização, estatísticas

#### 📍 Mudanças de Localização
- **Pergunta:** "Análise de localizações"
- **O que faz:** Identifica peças que mudaram de localização
- **Retorna:** Peças que se moveram, trajetória de mudanças

#### 📈 Insights Gerais
- **Pergunta:** "Insights gerais do estoque"
- **O que faz:** Análise estatística completa do estoque
- **Retorna:** Totais, médias, itens críticos, top localizações

### 💡 Exemplos de Perguntas
- "Qual foi a mudança no estoque entre as últimas planilhas?"
- "Histórico da peça A 0001808909"
- "Mostre mudanças de localização"
- "Dê um resumo do estoque"
- "Quais peças foram adicionadas recentemente?"
- "Análise de diferenças entre planilhas"

## 📁 Estrutura do Projeto

```
App/
├── main.py              # Backend Flask com análise inteligente
├── test_api.py          # Script de teste da API
├── test_chat.py         # Script de teste do chat
├── requirements.txt     # Dependências Python
├── package.json         # Dependências Node.js
├── planilhas/          # Planilhas Excel do estoque
├── src/
│   ├── App.jsx         # Componente principal React
│   ├── components/
│   │   ├── ChatWidget.jsx  # Componente do chat inteligente
│   │   └── ui/         # Componentes UI
│   └── main.jsx        # Ponto de entrada
└── README.md           # Este arquivo
```

## 🔧 Endpoints da API

### Endpoints Básicos
- `GET /` - Informações da API
- `GET /health` - Status do sistema
- `GET /stats` - Estatísticas do estoque
- `POST /search` - Busca no estoque

### Endpoints de Análise Inteligente
- `POST /chat/analyze` - Análise inteligente via chat
- `GET /analyze/changes` - Análise de mudanças no estoque
- `GET /analyze/peca/<numero>` - Histórico de uma peça específica
- `GET /analyze/locations` - Análise de mudanças de localização
- `GET /analyze/insights` - Insights gerais do estoque

## 📊 Funcionalidades

### ✅ Funcionalidades Básicas
- Carregamento automático de planilhas Excel
- Busca por número da peça, descrição ou localização
- Estatísticas em tempo real
- Interface moderna e responsiva
- Tratamento de erros robusto

### 🤖 Funcionalidades de IA
- **Análise temporal:** Compara planilhas de diferentes datas
- **Identificação de mudanças:** Detecta novos itens, remoções e alterações
- **Histórico de peças:** Rastreia a evolução de itens específicos
- **Análise de localização:** Identifica movimentações no estoque
- **Insights inteligentes:** Estatísticas avançadas e tendências
- **Chat natural:** Interface conversacional para consultas

## 🧠 Como Funciona a Análise

### 📅 Análise Temporal
O sistema compara planilhas cronologicamente para identificar:
- **Novos itens:** Peças que aparecem em planilhas mais recentes
- **Itens removidos:** Peças que desapareceram
- **Mudanças de quantidade:** Variações no estoque
- **Mudanças de localização:** Movimentações físicas

### 🔍 Processamento Inteligente
1. **Normalização:** Padroniza nomes de colunas e valores
2. **Comparação:** Analisa diferenças entre datas consecutivas
3. **Agregação:** Calcula estatísticas e tendências
4. **Interpretação:** Gera insights em linguagem natural

## 🐛 Solução de Problemas

### Erro "Failed to fetch"
- Certifique-se de que o backend está rodando (`python main.py`)
- Verifique se a porta 5000 está livre
- Execute `python test_api.py` para diagnosticar

### Erro ao carregar planilhas
- Verifique se as planilhas estão na pasta `planilhas/`
- Certifique-se de que os arquivos são .xlsx
- Verifique se as planilhas têm as colunas necessárias

### Chat não responde
- Execute `python test_chat.py` para verificar as funcionalidades
- Verifique se o backend está carregando as planilhas corretamente
- Confirme se as planilhas têm dados suficientes para análise

### Performance lenta
- O sistema processa todas as planilhas na memória
- Para grandes volumes, considere otimizar as planilhas
- O chat pode demorar alguns segundos para análises complexas

## 🔮 Próximas Funcionalidades

- [ ] Análise preditiva de estoque
- [ ] Alertas automáticos para estoque baixo
- [ ] Relatórios em PDF
- [ ] Integração com sistemas externos
- [ ] Análise de tendências sazonais
- [ ] Dashboard interativo com gráficos

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do backend
2. Execute os scripts de teste
3. Consulte a documentação da API
4. Teste com planilhas menores primeiro

---

**Desenvolvido com ❤️ para análise inteligente de estoque** 