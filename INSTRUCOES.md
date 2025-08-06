# Sistema de Consulta de Estoque - Instruções

## Melhorias Implementadas

### 1. Correção de Erros do openpyxl
- **Problema**: Erro `TypeError: expected <class 'str'>` ao carregar algumas planilhas
- **Solução**: Implementado sistema de fallback usando pandas quando openpyxl falha
- **Benefício**: Maior compatibilidade com diferentes formatos de planilha

### 2. Sistema de Timeout
- **Problema**: Busca infinita sem limite de tempo
- **Solução**: Implementado timeout de 30 segundos tanto no backend quanto no frontend
- **Benefício**: Usuário recebe feedback claro quando a busca demora muito

### 3. Cache de Dados
- **Problema**: Processamento lento das planilhas a cada busca
- **Solução**: Cache de 5 minutos para dados processados
- **Benefício**: Buscas subsequentes são muito mais rápidas

### 4. Melhor Feedback Visual
- **Problema**: Interface não mostrava progresso da busca
- **Solução**: Barra de progresso e mensagens de status claras
- **Benefício**: Usuário sabe que o sistema está funcionando

### 5. Tratamento de Erros Robusto
- **Problema**: Erros não tratados causavam travamentos
- **Solução**: Try-catch em todas as operações críticas
- **Benefício**: Sistema mais estável e confiável

## Como Usar

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o sistema**:
   ```bash
   python app.py
   ```

3. **Acessar no navegador**:
   ```
   http://localhost:5000
   ```

## Funcionalidades

### Busca de Peças
- Digite o código da peça no campo de busca
- Clique em "Buscar" ou pressione Enter
- O sistema procurará em todas as planilhas disponíveis
- Timeout de 30 segundos garante resposta rápida

### Resultados
- **Localização**: Onde a peça está armazenada
- **Quantidade**: Quantidade disponível em estoque
- **Nome da Peça**: Descrição completa da peça

### Tratamento de Erros
- **Peça não encontrada**: Mensagem clara quando o código não existe
- **Timeout**: Aviso quando a busca demora mais de 30 segundos
- **Erro de conexão**: Feedback quando há problemas de rede

## Estrutura de Arquivos

```
App/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── templates/
│   └── index.html        # Interface web
├── planilhas/            # Pasta com as planilhas Excel
└── INSTRUCOES.md         # Este arquivo
```

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Processamento**: openpyxl, pandas
- **Cache**: Sistema de cache em memória
- **Timeout**: Threading para controle de tempo

## Melhorias de Performance

1. **Cache Inteligente**: Dados processados ficam em cache por 5 minutos
2. **Fallback de Bibliotecas**: Se openpyxl falha, usa pandas
3. **Timeout Eficiente**: Threading para não bloquear a interface
4. **Processamento Otimizado**: Carregamento apenas de dados necessários

## Troubleshooting

### Erro ao carregar planilhas
- Verifique se as planilhas estão na pasta `planilhas/`
- Certifique-se de que são arquivos Excel (.xlsx ou .xls)
- Verifique se as planilhas não estão corrompidas

### Busca muito lenta
- O sistema tem cache de 5 minutos
- Primeira busca pode ser mais lenta
- Buscas subsequentes serão mais rápidas

### Timeout frequente
- Verifique se há muitas planilhas grandes
- Considere dividir planilhas muito grandes
- Verifique a performance do servidor

## Desenvolvido por Jonas
Sistema otimizado para consulta rápida e eficiente de estoque. 