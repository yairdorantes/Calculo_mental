import random

from tkinter import *
import sys
from tkinter import ttk
import tkinter

import pygame
import os
import sqlite3

import functools


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
path = resource_path('music.wav')
path2=resource_path('calculadora.ico')
path3=resource_path('start.png')
path4=resource_path('volumen.png')
path5=resource_path('images.png')
path6=resource_path('fasting.wav')
cuenta_regresiva = 80


correct = 0
def disminuir_tiempo():
    global cuenta_regresiva,correct
    if correct > 5:
        cuenta_regresiva = 30

conn = sqlite3.connect('puntajes')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Puntajes(Score INT)')

create_table()
#insert()


timer = 10
lista = []
res = 0
puntaje = 0
theBest = 0
tiempo = 100


def best_scores():
    global mejores_puntajes
    mejores_puntajess = []
    for i in c.execute("SELECT * FROM Puntajes"):
        res = functools.reduce(lambda sub, ele: sub * 10 + ele, i)
        mejores_puntajess.append(res)
    mejores_puntajes =  mejores_puntajess.sort()
    mejores_puntajes =  mejores_puntajess[::-1]

best_scores()


volumen = 1.0
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(path)
pygame.mixer.music.play()
pygame.mixer.music.set_volume(volumen)

def vol_music():
    global volumen
    if volumen < -0.1:
        volumen = 1.0
    else:
        volumen -= 0.2
    pygame.mixer.music.set_volume(volumen)



def play_music():
    pygame.mixer.music.load(path6)
    pygame.mixer.music.play()

altura=160

def posiciones(altura):
    posc=0
    
    contador_puntajes = 0
    for i in mejores_puntajes:
        contador_puntajes+=1
        if contador_puntajes > 3:
            break
        posc += 1
        altura+=50
        puntuacion = Label(raiz,fg='black',bg="#4AC9C5",text=f'{posc}° | {i}',font=("Courier", 16, "italic"))
        puntuacion.place(x=0,y=altura)

def inicio_barra():
    global tiempo, theBest
    barra["value"] = tiempo
    tiempo -= 1
    raiz.update_idletasks()
    if tiempo > 0:
        btnIniciar["state"] = "disabled"
        escribirResultado["state"] = "normal"
        #times["text"] = tiempo
    if tiempo == 0:
        c.execute('INSERT INTO Puntajes VALUES (?)', [puntaje])
        conn.commit()
        escribirResultado.delete(0, "end")
       # times["text"] = tiempo
        escribirResultado["state"] = "disabled"
        btnIniciar["state"] = "normal"
        evaluacion["text"] = "¡Se acabo el tiempo! :("
        posiciones(altura)

    barra.after(cuenta_regresiva, inicio_barra)


def msj_vacio():
    evaluacion["text"] = ""


def reiniciar_tiempo():
    global tiempo, puntaje
    tiempo = 100
    puntaje = 0
    score["text"] = "Puntaje: 0"


def msj():
    frases = ["Correcto!", "Sigue así!", "No te detengas!", "Excelente!", "Ve por más!"]
    evaluacion["text"] = random.choice(frases)


def simbolo():
    num = random.randrange(1, 5)
    if num == 1:
        simbolo = " + "
    if num == 2:
        simbolo = " - "
    if num == 3:
        simbolo = " x "
    if num == 4:
        simbolo = " / "
    return simbolo


def definir_ejercicio():
    simbol = simbolo()
    global lista
    aleatorio = random.randrange(5, 25)
    aleatorio_two = random.randrange(1,10)
    if simbol == ' / ':
        if aleatorio % aleatorio_two == 0:
            lista.append(aleatorio)
            lista.append(simbol)
            lista.append(aleatorio_two)
        else:
            definir_ejercicio()
    else:
        lista.append(aleatorio)
        lista.append(simbol)
        lista.append(aleatorio_two)

def ejercicio_escrito():
    global lista, boton
    txt = ""
    txt = txt.join(map(str, lista))
    ejercicio["text"] = txt

def leer_resultado(self):
    global lista, puntaje, tiempo,correct
    box = escribirResultado.get()
    try:
        resultado_usuario = int(box)
        if resultado_usuario == res:
            msj()
            lista = []
            escribirResultado.delete(0, "end")
            definir_ejercicio(), ejercicio_escrito(), procesar_ejercicio()
            tiempo = 100
            puntaje += 100
            score["text"] = f"Puntaje: {puntaje}"
            correct += 1
            disminuir_tiempo()
        else:
            evaluacion["text"] = "Resultado incorrecto, intenta de nuevo"
            #play_wrong()
            escribirResultado.delete(0, "end")
      

    except ValueError:
        evaluacion["text"] = "Valor no admitido"


