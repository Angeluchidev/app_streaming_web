# 🧪 Guía de Laboratorio: Desarrollo de App Streaming (Paso a Paso)

Esta guía contiene todo el código necesario para construir la aplicación **StreamFlow**. Sigue cada etapa cuidadosamente.

---

## 📅 Etapa 1: Preparación del Entorno
*Crea la carpeta del proyecto y el entorno aislado.*

1.  **Comandos de Consola:**
    ```bash
    # Crear carpeta e ingresar
    mkdir app_streaming_web
    cd app_streaming_web

    # Crear y activar entorno virtual (Windows)
    python -m venv venv
    .\venv\Scripts\activate

    # Instalar dependencias iniciales
    pip install flask flask-sqlalchemy
    ```

---

## 🏗️ Etapa 2: El Corazón de la App (`app.py`)
*Crea el archivo `app.py` en la raíz con la lógica de las rutas.*

```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de base de datos (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///streaming.db'
db = SQLAlchemy(app)

# Modelo de Datos (Ver DOCUMENTACION_UML.md)
class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    url_video = db.Column(db.String(200))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    # Simulamos datos por ahora (Etapa 3)
    videos = [
        {"id": 1, "titulo": "Aprender Flask", "categoria": "Tutorial"},
        {"id": 2, "titulo": "Desarrollo con Python", "categoria": "Educación"}
    ]
    return render_template('catalogo.html', videos=videos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crea la BD automáticamente
    app.run(debug=True)
```

---

## 🎨 Etapa 3: Diseño con Plantillas (Jinja2)
*Crea la carpeta `/templates` y dentro los siguientes archivos.*

### 1. `templates/base.html` (Plantilla Maestra)
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}StreamFlow{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-white">
    <nav class="navbar navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">🎬 StreamFlow</a>
            <div class="navbar-nav flex-row">
                <a class="nav-link me-3" href="/">Inicio</a>
                <a class="nav-link" href="/catalogo">Catálogo</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### 2. `templates/index.html` (Inicio)
```html
{% extends "base.html" %}
{% block content %}
<div class="text-center py-5">
    <h1>Bienvenido a StreamFlow</h1>
    <p class="lead">Tu plataforma educativa de streaming.</p>
    <a href="/catalogo" class="btn btn-lg btn-primary">Ver Catálogo</a>
</div>
{% endblock %}
```

### 3. `templates/catalogo.html` (Catálogo Dinámico)
```html
{% extends "base.html" %}
{% block content %}
<h2 class="mb-4">Nuestro Contenido</h2>
<div class="row">
    {% for video in videos %}
    <div class="col-md-4 mb-4">
        <div class="card bg-secondary text-white">
            <div class="card-body">
                <h5 class="card-title">{{ video.titulo }}</h5>
                <p class="card-text">Categoría: {{ video.categoria }}</p>
                <a href="#" class="btn btn-primary">Reproducir</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

---

## 🚀 Etapa 4: Ejecución y Pruebas
1.  Asegúrate de estar dentro del entorno virtual.
2.  Ejecuta la aplicación:
    ```bash
    python app.py
    ```
3.  Abre tu navegador en `http://127.0.0.1:5000`.

---
**[Volver al README principal](README.md)**
