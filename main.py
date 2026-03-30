"""
Instituto Tecnológico de Costa Rica
Escuela de Ingeniería en Computadores
Introducción a la programación
2026
Python 3.13
Estudiante: Samuel Ugalde Abrahams - 2026006212
Proyecto 1 Disney's Epic Adventure
Descripción: Juego con una interfaz gráfica simple que simula dinámicas de un juego de batalla por turnos.
"""

import tkinter as tk
import random
import os

class Pantalla_de_carga(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="blue")

        #Titulo
        tk.Label(self, text="Disney's Epic Adventure").pack(side="top")

        #Ingresar Nombre
        self.nombre_jugador = ""
        tk.Label(self, text="Ingrese Nombre:").pack(side="left")
        tk.Entry(self, textvariable=self.nombre_jugador, width=30).pack(side="left", padx= 2, pady=10, ipady=1)

        #About
        self.btn_about = tk.Button(self, text="About", command=self.get_about)
        self.btn_about.pack(side="top")

        #Avatar
        Avatar_Jugador = []
        self.avatar_elegido = ""
        self.avatar_1 = tk.Radiobutton(self, text="Avatar 1", )
        

    def cerrar_about(self, win):
        win.destroy()
        self.btn_about.config(state="normal")

    def get_about(self):
        self.btn_about.config(state="disabled")
        win = tk.Toplevel(self)
        win.title("About")
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_about(win))
        info = (
            "Disney's Epic Adventure\n"
            "Proyecto 1 - Introducción a la Programación\n"
            "Tecnológico de Costa Rica\n\n"
            "Profesores:\n"
            "  Santiago Ramirez\n"
            "  Ellioth Ramirez\n\n"
            "I Semestre 2026\n\n"
            "Temática: como Guardián de las Historias\n"
            "debes derrotar a los 5 Huecos y liberar\n"
            "a los personajes capturados."
        )
        tk.Label(win, text=info, justify="center", padx=30, pady=20).pack()
        tk.Button(win, text="Cerrar", command=lambda:self.cerrar_about(win), relief="flat", padx=12, pady=6).pack(pady=10)

    def actualizar_avatar(self):
        seleccion = self.avatar_var.get()
        
        imagenes = {
            "guerrero":  "img/guerrero.png",
            "guardian":  "img/guardian.png",
            "hechicero": "img/hechicero.png",
        }
        
        ruta = imagenes[seleccion]
        imagen = tk.PhotoImage(file=ruta)
        
        self.lbl_avatar.config(image=imagen)
        self.lbl_avatar.image = imagen

class Root(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Disney's Epic Adventure")
        self.geometry("800x600")
        self.resizable(False, False)
        self.pantalla_actual = None
        self.iniciar()

    def cambiar_pantalla(self, nueva):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
        self.pantalla_actual = nueva
        nueva.pack(fill="both", expand=True)

    def iniciar(self):
        pantalla = Pantalla_de_carga(self)
        self.cambiar_pantalla(pantalla)

if __name__ == "__main__":
    root = Root()
    root.mainloop()