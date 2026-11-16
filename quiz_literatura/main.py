#proyecto parte 2
#silver alexander diaz barranco
#12/11/2026
import csv
import random
import tkinter as tk
from tkinter import messagebox


class QuizLiteraturaApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Quiz de Literatura Española")
    self.root.geometry("600x500")

    self.nombre_jugador = ""
    self.preguntas_totales = []
    self.preguntas_partida = []
    self.indice_actual = 0
    self.puntaje = 0
    self.respuestas_correctas_contador = 0

    # Cargar preguntas al iniciar con manejo de errores
    self.cargar_preguntas()

    # Si hay al menos 5 preguntas, iniciar vista de inicio
    if self.preguntas_validas:
      self.mostrar_vista_inicio()

  def cargar_preguntas(self):
    self.preguntas_validas = False
    try:
      with open("preguntas.csv", mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
          self.preguntas_totales.append({
              "frase": fila["frase_incompleta"],
              "respuesta": fila["palabra_correcta"],
          })

      # Validar que tenga al menos 5 preguntas
      if len(self.preguntas_totales) < 5:
        messagebox.showerror(
            "Error",
            "El archivo 'preguntas.csv' debe contener al menos 5 preguntas.",
        )
        self.root.destroy()
      else:
        self.preguntas_validas = True
    except FileNotFoundError:
      messagebox.showerror(
          "Error Crítico",
          "No se encontró el archivo 'preguntas.csv'. Asegúrate de crearlo en"
          " la misma carpeta.",
      )
      self.root.destroy()

  def limpiar_ventana(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  # ==========================================
  # VISTA 1: INICIO
  # ==========================================
  def mostrar_vista_inicio(self):
    self.limpiar_ventana()

    titulo = tk.Label(
        self.root,
        text="Quiz de Literatura Española",
        font=("Times New Roman", 18, "bold"),
        fg="#0a0a0a",
    )
    titulo.pack(pady=30)

    lbl_nombre = tk.Label(
        self.root,
        text="Ingresa tu nombre:",
        font=("Times New Roman", 12),
        fg="#0a0a0a",
    )
    lbl_nombre.pack(pady=5)

    self.entry_nombre = tk.Entry(
        self.root, font=("Times New Roman", 12), width=30
    )
    self.entry_nombre.pack(pady=10)

    btn_jugar = tk.Button(
        self.root,
        text="Comenzar Juego",
        font=("Times New Roman", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        command=self.iniciar_juego,
    )
    btn_jugar.pack(pady=20)

  def iniciar_juego(self):
    nombre = self.entry_nombre.get().strip()
    if not nombre:
      messagebox.showwarning(
          "Advertencia", "Por favor ingresa tu nombre para continuar."
      )
      return

    self.nombre_jugador = nombre
    self.puntaje = 0
    self.respuestas_correctas_contador = 0
    self.indice_actual = 0

    # Seleccionar aleatoriamente 5 preguntas de todas las disponibles
    self.preguntas_partida = random.sample(self.preguntas_totales, 5)
    self.mostrar_vista_juego()

  # ==========================================
  # VISTA 2: JUEGO
  # ==========================================
  def mostrar_vista_juego(self):
    self.limpiar_ventana()

    pregunta_actual = self.preguntas_partida[self.indice_actual]

    # Indicador de progreso
    lbl_progreso = tk.Label(
        self.root,
        text=f"Pregunta {self.indice_actual + 1} de 5",
        font=("Times New Roman", 10, "italic"),
        fg="#555555",
    )
    lbl_progreso.pack(pady=10)

    # Frase incompleta
    lbl_frase = tk.Label(
        self.root,
        text=pregunta_actual["frase"],
        font=("Times New Roman", 14, "bold"),
        fg="#0a0a0a",
        wraplength=500,
        justify="center",
    )
    lbl_frase.pack(pady=20)

    # Entry para escribir respuesta
    lbl_instruccion_entry = tk.Label(
        self.root,
        text=(
            "Escribe la palabra (Otorga 10 puntos si aciertas):"
        ),
        font=("Times New Roman", 11),
        fg="#0a0a0a",
    )
    lbl_instruccion_entry.pack()

    self.entry_respuesta = tk.Entry(
        self.root, font=("Times New Roman", 12), width=30
    )
    self.entry_respuesta.pack(pady=5)

    # Listbox con palabras posibles (incluyendo la correcta y distractores)
    lbl_instruccion_list = tk.Label(
        self.root,
        text=(
            "O selecciona del Listbox (Otorga 5 puntos si aciertas):"
        ),
        font=("Times New Roman", 11),
        fg="#0a0a0a",
    )
    lbl_instruccion_list.pack(pady=(15, 0))

    self.listbox_opciones = tk.Listbox(
        self.root, font=("Times New Roman", 11), height=4, width=30, selectmode=tk.SINGLE
    )
    self.listbox_opciones.pack(pady=5)

    # Poblar el Listbox con la respuesta correcta y algunas opciones aleatorias del set total
    opciones = [pregunta_actual["respuesta"]]
    otras_opciones = [
        p["respuesta"]
        for p in self.preguntas_totales
        if p["respuesta"] != pregunta_actual["respuesta"]
    ]
    # Tomar hasta 3 distractores si existen
    if otras_opciones:
      opciones.extend(
          random.sample(
              otras_opciones, min(3, len(otras_opciones))
          )
      )
    random.shuffle(opciones)

    for op in opciones:
      self.listbox_opciones.insert(tk.END, op)

    # Botón validar
    btn_validar = tk.Button(
        self.root,
        text="Validar Respuesta",
        font=("Times New Roman", 12, "bold"),
        bg="#2196F3",
        fg="white",
        command=self.validar_respuesta,
    )
    btn_validar.pack(pady=20)

  def validar_respuesta(self):
    pregunta_actual = self.preguntas_partida[self.indice_actual]
    respuesta_correcta = pregunta_actual["respuesta"]

    # Regla: Si escribe en el Entry se usa el Entry; si no, se revisa el Listbox
    texto_entry = self.entry_respuesta.get().strip()
    seleccion_listbox = ""

    try:
      indice_seleccionado = self.listbox_opciones.curselection()
      if indice_seleccionado:
        seleccion_listbox = self.listbox_opciones.get(indice_seleccionado)
    except Exception:
      pass

    respuesta_usuario = ""
    tipo_ingreso = ""

    if texto_entry:
      respuesta_usuario = texto_entry
      tipo_ingreso = "entry"
    elif seleccion_listbox:
      respuesta_usuario = seleccion_listbox
      tipo_ingreso = "listbox"
    else:
      messagebox.showwarning(
          "Atención",
          "Debes escribir una respuesta en el Entry o seleccionar una opción"
          " del Listbox.",
      )
      return

    # Normalización requerida: .strip().lower() (respetando acentos tal cual el archivo)
    if respuesta_usuario.strip().lower() == respuesta_correcta.strip().lower():
      if tipo_ingreso == "entry":
        self.puntaje += 10
      else:
        self.puntaje += 5
      self.respuestas_correctas_contador += 1
      messagebox.showinfo("¡Correcto!", "¡Has acertado la respuesta!")
    else:
      messagebox.showerror(
          "Incorrecto",
          f"La respuesta correcta era: '{respuesta_correcta}'",
      )

    # Avanzar a la siguiente pregunta o finalizar
    self.indice_actual += 1
    if self.indice_actual < len(self.preguntas_partida):
      self.mostrar_vista_juego()
    else:
      self.mostrar_vista_resultados()

  # ==========================================
  # VISTA 3: RESULTADOS
  # ==========================================
  def mostrar_vista_resultados(self):
    self.limpiar_ventana()

    titulo_res = tk.Label(
        self.root,
        text="¡Juego Finalizado!",
        font=("Times New Roman", 18, "bold"),
        fg="#0a0a0a",
    )
    titulo_res.pack(pady=20)

    lbl_res_nombre = tk.Label(
        self.root,
        text=f"Jugador: {self.nombre_jugador}",
        font=("Times New Roman", 12),
    )
    lbl_res_nombre.pack(pady=5)

    lbl_res_puntaje = tk.Label(
        self.root,
        text=f"Puntaje Total Obtenido: {self.puntaje} puntos",
        font=("Times New Roman", 14, "bold"),
        fg="#2E7D32",
    )
    lbl_res_puntaje.pack(pady=10)

    lbl_res_aciertos = tk.Label(
        self.root,
        text=(
            "Respuestas correctas: "
            f"{self.respuestas_correctas_contador} de 5"
        ),
        font=("Times New Roman", 12),
    )
    lbl_res_aciertos.pack(pady=5)

    btn_reiniciar = tk.Button(
        self.root,
        text="Jugar Nuevamente",
        font=("Times New Roman", 11),
        command=self.mostrar_vista_inicio,
    )
    btn_reiniciar.pack(pady=15)

    btn_salir = tk.Button(
        self.root,
        text="Salir",
        font=("Times New Roman", 11),
        bg="#f44336",
        fg="white",
        command=self.root.destroy,
    )
    btn_salir.pack(pady=5)


if __name__ == "__main__":
  root = tk.Tk()
  app = QuizLiteraturaApp(root)
  root.mainloop()