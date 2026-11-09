"""
Control de Gastos Personales
Proyecto Final Integrador - Python Junior

MAPA DEL PROGRAMA (en el orden en que está escrito el archivo)
    BLOQUE 1: Imports y configuración   -> módulos, nombres de archivos, columnas
    BLOQUE 2: Base de datos en memoria  -> la lista "gastos"
    BLOQUE 3: Persistencia (CSV)        -> cargar_gastos() y guardar_gastos()
    BLOQUE 4: Lógica principal          -> agregar, calcular totales y mostrar
    BLOQUE 5: Pruebas automáticas       -> ejecutar_pruebas()
    BLOQUE 6: Programa principal        -> main()
    BLOQUE 7: Punto de entrada          -> if __name__ == "__main__"

ORDEN REAL DE EJECUCIÓN (al correr: python3 Control_gastos.py)
    1) Python lee el archivo de arriba hacia abajo y SOLO DEFINE las funciones
       (todavía no se ejecuta ninguna).
    2) Al llegar al BLOQUE 7 se llama a ejecutar_pruebas()
       -> prueba todo con archivos TEMPORALES (no toca tus datos reales).
    3) Si todas las pruebas pasan, se llama a main()
       -> programa real: lee gastos_entrada.csv, agrega gastos,
          muestra totales y guarda gastos_salida.csv.
"""

# =============================================================================
# BLOQUE 1: IMPORTS Y CONFIGURACIÓN
# =============================================================================

import csv  # Módulo para leer y escribir archivos CSV
import os   # Módulo para trabajar con archivos y rutas del sistema

# Carpeta donde está ESTE script (no la carpeta desde donde se ejecuta).
# Así los CSV siempre se buscan y se crean junto al script.
CARPETA = os.path.dirname(os.path.abspath(__file__))

# Constantes (en MAYÚSCULAS por convención: son valores fijos)
ARCHIVO_ENTRADA = os.path.join(CARPETA, "gastos_entrada.csv")  # De donde se LEE
ARCHIVO_SALIDA = os.path.join(CARPETA, "gastos_salida.csv")    # Donde se GUARDA
CAMPOS = ["monto", "categoria", "descripcion"]  # Columnas del CSV y su orden


# =============================================================================
# BLOQUE 2: BASE DE DATOS EN MEMORIA
# =============================================================================

# Lista global que guarda todos los gastos mientras el programa corre.
# Cada gasto es un diccionario, por ejemplo:
# {"monto": 50.0, "categoria": "Comida", "descripcion": "Farmacia"}
# Vive en la memoria RAM: se pierde al cerrar el programa (por eso existe el CSV).
gastos = []


# =============================================================================
# BLOQUE 3: PERSISTENCIA (LEER Y GUARDAR EN CSV)
# =============================================================================

def cargar_gastos(archivo: str = ARCHIVO_ENTRADA) -> None:
    """
    Carga los gastos desde un CSV hacia la lista en memoria.
    Si el archivo no existe, la lista queda vacía.
    Las filas dañadas se omiten y se avisa por pantalla.
    """
    # Paso 1: vaciar la lista para no duplicar datos si se llama dos veces
    gastos.clear()

    # Paso 2: si el archivo no existe, avisar y salir (evita FileNotFoundError)
    if not os.path.exists(archivo):
        print(f"Aviso: '{archivo}' no existe. Se inicia sin gastos.")
        return

    # Paso 3: leer el archivo (el try externo atrapa fallas de disco o permisos)
    try:
        # "with" abre el archivo y lo cierra solo al terminar
        with open(archivo, newline="", encoding="utf-8") as f:
            # DictReader entrega cada fila como diccionario (todo llega como texto)
            lector = csv.DictReader(f)

            # start=2 porque la fila 1 es el encabezado (así coincide con Excel)
            for numero_fila, fila in enumerate(lector, start=2):
                # El try interno atrapa una fila mala sin detener las demás
                try:
                    # Reutiliza agregar_gasto: el CSV pasa por las mismas validaciones
                    agregar_gasto(fila["monto"], fila["categoria"], fila["descripcion"])
                except (ValueError, KeyError, TypeError, AttributeError) as error:
                    # ValueError: dato inválido | KeyError: falta una columna
                    # TypeError/AttributeError: fila incompleta
                    print(f"Fila {numero_fila} inválida, se omite ({error}).")
    except OSError as error:
        # Errores del sistema de archivos (permisos, disco, etc.)
        print(f"Error al leer el archivo: {error}")


