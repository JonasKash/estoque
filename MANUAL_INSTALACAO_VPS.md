# 📋 Manual de Instalação - Sistema de Consulta de Estoque

## 🚀 Instalação na VPS

### Pré-requisitos
- Ubuntu 20.04+ ou Debian 10+
- Python 3.8+
- Acesso root ou sudo

---

## 📦 Passo 1: Atualizar o Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 🐍 Passo 2: Instalar Python e Dependências

```bash
# Instalar Python 3 e pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar dependências do sistema
sudo apt install nginx supervisor -y
```

---

## 📁 Passo 3: Criar Diretório do Projeto

```bash
# Criar diretório do projeto
sudo mkdir -p /var/www/estoque
sudo chown $USER:$USER /var/www/estoque
cd /var/www/estover
```

---

## 🔧 Passo 4: Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 📊 Passo 5: Preparar Planilhas

```bash
# Criar diretório para planilhas
mkdir planilhas

# Copiar planilhas para o diretório
# (Copie todas as planilhas .xlsx para /var/www/estoque/planilhas/)
```

---

## ⚡ Passo 6: Testar o Sistema

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar o sistema
python app.py
```

**Acesse:** `http://SEU_IP:5000`

---

## 🔄 Passo 7: Configurar como Serviço

### Criar arquivo de configuração do Supervisor

```bash
sudo nano /etc/supervisor/conf.d/estoque.conf
```

**Conteúdo do arquivo:**
```ini
[program:estoque]
directory=/var/www/estoque
command=/var/www/estoque/venv/bin/python app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/estoque.err.log
stdout_logfile=/var/log/estoque.out.log
user=www-data
environment=HOME="/var/www/estoque"
```

### Ativar o serviço

```bash
# Recarregar configurações
sudo supervisorctl reread
sudo supervisorctl update

# Iniciar o serviço
sudo supervisorctl start estoque

# Verificar status
sudo supervisorctl status estoque
```

---

## 🌐 Passo 8: Configurar Nginx (Opcional)

### Criar configuração do Nginx

```bash
sudo nano /etc/nginx/sites-available/estoque
```

**Conteúdo do arquivo:**
```nginx
server {
    listen 80;
    server_name SEU_DOMINIO.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Ativar o site

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/estoque /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

## 🔒 Passo 9: Configurar Firewall

```bash
# Permitir portas necessárias
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

## 📝 Comandos Úteis

### Gerenciar o serviço
```bash
# Parar o serviço
sudo supervisorctl stop estoque

# Iniciar o serviço
sudo supervisorctl start estoque

# Reiniciar o serviço
sudo supervisorctl restart estoque

# Ver logs
sudo tail -f /var/log/estoque.out.log
```

### Atualizar o sistema
```bash
cd /var/www/estoque
source venv/bin/activate
git pull  # se usar git
pip install -r requirements.txt
sudo supervisorctl restart estoque
```

---

## 🛠️ Solução de Problemas

### Verificar se o sistema está rodando
```bash
sudo supervisorctl status estoque
curl http://localhost:5000
```

### Verificar logs
```bash
sudo tail -f /var/log/estoque.err.log
sudo tail -f /var/log/estoque.out.log
```

### Reiniciar tudo
```bash
sudo supervisorctl restart estoque
sudo systemctl restart nginx
```

---

## 📞 Suporte

- **Logs do sistema:** `/var/log/estoque.out.log`
- **Logs de erro:** `/var/log/estoque.err.log`
- **Configuração:** `/etc/supervisor/conf.d/estoque.conf`

---

## ✅ Checklist de Instalação

- [ ] Sistema atualizado
- [ ] Python instalado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Planilhas copiadas
- [ ] Sistema testado
- [ ] Serviço configurado
- [ ] Nginx configurado (opcional)
- [ ] Firewall configurado
- [ ] Sistema funcionando

---

**🎉 Sistema instalado com sucesso!** 