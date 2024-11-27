import random
import json
from abc import ABC, abstractmethod

# Clase abstracta sensor
class Sensor(ABC):
    @abstractmethod
    def leer_dato(self):
        pass

    @abstractmethod
    def validar_dato(self, dato):
        pass

    def guardar_dato(self, dato, archivo_json):
        if not isinstance(dato, dict):
            raise TypeError("El dato debe ser un diccionario.")
        try:
            with open(archivo_json, 'a') as archivo:
                json.dump(dato, archivo)
                archivo.write('\n')
        except Exception as e:
            raise IOError(f"Error al guardar el dato en el archivo JSON: {e}")

# Sensor de temperatura la temperatura puesta en la validación es la mas baja y la mas alta en España y esta en grados centigrados
class SensorTemperatura(Sensor):
    def leer_dato(self):
        return {"tipo": "temperatura", "valor": random.randint(-40, 50)}

    def validar_dato(self, dato):
        if not (-32 <= dato["valor"] <= 47):
            raise ValueError("El valor del sensor de temperatura está fuera del rango permitido.")

# Sensor de presion este esta puesto en milibares ya que en atmosferas eran numeros extremadamente cercanos
class SensorPresion(Sensor):
    def leer_dato(self):
        return {"tipo": "presion", "valor": random.randint(980, 1060)}

    def validar_dato(self, dato):
        if not (991 <= dato["valor"] <= 1044):
            raise ValueError("El valor del sensor de presión está fuera del rango permitido.")

# Sensor de humedad la humedad fue sacada de manera porcentual y en el validar datos esta puesto el minimo y maximo comun
class SensorHumedad(Sensor):
    def leer_dato(self):
        return {"tipo": "humedad", "valor": random.randint(0, 100)}

    def validar_dato(self, dato):
        if not (30 <= dato["valor"] <= 60):
            raise ValueError("El valor del sensor de humedad está fuera del rango permitido.")

# Prueba
sensores = [SensorTemperatura(), SensorPresion(), SensorHumedad()]
for sensor in sensores:
    try:
        dato = sensor.leer_dato()
        sensor.validar_dato(dato)
        sensor.guardar_dato(dato, 'sensores.json')
        print(f"Dato guardado: {dato}")
    except Exception as e:
        print(f"Error con el sensor {sensor.__class__.__name__}: {e}")