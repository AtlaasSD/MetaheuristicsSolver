import sys
import os
import random
import json
import dataset_generator

# El import "dataset_generator" es un archivo que se encuentra en la misma carpeta que este archivo.
# Este archivo se encarga de generar datasets aleatorios y fijos para la mochila binaria.
# Los imports de arriba son default, es decir, no necesitan ser instalados.
# Cualquier duda sobre el codigo pueden escribirme, igual lo dejé muy documentado jajaja

# =====================================================================
# UTILIDADES DE INTERFAZ Y CONSOLA
# =====================================================================

BOLD = "\033[1m"
RESET = "\033[0m"

def limpiar_pantalla():
    """
    Limpia la terminal de comandos. Utiliza 'cls' en Windows y 'clear' en Linux/Mac.
    Mantiene la consola libre de texto para que no se sature la vista y sea más fácil de entender.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo():
    """Muestra el título principal"""
    limpiar_pantalla()
    print(f"{BOLD}{'='*80}{RESET}")
    print(f"{BOLD}{' '*25}RESOLUCIÓN DE MOCHILA BINARIA{RESET}")
    print(f"{BOLD}{' '*23}POR METAHEURÍSTICAS DE INDICADORES{RESET}")
    print(f"{BOLD}{'='*80}{RESET}\n")

def ingresar_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita un entero al usuario. Valida repetidamente hasta asegurar que la entrada cumple las regas.
    """
    while True:
        try:
            val = int(input(mensaje))
            if minimo is not None and val < minimo:
                print(f"Error: El valor debe ser al menos {minimo}.")
                continue
            if maximo is not None and val > maximo:
                print(f"Error: El valor debe ser como máximo {maximo}.")
                continue
            return val
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def ingresar_float(mensaje):
    """Solicita un número de punto flotante de forma segura."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido.")

def print_table(headers, rows):
    """
    Genera y tabula estéticamente los datos de forma automática.
    """
    if not headers:
        return
    
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
            
    separador = "-+-".join('-' * w for w in col_widths)
    head_fmt = " | ".join(f"{BOLD}{{:<{w}}}{RESET}" for w in col_widths)
    data_fmt = " | ".join(f"{{:<{w}}}" for w in col_widths)
    
    top_border = "+" + "-"*(len(separador)+2) + "+"
    print(top_border)
    print("| " + head_fmt.format(*headers) + " |")
    print("+" + separador + "+")
    for r in rows:
        print("| " + data_fmt.format(*r) + " |")
    print(top_border)

# =====================================================================
# FLUJO DEL MENÚ PRINCIPAL
# =====================================================================

def menu_principal():
    """
    Bucle principal de la aplicación.
    Con dos opciones: Nuevo Ejercicio y Salir.
    Esto se hace para que el programa no muera tras resolver un ejercicio,
    así seguirá en constante ejecución y el usuario podrá resolver ejercicios
    hasta que decida salir.
    """
    # Genera el dataset fijo en su disco por si luego decide escribir 'dataset_fijo.json'
    # Ignoren este dataset, el dataset fijo es realmente el del ejercicio que hicimos en Excel
    # Lo usé para validar que el código diera resultados correctos, lo dejo para que revisen ustedes
    # Si hacen algún cambio, revisen que siga funcionando correctamente con este dataset.
    dataset_generator.obtener_dataset_fijo()
    
    while True:
        mostrar_titulo()
        print(f"{BOLD}MENÚ PRINCIPAL{RESET}")
        print("1. Nuevo Ejercicio")
        print("2. Salir")
        
        opc = ingresar_entero("\nSeleccione una opción: ", 1, 2)
        if opc == 2:
            print("\nSaliendo del programa... ¡Hasta luego!")
            break
        elif opc == 1:
            ejecutar_flujo_ejercicio()


def ejecutar_flujo_ejercicio():
    """
    Orquestador del ejercicio, sigue un flujo definido para solucionar cualquier ejercicio.
    Primero mostrando menús donde se eligen opciones o se digita información.
    """
    limpiar_pantalla()
    print(f"{BOLD}CARGA DE DATOS{RESET}")
    print("1. Digitar valores manualmente")
    print("2. Cargar un dataset")
    
    opc_datos = ingresar_entero("\nSeleccione una opción: ", 1, 2)
    
    items = []
    if opc_datos == 1:
        n_items = ingresar_entero("\n¿Cuántos productos desea ingresar?: ", 1, 100)
        for i in range(1, n_items + 1):
            print(f"\nProducto {BOLD}X{i}{RESET}:")
            c = ingresar_entero("  Costo (Ci): ", 1)
            v = ingresar_entero("  Volumen (Vi): ", 1)
            items.append({"id": f"X{i}", "cost": c, "volume": v})
            
    elif opc_datos == 2:
        print("\nElija qué hacer:")
        print("1. Cargar desde archivo existente")
        print("2. Generar un NUEVO dataset aleatorio")
        opc_sub = ingresar_entero("Seleccione una opción: ", 1, 2)
        
        if opc_sub == 1:
            while True:
                filename = input("\nIngrese el nombre del archivo con su extensión (ej.dataset_aleatorio.json): ").strip()
                if not filename.endswith('.json'):
                    filename += '.json'
                    
                if not os.path.exists(filename):
                     print(f"Error: El archivo '{filename}' no se encuentra en el directorio.")
                     continue
                     
                try:
                     with open(filename, 'r', encoding='utf-8') as f:
                          items = json.load(f)
                     print(f"\nSe cargaron {BOLD}{len(items)}{RESET} productos del archivo '{filename}'.")
                     break
                except Exception as e:
                     print(f"Error al leer el archivo. Intente de nuevo. ({e})")
        else:
            n_items = ingresar_entero("\n¿Cuántos ítems desea que tenga el dataset aleatorio?: ", 1)
            dataset_generator.generar_dataset_aleatorio("dataset_aleatorio.json", n_items)
            with open("dataset_aleatorio.json", 'r', encoding='utf-8') as f:
                items = json.load(f)
            print(f"\nSe cargaron {BOLD}{len(items)}{RESET} productos generados al azar.")

    capacidad_mochila = ingresar_entero("\nIngrese la Capacidad máxima (Volumen) de la Mochila: ", 1)

    # Menú 2. Seleccionar metaheurística -> Aquí el usuario elige el tipo de metaheurística a aplicar
    limpiar_pantalla()
    print(f"{BOLD}TIPO DE METAHEURÍSTICA{RESET}")
    print("1. Constructivas")
    print("2. De reducción")
    print("3. De descomposición")
    tipo_meta = ingresar_entero("Seleccione el enfoque a utilizar: ", 1, 3)

    # Menú de Heurísticas de Sensibilidad -> Aquí el usuario elige la heurística a aplicar
    heuristicas_nombres = {
        1: "Mayor costo",
        2: "Menor volumen",
        3: "Mayor combinación lineal de factores",
        4: "Mayor costo / volumen",
        5: "Azar",
        6: "Alternancia",
        7: "Menor capacidad residual libre"
    }

    def pedir_heuristicas_lista(mensaje="Ingrese los números (separados por coma, ej: 1,3,4): "):
        """
        Helper visual para listar y recolectar las heurísticas múltiples solicitadas.
        Se utiliza un formato separado por comas, se valida siempre que se digite algo valido para evitar errores.
        """
        limpiar_pantalla()
        print(f"{BOLD}HEURÍSTICAS DE SENSIBILIDAD{RESET}")
        for k,v in heuristicas_nombres.items():
            print(f" {BOLD}{k}.{RESET} {v}")
            
        while True:
            sel = input('\n' + mensaje)
            try:
                opciones = [int(x.strip()) for x in sel.split(',')]
                fallos = [x for x in opciones if x < 1 or x > 7]
                if fallos:
                    print(f"Error: Opciones inválidas {fallos}.")
                    continue
                return opciones
            except ValueError:
                print("Error: Formato inválido.")

    configuraciones = [] 

    if tipo_meta in (1, 2):
        # Para Constructivas (empieza vacía y va metiendo ítems según el criterio) 
        # y Reducción (empieza llena y va sacando ítems según el criterio)
        seleccionadas = pedir_heuristicas_lista()
        configuraciones = armar_configuraciones(seleccionadas)
        ejecutar_solucionador(items, capacidad_mochila, tipo_meta, configuraciones)
        
    elif tipo_meta == 3:
        # Enfoque Descomposición (Se pregunta al usuario en cuanto quiere particionar la mochila)
        partes = ingresar_entero("\n¿En cuántas partes desea dividir la mochila? ", 2, 20)
        submochilas = []
        volumen_restante = capacidad_mochila
        
        for i in range(partes):
            limpiar_pantalla()
            print(f"{BOLD}--- CONFIGURANDO SUBMOCHILA {i+1} ---{RESET}")
            print(f"Capacidad global no asignada aún: {BOLD}{volumen_restante}{RESET}\n")
            cap = ingresar_entero(f"Asigne capacidad para la submochila {i+1}: ", 1, volumen_restante)
            volumen_restante -= cap
            
            print(f"\nSeleccione LA heurística para esta submochila:")
            h_sel = pedir_heuristicas_lista(mensaje="Ingrese SOLAMENTE un número de la lista (ej: 1): ")
            h_sel = h_sel[0] # Tomar solo primera
            conf = armar_configuraciones([h_sel])[0] 
            
            submochilas.append({
                "capacidad": cap,
                "config": conf
            })
            
        ejecutar_solucionador_descomposicion(items, capacidad_mochila, submochilas)
        
    print("\n-> Operación Finalizada.")
    input(f"{BOLD}Presione Enter para regresar al Menú Principal...{RESET}")


def armar_configuraciones(opciones):
    """
    Recibe los números de heurísticas ingresadas y 
    las formatea en diccionarios de configuración. Para combinaciones e hibridaciones,
    solicita los factores extra de el usuario (K1, K2 para combinaciones, Semillas para randomizar, etc).
    """
    confs = []
    for opc in list(set(opciones)):
        if opc == 3:
            num_comb = ingresar_entero(f"\n[{BOLD}Combinación Lineal{RESET}] ¿Cuántas combinaciones diferentes usarás? ", 1)
            for j in range(num_comb):
                print(f"\n  Combinación {j+1}:")
                k1 = ingresar_float("    Ingrese el valor de K1 para Costo: ")
                k2 = ingresar_float("    Ingrese el valor de K2 para Volumen: ")
                confs.append({"id": 3, "nombre": f"Comb. Lineal (K1={k1}, K2={k2})", "k1":k1, "k2":k2})
        elif opc == 5:
            semilla = ingresar_entero(f"\n[{BOLD}Azar{RESET}] Ingrese el número semilla: ")
            confs.append({"id": 5, "nombre": f"Azar (Semilla={semilla})", "semilla": semilla})
        elif opc == 6:
            print(f"\n[{BOLD}Alternancia{RESET}] Referencia de Reglas Base:")
            print(" 1. Mayor costo  | 2. Menor volumen | 3. Mayor cost/vol | 4. Menor residual")
            while True:
                sel = input("Ingrese hasta 3 números (1-4) separados por coma (el orden de aplicación): ")
                try:
                    seq = [int(x.strip()) for x in sel.split(',')]
                    if not (1 <= len(seq) <= 3) or any(not (1 <= x <= 4) for x in seq):
                        print("Por favor respete el margen (1 a 3 elementos válidos).")
                        continue
                    confs.append({"id": 6, "nombre": f"Alternancia ({'-'.join(map(str, seq))})", "seq": seq})
                    break
                except ValueError:
                    print("Formato inválido.")
        else:
            names = {1:"Mayor Costo", 2:"Menor Volumen", 4:"Mayor Costo/Volumen", 7:"Menor Capacidad Residual (Mayor Vol)"}
            confs.append({"id": opc, "nombre": names[opc]})
    return confs


# =====================================================================
# MOTORES MATEMÁTICOS DE RESOLUCIÓN
# =====================================================================

def score_item(item, conf_id, extra_params=None):
    """
    Determina cuán bueno es un producto evaluado con una heurística específica.
    Retornamos valores relativos asegurando que un mayor número siempre represente una mejor calificación.
    """
    if conf_id == 1:
        return item['cost']
    elif conf_id == 2:
        return -item['volume'] 
    elif conf_id == 3:
        return extra_params['k1'] * item['cost'] + extra_params['k2'] * item['volume']
    elif conf_id == 4:
        return item['cost'] / item['volume']
    elif conf_id == 7:
        return item['volume'] 
    return 0

def resolver_constructivo(items_orig, capacidad, config):
    """
    Algoritmo Constructivo: 
    Intenta llenar la mochila de capacidad N desde 0 
    incluyendo los artículos de mayor puntaje.
    """
    items = [dict(i) for i in items_orig]
    
    if config['id'] == 5: 
        rnd = random.Random(config['semilla'])
        rnd.shuffle(items)
    elif config['id'] == 6: 
        seq = config['seq']
        mapeo = {1:1, 2:2, 3:4, 4:7}
        seq = [mapeo[x] for x in seq]
    else: 
        items.sort(key=lambda x: score_item(x, config['id'], config), reverse=True)

    mochila = []
    v_actual = 0
    c_actual = 0
    
    if config['id'] == 6:
        # Lógica de matriz de Alternancia
        disponibles = items
        turno = 0
        while disponibles and v_actual < capacidad:
            heur_actual = seq[turno % len(seq)]
            disponibles.sort(key=lambda x: score_item(x, heur_actual), reverse=True)
            
            elegido = None
            for p in disponibles:
                if v_actual + p['volume'] <= capacidad:
                    elegido = p
                    break
            
            if elegido:
                mochila.append(elegido)
                v_actual += elegido['volume']
                c_actual += elegido['cost']
                disponibles.remove(elegido)
                turno += 1
            else:
                break 
    else:
        # Lógica normal
        for p in items:
            if v_actual + p['volume'] <= capacidad:
                mochila.append(p)
                v_actual += p['volume']
                c_actual += p['cost']
                
    return mochila, c_actual, v_actual

def resolver_reduccion(items_orig, capacidad, config):
    """
    Algoritmo de Reducción:
    Mete todos los artículos forzadamente e inicia a eliminar aquellos con 
    el peor puntaje para reducir el volumen hasta la capacidad permitida.
    """
    mochila = [dict(i) for i in items_orig]
    v_actual = sum(p['volume'] for p in mochila)
    c_actual = sum(p['cost'] for p in mochila)
    
    if v_actual <= capacidad:
        return mochila, c_actual, v_actual
    
    if config['id'] == 5:
        rnd = random.Random(config['semilla'])
        rnd.shuffle(mochila)
        while v_actual > capacidad and mochila:
             quitado = mochila.pop() 
             v_actual -= quitado['volume']
             c_actual -= quitado['cost']
             
    elif config['id'] == 6:
        seq = config['seq']
        mapeo = {1:1, 2:2, 3:4, 4:7}
        seq = [mapeo[x] for x in seq]
        turno = 0
        while v_actual > capacidad and mochila:
            heur_actual = seq[turno % len(seq)]
            # Reverse=False ubica a la calificación más mala de primera
            mochila.sort(key=lambda x: score_item(x, heur_actual), reverse=False)
            quitado = mochila.pop(0) 
            v_actual -= quitado['volume']
            c_actual -= quitado['cost']
            turno += 1
            
    else:
        mochila.sort(key=lambda x: score_item(x, config['id'], config), reverse=False)
        while v_actual > capacidad and mochila:
             quitado = mochila.pop(0) 
             v_actual -= quitado['volume']
             c_actual -= quitado['cost']
             
    return mochila, c_actual, v_actual

# =====================================================================
# RENDERIZADO AL USUARIO
# =====================================================================

def mostrar_tabla_global(items):
    """Genera la vista de los datos iniciales del ejercicio."""
    limpiar_pantalla()
    print(f"{BOLD}MATRIZ DE DE DATOS INICIALES{RESET}")
    headers = ["Id (Xi)", "Costo (Ci)", "Volumen (Vi)", "Ci / Vi Ratio"]
    rows = []
    
    def key_id(x):
        try: return int(x['id'][1:])
        except: return x['id']
        
    for it in sorted(items, key=key_id):
        ratio = round(it['cost'] / it['volume'], 2)
        rows.append([it['id'], it['cost'], it['volume'], ratio])
        
    print_table(headers, rows)

def graficar_resultados_heuristicas(items, resultados):
    """
    Presenta las tabulaciones que reflejan el ejercicio.
    """
    mejor_nombre = ""
    mejor_c = -1
    
    for r in resultados:
        if r['total_c'] > mejor_c:
            mejor_c = r['total_c']
            mejor_nombre = r['conf_name']
            
    print("\n")
    print("*"*80)
    print(f"{BOLD}{' '*25}>> RESULTADOS POR HEURÍSTICA <<{RESET}")
    print("*"*80)
    
    for r in resultados:
        print(f"\n{BOLD}[ --- {r['conf_name'].upper()} --- ]{RESET}")
        
        headers = ["Producto Agregado", "Costo (Ci)", "Volumen (Vi)"]
        rows = []
        vec_sol = {x['id']: 0 for x in items}
        
        for m in r['mochila']:
            rows.append([m['id'], m['cost'], m['volume']])
            vec_sol[m['id']] = 1 
            
        rows.append(["-"*10, "-"*10, "-"*10]) 
        rows.append(["TOTAL Z(C) / Z(V)", str(r['total_c']), str(r['total_v'])])
        
        print_table(headers, rows)
        
        def sort_keys(k):
             try: return int(k[1:])
             except: return k
             
        vec_strs = [str(vec_sol[k]) for k in sorted(vec_sol.keys(), key=sort_keys)]
        print(f"{BOLD}VECTOR SOLUCIÓN X{RESET} = {' '.join(vec_strs)}")
        
    print("\n" + "="*80)
    print(f"MEJOR SOLUCIÓN ENCONTRADA: {BOLD}{mejor_nombre.upper()}{RESET} con Costo Z(C) de {BOLD}{mejor_c}{RESET}")
    print("="*80)

def ejecutar_solucionador(items, capacidad, tipo_meta, configuraciones):
    mostrar_tabla_global(items)
    
    resultados = []
    for conf in configuraciones:
        if tipo_meta == 1:
            mochila, tc, tv = resolver_constructivo(items, capacidad, conf)
        else: 
            mochila, tc, tv = resolver_reduccion(items, capacidad, conf)
            
        resultados.append({
            'conf_name': conf['nombre'],
            'mochila': mochila,
            'total_c': tc,
            'total_v': tv
        })
        
    graficar_resultados_heuristicas(items, resultados)


def ejecutar_solucionador_descomposicion(items_orig, capacidad, submochilas):
    mostrar_tabla_global(items_orig)
    
    pool_disponible = [dict(i) for i in items_orig]
    mochila_global = [] 
    c_global = 0
    v_global = 0
    
    print(f"\n{BOLD}--- INICIANDO PROCESO DE DESCOMPOSICIÓN ---{RESET}")
    resultados_parciales = []
    
    for i, sub in enumerate(submochilas):
        conf = sub['config']
        cap = sub['capacidad']
        
        mochila_sub, tc_sub, tv_sub = resolver_constructivo(pool_disponible, cap, conf)
        
        elementos_a_quitar = set(x['id'] for x in mochila_sub)
        pool_disponible = [x for x in pool_disponible if x['id'] not in elementos_a_quitar]
        
        mochila_global.extend(mochila_sub)
        c_global += tc_sub
        v_global += tv_sub
        
        resultados_parciales.append({
            'conf_name': f"Sub. {i+1} - {conf['nombre']} (Cap. Int: {cap})",
            'mochila': mochila_sub,
            'total_c': tc_sub,
            'total_v': tv_sub
        })
        
    resultados_parciales.append({
        'conf_name': "RESULTADO GLOBAL SUMADO (DESCOMPOSICIÓN)",
        'mochila': mochila_global,
        'total_c': c_global,
        'total_v': v_global
    })
    
    graficar_resultados_heuristicas(items_orig, resultados_parciales)
    
if __name__ == "__main__":
    os.environ["COLORTERM"] = "truecolor" 
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nPrograma finalizado forzosamente por el usuario.")
        sys.exit(0)
