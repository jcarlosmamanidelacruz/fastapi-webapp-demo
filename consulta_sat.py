import sys, os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

load_dotenv()

# Configuración API KEY desde .env
api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY')

def resolver_captcha(sitekey, url):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(sitekey)

    result = solver.solve_and_return_solution()
    if result != 0:
        return result
    else:
        raise Exception(f"Error resolviendo el CAPTCHA: {solver.error_code}")

def consultar_sat(placa: str) -> dict:
    url = "https://www.sat.gob.pe/VirtualSAT/principal.aspx"

    options = Options()
    options.add_argument("--log-level=3")  # Solo errores fatales
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")  # Activa navegación sin interfaz gráfica
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get(url)
        
        # 1. Cambiar al frame que contiene el enlace
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "fraRightFrame"))
        )

        # 2. Esperar y hacer clic en el enlace que contiene 'papeletas.aspx'
        enlace = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'papeletas.aspx')]"))
        )

        enlace.click()
        
        # Seleccionar "Búsqueda por Placa"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tipoBusquedaPapeletas"))
        )
        Select(driver.find_element(By.ID, "tipoBusquedaPapeletas")).select_by_visible_text("Búsqueda por Placa")


        # Ingresar la placa
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_cplPrincipal_txtPlaca"))
        )
        driver.find_element(By.ID, "ctl00_cplPrincipal_txtPlaca").send_keys(placa)


        # Obtener el sitekey del CAPTCHA
        sitekey = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute('data-sitekey')

        # Resolver el CAPTCHA con Anti-Captcha
        try:
            token = resolver_captcha(sitekey, url)
        except Exception as e:
            raise Exception(f"Error resolviendo el CAPTCHA: {str(e)}")

        # Inyectar token en el campo oculto del CAPTCHA
        captcha_field = driver.find_element(By.ID, "g-recaptcha-response")
        driver.execute_script("arguments[0].style.display = 'block';", captcha_field)
        driver.execute_script(f"arguments[0].innerHTML = '{token}'", captcha_field)

        # Enviar formulario
        driver.find_element(By.ID, "ctl00_cplPrincipal_CaptchaContinue").click()

        # Capturar todas las filas (papeletas)
        
        try:
            # Esperar a que al menos una fila de resultado esté visible
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "grillaRows"))
            )
                        
            # Espera a que aparezca la tabla
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@id, 'grdEstadoCuenta')]"))
            )

            filas = driver.find_elements(By.XPATH, "//table[contains(@id, 'grdEstadoCuenta')]//tr[contains(@class, 'grilla')]")

            datos = []
            for fila in filas[1:]:  # saltamos encabezado
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) >= 15:
                    datos.append({
                        "placa": columnas[1].text.strip(),
                        "fecha": columnas[5].text.strip(),
                        "deuda": columnas[9].text.strip(),
                        "estado": columnas[10].text.strip(),
                        "licencia": columnas[12].text.strip(),
                        "documento": columnas[14].text.strip()
                    })
                    
            return {
                "status": 200,
                "message": "Exito",
                "data": {
                    "mensaje": f"Se encontraron {len(datos)} papeletas registradas.",
                    "resultado": datos
                }
            }
            
        except (TimeoutException, NoSuchElementException):
            return {
                "status": 400,
                "success": False,
                "message": f"No se encontraron papeletas registradas pendientes de pago para la placa {placa}.",
            }

    except Exception as e:
        return {
            "status": 400,
            "success": False,
            "message": str(e)
        }


    finally:
        driver.quit()
'''
# Para pruebas individuales
if __name__ == "__main__":
    #resultado = consultar_sat("V9W010")
    resultado = consultar_sat("Z6X275")
    #print(resultado)
    #https://comprar.lapositiva.com.pe/consulta_soat/
'''