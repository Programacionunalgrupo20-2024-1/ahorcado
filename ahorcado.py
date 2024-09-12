import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Variables globales
pistas_disponibles = 0
temporizador = 0
perdido_por_tiempo = False
perdido_por_intentos = False
imagenes = []
intentos = 6
palabra = ''
progreso = []
letras_ingresadas = set()

# Función para cargar las imágenes del ahorcado
def cargar_imagenes():
    global imagenes
    for i in range(7):
        img = Image.open(f"imagenes/ahorcado_{i}.png")
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        imagenes.append(ImageTk.PhotoImage(img))

def iniciar_juego():
    global palabra, progreso, letras_validas, letras_ingresadas, intentos, pistas_disponibles, temporizador, tiempo_label, perdido_por_tiempo, perdido_por_intentos
    palabra = solicitar_palabra()
    if palabra:
        progreso = inicializar_progreso(palabra)
        letras_validas = obtener_letras_validas()
        letras_ingresadas = set()
        intentos = 6
        perdido_por_tiempo = False
        perdido_por_intentos = False
        if len(palabra) >= 8:
            pistas_disponibles = 2
            pistas_button.config(state=tk.NORMAL)
            temporizador = 5 * 60
        elif len(palabra) >= 5:
            pistas_disponibles = 1
            pistas_button.config(state=tk.NORMAL)
            temporizador = 3 * 60
        else:
            pistas_disponibles = 0
            pistas_button.config(state=tk.DISABLED)
            temporizador = 1 * 60
        tiempo_label.config(text=f"Tiempo restante: {format_tiempo(temporizador)}")
        actualizar_ventana()
        contar_tiempo()

def solicitar_palabra():
    return palabra_entry.get().strip().lower()

def inicializar_progreso(palabra):
    return ['_'] * len(palabra)

def obtener_letras_validas():
    return set('abcdefghijklmnopqrstuvwxyzñ')

def jugar():
    letra = solicitar_letra(letras_ingresadas, letras_validas)
    if letra:
        procesar_intento(palabra, progreso, letra, letras_ingresadas)
        global intentos
        intentos = actualizar_intentos(palabra, letra, intentos)
        if intentos <= 0:
            global perdido_por_intentos
            perdido_por_intentos = True
        actualizar_ventana()
        if juego_terminado(intentos, progreso, perdido_por_tiempo, perdido_por_intentos):
            finalizar_juego()

def pedir_pista():
    global pistas_disponibles
    if pistas_disponibles > 0:
        revelar_letra()
        pistas_disponibles -= 1
        if pistas_disponibles == 0:
            pistas_button.config(state=tk.DISABLED)
        actualizar_ventana()
    elif len(palabra) <= 7:
        messagebox.showinfo("Sin Pistas", "La palabra tiene 7 letras o menos. No se pueden usar pistas.")
    else:
        messagebox.showwarning("Sin Pistas", "Ya no tienes más pistas disponibles.")

def revelar_letra():
    for idx, letra in enumerate(palabra):
        if progreso[idx] == '_':
            progreso[idx] = letra
            break

def juego_terminado(intentos, progreso, perdido_por_tiempo, perdido_por_intentos):
    return intentos <= 0 or '_' not in progreso or temporizador <= 0 or perdido_por_tiempo or perdido_por_intentos

def mostrar_progreso(progreso):
    progreso_label.config(text=' '.join(progreso))

def solicitar_letra(letras_ingresadas, letras_validas):
    letra = letra_entry.get().strip().lower()
    if es_letra_valida(letra, letras_validas, letras_ingresadas):
        letra_entry.delete(0, tk.END)
        return letra
    else:
        manejar_entrada_invalida(letra, letras_ingresadas)
        letra_entry.delete(0, tk.END)
        return None

def es_letra_valida(letra, letras_validas, letras_ingresadas):
    return len(letra) == 1 and letra in letras_validas and letra not in letras_ingresadas

def manejar_entrada_invalida(letra, letras_ingresadas):
    if letra in letras_ingresadas:
        messagebox.showwarning("Advertencia", f"Ya ingresaste la letra '{letra}'. Intenta con otra.")
    else:
        messagebox.showwarning("Advertencia", "Entrada no válida. Asegúrate de ingresar una letra válida.")

