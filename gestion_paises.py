import csv

# ==========================
#  FUNCIONES PRINCIPALES
# ==========================

def cargar_datos(nombre_archivo):
    #"""Lee los datos de países desde un archivo CSV y devuelve una lista de diccionarios."""
    paises = []
    try:
        with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                pais = {
                    "nombre": fila["nombre"],
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"]
                }
                paises.append(pais)
        print(f"✅ Se cargaron {len(paises)} registros correctamente.")
    except FileNotFoundError:
        print("❌ Error: el archivo no existe.")
    except KeyError:
        print("❌ Error: formato CSV incorrecto. Verifique los encabezados.")
    return paises


def mostrar_menu():
    #"""Muestra el menú de opciones y devuelve la opción seleccionada."""
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Listar todos los países")
    print("2. Buscar país por nombre")
    print("3. Filtrar por continente")
    print("4. Mostrar estadísticas")
    print("5. Ordenar países")
    print("6. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion


def listar_paises(paises):
    #"""Muestra todos los países con sus datos."""
    if not paises:
        print("No hay datos cargados.")
        return
    print("\n--- LISTADO DE PAÍSES ---")
    for p in paises:
        print(f"{p['nombre']:15} | {p['continente']:10} | Población: {p['poblacion']:,} | Superficie: {p['superficie']:,} km²")

# Método para la busqueda de países 
def buscar_pais(paises):
    #"""Busca un país sin distinguir mayúsculas/minúsculas y según la cantidad de letras ingresadas."""
    criterio = input("Ingrese parte o nombre del país: ").strip()
    if len(criterio) < 2:
        print("⚠️ Por favor, escriba al menos 2 letras para buscar.")
        return

    criterio_lower = criterio.lower()
    longitud = len(criterio_lower)

    resultados = []
    for p in paises:
        nombre_lower = p["nombre"].lower()
        # Coincidencia si el inicio del nombre coincide con la cantidad exacta de letras ingresadas
        if nombre_lower[:longitud] == criterio_lower:
            resultados.append(p)

    if resultados:
        print("\n--- Resultados encontrados ---")
        for p in resultados:
            print(f"{p['nombre']:15} | {p['continente']:10} | "
                  f"Población: {p['poblacion']:,} | Superficie: {p['superficie']:,} km²")
    else:
        print("❌ No se encontraron coincidencias.")


# ==========================
#  FUNCIÓN PRINCIPAL
# ==========================

def main():
    archivo = "paises.csv"
    paises = cargar_datos(archivo)

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            listar_paises(paises)
        elif opcion == "2":
            buscar_pais(paises)
        elif opcion == "3":
            filtrar_por_continente(paises)
        elif opcion == "4":
            mostrar_estadisticas(paises)
        elif opcion == "5":
            ordenar_paises(paises)
        elif opcion == "6":
            print("👋 Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")


# ==========================
#  PUNTO DE ENTRADA
# ==========================

if __name__ == "__main__":
    main()
