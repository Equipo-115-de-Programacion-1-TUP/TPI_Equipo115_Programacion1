# ==========================
#   SISTEMA DE GESTIÓN DE PAÍSES
#   Versión 5.7 Final TPI
# ==========================

import csv
import os
from tabulate import tabulate
from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

init(autoreset=True)

# -----------------------------------------------------------------------------------
# NORMALIZO EL TEXTO PARA SI USUARIO INTRODUCE LA PALABRA CON ACENTO, SEA, INSENSIBLE
# -----------------------------------------------------------------------------------
def sin_acentos(texto):
    reemplazos={"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n"}
    texto=texto.lower()
    for a,b in reemplazos.items():
        texto=texto.replace(a,b)
    return texto

def normalizar_continente(cont):
    cont=sin_acentos(cont.strip())
    if cont in ["america","americas","latinoamerica","norteamerica","sudamerica"]:
        return "América"
    if cont=="europa": return "Europa"
    if cont=="asia": return "Asia"
    if cont=="africa": return "África"
    if cont in ["oceania","oceanía"]: return "Oceanía"
    return cont.capitalize()

def normalizar_nombre(nombre):
    return " ".join(nombre.strip().split()).capitalize()

# ----------------------------------------------------
# AGREGO COLORES A LOS PAÍSES PARA MEJOR VISUALIZACIÓN
# ----------------------------------------------------
def color_por_continente(cont):
    cont=sin_acentos(cont)
    if cont=="america": return Fore.GREEN
    if cont=="europa": return Fore.BLUE
    if cont=="asia": return Fore.YELLOW
    if cont=="africa": return Fore.RED
    if cont=="oceania": return Fore.CYAN
    return Fore.WHITE

def color_tamaño(poblacion):
    if poblacion <= 10_000_000: return Fore.LIGHTGREEN_EX
    if poblacion <= 60_000_000: return Fore.LIGHTYELLOW_EX
    return Fore.LIGHTRED_EX

def color_superficie(superficie):
    if superficie <= 500_000: return Fore.LIGHTGREEN_EX
    if superficie <= 2_000_000: return Fore.LIGHTYELLOW_EX
    return Fore.LIGHTRED_EX

# -------------------------------
# ORDENAMIENTO x NOMBRE, POBLACIÓN, SUPERFICIE
# -------------------------------
def clave_nombre(p): return p["nombre"]
def clave_poblacion(p): return p["poblacion"]
def clave_superficie(p): return p["superficie"]

def autocompletar_nombres(paises):
    return WordCompleter([p["nombre"] for p in paises], ignore_case=True)

# -------------------------------
# GUARDO LOS EN EL CSV
# -------------------------------
def guardar_datos(nombre_archivo,paises):
    with open(nombre_archivo,"w",newline="",encoding="utf-8") as archivo:
        campos=["nombre","poblacion","superficie","continente"]
        escritor=csv.DictWriter(archivo,fieldnames=campos)
        escritor.writeheader()
        for p in paises:
            escritor.writerow(p)

def cargar_datos(nombre_archivo):
    paises=[]
    if not os.path.exists(nombre_archivo):
        return paises
    with open(nombre_archivo,newline="",encoding="utf-8") as archivo:
        lector=csv.DictReader(archivo)
        for f in lector:
            if not f["poblacion"].isdigit() or not f["superficie"].isdigit():
                continue
            nombre=normalizar_nombre(f["nombre"])
            if any(sin_acentos(x["nombre"])==sin_acentos(nombre) for x in paises):
                continue
            paises.append({
                "nombre":nombre,
                "poblacion":int(f["poblacion"]),
                "superficie":int(f["superficie"]),
                "continente":normalizar_continente(f["continente"])
            })
    print(f"✅ {len(paises)} países cargados.")
    return paises

