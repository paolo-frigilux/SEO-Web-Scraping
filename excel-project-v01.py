from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Counter
import pandas as pd
import csv
import time

# Leer los datos de la hoja de Excel
data = pd.read_excel("./archivo_excel.xlsx")

# Crear un archivo CSV para guardar los resultados
with open("skuseo.csv", "w") as f:
    writer = csv.writer(f)
    # Escribir la fila de encabezado
    writer.writerow(["SKU", "Marca", "Categoría", "Palabras clave"])

    # Procesar cada fila de datos
    for index, row in data.iterrows():
        # Obtener los datos de la fila
        sku = row["SKU"]
        marca = row["Marca"]
        categoria = row["Categoría"] if ("Categoría" in row.index) else ""

        # Realizar la búsqueda en Google
        query = f"{sku}+{marca}+{categoria}+SEO"
        browser = webdriver.Firefox()
        browser.get(f"https://www.google.com/search?q={query}")
        html = browser.page_source
        sel = Selector(text=html)
        results = sel.css('.r > a::attr(href)').extract()[:10]

        # Extraer las palabras clave SEO de los resultados de búsqueda
        keywords = []
        for url in results:
            # Obtener el contenido de la página web
            browser.get(url)
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Encontrar el elemento meta que contiene las palabras clave SEO
            keywords_element = soup.find("meta", attrs={"name": "keywords"})

            # Si el elemento meta no existe, buscar palabras clave en el contenido del cuerpo de la página
            if not keywords_element:
                body = soup.find("body")
                keywords_text = body.get_text().lower()
            else:
                keywords_text = keywords_element["content"].lower()

            # Tokenizar las palabras clave y eliminar las palabras vacías y las palabras comunes
            keywords_list = keywords_text.split()
            stopwords = set(nltk.corpus.stopwords.words("spanish"))
            common_words = set(["de", "la", "el", "en", "y", "a", "que"])
            filtered_keywords_list = [word for word in keywords_list if word not in stopwords and word not in common_words]

            # Agregar las palabras clave a la lista general de palabras clave
            keywords.extend(filtered_keywords_list)

        # Contar la frecuencia de cada palabra clave y seleccionar las 10 más frecuentes
        keyword_counts = Counter(keywords)
        top_keywords = keyword_counts.most_common(10)

        # Escribir los resultados en el archivo CSV
        writer.writerow([sku, marca, categoria, top_keywords])

    # Cerrar el navegador web
    browser.quit()