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

## 3. Liberar a porta no firewall (UFW)

> ⚠️ **Passo obrigatório.** O 1-Click Docker Droplet da DigitalOcean já vem com o UFW ativado, liberando por padrão **apenas** as portas `22` (SSH), `2375` e `2376` (Docker). Sem liberar a `8000`, a API não fica acessível de fora, mesmo com o container rodando perfeitamente.

```bash
sudo ufw allow 8000/tcp
sudo ufw status
```

Confirme que `8000/tcp` aparece como `ALLOW` na lista antes de seguir.

---

## 4. Clonar o projeto e configurar

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
```

> O `.env` é lido pelo `docker-compose.yml` via `env_file`, então nenhuma credencial fica hardcoded no compose. Adicione `.env` ao `.gitignore` para não subir isso pro GitHub:
> ```bash
> echo ".env" >> .gitignore
> ```

---

## 5. Configuração necessária no projeto (já resolvida no repositório)

As três correções abaixo já fazem parte do projeto a partir desta versão — ficam documentadas aqui apenas como referência, caso clone um fork antigo ou precise depurar de novo.

### 5.1. Banco SQLite com volume persistente

O `docker-compose.yml` usa um **volume nomeado** apontando para um **diretório** (nunca para o arquivo `.sqlite3` direto — montar um volume nomeado direto num arquivo faz o Docker criar uma pasta no lugar dele, e o Django não consegue abrir o "arquivo"):

```yaml
services:
  api:
    build: .
    container_name: api-escola
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - sqlite_data:/app/data

volumes:
  sqlite_data:
```

E o `settings.py` aponta o banco para dentro dessa pasta:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data" / "db.sqlite3",
    }
}
```

O `entrypoint.sh` garante que a pasta existe antes de qualquer comando do Django rodar (evita o erro `unable to open database file` caso o volume seja recriado do zero):

```bash
#!/bin/bash

# Garante que a pasta do banco de dados existe
mkdir -p /app/data

echo "Running database migrations..."
python manage.py migrate --noinput
# ... resto do entrypoint
```

### 5.2. Arquivos estáticos do Admin (CSS/JS) com WhiteNoise

Com `DEBUG=False`, o Django não serve arquivos estáticos por conta própria, e o Gunicorn também não — por isso o admin carregava sem nenhum CSS. A correção usa a lib `whitenoise`:

**`requirements.txt`** — adicionar:
```
whitenoise
```

**`settings.py`** — middleware (logo após o `SecurityMiddleware`):
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ... resto dos middlewares
]
```

**`settings.py`** — storage:
```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

> Se ao trocar para o `CompressedManifestStaticFilesStorage` aparecer um erro do tipo `Missing staticfiles manifest entry`, geralmente é um template referenciando um arquivo estático que não existe — nesse caso revisar os templates ou usar uma variante menos estrita do storage.

---

## 6. Subir o container

```bash
docker compose up -d --build
docker compose logs -f
# Pressione Ctrl+C para sair dos logs
```

> Se em algum momento o banco ou o volume ficarem em um estado inconsistente (ex: erro de `unable to open database file` mesmo após as correções acima), derrube tudo incluindo os volumes e recrie do zero:
> ```bash
> docker compose down -v
> docker compose build --no-cache
> docker compose up -d
> ```

---

## 7. Verificar se está funcionando

```bash
# Ver containers rodando
docker compose ps

# Testar localmente, de dentro do próprio Droplet
# (isola se o problema é rede/firewall ou se é o Django)
curl -I http://localhost:8000/admin/

# Ver logs novamente se precisar
docker compose logs
```

---

## 8. Acessar sua API

Use **http://**, não https — o Gunicorn não tem TLS configurado (TLS só entra na seção 9, com Nginx + Certbot).

- **API:** `http://SEU_IP_AQUI:8000/api/v1/`
- **Admin:** `http://SEU_IP_AQUI:8000/admin/`
- **Swagger:** `http://SEU_IP_AQUI:8000/swagger/`

Login admin: `admin` / `admin123`

---

## 9. (Opcional) Colocar domínio + SSL com Nginx

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

> Depois de ativar o SSL, liberar a porta 443 no firewall também:
> ```bash
> sudo ufw allow 443/tcp
> sudo ufw allow 80/tcp
> ```

---

## 10. Comandos úteis para manutenção

```bash
# Atualizar o projeto (após dar git push)
cd /opt/api-escola
git pull
docker compose down
docker compose up -d --build

# Parar containers
docker compose down

# Ver logs
docker compose logs -f

# Acessar o container
docker exec -it api-escola bash

# Ver firewall ativo
sudo ufw status
```

---

## 🛑 **IMPORTANTE SOBRE SQLITE**

SQLite funciona mas tem limitações em produção:
- Não lida bem com muitas requisições simultâneas
- Se o container reiniciar **sem o volume correto**, perde os dados

**Solução para não perder dados:** O `docker-compose.yml` já tem um volume persistente `sqlite_data` montado em `/app/data` (um diretório, não o arquivo direto), então seus dados são salvos mesmo se o container reiniciar ou for recriado.

Se no futuro você quiser migrar para PostgreSQL, é só me pedir!