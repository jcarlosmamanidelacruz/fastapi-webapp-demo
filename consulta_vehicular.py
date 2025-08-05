import sys, os, base64, time, traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.imagecaptcha import imagecaptcha
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# Configuración API KEY desde .env
api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY')

def resolver_captcha_imagen(driver):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    # Captura el src del captcha
    captcha_element = driver.find_element(By.ID, "image")
    captcha_base64 = captcha_element.get_attribute("src")

    # Remueve el prefijo base64 y guarda la imagen
    base64_data = captcha_base64.split(",")[1]
    with open("captcha.png", "wb") as f:
        f.write(base64.b64decode(base64_data))

    # Envíalo a AntiCaptcha
    captcha_text = solver.solve_and_return_solution("captcha.png")
    if captcha_text != 0:
        print(f"[INFO] CAPTCHA resuelto: {captcha_text}")
        return captcha_text
    else:
        raise Exception(f"Error resolviendo CAPTCHA: {solver.error_code}")

def consultar_vehicular(placa: str) -> dict:
    url = "https://consultavehicular.sunarp.gob.pe/consulta-vehicular/inicio"

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nroPlaca"))
        )
        driver.find_element(By.ID, "nroPlaca").send_keys(placa)

        # Resolver captcha
        captcha_resuelto = resolver_captcha_imagen(driver)
        driver.find_element(By.ID, "codigoCaptcha").send_keys(captcha_resuelto)

        # Click en el botón "Realizar Búsqueda"
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[span[contains(text(), "Realizar Busqueda")]]'))
        ).click()

        # Esperar a que se cargue el resultado
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "container-data-vehiculo"))
        )

        resultado_html = driver.find_element(By.CLASS_NAME, "container-data-vehiculo").get_attribute("outerHTML")

        # Parsear el HTML con BeautifulSoup y extraer el src del <img>
        soup = BeautifulSoup(resultado_html, "html.parser")
        img_tag = soup.find("img")
        img_src = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

        return {
            "status": 200,
            "message": "Exito",
            "data": {
                "imagen_src": img_src
            }
        }
    except Exception as e:
        return {
            "status": 400,
            "success": False,
            "message": str(e)
        }

    finally:
        driver.quit()