def sumar(num1, num2):
    result = num1 + num2
    return result


def restar(num1, num2):
    result = num1 - num2
    return result


def multiplicar(num1, num2):
    result = num1 * num2
    return result

def divisional(num1, num2):
    result = num1 / num2
    return result

def procesar_ejercicio():
    
    global res, lista
    if lista[1] == " + ":
        res = sumar(lista[0], lista[2])
    if lista[1] == " - ":
        res = restar(lista[0], lista[2])
    if lista[1] == " x ":
        res = multiplicar(lista[0], lista[2])
    if lista[1] == " / ":
        res = divisional(lista[0], lista[2])
    lista = []

raiz = Tk()


#raiz.iconbitmap(path2)
posiciones(altura)
raiz.geometry("800x400")
raiz.resizable(width=0, height=0)
raiz.configure(bg='#4AC9C5')
# barras

s = ttk.Style()
s.configure(
    "TProgressbar",
    background="#FF0000",
    troughcolor="white",
    thickness=20,
)

barra = ttk.Progressbar(raiz, style="TProgressbar", length=600, mode="determinate")

barra.pack()

# finbarra

#times = Label(raiz, fg="black", text=0, padx=10,bg="#4AC9C5")

ejercicio = Label(raiz, fg="black",bg='#4AC9C5', text="", padx=20,font=("bold",20))

evaluacion = Label(raiz, fg="#FF0000",bg="#4AC9C5", text="", padx=20,font=("bold", 11,))

score = Label(raiz, fg="black", bg="#4AC9C5",text=f"Puntaje: {puntaje}", padx=10, pady=10,font=("Courier", 16, "italic"))

best = Label(raiz, fg="black",bg="#4AC9C5", text=f"Mejores puntajes: ",font=("Courier", 16, "italic"))


best.place(x=0, y=150)
score.place(x=-7, y=100)
ejercicio.pack()
#times.pack()
evaluacion.pack()

# raiz.configure(bg="beige")

raiz.title("Calculo mental")

frame = Frame(raiz)
frame.pack()

starting = PhotoImage(file=path3)

starting = starting.subsample(5,5)

btnIniciar = Button(
    frame,
    image=starting,
    borderwidth=0,
    command=lambda: [
        definir_ejercicio(),
        ejercicio_escrito(),
        procesar_ejercicio(),
        reiniciar_tiempo(),
        msj_vacio(),
        best_scores(),
        posiciones(altura),
    ],
    
   
   
)

bocina = PhotoImage(file=path4)
bocina = bocina.subsample(15,15)
btn_bajar_vol = Button(raiz,image=bocina,command=vol_music)
btn_bajar_vol.place(x=720,y=0)
# imagen reloj arena

Imagen = PhotoImage(file=path5)

Imagen = Imagen.subsample(3,3)
imagen2 = Label(raiz, image=Imagen)

imagen2.place(x=0, y=0)

#imagen2.pack()

# fin imagen

btnCrearEjercicio = Button(
    frame,
    image = starting,
    command=lambda: [
        definir_ejercicio(),
        ejercicio_escrito(),
        procesar_ejercicio(),
        inicio_barra(),
        btnCrearEjercicio.grid_forget(),
        btnIniciar.grid(row=1, column=1),
        play_music(),
   
    ],
    bg="#4AC9C5"
)
btnCrearEjercicio.grid(row=1, column=1)


escribirResultado = Entry(
    raiz,
    fg="black",
    font=("bold", 15,)
    

   
)

escribirResultado.place(x=350, y=150,height=40,width=100)



# widget.bind(event, handler) funcion 'bind'
raiz.bind("<Return>", leer_resultado)

# Boton salir -------------------------
def quit():
    sys.exit()
exit = Button(raiz, text="Salir", command=quit,fg='black',bg="#4AC9C5")
exit.place(x=0, y=360)


# Menus --------------------------------

menubar = Menu(raiz)
#raiz.config(menu=menubar)
#salida = Menu(menubar)
#menubar.add_cascade(label="Salir", menu=salida, command=quit)


menubar.mainloop()
