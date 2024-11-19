import customtkinter
from prueba import simulator
import json
import os

def button_callback():
    sim=simulator("Ball\\esfera_prueba.xml")
    return sim.run() 

def button_carga():

    return 

    

app = customtkinter.CTk()
app.title("Simulador pelotas")
app.geometry("400x150")

button = customtkinter.CTkButton(app, text="Cargar configuración", command=button_carga)
button.grid(row=0, column=0, padx=20, pady=20)
button._hover_color='red'

button = customtkinter.CTkButton(app, text="Iniciar", command=button_callback)
button.grid(row=0, column=1, padx=20, pady=20)
button._hover_color='red'
app.mainloop()

