import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("Simulador pelotas")
app.geometry("400x150")

button = customtkinter.CTkButton(app, text="Cargar", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

button = customtkinter.CTkButton(app, text="Iniciar", command=button_callback)
button.grid(row=0, column=1, padx=20, pady=20)
app.mainloop()