# -------------------------------
# ACTUALIZAR PAÍSES
# -------------------------------
def actualizar_pais(paises,pais_preseleccionado=None):
    print("\n--- ACTUALIZAR PAÍS ---")

    if pais_preseleccionado:
        pais=pais_preseleccionado
    else:
        while True:
            nombre=input("Nombre del país (o X para volver): ").strip()
            if nombre.upper()=="X": return
            if not nombre.replace(" ","").isalpha():
                print("❌ Nombre inválido."); continue
            for p in paises:
                if sin_acentos(p["nombre"])==sin_acentos(nombre):
                    pais=p; break
            else:
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

        if nueva_p=="" and nueva_s=="":
            print("\n❗ No ingresó valores nuevos.")
            print("1) Reintentar")
            print("2) Cancelar y volver")
            if input("Opción: ").strip()!="1":
                print("↩ Cancelado."); return
            continue

        if nueva_p=="":
            nueva_p=pais["poblacion"]
        elif nueva_p.isdigit():
            nueva_p=int(nueva_p)
        else:
            print("❌ Población inválida."); continue

        if nueva_s=="":
            nueva_s=pais["superficie"]
        elif nueva_s.isdigit():
            nueva_s=int(nueva_s)
        else:
            print("❌ Superficie inválida."); continue

        print("\n--- CONFIRMAR ---")
        print(f"Población: {pais['poblacion']:,} → {nueva_p:,}".replace(",","."))
        print(f"Superficie: {pais['superficie']:,} km² → {nueva_s:,} km²".replace(",","."))
        if input("¿Aplicar cambios? (S/N): ").upper()!="S":
            print("↩ Cancelado."); return

        pais["poblacion"]=nueva_p
        pais["superficie"]=nueva_s
        guardar_datos("paises.csv",paises)
        print("✅ Actualizado.\n")
        return

# -------------------------------
# AGREGAR PAÍS
# -------------------------------
def agregar_pais(paises):
    print("\n--- AGREGAR PAÍS ---")
    print("")
    while True:
        nombre=input("Nombre (o X para volver): ").strip()
        if nombre.upper()=="X": return
        if not nombre.replace(" ","").isalpha():
            print("❌ Nombre inválido."); continue
        nombre=normalizar_nombre(nombre)

        for p in paises:
            if sin_acentos(p["nombre"])==sin_acentos(nombre):
                print(f"\n⚠️ '{nombre}' ya existe.")
                print("1) Actualizar")
                print("2) Cancelar")
                if input("Opción: ").strip()=="1":
                    actualizar_pais(paises,p)
                return

        poblacion=input("Población: ").replace(".","")
        if not poblacion.isdigit(): print("❌ Número inválido."); continue

        superficie=input("Superficie: ").replace(".","")
        if not superficie.isdigit(): print("❌ Número inválido."); continue

        continente=input("Continente: ").strip()
        if not continente.replace(" ","").isalpha():
            print("❌ Continente inválido."); continue

        paises.append({
            "nombre":nombre,
            "poblacion":int(poblacion),
            "superficie":int(superficie),
            "continente":normalizar_continente(continente)
        })
        guardar_datos("paises.csv",paises)
        print(f"✅ '{nombre}' agregado.\n")
        return

# -------------------------------
# BUSCAR x PAÍSES
# -------------------------------
def buscar_pais(paises):
    while True:
        print("\n--- BUSCAR PAÍS ---")
        nombre = prompt("Buscar: ", completer=autocompletar_nombres(paises)).strip()

        if nombre == "" or not nombre.replace(" ","").isalpha():
            print("❌ Entrada inválida.")
            return

        criterio = sin_acentos(nombre)
        resultados = [p for p in paises if criterio in sin_acentos(p["nombre"])]

        if len(resultados) == 0:
            print("❌ No se encontraron coincidencias.")
        else:
            listar_paises(resultados)

        # preguntar si desea volver a buscar
        while True:
            seguir = input("\n¿Buscar otro país? (S/N): ").strip().upper()
            if seguir == "S":
                break   # vuelve a pedir
            if seguir == "N":
                print("↩ Volviendo al menú anterior...")
                return
            print("❌ Debe ingresar S (sí) o N (no). Intente nuevamente.")