def guardar_gastos(archivo: str = ARCHIVO_SALIDA) -> None:
    """Guarda la lista de gastos en un CSV (reemplaza el contenido anterior)."""
    try:
        # "w" = escritura: crea el archivo o lo REEMPLAZA por completo
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            # DictWriter escribe cada diccionario como una fila, en el orden de CAMPOS
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()       # Escribe: monto,categoria,descripcion
            escritor.writerows(gastos)   # Escribe todos los gastos de una vez
    except OSError as error:
        # Si no puede escribir, avisa en vez de romper el programa
        print(f"Error al guardar el archivo: {error}")


# =============================================================================
# BLOQUE 4: LÓGICA PRINCIPAL (AGREGAR, CALCULAR Y MOSTRAR)
# =============================================================================

def agregar_gasto(monto, categoria: str, descripcion: str) -> dict:
    """
    Agrega un gasto validado a la lista.

    Args:
        monto: Monto del gasto (número mayor que 0).
        categoria (str): Categoría del gasto (no vacía).
        descripcion (str): Descripción corta (no vacía).

    Returns:
        dict: El gasto creado.

    Raises:
        ValueError: Si el monto no es numérico o no es mayor que 0,
                    o si la categoría o descripción están vacías.
    """
    # --- VALIDACIONES (primero se valida, después se guarda) ---

    # Validación 1: convertir el monto a número (el CSV entrega texto)
    try:
        monto = float(monto)
    except (TypeError, ValueError):
        # Cambia el error de Python por uno propio con mensaje claro
        raise ValueError("El monto debe ser un número.")

    # Validación 2: el monto debe ser mayor que 0 (requisito del enunciado)
    # "raise" corta la función: lo que sigue no se ejecuta
    if monto <= 0:
        raise ValueError("El monto debe ser mayor que 0.")

    # Validación 3 y 4: categoría y descripción no vacías
    # .strip() quita espacios; un texto vacío cuenta como "falso"
    if not categoria.strip():
        raise ValueError("La categoría no puede estar vacía.")

    if not descripcion.strip():
        raise ValueError("La descripción no puede estar vacía.")

    # --- CREAR Y GUARDAR EL GASTO (solo se llega aquí si todo es válido) ---

    # .title() pone mayúscula inicial: "comida" -> "Comida"
    gasto = {
        "monto": monto,
        "categoria": categoria.strip().title(),
        "descripcion": descripcion.strip(),
    }

    gastos.append(gasto)  # Agrega el diccionario al final de la lista
    return gasto          # Devuelve el gasto creado


def calcular_total_gastos() -> float:
    """Devuelve la suma de todos los gastos."""
    total = 0  # Acumulador: empieza en cero

    # Recorre cada gasto y suma su monto al acumulador
    for gasto in gastos:
        total += gasto["monto"]

    # El return va FUERA del for: devuelve el total cuando termina el ciclo
    return total


def calcular_total_categoria(categoria: str) -> float:
    """Devuelve la suma de los gastos de una categoría (ignora mayúsculas)."""
    total = 0  # Acumulador: empieza en cero

    for gasto in gastos:
        # Compara en minúsculas para que "Comida", "comida" y "COMIDA" sean iguales
        if gasto["categoria"].lower() == categoria.strip().lower():
            total += gasto["monto"]  # Solo suma si la categoría coincide

    # Si la categoría no existe, devuelve 0 (sin error)
    return total


def mostrar_gastos() -> None:
    """Muestra todos los gastos registrados."""
    # Si la lista está vacía, avisa y sale
    if not gastos:
        print("No existen gastos.")
        return

    print("\nTodos los gastos:")  # \n deja una línea en blanco antes

    # enumerate numera los gastos empezando en 1
    for indice, gasto in enumerate(gastos, start=1):
        # :.2f muestra el monto con 2 decimales (50.0 -> 50.00)
        print(
            f"{indice}. {gasto['categoria']} - "
            f"{gasto['descripcion']} : ${gasto['monto']:.2f}"
        )


# =============================================================================
# BLOQUE 5: PRUEBAS AUTOMÁTICAS
# Usan archivos TEMPORALES: no tocan los datos reales.
# =============================================================================

