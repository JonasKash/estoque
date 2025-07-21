# Estoque Guvito - Sistema de Consulta e Análise de Planilhas

Sistema web para consulta e análise de estoque a partir de planilhas Excel, com interface moderna em React, backend Python/Flask, deploy via Docker, Nginx e Traefik.

---

## 🚀 Como Funciona
- **Frontend:** React, build estático servido por Nginx
- **Backend:** Flask, leitura dinâmica das planilhas a cada busca
- **Proxy/API:** Nginx faz proxy do frontend para o backend em `/api`
- **Orquestração:** Docker Compose
- **Roteamento:** Traefik gerencia domínios e HTTPS

---

## 📦 Estrutura do Projeto
```
App/
├── Dockerfile.backend         # Backend Flask
├── Dockerfile.frontend        # Frontend React + Nginx
├── docker-compose.yml         # Orquestra tudo
├── nginx.conf                 # Configuração do Nginx
├── DEPLOY.md                  # Guia de deploy detalhado
├── planilhas/                 # Suas planilhas .xlsx
├── src/                       # Código React
├── main.py                    # Backend Flask
├── requirements.txt           # Dependências Python
├── package.json               # Dependências Node.js
└── ...
```

---

## 🌐 Variáveis de Ambiente
- **Frontend:** Usa `VITE_BACKEND_URL` (em produção já configurado para `/api` via docker-compose)
- **Backend:** Porta 5000

---

## 🛠️ Build e Deploy (Resumo)
1. **Clone o projeto e entre na pasta App:**
   ```sh
   git clone <repo> estoque-guvito
   cd estoque-guvito/App
   ```
2. **Coloque suas planilhas .xlsx na pasta `planilhas/`**
3. **Suba os containers:**
   ```sh
   sudo docker-compose up -d --build
   ```
4. **Configure o DNS:**
   - `www.estoque.guvito.site` → IP do servidor
   - (Opcional) `api.estoque.guvito.site` → IP do servidor
5. **Acesse:**
   - Frontend: http://www.estoque.guvito.site
   - API: http://api.estoque.guvito.site
   - Traefik dashboard: http://<seu-ip-ou-dominio>:8080

---

## 🔄 Atualizar código
```sh
git pull
sudo docker-compose up -d --build
```

---

## 🐞 Troubleshooting
- **Planilhas não aparecem:**
  - Confirme que estão em `App/planilhas/` e são `.xlsx`
  - Veja logs do backend: `docker logs estoque-backend`
- **Erro 404:**
  - Acesse sempre pelo domínio configurado
  - Verifique se containers estão rodando: `docker ps`
- **Backend não responde:**
  - Veja se a porta 5000 está exposta no container backend
- **Frontend não mostra dados:**
  - Veja se o build do React está ok e o Nginx está servindo `/api` corretamente

---

## 📄 Documentação de Deploy
Veja o arquivo [DEPLOY.md](./DEPLOY.md) para instruções detalhadas de deploy, DNS, atualização e troubleshooting.

---

**Dúvidas? Só perguntar!** 