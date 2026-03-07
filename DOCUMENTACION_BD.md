# Guía de Diseño de Base de Datos y Normalización

El diseño de una base de datos es fundamental para garantizar la integridad, eficiencia y escalabilidad de cualquier sistema de software.

## 1. El Proceso de Normalización

La **Normalización** es una técnica que se utiliza para organizar los datos en una base de datos relacional, con el fin de minimizar la redundancia y evitar anomalías en las actualizaciones.

A continuación, veremos las tres primeras formas normales utilizando un ejemplo de nuestro sistema de streaming.

### Escenario Inicial: Tabla "Sin Normalizar"
Imagina que guardamos todo en una sola tabla:

| ID_Pelicula | Titulo | Generos | Director | Email_Usuario |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Inception | Sci-Fi, Action | Nolan | user@email.com |

---

### 1.1. Primera Forma Normal (1NF)
**Regla:** Una tabla está en 1NF si todos sus atributos contienen valores atómicos (indivisibles) y no hay grupos repetitivos.

**Cambio:** Eliminamos la lista de géneros separada por comas.

| ID_Pelicula | Titulo | Genero | Director |
| :--- | :--- | :--- | :--- |
| 1 | Inception | Sci-Fi | Nolan |
| 1 | Inception | Action | Nolan |

---

### 1.2. Segunda Forma Normal (2NF)
**Regla:** Debe cumplir la 1NF y cada atributo que no sea parte de la clave primaria debe depender de **toda** la clave primaria (dependencia funcional completa).

**Problema en el ejemplo:** Si la clave es `(ID_Pelicula, Genero)`, el `Titulo` solo depende de `ID_Pelicula`, no del `Genero`. Esto causa redundancia.

**Cambio:** Separamos en dos tablas.

**Tabla Peliculas:**
| ID_Pelicula (PK) | Titulo | Director |
| :--- | :--- | :--- |
| 1 | Inception | Nolan |

**Tabla Peliculas_Generos:**
| ID_Pelicula (FK) | Genero |
| :--- | :--- |
| 1 | Sci-Fi |
| 1 | Action |

---

### 1.3. Tercera Forma Normal (3NF)
**Regla:** Debe cumplir la 2NF y no deben existir dependencias transitivas (una columna no debe depender de otra columna que no sea la clave primaria).

**Escenario:** Si en la tabla `Peliculas` tuviéramos `ID_Director` y `Nombre_Director`. El nombre depende del ID, y el ID de la película. Hay que separar al Director.

**Tabla Final Peliculas:**
| ID_Pelicula (PK) | Titulo | ID_Director (FK) |
| :--- | :--- | :--- |
| 1 | Inception | 10 |

**Tabla Directores:**
| ID_Director (PK) | Nombre |
| :--- | :--- |
| 10 | Nolan |

---

## 2. Conceptos Clave para Entender el Diseño

### 2.1. Claves Primarias (PK) y Foráneas (FK)
- **PK (Primary Key)**: Identificador único para cada registro (ej. `id_usuario`).
- **FK (Foreign Key)**: Un campo que vincula una tabla con la PK de otra tabla, estableciendo una relación.

### 2.2. Tipos de Relaciones
1. **Uno a Muchos (1:N)**: Un Director puede dirigir muchas películas, pero una película usualmente tiene un director principal.
2. **Muchos a Muchos (N:M)**: Una Película tiene muchos Géneros y un Género tiene muchas Películas. Requiere una **tabla intermedia**.

## 3. Beneficios de un Buen Diseño
1. **Integridad**: Evita datos contradictorios.
2. **Ahorro de Espacio**: Menos datos duplicados.
3. **Mantenimiento**: Si un director cambia de nombre, solo lo editas en un lugar.

[Volver al README principal](README.md)
