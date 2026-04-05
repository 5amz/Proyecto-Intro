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
from tkinter import messagebox
import random
import os
import csv
from PIL import Image, ImageTk

#Clase para crear los personajes jugables
class Personaje():
    def __init__(self, nombre, avatar, vida, ataque, defensa):
        self.nombre = nombre
        self.avatar = avatar
        self.vida_max = int(vida)
        self.vida = int(vida)
        self.ataque = int(ataque)
        self.defensa = int(defensa)

    def clonar(self):
        return Personaje(self.nombre, self.avatar, self.vida_max, self.ataque, self.defensa)
    
class Hollow():

    nombres = [
        "Grim",
        "Pale King",
        "Hollow Knight",
        "Radiance",
        "White Lady"
    ]

    avatars = [
        "grim.png",
        "pale_king.png",
        "hollow_knight",
        "radiance.png",
        "white_lady.png"
    ]

    def __init__(self, nombre, avatar, personajes):
        self.nombre = nombre
        self.avatar = avatar
        self.personajes = personajes

#Funcion para cargar los personajes desde el archivo de texto
def crear_personajes(ruta="personajes.txt"):
    personajes = []
    if not os.path.isabs(ruta):
        base = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base, ruta)

    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            personajes.append(Personaje(
                row["nombre"], row["avatar"],
                row["vida"], row["ataque"], row["defensa"]
            ))
    return personajes

def crear_hollow(nombre, avatar, todos_personajes):
    seleccion = random.sample(todos_personajes, 3)
    personajes = [p.clonar() for p in seleccion]
    return Hollow(nombre, avatar, personajes)

