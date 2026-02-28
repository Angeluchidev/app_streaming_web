# Guía de Inicio: Configuración del Proyecto Python y Flask

Esta guía detalla el proceso para configurar un entorno de desarrollo profesional para una aplicación web con Flask.

## 1. Creación del Entorno Virtual (VENV)

Un entorno virtual permite aislar las dependencias del proyecto de las del sistema global, evitando conflictos.

**Comando:**
```powershell
python -m venv venv
```

## 2. Activación del Entorno Virtual

Para trabajar dentro del entorno (instalar librerías y ejecutar la app):

*   **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
*   **Linux/macOS:** `source venv/bin/activate`

## 3. Instalación de Flask

Flask es un micro-framework ligero para Python.

**Comando:**
```powershell
.\venv\Scripts\python -m pip install flask
```

## 4. Estructura Base del Proyecto

Se ha creado un archivo `app.py` con el siguiente código base:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>¡Hola, alumnos!</h1><p>Aplicación Flask funcionando.</p>'

if __name__ == '__main__':
    app.run(debug=True)
```

## 5. Gestión de Dependencias

Se ha generado un archivo `requirements.txt` que lista todas las librerías instaladas:

**Comando para generar:**
```powershell
.\venv\Scripts\pip freeze > requirements.txt
```

## 6. Arquitectura de la Aplicación (MVT Simplificado)

Hemos evolucionado el proyecto para usar plantillas (HTML) y archivos estáticos (CSS/JS):

- **`/templates`**: Contiene los archivos HTML. Usamos **Jinja2** para la herencia de plantillas (`base.html`).
- **`/static`**: Aquí guardamos archivos que no cambian, como imágenes o estilos CSS personalizados.
- **`app.py`**: Ahora utiliza `render_template` para enviar los datos de Python a la interfaz web.

### ¿Cómo añadir una nueva página?
1. Crea la ruta en `app.py`.
2. Crea el archivo HTML en `/templates` que extienda de `base.html`.
3. ¡Listo! Flask se encarga de unirlo todo.

---
[Volver al README principal](README.md)
