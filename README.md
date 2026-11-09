# Control de Gastos Personales

Stephano Vivanco
Proyecto Final Integrador – Python Junior

## Objetivo del proyecto

Resolver un problema cotidiano: llevar el control de los gastos personales. Muchas personas anotan sus gastos de forma desordenada y no saben cuánto gastaron en total ni por categoría. Este programa registra gastos validados, calcula totales y guarda los datos en un archivo CSV para no perderlos al cerrar el programa.

## Funcionalidades

- Cargar gastos desde un archivo CSV (`gastos_entrada.csv`).
- Agregar gastos con validación (monto numérico y mayor que 0, categoría y descripción no vacías).
- Calcular el total general de gastos.
- Calcular el total de una categoría (sin distinguir mayúsculas y minúsculas).
- Mostrar todos los gastos numerados y con dos decimales.
- Guardar el resultado en un archivo CSV (`gastos_salida.csv`).
- Omitir y avisar de las filas dañadas del CSV sin detener el programa.
- Ejecutar pruebas automáticas antes del programa real.

## Tecnologías

- Python 3 (solo biblioteca estándar: `csv` y `os`).
- Archivos CSV para la persistencia.
- Sin dependencias externas ni frameworks.

## Requisitos

- Python 3.8 o superior.
- No se necesita instalar paquetes (`requirements.txt` no es necesario).

## Instalación

```bash
git clone https://github.com/TU_USUARIO/control-gastos.git
cd control-gastos
```

## Ejecución

```bash
python3 Control_gastos.py
```

El programa funciona en dos pasos:

1. Ejecuta `ejecutar_pruebas()` con archivos temporales (no toca tus datos reales).
2. Si todas las pruebas pasan, ejecuta `main()`: lee `gastos_entrada.csv`, agrega un gasto válido y uno inválido a propósito (para mostrar el manejo de errores), imprime los totales y guarda `gastos_salida.csv`.

Los archivos CSV se buscan y crean junto al script, sin importar desde qué carpeta se ejecute.

## Estructura del proyecto

```
control-gastos/
├── Control_gastos.py      # Código fuente
├── gastos_entrada.csv     # Datos de ejemplo (entrada)
├── README.md              # Esta documentación
└── .gitignore
```

`gastos_salida.csv` se genera al ejecutar el programa.

## Almacenamiento de datos

Cada gasto es un diccionario dentro de la lista global `gastos`:

```python
{"monto": 50.0, "categoria": "Comida", "descripcion": "Farmacia"}
```

Como la lista vive en memoria RAM, se pierde al cerrar el programa. Por eso se usa CSV:

- **Lectura:** `cargar_gastos()` usa `csv.DictReader` y pasa cada fila por `agregar_gasto()`, de modo que los datos del archivo reciben las mismas validaciones que los ingresados a mano.
- **Escritura:** `guardar_gastos()` usa `csv.DictWriter` y reemplaza el contenido anterior del archivo.

Formato del CSV:

```csv
monto,categoria,descripcion
40,Comida,Almuerzo
10,Transporte,Bus
70,Comida,Supermercado
```

## Pruebas realizadas

Las pruebas se ejecutan automáticamente con `assert` al iniciar el programa:

| Prueba | Tipo | Qué verifica | Resultado |
|--------|------|--------------|-----------|
| 1 | Normal | Total general = 170 y total de "COMIDA" = 150 (ignora mayúsculas) | OK |
| 2 | Límite | Monto mínimo 0.01 y categoría inexistente devuelve 0 | OK |
| 3 | Datos incorrectos | Monto 0, negativo, texto y categoría vacía lanzan `ValueError` | OK |
| 4 | Persistencia | Guardar, vaciar la lista y recargar da el mismo total | OK |
| 5 | Fila dañada | Una fila con monto "xyz" se omite y se carga solo la válida | OK |

Salida esperada con el CSV de ejemplo:

```
Prueba 1 (normal): OK
Prueba 2 (límite): OK
Prueba 3 (inválido) OK -> El monto debe ser mayor que 0.
Prueba 3 (inválido) OK -> El monto debe ser mayor que 0.
Prueba 3 (inválido) OK -> El monto debe ser un número.
Prueba 3 (inválido) OK -> La categoría no puede estar vacía.
Prueba 4 (persistencia CSV): OK
Fila 3 inválida, se omite (El monto debe ser un número.).
Prueba 5 (fila dañada): OK

Todas las pruebas pasaron.

Error: El monto debe ser mayor que 0.

Total gastos: 155.0
Total comida: 110.0
```

## Uso de inteligencia artificial

Se utilizó Claude como apoyo para comparar alternativas, revisar la validación y mejorar los comentarios. El código fue ejecutado y verificado personalmente. Ver el detalle en el PDF de entrega.

## Seguridad

El repositorio no contiene contraseñas, tokens ni datos personales sensibles.
