
import requests

def consultar_placa(placa: str) -> dict:
    
    url = f"https://api.factiliza.com/v1/placa/info/{placa}"
    
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOTE4OCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.DgSe6VHlcXgnLWHIwXjNb-0YDXOINRDlfCLRIjtymLE"
    }

    response = requests.get(url, headers=headers)

    return response.json()