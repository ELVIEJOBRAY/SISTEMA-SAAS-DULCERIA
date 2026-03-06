# SGDD — Sistema de Gestión de Dulcerías
**Tesis: Bryan Stiven Bonilla | Ingeniería de Sistemas**

Sistema SaaS Multi-Tenant para gestión integral de dulcerías con bot conversacional NLP.

---

## 🏗️ Estructura del Proyecto

```
sgdd/
├── backend/                    # Python + FastAPI
│   ├── main.py                 # Punto de entrada API REST
│   ├── database.py             # Conexión PostgreSQL (SQLAlchemy)
│   ├── models.py               # Modelos ORM (todas las entidades)
│   ├── schemas.py              # Schemas Pydantic (validación)
│   ├── auth.py                 # JWT + bcrypt
│   ├── requirements.txt        # Dependencias Python
│   ├── routers/
│   │   ├── productos.py        # CRUD productos
│   │   └── pedidos.py          # Pedidos + Bot endpoint
│   └── bot/
│       └── nlp_engine.py       # Motor NLP (clasificador intenciones)
│
├── frontend/                   # HTML5 + CSS3 + JavaScript
│   ├── index.html              # SPA principal
│   ├── css/
│   │   └── styles.css          # CSS3 completo (variables, layout, componentes)
│   └── js/
│       ├── api.js              # Cliente REST + Auth JWT
│       └── app.js              # Lógica SPA (routing, vistas, eventos)
│
└── database/
    └── schema.sql              # PostgreSQL schema completo
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 + FastAPI + SQLAlchemy |
| Base de datos | PostgreSQL 15 |
| Frontend | HTML5 + CSS3 + JavaScript (ES2022) |
| Auth | JWT (python-jose) + bcrypt |
| NLP Bot | Motor de reglas (regex + scoring) |
| ORM | SQLAlchemy 2.0 |

---

## ⚡ Inicio Rápido


1. Abrir una terminal en el proyecto
Abre PowerShell.
Cambia al directorio del proyecto:

cd "C:\Users\elvie\Documents\SISTEMA FINAL"
🐘 2. Crear y poblar la base de datos PostgreSQL
Si ya tienes Postgre instalado:


psql -U postgres
Dentro del prompt de psql ejecuta:


CREATE DATABASE sgdd_db;CREATE USER sgdd_user WITH PASSWORD 'sgdd_pass';GRANT ALL ON DATABASE sgdd_db TO sgdd_user;\q
Y luego aplica el esquema:


psql -U sgdd_user -d sgdd_db -f database\schema.sql
➤ esto crea las tablas necesarias en sgdd_db.

🐍 3. Levantar el servidor backend (FastAPI)

cd backendpython -m venv venv               # crea un entorno virtualvenv\Scripts\activate             # actívalo en Windowspip install -r requirements.txt   # instala dependencias# define las variables de entorno necesarias$env:DATABASE_URL="postgresql://sgdd_user:sgdd_pass@localhost:5432/sgdd_db"$env:JWT_SECRET_KEY="mi_clave_secreta"# ejecutar la aplicaciónpython main.py
Verás mensajes en la consola indicando que FastAPI se inició.
La API queda disponible en http://localhost:8000.
Puedes abrir en el navegador http://localhost:8000/api/docs para ver la documentación automática.
🌐 4. Probar el frontend
Tienes dos opciones:

Abrir directamente:

Haz doble clic en frontend\index.html o arrástralo a tu navegador.
Servirlo con un servidor simple:


cd frontendpython -m http.server 3000
Después visita http://localhost:3000.

✅ ¿Qué significa “está corriendo”?
La base de datos existe y tiene las tablas.
El proceso python main.py está en ejecución y responde en el puerto 8000.
El navegador puede cargar el frontend (index.html) y, al hacer clic en botones, ese código usa api.js para llamar a la API.
Si alguno de esos pasos falla (por ejemplo, el backend no inicia porque no encuentra DATABASE_URL), aparecerá un error en la consola; corrígelo y vuelve a intentarlo.

Si necesitas acompañamiento en alguna de las líneas de comando o algún error concreto, copia aquí lo que ves y te ayudo a resolverlo




### 1. Base de datos PostgreSQL

```bash
# Crear base de datos
psql -U postgres -c "CREATE DATABASE sgdd_db;"
psql -U postgres -c "CREATE USER sgdd_user WITH PASSWORD 'sgdd_pass';"
psql -U postgres -c "GRANT ALL ON DATABASE sgdd_db TO sgdd_user;"

