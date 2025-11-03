import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import os

# 🎨 Colores
BG = "#012E40"
BTN = "#018C8C"
TEXT = "#F2F2F2"
HIGHLIGHT = "#025E73"

class AdivinaAnimal:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Adivina el Animal - Versión Marina 🐠")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG)

        # --- Variables del juego ---
        self.jugadores = []
        self.puntajes = {}
        self.turno_actual = 0
        self.animal_secreto = None
        self.animales_descartados = set()
        self.respuestas_historial = []
        self.imagen_actual = None
        self.imagen_label = None

        # --- Construir interfaz ---
        self._build_ui()

    # 🧩 Crear la interfaz principal
    def _build_ui(self):
        top = tk.Frame(self.root, bg=HIGHLIGHT, height=60)
        top.pack(fill="x")

        tk.Label(top, text="🐾 Adivina el Animal 🐾",
                 bg=HIGHLIGHT, fg=TEXT, font=("Arial Rounded MT Bold", 20)).pack(side="left", padx=20)

        tk.Button(top, text="⚙️ Configurar", command=self.configurar_juego,
                  bg=BTN, fg=TEXT, font=("Arial", 12, "bold")).pack(side="right", padx=20)

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=15, pady=15)

        # 🧍 Panel izquierdo (historial + puntaje)
        left = tk.Frame(main, bg=BG, width=300)
        left.pack(side="left", fill="y")

        tk.Label(left, text="📜 Historial de Preguntas", bg=BG, fg=TEXT,
                 font=("Arial Rounded MT Bold", 14)).pack(pady=10)

        self.text_historial = tk.Text(left, width=35, height=25,
                                      bg="#01394C", fg=TEXT, wrap="word", state="disabled")
        self.text_historial.pack(pady=10, padx=10)

        tk.Label(left, text="🏆 Puntaje", bg=BG, fg=TEXT,
                 font=("Arial Rounded MT Bold", 14)).pack(pady=10)
        self.label_puntaje = tk.Label(left, text="—", bg=BG, fg=TEXT, font=("Arial", 12))
        self.label_puntaje.pack(pady=5)

        # 🐾 Panel derecho (preguntas)
        right = tk.Frame(main, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="❓ Preguntas", bg=BG, fg=TEXT,
                 font=("Arial Rounded MT Bold", 16)).pack(pady=10)

        # --- Contenedor de preguntas con scroll ---
        preguntas_frame = tk.Frame(right, bg=BG)
        preguntas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(preguntas_frame, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(preguntas_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 📸 Panel de imagen del animal
        self.image_panel = tk.Label(self.root, bg=BG)
        self.image_panel.pack(pady=10)

        # Botón para adivinar
        tk.Button(self.root, text="🦁 Adivinar Animal", command=self.adivinar_animal,
                  bg=BTN, fg=TEXT, font=("Arial Rounded MT Bold", 14), width=20).pack(pady=5)

    # ⚙️ Configurar el juego
    def configurar_juego(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Configuración del Juego")
        ventana.geometry("400x400")
        ventana.configure(bg=BG)

        tk.Label(ventana, text="Número de jugadores (1-6):", bg=BG, fg=TEXT).pack(pady=5)
        num_jugadores = tk.IntVar(value=2)
        tk.Spinbox(ventana, from_=1, to=6, textvariable=num_jugadores, width=5).pack(pady=5)

        tk.Label(ventana, text="Nombres de los jugadores:", bg=BG, fg=TEXT).pack(pady=5)
        nombres_frame = tk.Frame(ventana, bg=BG)
        nombres_frame.pack()

        nombres_vars = []
        for i in range(6):
            var = tk.StringVar()
            entry = tk.Entry(nombres_frame, textvariable=var, width=20)
            entry.grid(row=i, column=0, pady=2)
            nombres_vars.append(var)

        tk.Label(ventana, text="Animal secreto del Jugador 1:", bg=BG, fg=TEXT).pack(pady=10)
        animal_entry = tk.Entry(ventana, width=25)
        animal_entry.pack()

        def guardar_config():
            self.jugadores = [v.get() for v in nombres_vars if v.get()]
            if len(self.jugadores) < 1:
                messagebox.showwarning("Advertencia", "Debe haber al menos un jugador.")
                return

            self.puntajes = {j: 0 for j in self.jugadores}
            self.turno_actual = 0
            self.animal_secreto = animal_entry.get().strip().lower()
            self.actualizar_puntajes()
            self.generar_preguntas()
            ventana.destroy()

        tk.Button(ventana, text="Guardar y Comenzar", command=guardar_config,
                  bg=BTN, fg=TEXT, font=("Arial", 12, "bold")).pack(pady=20)

    # ❓ Crear botones de preguntas
    def generar_preguntas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        preguntas = [
            "¿Tiene pelo?", "¿Tiene plumas?", "¿Vive en el agua?", "¿Tiene patas?",
            "¿Tiene cola?", "¿Es carnívoro?", "¿Es herbívoro?", "¿Puede volar?",
            "¿Es doméstico?", "¿Caza a sus presas?", "¿Es grande?", "¿Tiene manchas?",
            "¿Tiene rayas?", "¿Tiene cuernos?", "¿Es un mamífero?", "¿Es un reptil?",
            "¿Tiene pico?", "¿Es blanco?", "¿Come insectos?", "¿Vive en la selva?",
            "¿Vive en el desierto?", "¿Tiene garras?", "¿Es rápido?", "¿Hace sonidos fuertes?",
            "¿Tiene aletas?", "¿Tiene colmillos?", "¿Es peligroso?", "¿Se mueve lento?",
            "¿Duerme mucho?", "¿Le gusta el frío?"
        ]

        for pregunta in preguntas:
            btn = tk.Button(self.scrollable_frame, text=pregunta,
                            bg=BTN, fg=TEXT, font=("Arial", 11, "bold"),
                            command=lambda p=pregunta: self.mostrar_respuesta(p))
            btn.pack(fill="x", pady=3, padx=10)

    # 💬 Mostrar ventana de respuesta
    def mostrar_respuesta(self, pregunta):
        respuesta = messagebox.askyesno("Responder", f"{pregunta}")
        resultado = "Sí" if respuesta else "No"

        self.text_historial.config(state="normal")
        self.text_historial.insert("end", f"• {pregunta} → {resultado}\n")
        self.text_historial.config(state="disabled")
        self.text_historial.see("end")

    # 🦁 Adivinar el animal
    def adivinar_animal(self):
        intento = simpledialog.askstring("Adivinar Animal", "¿Cuál crees que es el animal?").lower().strip()
        if intento == self.animal_secreto:
            jugador = self.jugadores[self.turno_actual]
            self.puntajes[jugador] += 1
            messagebox.showinfo("🎉 ¡Correcto!", f"¡{jugador} adivinó el animal secreto: {self.animal_secreto.capitalize()}!")
            self.mostrar_imagen_animal(self.animal_secreto)
        else:
            messagebox.showerror("❌ Incorrecto", "No es ese animal. Sigue intentando.")
        self.siguiente_turno()

    # 📸 Mostrar imagen
    def mostrar_imagen_animal(self, animal):
        ruta = os.path.join("imagenes_animales", f"{animal}.jpg")
        if not os.path.exists(ruta):
            messagebox.showwarning("Imagen no encontrada", f"No se encontró la imagen de {animal}.")
            return
        img = Image.open(ruta)
        img = img.resize((300, 300))
        self.imagen_actual = ImageTk.PhotoImage(img)
        self.image_panel.config(image=self.imagen_actual)
        self.image_panel.image = self.imagen_actual

    # 🔄 Cambiar turno
    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        jugador = self.jugadores[self.turno_actual]
        messagebox.showinfo("Cambio de Turno", f"Ahora es el turno de {jugador}.")
        self.actualizar_puntajes()

    # 🧮 Actualizar puntajes
    def actualizar_puntajes(self):
        texto = "\n".join([f"{j}: {p}" for j, p in self.puntajes.items()])
        self.label_puntaje.config(text=texto)


# 🐾 Iniciar el juego
if __name__ == "__main__":
    root = tk.Tk()
    app = AdivinaAnimal(root)
    root.mainloop()
