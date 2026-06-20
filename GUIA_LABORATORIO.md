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
from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'streaming.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_super_secreta_educativa' # NECESARIO PARA LAS SESIONES (Cifra las cookies de sesión)

db = SQLAlchemy(app)

# --- MODELOS DE DATOS (SINCRONIZADOS CON DIAGRAMA ER) ---
# Referencia: README.md (Sección 3.2 Diagrama MER)

# Tabla intermedia para relación Muchos a Muchos (PELICULA_GENERO)
pelicula_genero = db.Table('pelicula_genero',
    db.Column('pelicula_id', db.Integer, db.ForeignKey('pelicula.id'), primary_key=True),
    db.Column('genero_id', db.Integer, db.ForeignKey('genero.id'), primary_key=True)
)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.Date, default=datetime.utcnow)

class Pelicula(db.Model):
    __tablename__ = 'pelicula'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    sinopsis = db.Column(db.Text)
    anio_lanzamiento = db.Column(db.Integer)
    url_video = db.Column(db.String(200))
    
    # Relación N:M con Genero
    generos = db.relationship('Genero', secondary=pelicula_genero, backref=db.backref('peliculas', lazy='dynamic'))

class Genero(db.Model):
    __tablename__ = 'genero'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

# --- RUTAS ---
@app.route('/')
def index():
    return render_template('index.html')

# EXPLICACIÓN ALUMNOS: Ruta de Login (Admite tanto pedir la página GET, como enviar el formulario POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtenemos los datos que el usuario escribió en el formulario
        email = request.form['email']
        password = request.form['password']
        
        # Buscamos en la base de datos si existe el usuario por su email
        usuario = Usuario.query.filter_by(email=email).first()
        
        # Validamos si el usuario existe y si la contraseña coincide con su hash
        if usuario and check_password_hash(usuario.password, password):
            # Guardamos la sesión (una cookie segura en el navegador del usuario)
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas, intenta de nuevo.', 'danger')
            
    return render_template('login.html')

# EXPLICACIÓN ALUMNOS: Ruta para Cerrar Sesión
@app.route('/logout')
def logout():
    # Limpiamos todos los datos que guardamos en la sesión
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/catalogo')
def catalogo():
    # Obtenemos las películas de la base de datos centralizada
    todas_las_peliculas = Pelicula.query.all()
    return render_template('catalogo.html', videos=todas_las_peliculas)

# --- INICIALIZACIÓN DE DATOS (SEEDERS) ---
def init_db():
    with app.app_context():
        # Borrar y recrear para asegurar cambios de esquema
        db.drop_all() 
        db.create_all()
        
        # 1. Crear Géneros
        g1 = Genero(nombre="Acción")
        g2 = Genero(nombre="Educación")
        g3 = Genero(nombre="Sci-Fi")

        # 2. Crear Películas
        p1 = Pelicula(titulo="Aprender Flask", sinopsis="Tutorial de desarrollo web", anio_lanzamiento=2026, url_video="https://example.com/flask")
        p2 = Pelicula(titulo="Python para Ingenieros", sinopsis="Lógica de programación", anio_lanzamiento=2025, url_video="https://example.com/python")
        
        # 3. Asignar Géneros (Relación N:M)
        p1.generos.append(g2)
        p1.generos.append(g3)
        p2.generos.append(g2)

        # 4. Crear Usuario de Prueba (EXPLICACIÓN ALUMNOS: Se cifra la contraseña por seguridad)
        u1 = Usuario(
            nombre="Profesor Admin",
            email="admin@streamflow.com",
            password=generate_password_hash("123456")
        )

        db.session.add_all([g1, g2, g3, p1, p2, u1])
        db.session.commit()
        print("Base de datos sincronizada con el ER original.")

if __name__ == '__main__':
    init_db()
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

## 🔐 Etapa 4: Sistema de Autenticación (Login)
*Agregaremos seguridad a la aplicación usando sesiones y cifrado de contraseñas.*

1. **La Sesión (`session`):** 
   En la web, cada vez que recargas una página el servidor olvida quién eres. Para mantener tu estado de "conectado", usamos `session`. Flask guarda una "cookie" segura en el navegador del usuario. Para que esto sea seguro, necesitamos una llave secreta en `app.py`:
   ```python
   app.secret_key = 'clave_super_secreta_educativa'
   ```

2. **Cifrado de contraseñas (`werkzeug.security`):**
   Nunca se deben guardar contraseñas en texto plano en la base de datos (por si un hacker la roba). Usamos `generate_password_hash("123456")` para crear un texto ilegible, y `check_password_hash()` para comparar lo que el usuario escribió con el texto ilegible.

3. **Rutas de Login y Logout:**
   - **`/login`**: Recibe métodos `GET` (para mostrar el formulario) y `POST` (para procesar el email y password).
   - **`/logout`**: Limpia la sesión usando `session.clear()`.

---

## 🚀 Etapa 5: Ejecución y Pruebas
1.  Asegúrate de estar dentro del entorno virtual.
2.  Ejecuta la aplicación:
    ```bash
    python app.py
    ```
3.  Abre tu navegador en `http://127.0.0.1:5000`.

---
**[Volver al README principal](README.md)**
