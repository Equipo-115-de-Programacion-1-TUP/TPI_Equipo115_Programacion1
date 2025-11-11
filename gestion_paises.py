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

# -------------------------------
# ACTUALIZAR PAÍS (Corregido)
# -------------------------------
def actualizar_pais(paises, pais_preseleccionado=None):
    print("\n--- ACTUALIZAR PAÍS ---")

    if pais_preseleccionado:
        pais = pais_preseleccionado
    else:
        while True:
            nombre=input("Nombre del país (o X para volver): ").strip()
            if nombre.upper()=="X": return
            if nombre=="" or not nombre.replace(" ","").isalpha():
                print("❌ Debe ingresar un nombre válido.")
                continue

            nombre_norm=sin_acentos(nombre)
            pais=None
            for p in paises:
                if sin_acentos(p["nombre"])==nombre_norm:
                    pais=p
                    break

            if pais is None:
                print("❌ No existe.")
                if input("¿Reintentar? (S/N): ").upper()=="S": continue
                return
            break

    while True:
        print(f"\nPaís: {pais['nombre']}")
        print(f"Población actual: {pais['poblacion']:,}".replace(",","."))
        print(f"Superficie actual: {pais['superficie']:,} km²".replace(",","."))
        print("(Enter = mantener valor)\n")

        nueva_p=input("Nueva población: ").replace(".","").strip()
        nueva_s=input("Nueva superficie: ").replace(".","").strip()

        # ✅ Corrección solicitada:
        if nueva_p=="" and nueva_s=="":
            print("\n❗ No se modificó ningún valor.")
            print("1) Reintentar")
            print("2) Cancelar y volver")
            op=input("Opción: ").strip()
            if op=="1": continue
            print("↩ Operación cancelada.")
            return

        if nueva_p=="":
            nueva_p=pais["poblacion"]
        elif nueva_p.isdigit():
            nueva_p=int(nueva_p)
        else:
            print("❌ Debe ingresar un número válido para población.")
            continue

        if nueva_s=="":
            nueva_s=pais["superficie"]
        elif nueva_s.isdigit():
            nueva_s=int(nueva_s)
        else:
            print("❌ Debe ingresar un número válido para superficie.")
            continue

        print("\n--- CONFIRMAR CAMBIOS ---")
        print(f"Población: {pais['poblacion']:,} → {nueva_p:,}".replace(",","."))
        print(f"Superficie: {pais['superficie']:,} km² → {nueva_s:,} km²".replace(",","."))
        if input("¿Aplicar cambios? (S/N): ").upper()!="S":
            print("↩ Cancelado.")
            return

        pais["poblacion"]=nueva_p
        pais["superficie"]=nueva_s
        guardar_datos("paises.csv",paises)
        print("✅ Actualizado.\n")
        break

# -------------------------------
# AGREGAR PAÍS
# -------------------------------
def agregar_pais(paises):
    print("\n--- AGREGAR PAÍS ---")
    while True:
        nombre = input("Nombre (o X para volver): ").strip()
        if nombre.upper()=="X": return
        if nombre=="" or not nombre.replace(" ","").isalpha():
            print("❌ Nombre inválido.")
            continue

        nombre = normalizar_nombre(nombre)

        for p in paises:
            if sin_acentos(p["nombre"]) == sin_acentos(nombre):
                print(f"\n⚠️ '{nombre}' ya existe.")
                print("1) Actualizar este país")
                print("2) Cancelar y volver")
                if input("Opción: ").strip()=="1":
                    actualizar_pais(paises,p)
                return

        poblacion = input("Población: ").replace(".","")
        if not poblacion.isdigit(): print("❌ Número inválido."); continue

        superficie = input("Superficie: ").replace(".","")
        if not superficie.isdigit(): print("❌ Número inválido."); continue

        continente = input("Continente: ").strip()
        if continente=="" or not continente.replace(" ","").isalpha(): print("❌ Inválido."); continue

        paises.append({
            "nombre": nombre,
            "poblacion": int(poblacion),
            "superficie": int(superficie),
            "continente": normalizar_continente(continente)
        })
        guardar_datos("paises.csv", paises)
        print(f"✅ '{nombre}' agregado.\n")
        break

