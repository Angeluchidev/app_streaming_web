import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'streaming.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

        db.session.add_all([g1, g2, g3, p1, p2])
        db.session.commit()
        print("Base de datos sincronizada con el ER original.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
