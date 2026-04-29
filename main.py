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
        #Atributos de los personajes
        self.nombre = nombre
        self.avatar = avatar
        self.vida_max = int(vida)
        self.vida = int(vida)
        self.ataque = int(ataque)
        self.defensa = int(defensa)

    def clonar(self): #Funcion para clonar al personaje
        return Personaje(self.nombre, self.avatar, self.vida_max, self.ataque, self.defensa)
    
#Clase para crear los hollows    
class Hollow():

    nombres = [
        "Grim",
        "Pale King",
        "Hollow Knight",
        "Radiance",
        "White Lady"
    ]

    avatars = [
        "grimm.png",
        "pale_king.png",
        "hollow_knight.png",
        "radiance.png",
        "white_lady.png"
    ]

    def __init__(self, nombre, avatar, personajes):
        #Atributos de los hollows
        self.nombre = nombre
        self.avatar = avatar
        self.personajes = personajes
        self.puntaje = 0

#Funcion para cargar los personajes desde el archivo de texto
def crear_personajes(ruta="personajes.txt"):
    # Convierte una ruta relativa a absoluta
    if not os.path.isabs(ruta):
        base = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base, ruta)

    #Lee el archivo csv y crea los personajes
    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)

    #Funcion para leer cada fila del archivo de texto
    def leer_filas(filas, indice=0, personajes=None):
        if personajes is None:
            personajes = []
        if indice >= len(filas): #Caso base donde no quedan filas
            return personajes
        col = filas[indice]
        personajes.append(Personaje(col["nombre"], col["avatar"], col["vida"], col["ataque"], col["defensa"])) #Agrega el personaje
        return leer_filas(filas, indice + 1, personajes) #Lee la siguiente fila

    return leer_filas(filas, 0, [])

#Crea el hollow con 3 personajes aleatorios
def crear_hollow(nombre, avatar, todos_personajes):
    seleccion = random.sample(todos_personajes, 3)

    #Función para clonar los personajes
    def clonar_personajes(lista, indice=0, resultado=None): 
        if resultado is None:
            resultado = []
        if indice >= len(lista): #Caso base donde ya se clonaron los 3 personajes
            return resultado
        resultado.append(lista[indice].clonar())
        return clonar_personajes(lista, indice + 1, resultado)

    personajes = clonar_personajes(seleccion, 0, [])
    return Hollow(nombre, avatar, personajes)

#Clase para crear la pantalla de carga
class Pantalla_de_carga(tk.Frame):
    def __init__(self, master, callback_iniciar):
        super().__init__(master, bg="blue") #Llama al init de tk.Frame como padre de pantalla de carga para que este se tome como un Frame
        #Atributos de la pantalla de carga
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
        for index, personaje in enumerate(self.todos_personajes): #enumerate() añade un contador automatico a un objeto iterable y devuelve el objeto con los pares índice-valor
            var = tk.BooleanVar()
            self.check_variables.append(var) #Revisar si el personaje esta elejido

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
                variable=var, command=lambda idx=index: self.seleccion_personaje(idx),
                anchor="w") # Bottones de seleecion 
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
            "Hollownest's Epic Adventure\n"
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

    #Función para actualizar la elección del Avatar del jugador y enseñar su imagen
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
                messagebox.showwarning("Límite", "Solo podés elegir 3 personajes.") #Abre una pestaña con un mensaje de error
                return
            self.personajes_seleccionados.append(idx)
        else:
            if idx in self.personajes_seleccionados:
                self.personajes_seleccionados.remove(idx)
        self.lbl_conteo.config(text=f"Seleccionados: {len(self.personajes_seleccionados)}/3")

    #Función para clonar los personajes seleccionados del jugador
    def clonar_seleccionados(self, lista, indice=0, resultado=None):
        if resultado is None:
            resultado = []
        if indice >= len(lista):
            return resultado
        personaje = self.todos_personajes[lista[indice]].clonar()
        resultado.append(personaje)
        
        return self.clonar_seleccionados(lista, indice + 1, resultado)

    #Función para iniciar el juego y pasar a la pantalla del mapa
    def iniciar_juego(self):
        nombre = self.nombre_jugador.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingrese su nombre.") #Si no se ha ingresado el nombre abre un mensaje de error
            return
        if len(self.personajes_seleccionados) != 3:
            messagebox.showerror("Error", "Tiene que elegir exactamente 3 personajes.") #Si no se han seleccionado exactamente 3 personajes abre un mensaje de error
            return
        personajes = self.clonar_seleccionados(self.personajes_seleccionados)
        avatar = self.avatar_elegido.get()
        hollows_derrotados = set()
        self.callback_iniciar(nombre, avatar, personajes, hollows_derrotados) #Vuelve al Root para continuar

