from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from urllib.parse import urlparse


def configurar_driver():
    """
    Configura y retorna un WebDriver de Chrome.
    """
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Descomenta esta línea si deseas que no se abra la interfaz gráfica
    # options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def extraer_urls_filtradas(driver, url, filtro):
    """
    Extrae las URLs que contengan el filtro especificado.
    """
    try:
        driver.get(url)
        enlaces = driver.find_elements(By.CSS_SELECTOR, "a[href]")
        urls = [
            enlace.get_attribute("href") for enlace in enlaces
            if enlace.get_attribute("href") and filtro in enlace.get_attribute("href")
        ]
        return urls
    except Exception as e:
        print(f"Error al extraer URLs de {url}: {e}")
        return []


def guardar_urls_en_archivo(urls, archivo_txt):
    """
    Guarda la lista de URLs en un archivo.
    """
    with open(archivo_txt, mode='w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')


def ejecutar_extraccion_con_filtro():
    """
    Solicita al usuario una URL, extrae los enlaces que contengan un filtro y guarda los resultados en un archivo.
    """
    # url_base = input("Ingrese la URL de la página para extraer los enlaces: ").strip()
    # filtro = input("Ingrese el texto para filtrar las URLs (por ejemplo, 'peru', 'portugal'): ").strip()

    url_base = "https://worldpostalcode.com/argentina/".strip()
    filtro = "argentina".strip()

    carpeta_destino = "resultados_urls_filtradas"
    os.makedirs(carpeta_destino, exist_ok=True)

    driver = configurar_driver()
    try:
        print(f"Procesando la página: {url_base} con filtro: '{filtro}'")
        urls = extraer_urls_filtradas(driver, url_base, filtro)

        # Guardar resultados
        nombre_url = urlparse(url_base).netloc.replace(".", "_")
        archivo_txt = os.path.join(carpeta_destino, f"{nombre_url}_urls_filtradas.txt")
        guardar_urls_en_archivo(urls, archivo_txt)

        print(f"Enlaces extraídos y guardados en: {archivo_txt}")
    except Exception as e:
        print(f"Error durante el proceso: {e}")
    finally:
        driver.quit()
        print("Navegador cerrado.")


if __name__ == "__main__":
    ejecutar_extraccion_con_filtro()
