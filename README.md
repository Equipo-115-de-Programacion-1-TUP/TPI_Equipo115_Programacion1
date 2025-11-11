# 🌍 Sistema de Gestión de Paises (TPI Programación 1 - UTN)

Aplicación de consola en Python para gestionar información demográfica y geográfica de países, aplicando listas, diccionarios, funciones y persistencia de datos mediante CSV.

## 🧑‍💻 Integrantes
* César Luciano Angeleri
* Ronar Salazar Suzeta

## ✅ Requisitos y Restricciones del Proyecto

Este código fue desarrollado cumpliendo rigurosamente los siguientes puntos de la consigna:

### Requisitos Técnicos
* **Estructuras de Datos:** Uso de `listas` (para la colección de países) y `diccionarios` (para cada país).
* **Persistencia:** Lectura y escritura de datos mediante archivo `paises.csv`.
* **Funcionalidad:** Implementación de **filtros**, **ordenamientos** y **estadísticas** completas.
* **Modularidad:** Código dividido en funciones, aplicando el principio de "una función = una responsabilidad".
* **Control de Flujo:** Uso de `while` para bucles principales y `match/case` para la navegación en menús.

---

## 🛠️ Configuración y Ejecución

### 1. Requisitos Previos

Necesitas **Python 3.10 o superior** y las siguientes bibliotecas.

Instala las dependencias ejecutando:
```
pip install tabulate colorama prompt_toolkit
```
### 2. Estructura de Archivos

Asegúrate de tener estos archivos en el mismo directorio:

* ```sistema_paises.py```(el código fuente del proyecto).

* ```paises.csv``` (el archivo de datos base, si no existe, el programa lo crea al guardar).

### 3. Instrucciones de Uso

1. Abre tu terminal.

2. Navega hasta el directorio del proyecto.

3. Ejecuta el script:
```
python sistema_paises.py
```

4. El programa te dará la bienvenida, cargará los datos existentes y mostrará el Menú Principal.

## 📜 Ejemplos de Entradas y Salidas

### 1. Agregar y Normalizar (Opción 1)

El sistema normaliza el nombre y el continente, y maneja la robustez de datos (puntos como separadores de miles).

Entrada (Usuario):
```
Nombre (o X para volver): brasil
Población: 213.000.000
Superficie: 8515767
Continente: sudamerica
```

Salida (Sistema):
```
💾 Datos guardados.
✅ 'Brasil' agregado.
```

(El continente "sudamerica" se normaliza a "América")

### 2. Buscar con Autocompletado (Opción 3)

Se utiliza ```prompt_toolkit``` para autocompletar nombres de países existentes. La búsqueda permite coincidencias parciales.

Entrada (Usuario):
```
--- BUSCAR PAÍS ---
Buscar: arg
```

Salida (Sistema, si "Argentina" existe):
```
╒═══════════╤═════════════╤════════════════╤═════════════╕
│ nombre    │ poblacion   │ superficie     │ continente  │
╞═══════════╪═════════════╪════════════════╪═════════════╡
│ Argentina │ 45.376.763  │ 2.780.400 km²  │ América     │
╘═══════════╧═════════════╧════════════════╧═════════════╛
```

### 3. Mostrar Estadísticas (Opción 6)

Salida (Sistema):
```
📊 ESTADÍSTICAS 📊
Mayor población: China (1.400.000.000)
Menor población: San Marino (33.000)
Población promedio: 50.000.000
Superficie promedio: 1.000.000 km²

Cantidad por continente:
 - América: 10
 - Asia: 8
 - Europa: 5
 - África: 6
 - Oceanía: 2
```