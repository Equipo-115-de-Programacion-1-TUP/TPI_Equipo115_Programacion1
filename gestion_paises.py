# ==========================
#   SISTEMA DE GESTIÓN DE PAÍSES
#   Versión 5.2 (Final TPI Corregida)
#   Cumple con: menú con while + match/case, modularización, listas/dicts, CSV, filtros, ordenamientos y estadísticas
#   Restricciones: sin lambdas, sin clases, sin excepciones para control lógico, sin variables globales
# ==========================

import csv
import os
from tabulate import tabulate
from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

init(autoreset=True)

# -------------------------------
# NORMALIZACIÓN
# -------------------------------
def sin_acentos(texto):
    reemplazos = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n"}
    texto = texto.lower()
    for a,b in reemplazos.items():
        texto = texto.replace(a,b)
    return texto

def normalizar_continente(cont):
    cont = sin_acentos(cont.strip())
    if cont in ["america","americas","latinoamerica","norteamerica","sudamerica"]:
        return "América"
    if cont == "europa":
        return "Europa"
    if cont == "asia":
        return "Asia"
    if cont == "africa":
        return "África"
    if cont in ["oceania","oceanía"]:
        return "Oceanía"
    return cont.capitalize()

def normalizar_nombre(nombre):
    return " ".join(nombre.strip().split()).capitalize()

# -------------------------------
# COLORES
# -------------------------------
def color_por_continente(cont):
    cont = sin_acentos(cont)
    if cont=="america": return Fore.GREEN
    if cont=="europa": return Fore.BLUE
    if cont=="asia": return Fore.YELLOW
    if cont=="africa": return Fore.RED
    if cont=="oceania": return Fore.CYAN
    return Fore.WHITE

# -------------------------------
# CLAVES ORDENAMIENTO (sin lambda)
# -------------------------------
def clave_nombre(p): return p["nombre"]
def clave_poblacion(p): return p["poblacion"]
def clave_superficie(p): return p["superficie"]

def autocompletar_nombres(paises):
    return WordCompleter([p["nombre"] for p in paises], ignore_case=True)

# -------------------------------
# BASE DE DATOS CSV
# -------------------------------
def guardar_datos(nombre_archivo, paises):
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        campos = ["nombre","poblacion","superficie","continente"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for p in paises:
            escritor.writerow(p)
    print("💾 Datos guardados.\n")

def cargar_datos(nombre_archivo):
    paises=[]
    if not os.path.exists(nombre_archivo):
        return paises
    archivo=open(nombre_archivo,newline="",encoding="utf-8")
    lector=csv.DictReader(archivo)

    for f in lector:
        if not f["poblacion"].isdigit() or not f["superficie"].isdigit(): continue
        nombre=normalizar_nombre(f["nombre"])
        continente=normalizar_continente(f["continente"])

        if any(sin_acentos(x["nombre"])==sin_acentos(nombre) for x in paises): continue

        paises.append({
            "nombre":nombre,
            "poblacion":int(f["poblacion"]),
            "superficie":int(f["superficie"]),
            "continente":continente
        })
    archivo.close()
    print(f"✅ {len(paises)} países cargados.")
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

def menu_filtrar(paises):
    while True:
        print("\n--- FILTRAR ---")
        print("1. Por continente")
        print("2. Por rango de población (automático)")
        print("3. Por rango de superficie (automático)")
        print("X. Volver")
        op=input("Opción: ").strip().upper()
        match op:
            case "X": return
            case "1": filtrar_por_continente(paises)
            case "2": filtrar_por_poblacion_aut(paises)
            case "3": filtrar_por_superficie_aut(paises)
            case _: print("❌ Inválida.")

# -------------------------------
# ORDENAR
# -------------------------------
def menu_ordenar(paises):
    print("\n--- ORDENAR ---")
    print("1. Nombre (A-Z)")
    print("2. Población (desc.)")
    print("3. Superficie (asc.)")
    print("4. Superficie (desc.)")
    op=input("Opción: ").strip()
    match op:
        case "1": datos=sorted(paises,key=clave_nombre)
        case "2": datos=sorted(paises,key=clave_poblacion,reverse=True)
        case "3": datos=sorted(paises,key=clave_superficie)
        case "4": datos=sorted(paises,key=clave_superficie,reverse=True)
        case _: print("❌ Inválida."); return
    listar_paises(datos)

# -------------------------------
# ESTADÍSTICAS
# -------------------------------
def mostrar_estadisticas(paises):
    total=len(paises)
    mayor=max(paises,key=clave_poblacion)
    menor=min(paises,key=clave_poblacion)
    prom_pob=sum(p["poblacion"] for p in paises)/total
    prom_sup=sum(p["superficie"] for p in paises)/total
    cont_count={}
    for p in paises:
        c=normalizar_continente(p["continente"])
        cont_count[c]=cont_count.get(c,0)+1

    print("\n📊 ESTADÍSTICAS 📊")
    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']:,})".replace(",","."))
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,})".replace(",","."))
    print(f"Población promedio: {int(prom_pob):,}".replace(",","."))
    print(f"Superficie promedio: {int(prom_sup):,} km²".replace(",","."))
    print("\nCantidad por continente:")
    for c,n in cont_count.items():
        print(f" - {c}: {n}")

# -------------------------------
# LISTAR
# -------------------------------
def listar_paises(paises):
    if len(paises)==0:
        print("No hay resultados.")
        return
    tabla=[]
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
    paises=cargar_datos("paises.csv")
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

if __name__=="__main__":
    main()