# -------------------------------
# FILTRAR X CONTINENTE
# -------------------------------
def filtrar_por_continente(paises):
    print("\n--- FILTRAR POR CONTINENTE ---")
    while True:
        cont=input("Continente (o X para volver): ").strip()
        if cont.upper()=="X": return
        if not cont.replace(" ","").isalpha():
            print("❌ Inválido."); continue
        cont=normalizar_continente(cont)
        filtrados=[p for p in paises if sin_acentos(p["continente"])==sin_acentos(cont)]
        print(f"\n📌 Países en {cont}\n")
        listar_paises(filtrados)
        return

def filtrar_por_poblacion_aut(paises):
    print("\n====== FILTRAR POR POBLACIÓN ======")
    print("1) Pequeños (0 - 10M)")
    print("2) Medianos (10M - 60M)")
    print("3) Grandes  (+60M)")
    print("X) Volver")
    op=input("Opción: ").upper()

    match op:
        case "1": minv,maxv=0,10_000_000; texto="PEQUEÑOS (0 - 10M)"
        case "2": minv,maxv=10_000_001,60_000_000; texto="MEDIANOS (10M - 60M)"
        case "3": minv,maxv=60_000_001,9_999_999_999; texto="GRANDES (+60M)"
        case "X": return
        case _: print("❌ Inválida."); return

    filtrados=[p for p in paises if minv<=p["poblacion"]<=maxv]
    print(f"\n📌 Filtrando países: {texto}\n")
    listar_paises(filtrados)
    print("\n🟢 Pequeños   🟡 Medianos   🔴 Grandes\n")

def filtrar_por_superficie_aut(paises):
    print("\n--- FILTRAR POR SUPERFICIE ---")
    print("1) Pequeños (0 - 500.000 km²)")
    print("2) Medianos (500.001 - 2.000.000 km²)")
    print("3) Grandes  (+2.000.000 km²)")
    print("X) Volver")
    op=input("Opción: ").upper()

    match op:
        case "1": minv,maxv=0,500_000; texto="PEQUEÑOS (0 - 500k km²)"
        case "2": minv,maxv=500_001,2_000_000; texto="MEDIANOS (500k - 2M km²)"
        case "3": minv,maxv=2_000_001,9_999_999_999; texto="GRANDES (+2M km²)"
        case "X": return
        case _: print("❌ Inválida."); return

    filtrados=[p for p in paises if minv<=p["superficie"]<=maxv]
    print(f"\n📌 Filtrando países: {texto}\n")
    listar_paises(filtrados)
    print("\n🟢 Pequeños   🟡 Medianos   🔴 Grandes\n")

def menu_filtrar(paises):
    while True:
        print("\n--- FILTRAR ---")
        print("1. Por continente")
        print("2. Por rango de población (automático)")
        print("3. Por rango de superficie (automático)")
        print("X. Volver")
        op=input("Opción: ").upper()

        match op:
            case "1": filtrar_por_continente(paises)
            case "2": filtrar_por_poblacion_aut(paises)
            case "3": filtrar_por_superficie_aut(paises)
            case "X": return
            case _: print("❌ Inválida.")

# -------------------------------
# ORDENAR (con repetir)
# -------------------------------
def menu_ordenar(paises):
    while True:
        print("\n--- ORDENAR ---")
        print("1. Nombre (A-Z)")
        print("2. Población (desc.)")
        print("3. Superficie (asc.)")
        print("4. Superficie (desc.)")
        print("X. Volver")
        op=input("Opción: ").upper()

        match op:
            case "1": datos=sorted(paises,key=clave_nombre)
            case "2": datos=sorted(paises,key=clave_poblacion,reverse=True)
            case "3": datos=sorted(paises,key=clave_superficie)
            case "4": datos=sorted(paises,key=clave_superficie,reverse=True)
            case "X": return
            case _: print("❌ Inválida."); continue

        listar_paises(datos)

        print("\n¿Ordenar nuevamente?")
        print("1) Sí")
        print("2) No (volver)")
        if input("Opción: ")!="1":
            return

