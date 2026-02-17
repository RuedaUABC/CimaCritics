# 🚀 Guía de Deployment - CimaCritics

## 1. Pre-requisitos
- Python 3.8+
- PostgreSQL (producción) o SQLite (desarrollo)
- Git
- Cuenta en plataforma de hosting

## 2. Opciones de Deployment

### 2.1 Heroku (Recomendado para principiantes)
**Ventajas:**
- Fácil setup
- Base de datos PostgreSQL incluida
- Auto-scaling
- Integración Git

**Desventajas:**
- Costo por uso
- Limitaciones en algunos add-ons

### 2.2 PythonAnywhere
**Ventajas:**
- Especializado en Python
- Fácil deployment
- Precios accesibles

**Desventajas:**
- Menos flexible que VPS
- Limitaciones de recursos

### 2.3 VPS (DigitalOcean, Linode, AWS)
**Ventajas:**
- Control total
- Escalabilidad
- Costo-efectivo a largo plazo

**Desventajas:**
- Requiere más configuración
- Mantenimiento del servidor

## 3. Deployment en Heroku

### 3.1 Preparación
```bash
# Instalar Heroku CLI
# Crear cuenta en Heroku
heroku login

# Crear app
heroku create cima-critics

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev
```

### 3.2 Configuración
```python
# config.py - Agregar configuración de producción
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
```

### 3.3 Archivos Necesarios
**requirements.txt:**
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-JWT-Extended==4.5.2
Flask-CORS==4.0.0
psycopg2-binary==2.9.7
python-dotenv==1.0.0
bcrypt==4.0.1
```

**Procfile:**
```
web: python app.py
```

**runtime.txt:**
```
python-3.8.16
```

### 3.4 Variables de Entorno
```bash
heroku config:set SECRET_KEY="tu-secret-key-aqui"
heroku config:set JWT_SECRET_KEY="tu-jwt-secret-aqui"
heroku config:set FLASK_ENV="production"
```

### 3.5 Deploy
```bash
# Commit cambios
git add .
git commit -m "Ready for deployment"

# Push a Heroku
git push heroku main

# Ejecutar migraciones
heroku run python manage.py db upgrade

# Abrir app
heroku open
```

## 4. Deployment en PythonAnywhere

### 4.1 Setup
1. Crear cuenta en PythonAnywhere
2. Crear web app con Flask
3. Configurar dominio (opcional)

### 4.2 Configuración
- Subir código via Git o FTP
- Instalar dependencias en virtualenv
- Configurar variables de entorno
- Configurar base de datos MySQL/PostgreSQL

## 5. Deployment en VPS

### 5.1 Preparación del Servidor
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade

# Instalar Python y pip
sudo apt install python3 python3-pip python3-venv

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Instalar Nginx
sudo apt install nginx

# Instalar Gunicorn
pip install gunicorn
```

### 5.2 Configuración de la Aplicación
```bash
# Crear directorio del proyecto
sudo mkdir /var/www/cima-critics
cd /var/www/cima-critics

# Clonar repositorio
git clone https://github.com/RuedaUABC/CimaCritics.git .

# Crear virtualenv
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 5.3 Configuración de PostgreSQL
```bash
# Crear usuario y base de datos
sudo -u postgres psql
CREATE USER cima_critics WITH PASSWORD 'tu_password';
CREATE DATABASE cima_critics OWNER cima_critics;
\q
```

### 5.4 Configuración de Gunicorn
**gunicorn.conf.py:**
```python
bind = "127.0.0.1:8000"
workers = 3
user = "www-data"
group = "www-data"
tmp_upload_dir = None
```

### 5.5 Configuración de Nginx
**/etc/nginx/sites-available/cima-critics:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static {
        alias /var/www/cima-critics/static;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/cima-critics /etc/nginx/sites-enabled

# Probar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 5.6 Configuración de Systemd
**/etc/systemd/system/cima-critics.service:**
```ini
[Unit]
Description=CimaCritics Flask app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/cima-critics
Environment="PATH=/var/www/cima-critics/venv/bin"
ExecStart=/var/www/cima-critics/venv/bin/gunicorn --config gunicorn.conf.py app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar servicio
sudo systemctl start cima-critics
sudo systemctl enable cima-critics
```

### 5.7 SSL con Let's Encrypt
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com
```

## 6. Monitoreo y Mantenimiento

### 6.1 Logs
```bash
# Ver logs de la aplicación
sudo journalctl -u cima-critics -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

### 6.2 Backups
```bash
# Backup de base de datos
pg_dump cima_critics > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup de archivos
tar -czf backup_files_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/cima-critics
```

### 6.3 Monitoreo
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Error tracking**: Sentry
- **Performance**: New Relic, DataDog
- **Logs**: ELK Stack

## 7. Troubleshooting Común

### 7.1 Error 500
- Verificar logs de la aplicación
- Comprobar configuración de base de datos
- Validar variables de entorno

### 7.2 Problemas de Conexión a BD
- Verificar credenciales
- Comprobar conectividad de red
- Validar permisos de usuario

### 7.3 Problemas de Rendimiento
- Optimizar consultas SQL
- Implementar caché
- Configurar workers de Gunicorn

## 8. Checklist de Deployment
- [ ] Código probado en staging
- [ ] Variables de entorno configuradas
- [ ] Base de datos migrada
- [ ] Archivos estáticos servidos correctamente
- [ ] SSL configurado
- [ ] Dominio apuntando correctamente
- [ ] Monitoreo configurado
- [ ] Backups automáticos
- [ ] Documentación de mantenimiento