import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

# Función para buscar palabras clave en Google
def buscar_palabras_clave(sku, marca):
    palabras_clave = []
    url = f"https://www.google.com/search?q={marca}+{sku}&num=12"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    fname = f"{marca}-{sku}.xml"
    fxml = open(fname, "w")
    for link in soup.find_all("a"):
        fxml.write(link.__str__())
    fxml.close()
    for link in soup.find_all("a"):
        href = link.get("href")
        if "/url?q=" in href:
            palabra_clave = href.split("/url?q=")[1].split("&")[0]
            if "search?q=" not in palabra_clave:
                palabras_clave.append(palabra_clave)
    return palabras_clave[:12] # Solo tomamos las primeras 12 palabras clave

# Función para descargar imágenes de Google
def descargar_imagenes(sku, marca):
    imagenes = []
    url = f"https://www.google.com/search?q={marca}+{sku}&tbm=isch&num=4"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    for raw_img in soup.find_all("img"):
        link = raw_img.get("src")
        if "https" in link and "gstatic" not in link:
            imagenes.append(link)
    return imagenes[:4] # Solo tomamos las primeras 4 imágenes

# Función para escribir el DataFrame en el archivo de Excel
def escribir_excel(df):
    with pd.ExcelWriter("masterseo.xlsx", engine="openpyxl") as writer:
        writer.book = openpyxl.load_workbook("masterseo.xlsx")
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
        reader = pd.read_excel(r"masterseo.xlsx")
        df.to_excel(writer, index=False, header=not bool(reader.size))
        writer.save()

# Ingresar el SKU y la marca manualmente
sku = input("Ingrese el SKU: ")
marca = input("Ingrese la marca: ")

# Obtener las palabras clave y las imágenes
palabras_clave = buscar_palabras_clave(sku, marca)
imagenes = descargar_imagenes(sku, marca)

# Crear el DataFrame con la información del SKU
data = {"SKU": [sku], "Marca": [marca], "Palabras clave": [palabras_clave], "Imágenes": [imagenes]}
df = pd.DataFrame(data)

# Escribir el DataFrame en el archivo de Excel
escribir_excel(df)

print("La información se ha guardado correctamente en el archivo 'masterseo.xlsx'.")

# Esta es la última línea del programa
