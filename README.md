# 📚 TPI - Gestión de Datos de Países en Python

## Sistema de Análisis y Gestión de Datos Geográficos (Programación 1)

---

### 🌍 1. Descripción del Proyecto

Este proyecto es el Trabajo Práctico Integrador (TPI) de la materia Programación 1. Consiste en una aplicación de consola desarrollada en **Python** para gestionar información geográfica y demográfica de distintos países, con persistencia de datos mediante un archivo CSV.

El desarrollo se enfocó en la **modularidad**, la **robustez** del código y el uso eficiente de las estructuras de datos fundamentales (`Listas` y `Diccionarios`) para implementar funcionalidades de gestión, búsqueda avanzada, filtrado dinámico, ordenamiento y cálculos estadísticos clave.

---

### 🎓 2. Datos Académicos

| Categoría | Detalle |
| :--- | :--- |
| **Universidad** | Universidad Tecnológica Nacional (UTN) |
| **Carrera** | Tecnicatura Universitaria en Programación a Distancia (TUPAD) |
| **Materia** | Programación 1 |
| **Fecha de Entrega** | 11 de Noviembre de 2025 |

#### 🧑 Integrantes

| Nombre Completo | Comisión | Email de Contacto |
| :--- | :--- | :--- |
| **Cesar Luciano Angeleri** | Comisión 1 | lcnang@gmail.com |
| **Ronar Salazar Suzeta** | Comisión 3 | ronar76@gmail.com |

#### 👨‍🏫 Cuerpo Docente

| Rol | Nombre |
| :--- | :--- |
| **Docente Titular (C1 y C3)** | Cinthia Rigoni |
| **Docente Tutor (C1)** | Martin Garcia |
| **Docente Tutor (C3)** | Brian Lara |

---

### 🛠️ 3. Instalación y Ejecución

Para probar el proyecto, necesitas Python 3.10 o superior y las librerías de terceros que mejoran la experiencia de usuario.

#### 3.1. Instalación de Dependencias

Ejecuta el siguiente comando en tu terminal para instalar las librerías necesarias:

```
pip install tabulate colorama prompt_toolkit
```
#### 3.2. Estructura Requerida

Asegúrate de que los siguientes archivos se encuentren en el mismo directorio:

1.  `gestion_paises.py` (Código fuente)
2.  `paises.csv` (Dataset inicial)

#### 3.3. Instrucciones de Ejecución

1.  Abre la terminal o línea de comandos.
2.  Navega hasta el directorio donde se encuentran los archivos.
3.  Ejecuta la aplicación:
    ```bash
    python gestion_paises.py
    ```
4.  El sistema cargará el dataset desde `paises.csv` y te presentará el menú principal.

### 4. Uso de Librerías de Terceros

Las siguientes librerías se integraron para cumplir requisitos de presentación y usabilidad:

| Librería | Función Principal | Instalación |
| :--- | :--- | :--- |
| `csv` | Lectura y escritura del dataset (`paises.csv`). | Persistencia de datos. |
| `tabulate` | Generación de tablas de consola para listados. | Mejora la legibilidad y formalidad de las listas de datos. |
| `colorama` | Manejo de colores en el texto. | Mejora la interfaz (UX) para distinguir continentes o mensajes de estado. |
| `prompt_toolkit`| Autocompletado interactivo en la función de búsqueda (Opción 3). | Optimiza la eficiencia en la búsqueda de países. |

---

### 📑 5. Estructura y Módulos Clave

El código `gestion_paises.py` está diseñado bajo un esquema de **modularización por responsabilidad** para garantizar la legibilidad y el mantenimiento, cumpliendo con la filosofía "una función, una responsabilidad".

| Módulo Lógico | Propósito Principal |
| :--- | :--- |
| **Persistencia de Datos** | Manejo de la lectura/escritura del archivo `paises.csv` para la persistencia. |
| **Normalización y Utilidades** | Funciones auxiliares para estandarizar datos (eliminar acentos, unificar continentes) y usar el ordenamiento. |
| **Lógica de Negocio (CRUD)**| Implementación de las operaciones de alta y modificación de registros. |
| **Consultas y Análisis** | Contiene la lógica para la búsqueda, filtrado, ordenamiento y cálculo de estadísticas. |

---

### 📈 6. Ejemplos de Entrada y Salida (Menú Completo)

El programa ofrece un menú interactivo. A continuación, se detalla la funcionalidad y un ejemplo de uso para cada opción:

#### **Menú Principal**
```
===== MENÚ PRINCIPAL =====

1. Agregar país

2. Actualizar país

3. Buscar país

4. Filtrar países

5. Ordenar países

6. Mostrar estadísticas

7. Salir
```

1. **Agregar país**:**Crea** un nuevo registro. El sistema maneja validaciones de tipos de datos y normalización de texto.
    + *Entrada:* `Opción: 1` -> *Ingreso de datos.*
    + *Salida:* `✅ País 'Chile' agregado exitosamente. 💾 Archivo actualizado.`
2. **Actualizar país**: **Modifica** los datos de **Población** y **Superficie** de un país existente.
    + *Entrada:* `Opción: 2` -> `Ingrese el nombre del país a actualizar: argentina` -> *Nuevos valores.*
    + *Salida:* `✅ Datos de 'Argentina' actualizados correctamente. 💾 Archivo actualizado.`
3. **Buscar país**: **Busca** registros por coincidencia **parcial o exacta** del nombre, utilizando el autocompletado (`prompt_toolkit`).
    + *Entrada:* `Opción: 3` -> `Ingrese nombre (use TAB para autocompletar): col`+
    + *Salida:* Muestra la tabla del país encontrado (e.g., Colombia).
4. **Filtrar países**: Permite filtrar el listado por tres criterios: **Continente**, **Rango de Población**, o **Rango de Superficie**.
    + *Ejemplo:* Filtrado por Rango de Población (`Mínima: 100000000 / Máxima: 400000000`).
5. **Ordenar países**: Permite reordenar el listado por **Nombre**, **Población** o **Superficie** (ASC/DESC).
    + *Ejemplo:* Ordenar por Población (DESC).
6. **Mostrar estadísticas**:Calcula y muestra indicadores clave (Mayor/Menor Población, Promedios, Conteo por Continente).+
    + *Salida:* `📈 País con MAYOR Población: China (1.400.000.000 hab.)`
7. **Salir**: Finaliza la ejecución de la aplicación, cerrando la sesión.
    + *Salida:* `¡Gracias por usar el sistema de gestión de países!`

---

### 🔗 7. Enlaces a Entregables

| Recurso | Enlace |
| :--- | :--- |
| **Repositorio GitHub** | `https://github.com/Equipo-115-de-Programacion-1-TUP/TPI_Equipo115_Programacion1.git` |
| **Video Tutorial y Exposición** | [Video](https://www.canva.com/design/DAG4cV4sJ8k/9Mk4FK2FITZz-Tz-IwQztg/watch?utm_content=DAG4cV4sJ8k&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h20b225e87e) |
| **Documento del TPI (PDF)**| [Ver Documento](https://docs.google.com/document/d/1pQ3xIWjH0VXJpW2GyazQZjNliQz0t008V0RZzYK25E8/edit?usp=sharing) |