#Clase para crear la pantalla del mapa
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
        #Atributos de la pantalla del mapa
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

        #Crear botones de cada batalla
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
                self, text=f"{'✔' if derrotado else '⚔'} {nombre_lugar}",
                command=lambda i=idx, d=derrotado: self.ir_batalla(i, d),
                bg="#2c2c54" if not derrotado else "#4a4a4a",
                fg="white" if not derrotado else "#888", relief="flat",
                padx=6, pady=3, state="normal" if not derrotado else "disabled" ) #Crea los botones y los desabilita si el hollow ya fue derrotado
            btn.place(x=x, y=y) #Pone los botones en las coordenadas del mapa

    def ir_batalla(self, idx, derrotado):
        if derrotado:
            return
        self.callback_batalla(idx) #Vuelve al Root para continuar a la batalla

#Clase para crear la pantalla de batalla
class Pantalla_batalla(tk.Frame):
    def __init__(self, master, nombre_jugador, avatar_jugador, personajes_jugador, hollow, puntaje, callback_fin):
        super().__init__(master)
        #Atributos de la pantalla de batalla
        self.jugador_nombre = nombre_jugador
        self.avatar_jugador = avatar_jugador
        self.hollow = hollow
        self.callback_fin = callback_fin
        self.personajes_jugador = personajes_jugador
        self.activo_jugador = None
        self.activo_hollow = random.choice(hollow.personajes)
        self.puntaje_jugador = puntaje
        self.hollow.puntaje = 0
        self.batalla_iniciada = False
        self.imagenes = []

        #Contruir la ventana
        zona = tk.Frame(self, bg="#0d0d1a")
        zona.pack(fill="x", padx=10, pady=5)
        zona.columnconfigure(0, weight=1)
        zona.columnconfigure(2, weight=1)

        #Panel Jugador
        self.panel_jugador = tk.Frame(zona, bg="#16213e", relief="solid", bd=1)
        self.panel_jugador.grid(row=0, column=0, sticky="nsew", padx=5)

        tk.Label(zona, text="VS", bg="#0d0d1a", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10)

        #Panel Hollow
        self.panel_hollow = tk.Frame(zona, bg="#2c1a1a", relief="solid", bd=1)
        self.panel_hollow.grid(row=0, column=2, sticky="nsew", padx=5)

        #Log de batalla
        frame_log = tk.Frame(self, bg="#0d0d1a")
        frame_log.pack(fill="both", padx=10, pady=5, expand=True)
        tk.Label(frame_log, text="📜 Log de batalla", bg="#0d0d1a", fg="#888").pack(anchor="w")
        self.log_txt = tk.Text(frame_log, height=5, state="disabled", bg="#050510", fg="white", 
                           font=("Courier", 9), relief="flat")
        self.log_txt.pack(fill="both", expand=True)

        #Botones de acción
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

        #Empezar batalla
        self.deshabilitar_botones()
        self.log(f"Batalla contra {self.hollow.nombre}!")
        self.log("Elija su personaje inicial:")
        self.elegir_personaje()

    #Limpiar por completo un frame
    def limpiar(self, frame):
        for wid in frame.winfo_children():
            wid.destroy()

    #Funcion para cargar las imagenes
    def cargar_imagen(self, nombre_archivo, size=(50, 50)):
        base = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base, "img", nombre_archivo)
        img = Image.open(ruta)
        img = img.resize(size)
        foto = ImageTk.PhotoImage(img)
        self.imagenes.append(foto) #Evitar el garbage collector
        return foto
    
    def actualizar_pantalla(self):
        self.imagenes = [] #Limpiar la lista de imagenes para evitar que se acumulen
        #Limpar los paneles de jugador y hollow para actualizar la informacion
        self.limpiar(self.panel_jugador)
        self.limpiar(self.panel_hollow)

        #Actualizar Panel Jugador
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

        #Actualizar Panel Hollow
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

    #Funcion para crear una tarjeta con la informacion del personaje del jugador o hollow
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
        
    #Funcion para desactivar los botones de acción
    def deshabilitar_botones(self):
        self.btn_atacar.config(state="disabled")
        self.btn_cambiar.config(state="disabled")
        self.btn_mostrar_hollow.config(state="disabled")

    #Funcion para activar los botones de acción
    def habilitar_botones(self):
        self.btn_atacar.config(state="normal")
        self.btn_cambiar.config(state="normal")
        self.btn_mostrar_hollow.config(state="normal")

    #Funcion para el ciclo de batalla
    def batalla(self, turno="jugador"):
        #Si el hollow no tiene personajes, termina la batalla con victoria del jugador
        if not self.hollow.personajes:
            self.actualizar_pantalla()
            self.log(f"Felicidades! Derroto a {self.hollow.nombre}.")
            self.deshabilitar_botones()

            #Función para curar los personajes del jugador
            def curar_personajes(lista, indice=0):
                if indice >= len(lista): #Caso base enel que ya recorre todos los personajes
                    return
                lista[indice].vida = lista[indice].vida_max
                # Caso recursivo: siguiente personaje
                curar_personajes(lista, indice + 1)

            curar_personajes(self.personajes_jugador)
            self.log(f"Tus personajes se han curado.")
            self.after(2500, lambda: self.callback_fin(True, self.puntaje_jugador))
            return

        #Si el jugador no tiene personajes, termina la batalla con victoria del hollow
        if not self.personajes_jugador:
            self.actualizar_pantalla()
            self.log("Perdio todos sus personajes...")
            self.deshabilitar_botones()
            self.after(2000, lambda: self.callback_fin(False, self.puntaje_jugador))
            return
        
        self.actualizar_pantalla()

        #Si ambos jugadores tienen personajes, continua la batalla dependiendo de de quien sea el turno
        if turno == "jugador":
            self.turno_jugador() #Ejecuta turno jugador
        else:
            self.after(700, self.turno_hollow) #Ejecuta turno hollow

    #Funcion cuando sea el turno del jugador
    def turno_jugador(self):
        self.habilitar_botones()

    #Funcion cuando sea el turno del hollow
    def turno_hollow(self):
        self.deshabilitar_botones()
        vivos = self.lista_vivos(self.hollow.personajes)
        if not vivos:
            self.batalla("jugador")
            return
        
        accion = random.choice(["atacar", "cambiar"])
        if accion == "cambiar" and len(vivos) > 1: #Puede cambiar si tiene más de un personaje vivo
            self.activo_hollow = random.choice(self.filtrar_personajes(self.hollow.personajes, self.activo_hollow))
            self.log(f"{self.hollow.nombre} cambia a {self.activo_hollow.nombre}")
        else:
            #Le hace daño al personaje activo del jugador
            dano = max(1, self.activo_hollow.ataque - self.activo_jugador.defensa)
            self.activo_jugador.vida = max(0, self.activo_jugador.vida - dano)
            self.log(f"{self.activo_hollow.nombre} inflige {dano} pts de daño a {self.activo_jugador.nombre}")
            self.log(f"HP de {self.activo_jugador.nombre}: {self.activo_jugador.vida}")
            
            if self.activo_jugador.vida <= 0: #Si el personaje del jugador se queda sin vida, pasa a ser un personaje del hollow
                self.log(f"{self.activo_jugador.nombre} fue derrotado.")
                self.hollow.puntaje += 1
                
                capturado = self.activo_jugador.clonar()
                capturado.vida = capturado.vida_max
                if not self.revisar_nombre(self.hollow.personajes, capturado.nombre): #Revisa si el personaje esta en el equipo del hollow
                    self.hollow.personajes.append(capturado)
                    self.log(f"{capturado.nombre} se unió al equipo del Hollow.")
                else:
                    self.log(f"{capturado.nombre} ya está en el equipo del Hollow.")

                self.actualizar_pantalla()

                self.personajes_jugador.remove(self.activo_jugador) #Elimina el personaje derrotado del jugador
                self.activo_jugador = None

                vivos_j = self.lista_vivos(self.personajes_jugador)
                if not vivos_j: #Si el jugador no tiene personajes vivos, llama a batalla para terminar
                    self.batalla("hollow")
                    return
                self.actualizar_pantalla()
                self.elegir_personaje()

        self.batalla("jugador") #Pasa el turno al jugador

    #Funcion para elegir el personaje activo del jugador
    def elegir_personaje(self, obligatorio = True):
        win = tk.Toplevel(self)
        win.title("Elija su personaje")
        win.resizable(False, False)
        win.grab_set() #Bloquea la interacción con otras ventanas
        win.images = [] #Evitar garbage collector

        if obligatorio:
            win.protocol("WM_DELETE_WINDOW", lambda: None) #Evitar que cierren la ventana con la X

        mensaje = "¿A quién quiere enviar a la batalla?" if obligatorio else "¿A quién envia a la batalla?"
        tk.Label(win, text=mensaje, font=("Arial", 11), pady=10).pack()

        #Scrollbar por su hay muchos personajes
        canvas = tk.Canvas(win, highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=5)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        vivos = self.filtrar_personajes(self.personajes_jugador, self.activo_jugador)

        #Crea una fila por cada personaje del jugador con su información y un botón para elegirlo
        for p in vivos:
            fila = tk.Frame(inner_frame, padx=10, pady=5)
            fila.pack(fill="x", padx=10)

            try:
                #Guardar las imagenes en la ventana, evitar el actualizar_pantalla()
                base = os.path.dirname(os.path.abspath(__file__))
                ruta = os.path.join(base, "img", p.avatar)
                img = Image.open(ruta)
                img = img.resize((50, 50))
                foto = ImageTk.PhotoImage(img)
                win.images.append(foto)
                tk.Label(fila, image=foto).pack(side="left", padx=(0, 8))
            except:
                tk.Label(fila, text="?", width=4).pack(side="left")

            info = tk.Frame(fila)
            info.pack(side="left", fill="x", expand=True)

            tk.Label(info, text=p.nombre, font=("Arial", 10, "bold"), anchor="w").pack(fill="x")
            tk.Label(info, text=f"HP: {p.vida}/{p.vida_max}  ATK: {p.ataque}  DEF: {p.defensa}",
                    font=("Courier", 9), anchor="w").pack(fill="x")

            tk.Button(info, text="Enviar", command=lambda elegido=p, ob=obligatorio: self.confirmar_cambio(elegido, ob, win),
                    bg="#16213e", fg="white", relief="flat", padx=8, pady=3).pack(anchor="w", pady=(3, 0))
            
        #Si la elección no es obligatoria, crear boton para cancelar
        if not obligatorio:
            tk.Button(win, text="Cancelar", command=win.destroy, bg="#3a3a3a", fg="white",
                    relief="flat", padx=10, pady=6).pack(pady=(0, 10))
            
    #Funcion para atacar al personaje del hollow
    def atacar(self):
        dano = max(1, self.activo_jugador.ataque - self.activo_hollow.defensa)
        self.activo_hollow.vida = max(0, self.activo_hollow.vida - dano)
        self.log(f"{self.activo_jugador.nombre} inflige {dano} pts de daño a {self.activo_hollow.nombre}")
        self.log(f"HP de {self.activo_hollow.nombre}: {self.activo_hollow.vida}")

        #Si el personaje del hollow se queda sin vida, pasa a ser un personaje del jugador
        if self.activo_hollow.vida <= 0:
            self.log(f"{self.activo_hollow.nombre} fue derrotado.")
            self.puntaje_jugador += 1

            capturado = self.activo_hollow.clonar()
            capturado.vida = capturado.vida_max
            if not self.revisar_nombre(self.personajes_jugador, capturado.nombre):
                self.personajes_jugador.append(capturado)
                self.log(f"{capturado.nombre} se unió al equipo de {self.jugador_nombre}.")
            else:
                self.log(f"{capturado.nombre} ya está en el equipo de {self.jugador_nombre}.")
            self.hollow.personajes.remove(self.activo_hollow)
            self.activo_hollow = None

            #El hollow elige un personaje activo aleatorio
            if self.hollow.personajes:
                self.activo_hollow = random.choice(self.hollow.personajes)

        self.batalla("hollow") #Pasa el turno al hollow

    #Funcion para abrir la ventana de cambio de personaje
    def abrir_cambio(self):
        vivos = self.filtrar_personajes(self.personajes_jugador, self.activo_jugador)
        if not vivos:
            messagebox.showinfo("Sin opciones", "No tiene otros personajes disponibles.")
            return
        self.elegir_personaje(obligatorio=False)

    #Funcion para confirmar el cambio del personaje activo
    def confirmar_cambio(self, personaje, obligatorio, win):
        win.destroy()
        self.activo_jugador = personaje
        self.log(f"{self.jugador_nombre} envía a {personaje.nombre}")
        if not self.batalla_iniciada:
            self.batalla_iniciada = True
            self.batalla("jugador") #Inicia la batalla con el turno del jugador
        elif obligatorio:
            self.batalla("jugador") #Turno del jugador si le matan a un personaje y tiene que cambiar
        else:
            self.batalla("hollow") #Pasa el turno al hollow despues de cambiar el personaje

    #Funcion para mostrar la ventana con la información de los personajes del hollow
    def mostrar_hollow(self):
        win = tk.Toplevel(self)
        win.title(f"Personajes de {self.hollow.nombre}")
        win.resizable(False, False)
        win.grab_set() #Evitar interacción con otras pantallas
        win.images = [] #Evitar garbage collector

        #Scrollbar
        canvas = tk.Canvas(win, highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=5)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for p in self.hollow.personajes:
            fila = tk.Frame(inner_frame, padx=10, pady=5)
            fila.pack(fill="x", padx=10)

            try:
                #Guardar las imagenes en la ventana, evitar el actualizar_pantalla()
                base = os.path.dirname(os.path.abspath(__file__))
                ruta = os.path.join(base, "img", p.avatar)
                img = Image.open(ruta)
                img = img.resize((50, 50))
                foto = ImageTk.PhotoImage(img)
                win.images.append(foto)
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

    #Función para escribir un mensaje en el log de batalla
    def log(self, mensaje):
        self.log_txt.config(state="normal")
        self.log_txt.insert("end", mensaje + "\n")
        self.log_txt.see("end")
        self.log_txt.config(state="disabled")

    #Función para obtener una lista de los personajes vivos
    def lista_vivos(self, lista, indice=0, resultado=None):
        if resultado == None: #Crear lista en la primera llamada
            resultado = []
        if indice >= len(lista): #Caso base en el que ya recorre todos los personajes
            return resultado
        if lista[indice].vida > 0: #Agrega el personaje si esta vivo
            resultado.append(lista[indice])
        return self.lista_vivos(lista, indice + 1, resultado)

    #Función para excluir el personaje activo del jugador
    def filtrar_personajes(self, lista, excluir, indice=0, resultado=None):
        if resultado is None: #Crear lista en la primera llamada
            resultado = []
        if indice >= len(lista): #Caso base en el que ya recorre todos los personajes
            return resultado
        if lista[indice] is not excluir: #Agrega el personaje si no es el que se quiere excluir
            resultado.append(lista[indice])
        return self.filtrar_personajes(lista, excluir, indice + 1, resultado)
    
    #Función para revisar si un personaje con el mismo nombre ya esta en la lista
    def revisar_nombre(self, lista, nombre, indice=0):
        if indice >= len(lista): #Caso base en el que ya recorre todos los personajes
            return False
        if lista[indice].nombre == nombre: #Si encuentra un personaje con el mismo nombre devuelve True
            return True
        return self.revisar_nombre(lista, nombre, indice + 1)

