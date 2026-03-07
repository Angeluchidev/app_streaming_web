# 🧪 Guía de Laboratorio: Desarrollo de App Streaming con Flask

Esta guía está diseñada para que los alumnos sigan un proceso ordenado de ingeniería y desarrollo para construir la aplicación **StreamFlow**.

---

## 📅 Etapa 1: Configuración del Entorno de Desarrollo
*Objetivo: Preparar el espacio de trabajo y las herramientas básicas.*

1.  **Crear carpeta del proyecto:** Crea una carpeta llamada `app_streaming_web`.
2.  **Crear Entorno Virtual (VENV):**
    ```bash
    python -m venv venv
    ```
3.  **Activar Entorno Virtual:**
    - **Windows:** `.\venv\Scripts\activate`
    - **Linux/macOS:** `source venv/bin/activate`
4.  **Instalar Flask:**
    ```bash
    pip install flask
    ```

---

## 🏗️ Etapa 2: Estructura Base y Plantilla Maestra (Base.html)
*Objetivo: Crear el esqueleto de la aplicación y la estructura visual común.*

1.  **Crear Carpetas Necesarias**:
    - `/templates` (Para los archivos HTML).
    - `/static/css` (Para los estilos CSS).
2.  **Crear `base.html` en `/templates`**:
    - Este archivo contendrá el **diseño global** (Navbar, Footer, enlaces a Bootstrap).
    - Utiliza el tag `{% block content %}{% endblock %}` donde se inyectarán las demás páginas.
3.  **Vincular Recursos**: Asegúrate de incluir los links de Bootstrap y tu `style.css` en el `<head>`.


---

## 🎨 Etapa 3: Creación de Páginas (Vistas HTML)
*Objetivo: Desarrollar las páginas individuales usando Herencia de Plantillas.*

1.  **Página de Inicio (`index.html`)**:
    - Crea el archivo dentro de `/templates`.
    - Usa `{% extends "base.html" %}` al inicio para heredar el diseño.
    - Coloca el contenido de bienvenida dentro del bloque `{% block content %}`.
2.  **Página de Catálogo (`catalogo.html`)**:
    - Crea el archivo y hereda de `base.html`.
    - Implementa un bucle `{% for video in videos %}` para recorrer la lista enviada desde Python.
    - Diseña Cards de Bootstrap para mostrar cada película.
3.  **Configurar Rutas en `app.py`**: 
    - Usa `render_template('index.html')` en la ruta `/`.
    - Usa `render_template('catalogo.html', videos=VIDEOS)` en la ruta `/catalogo`.


---

## 📊 Etapa 4: Modelado de Datos y Persistencia (SQLite)
*Objetivo: Conectar la aplicación a una base de datos real.*

1.  **Instalar SQLAlchemy**:
    ```bash
    pip install flask-sqlalchemy
    ```
2.  **Definir Modelos**: Crear la clase `Pelicula` basada en el [Diagrama de Clases](DOCUMENTACION_UML.md).
3.  **Normalización**: Asegúrate de que las tablas sigan las reglas de la [Guía de BD](DOCUMENTACION_BD.md).
4.  **Inicializar Base de Datos**: Crear el archivo `.db` desde la consola de Python.

---

## 🎬 Etapa 5: Lógica de Negocio y Streaming
*Objetivo: Reproducción y gestión de catálogo.*

1.  **Página de Detalles**: Crear una ruta que reciba un ID (ej. `/video/<int:id>`).
2.  **Embed de Video**: Usar la etiqueta `<video>` o `<iframe>` para reproducir contenido.
3.  **Búsqueda y Filtros**: Implementar el flujo diseñado en el [DFD Nivel 1](DOCUMENTACION_DFD.md).

---

## ✅ Etapa 6: Pruebas y Despliegue
*Objetivo: Verificar que todo funcione.*

1.  **Modo Debug**: Asegurarse de que `app.run(debug=True)` esté activo durante el desarrollo.
2.  **Requerimientos**: Generar el archivo para que otros puedan instalar tu app:
    ```bash
    pip freeze > requirements.txt
    ```

---

### 💡 Tips para los Alumnos:
- **No saltes etapas**: El desarrollo estructurado evita errores difíciles de rastrear.
- **Lee los Diagramas**: Si tienes dudas sobre qué atributos poner en una clase, consulta la [Documentación UML](DOCUMENTACION_UML.md).
- **Consola es tu amiga**: Los errores de Python en la terminal te dirán exactamente qué falta.

[Volver al README principal](README.md)
