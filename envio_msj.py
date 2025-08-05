
import sys, os,requests

def enviar_mensaje(numero_telefono: str, mensaje: str) -> dict:
    
    url = "https://apiwsp.factiliza.com/v1/message/sendtext/NTE5ODcyNTk2NjU="

    payload = {
        "number": numero_telefono,
        "text": mensaje
    }
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOTE4OCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.w1meBRiiGBG-9CSZ44JainWQ67Aeh6XlrmB-UefyzN8",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()