#Clase principal del juego, maneja el estado actual del juego y el cambio entre pantallas
class Root(tk.Tk):

    def __init__(self):
        super().__init__()
        #Atributos del Root
        self.title("Hollownest's Epic Adventure")
        self.geometry("800x600")
        self.resizable(False, False) #No permite cambiar el tamaño de la ventana

        self.nombre_jugador = ""
        self.avatar_jugador = ""
        self.personajes_jugador = []
        self.puntaje_jugador = 0
        self.pantalla_actual = None
        self.todos_personajes = crear_personajes()
        self.hollows = []
        self.hollows_derrotados = set()
        self.iniciar()

    #Funcion para cambiar la pantalla actual del juego
    def cambiar_pantalla(self, nueva):
        if self.pantalla_actual:
            self.pantalla_actual.destroy() #Destruye la pantalla actual
        self.pantalla_actual = nueva
        nueva.pack(fill="both", expand=True) #Muestra la nueva pantalla

    #Funcion para crear los hollows
    def iniciar_hollow(self, nombres, avatars, personajes, indice=0, resultado=None):
        if resultado is None:
            resultado = []
        if indice >= len(nombres):
            return resultado
        hollow = crear_hollow(nombres[indice], avatars[indice], personajes)
        resultado.append(hollow)
        return self.iniciar_hollow(nombres, avatars, personajes, indice + 1, resultado)

    #Función para iniciar el juego
    def iniciar(self):
        #Crea los hollows con sus personajes, el puntaje del jugador y los hollows derrotados se reinician
        self.hollows = self.iniciar_hollow(Hollow.nombres, Hollow.avatars, self.todos_personajes)
        self.puntaje_jugador = 0
        self.hollows_derrotados = set()
        #Crea la pantalla de carga
        pantalla = Pantalla_de_carga(self, self.ir_mapa)
        self.cambiar_pantalla(pantalla)

    #Función para ir a la pantalla del mapa
    def ir_mapa(self, nombre, avatar, personajes, hollows_derrotados):
        #Actualiza los atributos del jugador con la información recibida desde la pantalla de carga
        self.nombre_jugador = nombre
        self.avatar_jugador = avatar
        self.personajes_jugador = personajes
        self.hollows_derrotados = hollows_derrotados
        #Crea la pantalla del mapa con la información del jugador y los hollows derrotados para mostrar el progreso
        pantalla = Pantalla_de_mapa(self, nombre, avatar, personajes, self.hollows_derrotados, self.ir_batalla)
        self.cambiar_pantalla(pantalla)

    #Función para ir a la pantalla de batalla
    def ir_batalla(self, idx_hollow):
        hollow = self.hollows[idx_hollow] #Obtiene el hollow correspondiente al índice recibido
        #Crea la pantalla de batalla con la informacion del jugador y el hollow
        pantalla = Pantalla_batalla(self, self.nombre_jugador, self.avatar_jugador, self.personajes_jugador, hollow, self.puntaje_jugador, 
                                lambda victoria, puntaje, idx=idx_hollow: self.fin_batalla(victoria, puntaje, idx))
        self.cambiar_pantalla(pantalla)

    #Función para cuando termina la batalla
    def fin_batalla(self, victoria, puntaje, idx_hollow):
        self.puntaje_jugador = puntaje
        #Verifica si gana el jugador
        if victoria:
            self.hollows_derrotados.add(idx_hollow)
            if len(self.hollows_derrotados) == 5: #Si el jugador derrotó a los 5 hollows, muestra mensaje de victoria y reinicia el juego
                messagebox.showinfo("¡Ganaste!",
                                    f"¡Felicidades {self.nombre_jugador}!\n"
                                    "Derrotaste a todos los Hollows.")
                self.iniciar()
            else: #Vuelve al mapa con el información actualizada
                self.ir_mapa(self.nombre_jugador, self.avatar_jugador, self.personajes_jugador, self.hollows_derrotados)
        else: #Si pierde el jugador, muestra mensaje de derrota y reinicia el juego
            messagebox.showwarning("Perdiste", "Perdiste la batalla...")
            self.iniciar()


if __name__ == "__main__": #Ejecuta si es el archivo principal
    root = Root()
    root.mainloop() #Mantiene la ventana abierta y espera los eventos