# -------------------------------
# ESTADÍSTICAS (DINÁMICAS + validación S/N)
# -------------------------------
def mostrar_estadisticas(paises):
    if len(paises)==0:
        print("No hay países cargados.")
        return

    while True:
        print("\n📊 ESTADÍSTICAS 📊")
        print("1. País con mayor población")
        print("2. País con menor población")
        print("3. Promedio de población")
        print("4. Promedio de superficie")
        print("5. Cantidad de países por continente")
        print("X. Volver")
        print("")

        op=input("Opción: ").upper()

        match op:
            case "1":
                mayor=paises[0]
                for p in paises:
                    if p["poblacion"]>mayor["poblacion"]:
                        mayor=p
                print(f"\n🌍 Mayor población: {mayor['nombre']} ({mayor['poblacion']:,})".replace(",","."))
            case "2":
                menor=paises[0]
                for p in paises:
                    if p["poblacion"]<menor["poblacion"]:
                        menor=p
                print(f"\n🏳️ Menor población: {menor['nombre']} ({menor['poblacion']:,})".replace(",","."))
            case "3":
                prom=sum(p["poblacion"] for p in paises)//len(paises)
                print(f"\n📈 Promedio de población: {prom:,} hab.".replace(",","."))
            case "4":
                prom=sum(p["superficie"] for p in paises)//len(paises)
                print(f"\n🌐 Promedio de superficie: {prom:,} km²".replace(",","."))
            case "5":
                cont={}
                for p in paises:
                    c=normalizar_continente(p["continente"])
                    cont[c]=cont.get(c,0)+1
                print("\n🗺️ Países por continente:")
                for k,v in cont.items():
                    print(f" - {k}: {v}")
            case "X": return
            case _: print("❌ Opción inválida."); continue

        while True:
            seguir = input("\n¿Ver otra estadística? (S/N): ").strip().upper()
            if seguir == "S":
                break
            if seguir == "N":
                print("↩ Volviendo al menú anterior...")
                return
            print("❌ Debe ingresar S (sí) o N (no). Intente nuevamente.")

# -------------------------------
# LISTAR PAÍSES
# -------------------------------
def listar_paises(paises):
    if len(paises)==0:
        print("No hay resultados.")
        return

    tabla=[]
    for p in paises:
        c1=color_por_continente(p["continente"])
        c2=color_tamaño(p["poblacion"])
        c3=color_superficie(p["superficie"])

        tabla.append([
            c1+p["nombre"]+Style.RESET_ALL,
            c2+f"{p['poblacion']:,}".replace(",",".")+Style.RESET_ALL,
            c3+f"{p['superficie']:,} km²".replace(",",".")+Style.RESET_ALL,
            c1+p["continente"]+Style.RESET_ALL
        ])

    print(tabulate(tabla,headers=["nombre","poblacion","superficie","continente"],tablefmt="fancy_grid"))

# -------------------------------
# MENÚ PRINCIPAL
# -------------------------------
def main():
    paises=cargar_datos("paises.csv")
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("")
        print("1. Agregar país")
        print("2. Actualizar país")
        print("3. Buscar país")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Mostrar estadísticas")
        print("7. Salir")
        print("")
        print("======--↓--======")
        print("")

        op=input("Opción: ").strip()

        match op:
            case "1": agregar_pais(paises)
            case "2": actualizar_pais(paises)
            case "3": buscar_pais(paises)
            case "4": menu_filtrar(paises)
            case "5": menu_ordenar(paises)
            case "6": mostrar_estadisticas(paises)
            case "7": print("👋 Saliendo..."); break
            case _: print("❌ Opción inválida.")

if __name__=="__main__":
    main()