#Clase para crear la pantalla de carga
class Pantalla_de_carga(tk.Frame):
    def __init__(self, master, callback_iniciar):
        super().__init__(master, bg="blue")
        self.callback_iniciar = callback_iniciar

        #Division de la pantalla
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        frame_sup_izq = tk.Frame(self, relief="solid", bd=1, width=200, height=250)
        frame_sup_izq.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_sup_izq.grid_propagate(False)

        frame_inf_izq = tk.Frame(self, relief="solid", bd=1, width=200, height=250)
        frame_inf_izq.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_inf_izq.grid_propagate(False)

        frame_der = tk.Frame(self, relief="solid", bd=1, width=200, height=250)
        frame_der.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        frame_der.grid_propagate(False)

        #Titulo
        tk.Label(frame_sup_izq, text="Hollownest's Epic Adventure").pack(side="top")
        tk.Label(frame_sup_izq, text="Proyecto 1 - Intro 2026").pack(side="top")

        #Ingresar Nombre
        self.nombre_jugador = tk.StringVar()
        tk.Label(frame_sup_izq, text="Ingrese Nombre:").pack(side="left")
        tk.Entry(frame_sup_izq, textvariable=self.nombre_jugador, width=20).pack(side="left", padx= 2, pady=10, ipady=1)

        #About
        self.btn_about = tk.Button(frame_sup_izq, text="About", command=self.get_about, padx=5)
        self.btn_about.pack(side="right", padx=15)

        #Selección de avatar
        Avatar_Jugador = ["teacher", "watcher", "beast"]
        tk.Label(frame_inf_izq, text="Elija Avatar:").pack()
        self.avatar_elegido = tk.StringVar(value=Avatar_Jugador[0])
        for avatar in Avatar_Jugador:
            radbut = tk.Radiobutton(frame_inf_izq, text=avatar, variable=self.avatar_elegido, value=avatar, command=self.actualizar_avatar)
            radbut.pack(padx=5, pady=3)
        self.img_avatar = tk.Label(frame_inf_izq)
        self.img_avatar.pack(anchor="center", pady=20)
        self.img_avatar.pack_propagate(False)
        self.actualizar_avatar()

        #Selección de personajes
        self.todos_personajes = crear_personajes()
        self.personajes_seleccionados = []
        self.check_variables = []

        tk.Label(frame_der, text="Elija 3 Personajes:").pack(pady=(10,5))
        self.lbl_conteo = tk.Label(frame_der, text="Seleccionados: 0/3")
        self.lbl_conteo.pack()

        canvas = tk.Canvas(frame_der, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_der, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=5)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.imagenes_personajes = []
        for index, personaje in enumerate(self.todos_personajes):
            var = tk.BooleanVar()
            self.check_variables.append(var)

            fila = tk.Frame(inner_frame)
            fila.pack(fill="x", padx=5, pady=2)

            # Cargar imagen del personaje
            base = os.path.dirname(os.path.abspath(__file__))
            ruta = os.path.join(base, "img", personaje.avatar)
            img = Image.open(ruta)
            img = img.resize((40, 40))
            foto = ImageTk.PhotoImage(img)

            self.imagenes_personajes.append(foto)

            lbl_img = tk.Label(fila, image=foto)
            lbl_img.pack(side="left")

            cb = tk.Checkbutton(
                fila,
                text=f"{personaje.nombre}  HP:{personaje.vida_max} ATK:{personaje.ataque} DEF:{personaje.defensa}",
                variable=var,
                command=lambda idx=index: self.seleccion_personaje(idx),
                anchor="w"
            )
            cb.pack(side="left", padx=5)

        #Iniciar juego
        self.btn_iniciar = tk.Button(frame_sup_izq, text="Iniciar", command=self.iniciar_juego, padx=5)
        self.btn_iniciar.pack(side="bottom", anchor="center", pady=15)
        
    #Función para cerrar la pantalla del About
    def cerrar_about(self, win):
        win.destroy()
        self.btn_about.config(state="normal")

    #Función para abrir la pantalla del About
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
        tk.Button(win, text="Cerrar", command=lambda:self.cerrar_about(win), relief="solid", padx=12, pady=6).pack(pady=10)

    #Función para actualizar la elección del Avatar del jugador
    def actualizar_avatar(self):
        seleccion = self.avatar_elegido.get()

        base = os.path.dirname(os.path.abspath(__file__))

        imagenes_avatar = {
            "teacher":  os.path.join(base, "img", "teacher.png"),
            "watcher":  os.path.join(base, "img", "watcher.png"),
            "beast": os.path.join(base, "img", "beast.png"),
        }
        
        ruta = imagenes_avatar[seleccion]
        img = Image.open(ruta)
        img = img.resize((190, 190))          
        imagen_avatar = ImageTk.PhotoImage(img)

        self.img_avatar.config(image=imagen_avatar)
        self.img_avatar.image = imagen_avatar

    #Función para conseguir y actualizar la elección de los personajes del jugador
    def seleccion_personaje(self, idx):
        var = self.check_variables[idx]
        if var.get():
            if len(self.personajes_seleccionados) >= 3:
                var.set(False)
                messagebox.showwarning("Límite", "Solo podés elegir 3 personajes.")
                return
            self.personajes_seleccionados.append(idx)
        else:
            if idx in self.personajes_seleccionados:
                self.personajes_seleccionados.remove(idx)
        self.lbl_conteo.config(text=f"Seleccionados: {len(self.personajes_seleccionados)}/3")

    #Función para iniciar el juego y pasar a la pantalla del mapa
    def iniciar_juego(self):
        nombre = self.nombre_jugador.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingrese su nombre.")
            return
        if len(self.personajes_seleccionados) != 3:
            messagebox.showerror("Error", "Tiene que elegir exactamente 3 personajes.")
            return
        personajes = [self.todos_personajes[i].clonar() for i in self.personajes_seleccionados]
        avatar = self.avatar_elegido.get()
        self.callback_iniciar(nombre, avatar, personajes)

