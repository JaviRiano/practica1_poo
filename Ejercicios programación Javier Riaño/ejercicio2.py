from abc import ABC, abstractmethod
import json
import random
from ejercicio1 import SensorPresion
from ejercicio1 import SensorHumedad
from ejercicio1 import SensorTemperatura

class AlmacenamientoJSON:
    def guardar_datos(self, dato, archivo_json):
        if not isinstance(dato, dict):
            raise TypeError("El dato debe ser un diccionario.")
        try:
            with open(archivo_json, 'a') as archivo:
                json.dump(dato, archivo)
                archivo.write('\n')
        except Exception as e:
            raise IOError(f"Error al guardar el dato en el archivo JSON: {e}")

# Herencia del sensor humedad del ejercicio 1
class Humedad(SensorHumedad, AlmacenamientoJSON):
    pass

# Herencia del sensor presion del ejercicio 1
class Presion(SensorPresion, AlmacenamientoJSON):
    pass

# Herencia del sensor temperatura del ejercicio 1
class Temperatura(SensorTemperatura, AlmacenamientoJSON):
    pass

# Prueba
if __name__ == "__main__":
    sensores = [Humedad(), Presion(), Temperatura()]
    for sensor in sensores:
        try:
            dato = sensor.leer_dato()
            sensor.validar_dato(dato)
            sensor.guardar_datos(dato, 'sensores_monitoreo.json')
            print(f"Dato guardado: {dato}")
        except Exception as e:
            print(f"Error con el sensor {sensor.__class__.__name__}: {e}")

