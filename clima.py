from datetime import datetime, timedelta, timezone
import requests
from claves import OPENWEATHER_API_KEY


def consultar_pronostico(inicio):
    """Consulta el pronóstico más cercano al turno en General Deheza."""
    hora_argentina = timezone(timedelta(hours=-3))
    turno = inicio.replace(tzinfo=hora_argentina)
    ahora = datetime.now(hora_argentina)
    
    if turno <= ahora:
        return "Elegí un turno futuro."
    if turno > ahora + timedelta(days=5):
        return "Todavía no hay pronóstico para esa fecha."
    if not OPENWEATHER_API_KEY:
        return "Falta configurar OPENWEATHER_API_KEY en claves.py."
    
    parametros = {
        "lat": -32.76,
        "lon": -63.79,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "es",
    }
    
    try:
        respuesta = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params=parametros,
            timeout=5,
            )
        if respuesta.status_code == 401: #401 es el código de error que devuelve OpenWeather cuando la api key es inválida o está desactivada.
            return "OpenWeather rechazó la clave. Revisá que esté activa."
        
        respuesta.raise_for_status()
        intervalos = respuesta.json()["list"]
        if not intervalos or turno.timestamp() > intervalos[-1]["dt"]:
            return "Todavía no hay pronóstico para ese horario."
        
        # Elegimos el intervalo con menor diferencia respecto al inicio del turno.
        cercano = min(intervalos, key=lambda dato: abs(dato["dt"] - turno.timestamp()))
        hora = datetime.fromtimestamp(cercano["dt"], hora_argentina)
        temperatura = cercano["main"]["temp"]
        descripcion = cercano["weather"][0]["description"]
        
        return f"General Deheza · {hora:%d/%m %H:%M} · {temperatura:.0f} °C · {descripcion}"
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return "Pronóstico no disponible. Podés guardar la reserva igualmente."