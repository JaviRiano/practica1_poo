from ejercicio1 import Sensor
from ejercicio1 import SensorTemperatura
from ejercicio1 import SensorHumedad
from ejercicio1 import SensorPresion
class SensorManager:
    def __init__(self):
        self.sensores = []

    def agregar_sensor(self, sensor):
        if not isinstance(sensor, Sensor):
            raise TypeError("Solo se pueden agregar objetos que hereden de la clase Sensor.")
        self.sensores.append(sensor)

    def capturar_datos(self):
        for sensor in self.sensores:
            try:
                dato = sensor.leer_dato()
                sensor.validar_dato(dato)
                print(f"Dato válido: {dato}")
            except ValueError as ve:
                print(f"Error de validación: {ve}")
            except Exception as e:
                print(f"Error inesperado: {e}")

    def buscar_sensores_por_tipo(self, tipo):
        return [sensor for sensor in self.sensores if sensor.__class__.__name__.lower().startswith(tipo.lower())]