# Ejecutar schema
psql -U sgdd_user -d sgdd_db -f database/schema.sql
```

### 2. Backend Python

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Variables de entorno
export DATABASE_URL="postgresql://sgdd_user:sgdd_pass@localhost:5432/sgdd_db"
export JWT_SECRET_KEY="tu-clave-secreta-segura"

# Ejecutar
python main.py
# API disponible en: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

### 3. Frontend

```bash
# Abrir directamente en el navegador
open frontend/index.html

# O servir con cualquier servidor HTTP:
cd frontend && python -m http.server 3000
```

---

## 🗄️ Modelo de Datos

```
tenants ─┬─── usuarios
         ├─── productos ──── inventario
         │                └── inventario_lotes (FIFO)
         ├─── clientes
         ├─── pedidos ──── detalle_pedidos
         ├─── conversaciones_bot
         └─── auditoria
```

**Aislamiento Multi-Tenant:** Toda tabla incluye `tenant_id` como filtro obligatorio.

---

## 🤖 Bot Conversacional NLP

### Intenciones soportadas

| Intención | Ejemplo |
|-----------|---------|
| `crear_pedido` | "Quiero 5 chocolates Jet" |
| `consultar_precio` | "¿Cuánto cuesta un Bon Bon Bum?" |
| `consultar_stock` | "¿Tienen gomitas disponibles?" |
| `cotizacion_evento` | "Necesito surtido para piñata" |
| `estado_pedido` | "¿Dónde está mi pedido?" |
| `saludo` | "Hola buenas tardes" |

### Métricas de Aceptación (ISO/IEC 25010)

| Métrica | Objetivo |
|---------|---------|
| Precisión | ≥ 0.90 |
| Recall | ≥ 0.85 |
| F1-Score | ≥ 0.88 |
| T_respuesta (p95) | ≤ 3000 ms |

### Regla de escalado

```
Si confianza_NLP < 0.75 → escalar a operador humano
```

---

## 🔐 Seguridad (Multi-Tenant)

- **JWT** con `tenant_id` embebido en el payload
- **bcrypt** (rounds=12) para hash de contraseñas
- **HTTPS** obligatorio en producción
- **Middleware multi-tenant**: cada query filtra por `tenant_id`
- **Auditoría**: registro de todas las acciones

---

## 📊 Endpoints principales

```
POST   /api/v1/auth/login            Login JWT
GET    /api/v1/auth/me               Perfil usuario
POST   /api/v1/auth/register-tenant  Nueva dulcería

GET    /api/v1/productos             Listar productos
POST   /api/v1/productos             Crear producto
PATCH  /api/v1/productos/{id}        Actualizar producto

GET    /api/v1/pedidos               Listar pedidos
POST   /api/v1/pedidos               Crear pedido
PATCH  /api/v1/pedidos/{id}/estado   Cambiar estado

POST   /api/v1/bot/mensaje           Procesar mensaje NLP
```

---

## 🎓 Estándares Aplicados

- **ISO/IEC 25010** — Calidad del software
- **ISO/IEC/IEEE 29148** — Especificación de requisitos
- **Clean Architecture** — Separación en capas
- **FIFO** — Rotación de inventario perecedero

---

## 👤 Autor

**Bryan Stiven Bonilla**  
Ingeniería de Sistemas | Investigación I
