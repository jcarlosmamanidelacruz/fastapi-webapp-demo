import json
from fastapi import FastAPI
from consulta_sat import consultar_sat
from consulta_soat import consultar_soat
from consulta_placa import consultar_placa
from consulta_vehicular import consultar_vehicular
from envio_msj import enviar_mensaje
from usuarios import UsuarioIn, registrar_usuario, activar_usuario, reenviar_codigo
app = FastAPI()

def consultar_papeletavigente(placa: str):
    resultado = consultar_sat(placa.upper().strip())
    return resultado

@app.get("/consulta/soat/{placa}")
def consultar_soatvigente(placa: str):
    resultado = consultar_soat(placa.upper().strip())
    return resultado

@app.get("/consulta/placa/{placa}")
def consultar_placavigente(placa: str):
    resultado = consultar_placa(placa.upper().strip())
    return resultado

@app.get("/consulta/vehicular/{placa}")
def consultar_vehicularvigente(placa: str):
    resultado = consultar_vehicular(placa.upper().strip())
    return resultado


@app.get("/consulta/enviar_msj/{numero_telefono}/{mensaje}")
def enviar_mensaje_telefono(numero_telefono: str, mensaje: str):
    resultado = enviar_mensaje(numero_telefono.strip(), mensaje)
    return resultado

#  CREAR USUARIO

@app.post("/crear_usuario")
def crear_usuario(usuario: UsuarioIn):
    
    # 1. Ejecuta el SP que retorna un JSON como string
    raw_result = registrar_usuario(usuario)  # <- string
    resultado = json.loads(raw_result)       # <- dict

    if resultado.get("status") == 200:
        codigo = resultado["data"]["co_valida"]
        mensaje = f"Tu código de verificación es: {codigo} por tu seguridad, no lo compartas."
        numero_con_prefijo = "51" + usuario.nu_telefo.strip()
        envio_resultado = enviar_mensaje(numero_con_prefijo, mensaje)

    return resultado

#  ACTIVAR USUARIO

@app.post("/activar_usuario")
def ejecutar_activar_usuario(usuario: UsuarioIn):
    
    # 1. Ejecuta el SP que retorna un JSON como string
    raw_result = activar_usuario(usuario)  # <- string
    resultado = json.loads(raw_result)       # <- dict

    return resultado

#  REENVIAR CODIGO DE VERIFICACION

@app.post("/reenviar_verificacion")
def ejecutar_reenviar_codigo(usuario: UsuarioIn):
    
    # 1. Ejecuta el SP que retorna un JSON como string
    raw_result = reenviar_codigo(usuario)  # <- string
    resultado = json.loads(raw_result)       # <- dict

    if resultado.get("status") == 200:
        codigo = resultado["data"]["co_valida"]
        mensaje = f"Tu código de verificación es: {codigo} por tu seguridad, no lo compartas."
        numero_con_prefijo = "51" + usuario.nu_telefo.strip()
        envio_resultado = enviar_mensaje(numero_con_prefijo, mensaje)
        
    return resultado