def ejecutar_pruebas() -> None:
    """Se prueba un caso normal, uno límite, datos incorrectos y la persistencia."""
    # Empieza con la lista limpia para no mezclar datos
    gastos.clear()

    # Archivos temporales que se crean y se borran durante las pruebas
    temp_entrada = os.path.join(CARPETA, "prueba_entrada.csv")
    temp_salida = os.path.join(CARPETA, "prueba_salida.csv")

    try:
        # --- Prueba 1: CASO NORMAL (datos válidos) ---
        agregar_gasto(50, "Comida", "Farmacia")
        agregar_gasto(20, "Transporte", "Taxi")
        agregar_gasto(100, "comida", "Restaurante")  # minúscula a propósito
        # assert: si la condición es falsa, el programa se detiene con AssertionError
        assert calcular_total_gastos() == 170
        assert calcular_total_categoria("COMIDA") == 150  # ignora mayúsculas
        print("Prueba 1 (normal): OK")

        # --- Prueba 2: CASO LÍMITE (monto mínimo y categoría inexistente) ---
        agregar_gasto(0.01, "Otros", "Chicle")
        # round(..., 2) evita problemas de precisión con decimales
        assert round(calcular_total_gastos(), 2) == 170.01
        assert calcular_total_categoria("Salud") == 0  # no existe -> 0
        print("Prueba 2 (límite): OK")

        # --- Prueba 3: DATOS INCORRECTOS (cada uno debe lanzar ValueError) ---
        casos_invalidos = [
            (0, "Entretenimiento", "Cine"),   # monto cero
            (-5, "Comida", "Prueba"),         # monto negativo
            ("abc", "Comida", "Prueba"),      # monto no numérico
            (10, "", "Prueba"),               # categoría vacía
        ]
        for monto, categoria, descripcion in casos_invalidos:
            try:
                agregar_gasto(monto, categoria, descripcion)
                # Si llega aquí, NO falló y la prueba debe fallar
                # (AssertionError no es ValueError, así que el except no lo atrapa)
                raise AssertionError(f"Debió fallar con monto={monto!r}")
            except ValueError as error:
                print(f"Prueba 3 (inválido) OK -> {error}")

        # --- Prueba 4: PERSISTENCIA (guardar en un archivo y cargar de otro) ---
        total_antes = calcular_total_gastos()
        guardar_gastos(temp_salida)             # guarda la lista en un CSV
        os.replace(temp_salida, temp_entrada)   # la salida pasa a ser la entrada
        gastos.clear()                          # vacía la memoria
        cargar_gastos(temp_entrada)             # recupera desde el CSV
        # El total recuperado debe ser igual al que había antes de guardar
        assert round(calcular_total_gastos(), 2) == round(total_antes, 2)
        print("Prueba 4 (persistencia CSV): OK")

        # --- Prueba 5: ARCHIVO CON UNA FILA DAÑADA (se omite, no se rompe) ---
        with open(temp_entrada, "w", newline="", encoding="utf-8") as f:
            f.write("monto,categoria,descripcion\n")
            f.write("30,Comida,Almuerzo\n")   # fila válida
            f.write("xyz,Comida,Dañada\n")    # fila dañada (monto no numérico)
        cargar_gastos(temp_entrada)
        assert len(gastos) == 1  # solo la fila válida se cargó
        print("Prueba 5 (fila dañada): OK")

    finally:
        # "finally" se ejecuta SIEMPRE, pase lo que pase en las pruebas.
        # Limpieza: borra los archivos temporales y vacía la lista.
        for archivo in (temp_entrada, temp_salida):
            if os.path.exists(archivo):
                os.remove(archivo)
        gastos.clear()

    print("\nTodas las pruebas pasaron.\n")


# =============================================================================
# BLOQUE 6: PROGRAMA PRINCIPAL (USO REAL, PIPELINE EXTRACT -> TRANSFORM -> LOAD)
# =============================================================================

def main() -> None:
    """Carga la entrada, agrega gastos nuevos, muestra totales y guarda la salida."""
    # 1. EXTRACT: lee gastos_entrada.csv y llena la lista en memoria
    cargar_gastos(ARCHIVO_ENTRADA)

    # 2. TRANSFORM: agrega gastos nuevos con validación
    try:
        agregar_gasto(35, "Salud", "Consulta")  # válido: se agrega
        agregar_gasto(0, "Ocio", "Cine")        # inválido a propósito: lanza ValueError
    except ValueError as error:
        # El error se atrapa y el programa continúa sin romperse
        print("Error:", error)

    # 3. REPORTE: calcula y muestra los resultados
    print("\nTotal gastos:", calcular_total_gastos())
    print("Total comida:", calcular_total_categoria("Comida"))
    mostrar_gastos()

    # 4. LOAD: guarda el resultado en gastos_salida.csv
    guardar_gastos(ARCHIVO_SALIDA)
    print(f"\nResultado guardado en '{ARCHIVO_SALIDA}'.")


# =============================================================================
# BLOQUE 7: PUNTO DE ENTRADA
# =============================================================================

# Este bloque solo corre si ejecuto este archivo directamente
# (no si otro archivo lo importa como módulo).
if __name__ == "__main__":
    ejecutar_pruebas()  # 1º: verifica que todo funcione (con archivos temporales)
    main()              # 2º: ejecuta el programa real
