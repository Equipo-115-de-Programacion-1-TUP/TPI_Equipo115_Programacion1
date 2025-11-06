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
    print("6. Agregar un pais")
    print("7. Salir")
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

#Función para guardar datos en el CSV
def guardar_datos_pais(nombre_archivo, lista_paises):
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()

            for pais in lista_paises:
                escritor.writerow(pais)
        return True
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")
        return False
    
#Funcion para añadir un paies
def agregar_pais(lista_paises):
    #Agrega un nuevo país a la lista y lo guarda en el archivo CSV."""
    print("="*10,"Agregar un pais","="*10)
    # Validación y asignación del nombre
    while True:
        nombre_str = input("Ingrese el nombre de pais a agregar: ").strip()

        if nombre_str.isdigit():
            print("❌ Error: Ingrese un nombre de país válido (formato texto).")
            continue
        if nombre_str=="":
            print("❌ Error: Ingrese un nombre de país válido (no vacío).")
            continue
        print(f"Nombre de pais guardado: {nombre_str}")
        break
    
    # Validación y asignación de población   
    while True:   
        poblacion_str = input("Ingrese la cantidad de población del nuevo pais a agregar: ").strip()
        
        if not poblacion_str.isdigit():
            print("❌ Error: Ingrese un valor de población válido (formato numérico).")
            continue
        if poblacion_str=="":
            print("❌ Error: Ingrese un valor de población válido (no vacío).")
            continue
        poblacion_int=int(poblacion_str)
        if poblacion_int <= 0:
            print("❌ Error: La población debe ser mayor a 0.")
            continue
        print(f"Población de pais guardado: {poblacion_int} habitantes.")
        break

    # Validación y asignación de superficie
    while True:   
        superficie_str = input("Ingrese la superficie (km²) del nuevo pais a agregar: ").strip()
        
        if not superficie_str.isdigit():
            print("❌ Error: Ingrese un valor de superficie válido (formato numérico).")
            continue
        if superficie_str=="":
            print("❌ Error: Ingrese un valor de superficie válido (no vacío).")
            continue
        superficie_int = int(superficie_str)
        if superficie_int <= 0:
            print("❌ Error: La superficie debe ser mayor a 0.")
            continue
        print(f"Superficie de pais guardado: {superficie_int}")
        break
   
    # Validación y asignación de superficie
    while True:
        print("Va a seleccionar el continente al que pertenece el nuev país a agregar.")   
        print("1. Asia")
        print("2. África")
        print("3. Europa")
        print("4. América")
        print("5. Oceanía")
        print("6. Antártida")
        continente_str = input("Seleccione el continente al que pertenece nuevo pais a agregar: ").strip()
        
        if not continente_str.isdigit():
            print("❌ Error: Ingrese un valor válido (formato númerico).")
            continue
        if continente_str=="":
            print("❌ Error: Ingrese un valor de continente válido (no vacío).")
            continue
        match continente_str:
            case "1":
                continente_str = "Asia"
                print(f"Continente de pais guardado: {continente_str}")
            case "2":
                continente_str = "África"
                print(f"Continente de pais guardado: {continente_str}")
            case "3":
                continente_str = "Europa"
                print(f"Continente de pais guardado: {continente_str}")
            case "4":
                continente_str = "América"
                print(f"Continente de pais guardado: {continente_str}")
            case "5":
                continente_str = "Oceanía"
                print(f"Continente de pais guardado: {continente_str}")
            case "6":
                continente_str = "Antártida"
                print(f"Continente de pais guardado: {continente_str}")
            case _:
                print("❌ Error: Seleccione alguna de las opciones del menú de continentes.")
        break
    
    # Crear el nuevo país
    nuevo_pais = {
        "nombre": nombre_str,
        "poblacion": poblacion_int,
        "superficie": superficie_int,
        "continente": continente_str
    }

    # Agregar a la lista
    lista_paises.append(nuevo_pais)

    # Guardar en el archivo CSV
    if guardar_datos_pais("paises.csv", lista_paises):
        print(f"\n✅ País '{nombre_str}' agregado exitosamente.")
    else:
        print(f"\n⚠️ El país se agregó a la lista pero hubo un error al guardar en el archivo.")

#Funcion a desarrollar
def filtrar_por_continente(lista_paises):
    pass

#Funcion a desarrollar
def mostrar_estadisticas(lista_paises):
    pass

#Funcion a desarrollar
def ordenar_paises(lista_paises):
    pass


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
            agregar_pais(paises)
        elif opcion == "7":
            print("👋 Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")


# ==========================
#  PUNTO DE ENTRADA
# ==========================

if __name__ == "__main__":
    main()
