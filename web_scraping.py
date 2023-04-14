import pandas as pd
import requests
from bs4 import BeautifulSoup

# Leer archivo de SKU y marcas
df = pd.read_excel('archivo_excel.xlsx')

# Recorrer filas del archivo y generar palabras clave y textos destacados para cada SKU
for i, row in df.iterrows():
    sku = str(row['SKU'])
    marca = str(row['Marca'])
    palabras_claves = [sku, marca]

    # Obtenemos las palabras clave sugeridas de Google
    sugerencias = []
    for palabra in palabras_claves:
        url = "http://suggestqueries.google.com/complete/search?client=firefox&q=" + palabra
        respuesta = requests.get(url)
        bs = BeautifulSoup(respuesta.text, "html.parser")
        sugerencias.extend([s.text for s in bs.find_all("suggestion")])

    # Agregamos las sugerencias a las palabras claves
    palabras_claves.extend(sugerencias)

    # Eliminamos las palabras repetidas
    palabras_claves = list(set(palabras_claves))

    # Imprimimos las palabras clave encontradas
    print(f"\nPalabras clave encontradas para SKU {sku} y marca {marca}:")
    for palabra in palabras_claves:
        print(palabra)

    # Reemplazamos la palabra clave en el texto motivacional y de acción
    texto_motivacional = f"¡Consigue ahora tu {sku} {marca} y disfruta de todas sus funcionalidades!"
    texto_accion = f"Compra ya tu {sku} {marca} al mejor precio y descubre todas sus características"

    for palabra in palabras_claves:
        texto_motivacional = texto_motivacional.replace(palabra, f"<strong>{palabra}</strong>")
        texto_accion = texto_accion.replace(palabra, f"<strong>{palabra}</strong>")

    # Imprimimos los textos con las palabras clave destacadas
    print("\nTexto motivacional:")
    print(f"<h2>{texto_motivacional}</h2>")

    print("\nTexto de acción:")
    print(f"<h3>{texto_accion}</h3>")

    # Texto de cierre
    texto_cierre = f"No esperes más y adquiere tu {sku} {marca} ahora mismo para disfrutar de sus múltiples beneficios"

    # Imprimimos el texto de cierre
    print("\nTexto de cierre:")
    print(texto_cierre)

# Programa finalizado por ChatGPT
print("\nPrograma finalizado por ChatGPT")