class Pantalla_de_mapa(tk.Frame):

    lugares = [
        ("Dirtmouth", 0),
        ("Palace Grounds", 1),
        ("City of Tears", 2),
        ("Black Egg Temple", 3),
        ("Queen's Garden", 4),
    ]

    def __init__(self, master, nombre, avatar, personajes, callback_batalla):
        super().__init__(master)
        self.nombre = nombre
        self.avatar = avatar
        self.personajes = personajes
        self.callback_batalla = callback_batalla
        self.hollows_derrotados = set()

        #Cargar la imagen del mapa
        self.canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0)
        self.canvas.pack()
        base = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base, "img", "mapa.png")
        img = Image.open(ruta)
        img = img.resize((800, 600))
        self.img_mapa = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_mapa)

        #Crear botones de batalla
        coordenadas = {
            "Dirtmouth": (290, 105),
            "Palace Grounds": (500, 555),
            "City of Tears": (480, 340),
            "Black Egg Temple": (345, 210),
            "Queen's Garden": (100, 320),
        }

        for nombre_lugar, idx in self.lugares:
            x, y = coordenadas[nombre_lugar]
            derrotado = idx in self.hollows_derrotados
            btn = tk.Button(
                self,
                text=f"{'✔' if derrotado else '⚔'} {nombre_lugar}",
                command=lambda i=idx, d=derrotado: self.ir_batalla(i, d),
                bg="#2c2c54" if not derrotado else "#4a4a4a",
                fg="white" if not derrotado else "#888",
                relief="flat",
                padx=6,
                pady=3,
                state="normal" if not derrotado else "disabled"
            )
            btn.place(x=x, y=y)

    def ir_batalla(self, idx, derrotado):
        if derrotado:
            return
        self.callback_batalla(idx)

class Pantalla_batalla(tk.Frame):
    def __init__(self, master, nombre_jugador, avatar_jugador, personajes_jugador, hollow, callback_fin):
        super().__init__(master)
        self.jugador_nombre = nombre_jugador
        self.avatar_jugador = avatar_jugador
        self.hollow = hollow
        self.callback_fin = callback_fin
        self.personajes_jugador = personajes_jugador
        self.activo_jugador = None
        self.activo_hollow = random.choice(hollow.personajes)
        self.puntaje_jugador = 0
        self.puntaje_hollow = 0
        self.imagenes = []

class Root(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Hollownest's Epic Adventure")
        self.geometry("800x600")
        self.resizable(False, False)

        self.nombre_jugador = ""
        self.avatar_jugador = ""
        self.personajes_jugador = []
        self.pantalla_actual = None
        self.todos_personajes = crear_personajes()
        self.hollows = []
        self.hollows_derrotados = set()
        self.iniciar()

    def cambiar_pantalla(self, nueva):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
        self.pantalla_actual = nueva
        nueva.pack(fill="both", expand=True)

    def iniciar(self):
        pantalla = Pantalla_de_carga(self, self.ir_mapa)
        self.cambiar_pantalla(pantalla)

    def ir_mapa(self, nombre, avatar, personajes):
        self.nombre_jugador = nombre
        self.avatar_jugador = avatar
        self.personajes_jugador = personajes
        self.hollows = [crear_hollow(Hollow.nombres[i], Hollow.avatars[i], self.todos_personajes) for i in range(5)]
        pantalla = Pantalla_de_mapa(self, nombre, avatar, personajes, self.ir_batalla)
        self.cambiar_pantalla(pantalla)

    def ir_batalla(self, idx_hollow):
        hollow = self.hollows[idx_hollow]
        pantalla = Pantalla_batalla(self, self.nombre_jugador, self.avatar_jugador, self.personajes_jugador, hollow, 
                                lambda victoria, idx=idx_hollow: self.fin_batalla(victoria, idx))
        self.cambiar_pantalla(pantalla)

    def fin_batalla(self, victoria, idx_hollow):
        if victoria:
            self.hollows_derrotados.add(idx_hollow)
            if len(self.hollows_derrotados) == 5:
                messagebox.showinfo("¡Ganaste!",
                                    f"¡Felicidades {self.nombre_jugador}!\n"
                                    "Derrotaste a todos los Hollows.")
                self.iniciar()
                return
        else:
            messagebox.showwarning("Perdiste", "Perdiste la batalla...")
        self.ir_mapa(self.nombre_jugador, self.avatar_jugador, self.personajes_jugador)

if __name__ == "__main__":
    root = Root()
    root.mainloop()