def procesar_intento(palabra, progreso, letra, letras_ingresadas):
    if letra in palabra:
        actualizar_progreso(palabra, progreso, letra)
        messagebox.showinfo("Correcto", "¡Correcto!")
    else:
        global intentos
        intentos -= 1
        actualizar_imagen(intentos)
        messagebox.showinfo("Incorrecto", "¡Incorrecto!")
    letras_ingresadas.add(letra)

def actualizar_progreso(palabra, progreso, letra):
    for idx, char in enumerate(palabra):
        if char == letra:
            progreso[idx] = letra

def actualizar_intentos(palabra, letra, intentos):
    if letra not in palabra:
        intentos -= 0
    return intentos

def actualizar_imagen(intentos):
    ahorcado_label.config(image=imagenes[6 - intentos])

def actualizar_ventana():
    mostrar_progreso(progreso)
    intentos_label.config(text=f"Intentos restantes: {intentos}")
    pistas_label.config(text=f"Pistas restantes: {pistas_disponibles}")
    tiempo_label.config(text=f"Tiempo restante: {format_tiempo(temporizador)}")

def format_tiempo(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02}:{segundos:02}"

def contar_tiempo():
    global temporizador, perdido_por_tiempo
    if temporizador > 0:
        temporizador -= 1
        tiempo_label.config(text=f"Tiempo restante: {format_tiempo(temporizador)}")
        root.after(1000, contar_tiempo)
    elif temporizador <= 0 and not perdido_por_intentos:
        perdido_por_tiempo = True
        finalizar_juego()

def finalizar_juego():
    global perdido_por_tiempo, perdido_por_intentos
    detener_temporizador()  # Detener el temporizador
    if perdido_por_intentos:
        messagebox.showinfo("¡Perdiste!", "Has perdido por intentos. La palabra era: " + palabra)
    elif '_' not in progreso:
        messagebox.showinfo("¡Ganaste!", "¡Felicidades, has ganado!")
    else:
        # Solo se muestra el mensaje de pérdida por tiempo si el juego no se ha ganado
        if perdido_por_tiempo:
            messagebox.showinfo("¡Perdiste!", "Has perdido por tiempo. La palabra era: " + palabra)
    resetear_juego()

def detener_temporizador():
    global temporizador
    temporizador = 0

def resetear_juego():
    global pistas_disponibles, temporizador, perdido_por_tiempo, perdido_por_intentos, intentos
    pistas_disponibles = 0
    temporizador = 0
    perdido_por_tiempo = False
    perdido_por_intentos = False
    intentos = 6
    palabra_entry.delete(0, tk.END)
    letra_entry.delete(0, tk.END)
    intentos_label.config(text="Intentos restantes: 6")
    pistas_label.config(text="Pistas restantes: 0")
    tiempo_label.config(text="Tiempo restante: 00:00")
    ahorcado_label.config(image=imagenes[0])

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Juego del Ahorcado")

# Cargar imágenes
cargar_imagenes()

# Widgets
palabra_label = tk.Label(root, text="Ingresa la palabra a adivinar:")
palabra_label.pack()

palabra_entry = tk.Entry(root, show="*")
palabra_entry.pack()

comenzar_button = tk.Button(root, text="Comenzar Juego", command=iniciar_juego)
comenzar_button.pack()

progreso_label = tk.Label(root, text="_ _ _ _ _")
progreso_label.pack()

letra_label = tk.Label(root, text="Adivina una letra:")
letra_label.pack()

letra_entry = tk.Entry(root)
letra_entry.pack()

jugar_button = tk.Button(root, text="Adivinar", command=jugar)
jugar_button.pack()

pistas_button = tk.Button(root, text="Pedir Pista", command=pedir_pista)
pistas_button.pack()

intentos_label = tk.Label(root, text="Intentos restantes: 6")
intentos_label.pack()

pistas_label = tk.Label(root, text="Pistas restantes: 0")
pistas_label.pack()

tiempo_label = tk.Label(root, text="Tiempo restante: 00:00")
tiempo_label.pack()

ahorcado_label = tk.Label(root, image=imagenes[0])
ahorcado_label.pack()

reiniciar_button = tk.Button(root, text="Reiniciar", command=resetear_juego)
reiniciar_button.pack()

root.mainloop()


