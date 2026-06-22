# Guia de Deploy no DigitalOcean (Droplet Docker)

## Requisitos
- Conta no DigitalOcean
- Seu projeto já está no GitHub: https://github.com/WebEvolui/Curso-Django-REST-Framework-crie-APIs-com-Python.git

---

## 1. Criar o Droplet no DigitalOcean

1. Acesse https://cloud.digitalocean.com
2. Clique em **"Create"** → **"Droplets"**
3. Em **"Choose an image"** → **"Marketplace"** → pesquise **"Docker"**
4. Escolha o plano (recomendo **$6/mês** - 1GB RAM, 1 vCPU)
5. Escolha um datacenter próximo (ex: NYC3)
6. Em **"Authentication"**, escolha **SSH Key** ou **Password**
7. Dê um nome ao Droplet (ex: `api-escola`)
8. Clique em **"Create Droplet"**

---

## 2. Conectar no Droplet via SSH

```bash
ssh root@SEU_IP_AQUI
```

> **Nota:** O IP aparece no painel do DigitalOcean após criar o Droplet.

---

## 3. Clonar o projeto e rodar

Execute estes comandos no terminal do Droplet:

```bash
# Clonar o repositório
cd /opt
git clone https://github.com/WebEvolui/Curso-Django-REST-Framework-crie-APIs-com-Python.git api-escola
cd api-escola

# Criar .env com suas configurações de produção
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=coloque-uma-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,SEU_IP_AQUI
CORS_ALLOWED_ORIGINS=http://localhost:8042,http://127.0.0.1:8042,http://SEU_IP_AQUI:8042
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin123
DJANGO_SUPERUSER_EMAIL=admin@example.com
EOF

# GERAR UMA SECRET_KEY FORTE (importante!):
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# Copie o resultado e cole no .env no lugar de "coloque-uma-chave-secreta-aqui"
# Depois rode:

# Subir o container
docker compose up -d

# Ver logs
docker compose logs -f

# Pressione Ctrl+C para sair dos logs
```

---

## 4. Verificar se está funcionando

```bash
# Ver containers rodando
docker ps

# Testar a API
curl http://localhost:8000/api/v1/

# Ver logs novamente se precisar
docker compose logs
```

---

## 5. Acessar sua API

- **API:** `http://SEU_IP_AQUI:8000/api/v1/`
- **Admin:** `http://SEU_IP_AQUI:8000/admin/`
- **Swagger:** `http://SEU_IP_AQUI:8000/swagger/`

Login admin: `admin` / `admin123`

---

## 6. (Opcional) Colocar domínio + SSL com Nginx

Acesse o Droplet via SSH e execute:

```bash
# Instalar Nginx e Certbot
apt update && apt install -y nginx certbot python3-certbot-nginx

# Criar configuração
cat > /etc/nginx/sites-available/api-escola << 'NGINX'
server {
    listen 80;
    server_name SEU_DOMINIO_AQUI;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/api-escola/staticfiles/;
    }
}
NGINX

# Ativar
ln -s /etc/nginx/sites-available/api-escola /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# Certificado SSL (Let's Encrypt)
certbot --nginx -d SEU_DOMINIO_AQUI
```

---

## 7. Comandos úteis para manutenção

```bash
# Atualizar o projeto (após dar git push)
cd /opt/api-escola
git pull
docker compose down
docker compose up -d

# Parar containers
docker compose down

# Ver logs
docker compose logs -f

# Acessar o container
docker exec -it api-escola bash
```

---

## 🛑 **IMPORTANTE SOBRE SQLITE**

SQLite funciona mas tem limitações em produção:
- Não lida bem com muitas requisições simultâneas
- Se o container reiniciar sem o volume, perde os dados

**Solução para não perder dados:** O `docker-compose.yml` já tem um volume persistente `sqlite_data`, então seus dados serão salvos mesmo se o container reiniciar.

Se no futuro você quiser migrar para PostgreSQL, é só me pedir!