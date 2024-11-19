class Simulacion:
    def __init__(self, esferas, rampas):
        self.esferas = esferas  
        self.rampas = rampas  
        self.tiempo = 0.0

    def correr(self, delta_t, duracion):
        
        pasos = int(duracion / delta_t)
        for _ in range(pasos):
            self.actualizar(delta_t)
            self.tiempo += delta_t

    def actualizar(self, delta_t):
       
        for esfera in self.esferas:
            for rampa in self.rampas:
                
                aceleracion = rampa.calcular_aceleracion(esfera.masa)
                esfera.actualizar_posicion(aceleracion, delta_t)

    def __repr__(self):
        return f"Simulacion(esferas={self.esferas}, rampas={self.rampas})"