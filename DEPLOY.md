# Guia de Deploy - Estoque Guvito

## 1. Pré-requisitos
- Docker e Docker Compose instalados
- Acesso ao domínio www.estoque.guvito.site
- Acesso ao servidor (Linux recomendado)

## 2. Subir para o GitHub
1. Crie uma branch nova:
   ```sh
git checkout -b deploy-docker-nginx-traefik
   ```
2. Adicione, commite e suba:
   ```sh
git add .
git commit -m "Infraestrutura Docker, Nginx, Traefik"
git push origin deploy-docker-nginx-traefik
   ```

## 3. Build e Deploy
No servidor:
```sh
git clone <repo> estoque-guvito
cd estoque-guvito/App
cp -r suas-planilhas-xlsx ./planilhas
sudo docker-compose up -d --build
```

## 4. Configurar DNS
- Aponte o domínio www.estoque.guvito.site para o IP do servidor
- (Opcional) api.estoque.guvito.site para o mesmo IP

## 5. Acessar
- Frontend: http://www.estoque.guvito.site
- Backend API: http://api.estoque.guvito.site
- Traefik dashboard: http://<seu-ip-ou-dominio>:8080

## 6. Atualizar código
```sh
git pull
sudo docker-compose up -d --build
```

---

**Dúvidas? Só perguntar!** 