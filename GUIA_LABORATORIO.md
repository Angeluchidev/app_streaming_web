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
*Crea el archivo `app.py` en la raíz con la lógica de las rutas y modelos ER.*

```python
import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///streaming.db'
db = SQLAlchemy(app)

# --- MODELOS SINCRONIZADOS CON EL DER ---

# Tabla intermedia N:M
pelicula_genero = db.Table('pelicula_genero',
    db.Column('pelicula_id', db.Integer, db.ForeignKey('pelicula.id'), primary_key=True),
    db.Column('genero_id', db.Integer, db.ForeignKey('genero.id'), primary_key=True)
)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fecha_registro = db.Column(db.Date, default=datetime.utcnow)

class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    sinopsis = db.Column(db.Text)
    anio_lanzamiento = db.Column(db.Integer)
    url_video = db.Column(db.String(200))
    generos = db.relationship('Genero', secondary=pelicula_genero, backref='peliculas')

class Genero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

@app.route('/')
def index(): return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    videos = Pelicula.query.all()
    return render_template('catalogo.html', videos=videos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

## 🎨 Etapa 3: Diseño con Plantillas (Jinja2)
*Crea la carpeta `/templates` y los archivos correspondientes.*

### 1. `templates/base.html` (Mismo que antes)
... (mantener estructura base) ...

### 2. `templates/catalogo.html` (Iterando géneros)
```html
{% extends "base.html" %}
{% block content %}
<div class="row">
    {% for v in videos %}
    <div class="col-md-4 mb-4">
        <div class="card bg-secondary text-white">
            <div class="card-body">
                <h5 class="card-title">{{ v.titulo }}</h5>
                <p>
                    {% for g in v.generos %}
                        <span class="badge bg-primary">{{ g.nombre }}</span>
                    {% endfor %}
                </p>
                <p>{{ v.sinopsis }}</p>
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
