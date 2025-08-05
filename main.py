import json
from fastapi import FastAPI
from consulta_soat import consultar_soat
from envio_msj import enviar_mensaje
from usuarios import UsuarioIn, registrar_usuario, activar_usuario, reenviar_codigo
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/consulta/soat/{placa}")
def consultar_soatvigente(placa: str):
    resultado = consultar_soat(placa.upper().strip())
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
