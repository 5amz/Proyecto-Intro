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
        self.puntaje = 0

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
        hollows_derrotados = set()
        self.callback_iniciar(nombre, avatar, personajes, hollows_derrotados)

class Pantalla_de_mapa(tk.Frame):

    lugares = [
        ("Dirtmouth", 0),
        ("Palace Grounds", 1),
        ("City of Tears", 2),
        ("Black Egg Temple", 3),
        ("Queen's Garden", 4),
    ]

    def __init__(self, master, nombre, avatar, personajes, hollows_derrotados, callback_batalla):
        super().__init__(master)
        self.nombre = nombre
        self.avatar = avatar
        self.personajes = personajes
        self.callback_batalla = callback_batalla
        self.hollows_derrotados = hollows_derrotados

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
        self.hollow.puntaje = 0
        self.batalla_iniciada = False
        self.imagenes = []

        #Contruir la ventana
        zona = tk.Frame(self, bg="#0d0d1a")
        zona.pack(fill="x", padx=10, pady=5)
        zona.columnconfigure(0, weight=1)
        zona.columnconfigure(2, weight=1)

        self.panel_jugador = tk.Frame(zona, bg="#16213e", relief="solid", bd=1)
        self.panel_jugador.grid(row=0, column=0, sticky="nsew", padx=5)

        tk.Label(zona, text="VS", bg="#0d0d1a", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10)

        self.panel_hollow = tk.Frame(zona, bg="#2c1a1a", relief="solid", bd=1)
        self.panel_hollow.grid(row=0, column=2, sticky="nsew", padx=5)

        frame_log = tk.Frame(self, bg="#0d0d1a")
        frame_log.pack(fill="both", padx=10, pady=5, expand=True)
        tk.Label(frame_log, text="📜 Log de batalla", bg="#0d0d1a", fg="#888").pack(anchor="w")
        self.log_txt = tk.Text(frame_log, height=5, state="disabled", bg="#050510", fg="white", 
                           font=("Courier", 9), relief="flat")
        self.log_txt.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="#0d0d1a")
        btn_frame.pack(pady=6)

        self.btn_atacar = tk.Button(btn_frame, text="ATACAR", command=self.atacar, bg="#8b0000", fg="white",
                                    font=("Arial", 10, "bold"), padx=15, pady=6, relief="flat")
        self.btn_atacar.grid(row=0, column=0, padx=8)

        self.btn_cambiar = tk.Button(btn_frame, text="CAMBIAR", command=self.abrir_cambio, bg="#16213e", fg="white",
                                     font=("Arial", 10, "bold"), padx=15, pady=6, relief="flat")
        self.btn_cambiar.grid(row=0, column=1, padx=8)

        self.btn_mostrar_hollow = tk.Button(btn_frame, text="PERSONAJES", command=self.mostrar_hollow, bg="#216947", fg="white",
                                     font=("Arial", 10, "bold"), padx=15, pady=6, relief="flat")
        self.btn_mostrar_hollow.grid(row=0, column=2, padx=8)

        self.deshabilitar_botones()
        self.log(f"Batalla contra {self.hollow.nombre}!")
        self.log("Elija su personaje inicial:")
        self.elegir_personaje()

    def limpiar(self, frame):
        for wid in frame.winfo_children():
            wid.destroy()

    def cargar_imagen(self, nombre_archivo, size=(50, 50)):
        base = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base, "img", nombre_archivo)
        img = Image.open(ruta)
        img = img.resize(size)
        foto = ImageTk.PhotoImage(img)
        self.imagenes.append(foto)
        return foto
    
    def actualizar_pantalla(self):
        self.imagenes = []
        self.limpiar(self.panel_jugador)
        self.limpiar(self.panel_hollow)

        #Panel Jugador
        cab_j = tk.Frame(self.panel_jugador, bg="#16213e")
        cab_j.pack(fill="x", padx=5, pady=5)
        try:
            foto_j = self.cargar_imagen(f"{self.avatar_jugador}.png", (40, 40))
            tk.Label(cab_j, image=foto_j, bg="#16213e").pack(side="left", padx=4)
        except:
            pass
        info_j = tk.Frame(cab_j, bg="#16213e")
        info_j.pack(side="left")
        tk.Label(info_j, text=self.jugador_nombre, bg="#16213e", fg="#e8a020", font=("Arial", 11, "bold")).pack(side="left")
        tk.Label(info_j, text=f"Puntaje: {self.puntaje_jugador}", bg="#16213e", fg="white", font=("Arial", 9)).pack(side="right", padx=5)

        if self.activo_jugador:
            self.tarjeta_personaje(self.panel_jugador, self.activo_jugador, ko=(self.activo_jugador.vida <= 0))

        #Panel Hollow
        cab_h = tk.Frame(self.panel_hollow, bg="#2c1a1a")
        cab_h.pack(fill="x", padx=5, pady=5)
        try:
            foto_h = self.cargar_imagen(self.hollow.avatar, (40, 40))
            tk.Label(cab_h, image=foto_h, bg="#2c1a1a").pack(side="left", padx=4)
        except:
            pass
        info_h = tk.Frame(cab_h, bg="#2c1a1a")
        info_h.pack(side="left")
        tk.Label(info_h, text=self.hollow.nombre, bg="#2c1a1a", fg="#c0392b", font=("Arial", 11, "bold")).pack(side="left")
        tk.Label(info_h, text=f"Puntaje: {self.hollow.puntaje}", bg="#2c1a1a", fg="white", font=("Arial", 9)).pack(side="right", padx=5)

        if self.activo_hollow:
            self.tarjeta_personaje(self.panel_hollow, self.activo_hollow, ko=(self.activo_hollow.vida <= 0))

    def tarjeta_personaje(self, parent, personaje, ko=False):
        bg = "#3a3a3a" if ko else "#2a4a2a"
        fg = "#aaa" if ko else "white"

        card = tk.Frame(parent, bg=bg, padx=6, pady=4, relief="groove", bd=2)
        card.pack(fill="x", padx=5, pady=3)

        try:
            foto = self.cargar_imagen(personaje.avatar, (45, 45))
            tk.Label(card, image=foto, bg=bg).pack(side="left", padx=(0, 6))
        except:
            tk.Label(card, text="?", bg=bg, fg=fg, width=4).pack(side="left")

        info = tk.Frame(card, bg=bg)
        info.pack(side="left", fill="x", expand=True)

        estado = " [KO]" if ko else " ◄"
        tk.Label(info, text=f"{personaje.nombre}{estado}", bg=bg, fg=fg, font=("Arial", 9, "bold"), anchor="w").pack(fill="x")
        tk.Label(info, text=f"HP: {personaje.vida}/{personaje.vida_max}",
                bg=bg, fg=fg, font=("Courier", 8), anchor="w").pack(fill="x")
        tk.Label(info, text=f"ATK: {personaje.ataque}  DEF: {personaje.defensa}",
                bg=bg, fg=fg, font=("Courier", 8), anchor="w").pack(fill="x")
        
    def deshabilitar_botones(self):
        self.btn_atacar.config(state="disabled")
        self.btn_cambiar.config(state="disabled")
        self.btn_mostrar_hollow.config(state="disabled")

    def habilitar_botones(self):
        self.btn_atacar.config(state="normal")
        self.btn_cambiar.config(state="normal")
        self.btn_mostrar_hollow.config(state="normal")

    def batalla(self, turno="jugador"):
        vivos_hollow = [p for p in self.hollow.personajes]
        if not vivos_hollow :
            self.actualizar_pantalla()
            self.log(f"Felicidades! Derroto a {self.hollow.nombre}.")
            self.deshabilitar_botones()
            self.after(1200, lambda: self.callback_fin(True))
            return

        vivos_jugador = [p for p in self.personajes_jugador]
        if not vivos_jugador:
            self.actualizar_pantalla()
            self.log("Perdio todos tus personajes...")
            self.deshabilitar_botones()
            self.after(1200, lambda: self.callback_fin(False))
            return
        
        self.actualizar_pantalla()
        if turno == "jugador":
            self.turno_jugador()
        else:
            self.after(700, self.turno_hollow)

    def turno_jugador(self):
        self.habilitar_botones()

    def turno_hollow(self):
        self.deshabilitar_botones()
        vivos = [p for p in self.hollow.personajes]
        if not vivos:
            self.batalla("jugador")
            return
        
        accion = random.choice(["atacar", "cambiar"])
        if accion == "cambiar" and len(vivos) > 1:
            self.activo_hollow = random.choice([p for p in vivos if p is not self.activo_hollow])
            self.log(f"{self.hollow.nombre} cambia a {self.activo_hollow.nombre}")
        else:
            dano = max(1, self.activo_hollow.ataque - self.activo_jugador.defensa)
            self.activo_jugador.vida = max(0, self.activo_jugador.vida - dano)
            self.log(f"{self.activo_hollow.nombre} inflige {dano} pts de daño a {self.activo_jugador.nombre}")
            self.log(f"HP de {self.activo_jugador.nombre}: {self.activo_jugador.vida}")
            
            if self.activo_jugador.vida <= 0:
                self.log(f"{self.activo_jugador.nombre} fue derrotado.")
                self.hollow.puntaje += 1

                capturado = self.activo_jugador.clonar()
                capturado.vida = capturado.vida_max
                self.hollow.personajes.append(capturado)
                self.log(f"{capturado.nombre} se unió al equipo del Hollow.")

                self.actualizar_pantalla()

                self.personajes_jugador.remove(self.activo_jugador)
                self.activo_jugador = None

                vivos_j = [p for p in self.personajes_jugador]
                if not vivos_j:
                    self.batalla("hollow")
                    return
                self.actualizar_pantalla()
                self.elegir_personaje()

        self.batalla("jugador")

    def elegir_personaje(self, obligatorio = True):
        win = tk.Toplevel(self)
        win.title("Elija su personaje")
        win.resizable(False, False)
        win.grab_set() #Bloquea la interacción con otras ventanas

        mensaje = "¿A quién quiere enviar a la batalla?" if obligatorio else "¿A quién envia a la batalla?"
        tk.Label(win, text=mensaje, font=("Arial", 11), pady=10).pack()

        vivos = [p for p in self.personajes_jugador if p is not self.activo_jugador]

        for p in vivos:
            fila = tk.Frame(win, padx=10, pady=5)
            fila.pack(fill="x", padx=10)

            try:
                foto = self.cargar_imagen(p.avatar)
                tk.Label(fila, image=foto).pack(side="left", padx=(0, 8))
            except:
                tk.Label(fila, text="?", width=4).pack(side="left")

            info = tk.Frame(fila)
            info.pack(side="left", fill="x", expand=True)

            tk.Label(info, text=p.nombre, font=("Arial", 10, "bold"), anchor="w").pack(fill="x")
            tk.Label(info, text=f"HP: {p.vida}/{p.vida_max}  ATK: {p.ataque}  DEF: {p.defensa}",
                    font=("Courier", 9), anchor="w").pack(fill="x")

            tk.Button(info, text="Enviar", command=lambda elegido=p: self.confirmar_cambio(elegido, win),
                    bg="#16213e", fg="white", relief="flat", padx=8, pady=3).pack(anchor="w", pady=(3, 0))
            
        if not obligatorio:
            tk.Button(win, text="Cancelar", command=win.destroy, bg="#3a3a3a", fg="white",
                    relief="flat", padx=10, pady=6).pack(pady=(0, 10))
            
    def atacar(self):
        dano = max(1, self.activo_jugador.ataque - self.activo_hollow.defensa)
        self.activo_hollow.vida = max(0, self.activo_hollow.vida - dano)
        self.log(f"{self.activo_jugador.nombre} inflige {dano} pts de daño a {self.activo_hollow.nombre}")
        self.log(f"HP de {self.activo_hollow.nombre}: {self.activo_hollow.vida}")

        if self.activo_hollow.vida <= 0:
            self.log(f"{self.activo_hollow.nombre} fue derrotado.")
            self.puntaje_jugador += 1

            capturado = self.activo_hollow.clonar()
            capturado.vida = capturado.vida_max
            self.personajes_jugador.append(capturado)
            self.log(f"{capturado.nombre} se unió al equipo de {self.jugador_nombre}.")

            self.hollow.personajes.remove(self.activo_hollow)
            self.activo_hollow = None

            vivos_hollow = [p for p in self.hollow.personajes]
            if vivos_hollow:
                self.activo_hollow = random.choice(vivos_hollow)

        self.batalla("hollow")

    def abrir_cambio(self):
        vivos = [p for p in self.personajes_jugador if p is not self.activo_jugador]
        if not vivos:
            messagebox.showinfo("Sin opciones", "No tiene otros personajes disponibles.")
            return
        self.elegir_personaje(obligatorio=False)

    def confirmar_cambio(self, personaje, win):
        win.destroy()
        self.activo_jugador = personaje
        self.log(f"{self.jugador_nombre} envía a {personaje.nombre}")
        if not self.batalla_iniciada:
            self.batalla_iniciada = True
            self.batalla("jugador")
        else:
            self.batalla("hollow")

    def mostrar_hollow(self):
        win = tk.Toplevel(self)
        win.title(f"Personajes de {self.hollow.nombre}")
        win.resizable(False, False)
        win.grab_set()
        vivos = [p for p in self.hollow.personajes]

        for p in vivos:
            fila = tk.Frame(win, padx=10, pady=5)
            fila.pack(fill="x", padx=10)

            try:
                foto = self.cargar_imagen(p.avatar)
                tk.Label(fila, image=foto).pack(side="left", padx=(0, 8))
            except:
                tk.Label(fila, text="?", width=4).pack(side="left")

            info = tk.Frame(fila)
            info.pack(side="left", fill="x", expand=True)

            tk.Label(info, text=p.nombre, font=("Arial", 10, "bold"), anchor="w").pack(fill="x")
            tk.Label(info, text=f"HP: {p.vida}/{p.vida_max}  ATK: {p.ataque}  DEF: {p.defensa}",
                    font=("Courier", 9), anchor="w").pack(fill="x")
            
        tk.Button(win, text="Cancelar", command=win.destroy, bg="#3a3a3a", fg="white", 
                relief="flat", padx=10, pady=6).pack(pady=(0, 10))

    def log(self, mensaje):
        self.log_txt.config(state="normal")
        self.log_txt.insert("end", mensaje + "\n")
        self.log_txt.see("end")
        self.log_txt.config(state="disabled")

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
        self.hollows = [crear_hollow(Hollow.nombres[i], Hollow.avatars[i], self.todos_personajes) for i in range(5)]
        pantalla = Pantalla_de_carga(self, self.ir_mapa)
        self.cambiar_pantalla(pantalla)

    def ir_mapa(self, nombre, avatar, personajes, hollows_derrotados):
        self.nombre_jugador = nombre
        self.avatar_jugador = avatar
        self.personajes_jugador = personajes
        self.hollows_derrotados = hollows_derrotados
        pantalla = Pantalla_de_mapa(self, nombre, avatar, personajes, hollows_derrotados, self.ir_batalla)
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
            else:
                self.ir_mapa(self.nombre_jugador, self.avatar_jugador, self.personajes_jugador, self.hollows_derrotados)
        else:
            messagebox.showwarning("Perdiste", "Perdiste la batalla...")
            self.iniciar()


if __name__ == "__main__":
    root = Root()
    root.mainloop()