# -------------------------------
# BUSCAR
# -------------------------------
def buscar_pais(paises):
    print("\n--- BUSCAR PAÍS ---")
    nombre = prompt("Buscar: ", completer=autocompletar_nombres(paises)).strip()
    if nombre=="" or not nombre.replace(" ","").isalpha(): print("❌ Inválido."); return
    criterio=sin_acentos(nombre)
    resultados=[p for p in paises if criterio in sin_acentos(p["nombre"])]
    if not resultados: print("❌ Sin resultados."); return
    listar_paises(resultados)

# -------------------------------
# FILTRAR
# -------------------------------
def filtrar_por_poblacion_aut(paises):
    print("\n--- FILTRAR POR POBLACIÓN ---")
    print("1) Pequeños (0 - 10.000.000)")
    print("2) Medianos (10.000.001 - 60.000.000)")
    print("3) Grandes (+60.000.000)")
    print("X) Volver")
    op=input("Opción: ").strip().upper()
    match op:
        case "X": return
        case "1": minv,maxv=0,10000000
        case "2": minv,maxv=10000001,60000000
        case "3": minv,maxv=60000001,9999999999
        case _: print("❌ Inválida."); return
    listar_paises([p for p in paises if minv<=p["poblacion"]<=maxv])

def filtrar_por_superficie_aut(paises):
    print("\n--- FILTRAR POR SUPERFICIE ---")
    print("1) Pequeños (0 - 500.000 km²)")
    print("2) Medianos (500.001 - 2.000.000 km²)")
    print("3) Grandes (+2.000.000 km²)")
    print("X) Volver")
    op=input("Opción: ").strip().upper()
    match op:
        case "X": return
        case "1": minv,maxv=0,500000
        case "2": minv,maxv=500001,2000000
        case "3": minv,maxv=2000001,9999999999
        case _: print("❌ Inválida."); return
    listar_paises([p for p in paises if minv<=p["superficie"]<=maxv])

def filtrar_por_continente(paises):
    print("\n--- FILTRAR POR CONTINENTE ---")
    while True:
        cont=input("Continente (o X para volver): ").strip()
        if cont.upper()=="X": return
        if cont=="" or not cont.replace(" ","").isalpha(): print("❌ Inválido."); continue
        cont=normalizar_continente(cont)
        listar_paises([p for p in paises if sin_acentos(p["continente"])==sin_acentos(cont)])
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
        c=color_por_continente(p["continente"])
        tabla.append([
            c+p["nombre"]+Style.RESET_ALL,
            f"{p['poblacion']:,}".replace(",","."),
            f"{p['superficie']:,} km²".replace(",","."),
            c+p["continente"]+Style.RESET_ALL
        ])
    print(tabulate(tabla,headers=["nombre","poblacion","superficie","continente"],tablefmt="fancy_grid"))

# -------------------------------
# MENÚ PRINCIPAL
# -------------------------------
def main():
    paises=cargar_datos("paises.csv")
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Agregar país")
        print("2. Actualizar país")
        print("3. Buscar país")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Mostrar estadísticas")
        print("7. Salir")
        op=input("Opción: ").strip()
        match op:
            case "1": agregar_pais(paises)
            case "2": actualizar_pais(paises)
            case "3": buscar_pais(paises)
            case "4": menu_filtrar(paises)
            case "5": menu_ordenar(paises)
            case "6": mostrar_estadísticas(paises)
            case "7":
                print("👋 Saliendo...")
                break
            case _: print("❌ Opción inválida.")

if __name__=="__main__":
    main()
