from flask import Flask, render_template

app = Flask(__name__)

# Simulación de una base de datos de películas/series
VIDEOS = [
    {"id": 1, "titulo": "Aprender Flask", "categoria": "Tutorial"},
    {"id": 2, "titulo": "Desarrollo con Python", "categoria": "Educación"},
    {"id": 3, "titulo": "Streaming en Tiempo Real", "categoria": "Avanzado"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', videos=VIDEOS)

if __name__ == '__main__':
    app.run(debug=True)
