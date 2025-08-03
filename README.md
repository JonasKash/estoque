# 🔍 Sistema de Consulta de Estoque

Sistema web otimizado para consulta rápida de peças em estoque através de códigos.

## ⚡ Características

- **Busca Instantânea**: Índice otimizado para respostas em menos de 1 segundo
- **Normalização de Códigos**: Encontra códigos com ou sem espaços
- **Cache Inteligente**: Carregamento otimizado na inicialização
- **Interface Moderna**: Design responsivo e amigável
- **Auto-recuperação**: Reset automático em caso de erro

## 🚀 Performance

- **Inicialização**: 2-3 segundos
- **Busca**: Instantânea (< 1 segundo)
- **Cache**: Persistente em arquivo
- **Índice**: 2200+ códigos únicos

## 📊 Funcionalidades

### Busca Flexível
- ✅ `A0075422318` - Busca exata
- ✅ `A 0075422318` - Com espaços
- ✅ `a0075422318` - Minúsculo
- ✅ `a 0075422318` - Minúsculo com espaços

### Informações Exibidas
- 📍 **Localização** da peça
- 📦 **Quantidade** em estoque
- 🔧 **Nome/Descrição** da peça
- 📅 **Última alteração** (se disponível)

## 🛠️ Instalação Local

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clonar/Download do projeto**
```bash
cd /caminho/do/projeto
```

2. **Instalar dependências**
```bash
pip install -r requirements.txt
```

3. **Preparar planilhas**
```bash
# Copiar planilhas .xlsx para a pasta planilhas/
```

4. **Executar sistema**
```bash
python app.py
```

5. **Acessar**
```
http://localhost:5000
```

## 🌐 Instalação VPS

Consulte o [Manual de Instalação VPS](MANUAL_INSTALACAO_VPS.md) para instruções completas.

## 📁 Estrutura do Projeto

```
App/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── templates/
│   └── index.html        # Interface web
├── planilhas/            # Planilhas Excel
│   ├── ESTOQUE300525.xlsx
│   └── ...
├── MANUAL_INSTALACAO_VPS.md
└── README.md
```

## 🔧 Configuração

### Planilhas Suportadas
- Formato: `.xlsx`
- Estrutura: Código, Nome, Quantidade, Localização
- Cabeçalho: Linha 3 (padrão)

### Cache
- Arquivo: `cache_dados.pkl`
- Duração: 1 hora
- Recriação: Automática

## 📝 Uso

1. **Abrir o sistema** no navegador
2. **Aguardar** carregamento (2-3 segundos)
3. **Digitar código** da peça
4. **Pressionar Enter** ou clicar em Buscar
5. **Ver resultado** instantâneo

## 🛠️ Comandos Úteis

### Verificar status
```bash
curl http://localhost:5000/api/status
```

### Debug de código
```bash
curl http://localhost:5000/api/debug/CODIGO
```

### Listar planilhas
```bash
curl http://localhost:5000/api/planilhas
```

## 🔍 Solução de Problemas

### Sistema não carrega
- Verificar se planilhas estão na pasta `planilhas/`
- Verificar permissões de arquivo
- Verificar logs do console

### Busca não funciona
- Verificar formato das planilhas
- Verificar se cache foi criado
- Reiniciar aplicação

### Erro de conexão
- Verificar se porta 5000 está livre
- Verificar firewall
- Verificar logs de erro

## 📞 Suporte

- **Desenvolvedor**: Jonas
- **Tecnologia**: Flask + Pandas + OpenPyXL
- **Versão**: 1.0

## 🎯 Melhorias Futuras

- [ ] Busca por nome da peça
- [ ] Histórico de buscas
- [ ] Exportação de dados
- [ ] Múltiplas planilhas simultâneas
- [ ] API REST completa

---

**⚡ Sistema otimizado para máxima performance e usabilidade!** 