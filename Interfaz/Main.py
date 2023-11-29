'''Author: Nayeli Itzel Dominguez Avila
Aplicacion para buscar palabras mediante una interfaz dado un diccionario (ejercicios anteriores)'''

# Librerias creadar por autores
from funcs import recovery_url
from funcs import recovery_title
from funcs import recovery_frec

import tkinter as tk # Libreria para interfaz
from tkinter import scrolledtext as st # Libreria de interfaz para barra de deslizamiento
from tkinter import filedialog as fd # Libreria de interfaz para abrir archivos
from tkinter import messagebox as mb # Libreria para mostra ventanas de error advertencia, etc.

import sys # Libreria para reconer el sistema en el que se trabaja (Windows)
import operator # Libreria para poder organizar alguna lista con subs listas

from customtkinter import * # Libreria para customizar interfaz
import ast # libreria para convertir str a dict
import spacy # Libreria para NLP
import spacy_spanish_lemmatizer # Libreria especial para NLP en español
import copy # Libreria para hacer copia profunda y superficial de alguna lista.

class Aplicacion:
    def __init__(self): # Funcion inicial
        self.ventana1= tk.Tk() # Inicializacion de la interfaz
        self.ventana1.title("Mini Buscador") # Titulo de ventana
        self.valida_txt = False # Validacion auxiliar para TXT
        if "win" in sys.platform: # Condicionante para elegir modo de ventana
            if get_appearance_mode() == "Dark":
                self.ventana1.configure(bg="gray20")  # set window background to dark color
        tk.Grid.columnconfigure(self.ventana1, 0, weight=1) # Funcion para redimencion de interfaz
        tk.Grid.rowconfigure(self.ventana1, 0, weight=1) # Funcion para redimencion de interfaz
        self.ventana1.geometry("700x600") # Tamaño inicial de ventana
        self.agregar_menu() # Funcion agergar menu
        # Agregar logo en interfaz
        self.img_logo = tk.PhotoImage(file=r"Cool Text - Busqueda 397680572648656.png")
        self.Label_logo = tk.Label(self.ventana1, image=self.img_logo, border="0", bg="#333333")
        self.Label_logo.grid(row=0, column=0)
        # Agregar entrada de texto
        self.entry = CTkEntry( master=self.ventana1, width=400, height=28, corner_radius=5, justify="center")
        self.entry.grid(row=1, column=0)
        # Agrega boton para buscar
        self.BBuscar = CTkButton(master=self.ventana1, border_color="#5EA880", fg_color=None,
                                               hover_color="#458577", height=28, text="Buscar", border_width=1,
                                               corner_radius=5, command=self.func_busqueda).grid(row=2, column=0)
        # Agrega boton para eliminar
        self.BEliminar = CTkButton(master=self.ventana1, border_color="#5EA880", fg_color=None,
                                               hover_color="#458577", height=28, text="Eliminar", border_width=1,
                                               corner_radius=5, command=self.Eliminar).grid(row=3, column=0)
        # Agrega cuadro de texto (edicion de texto)
        self.scrolledtext1 = st.ScrolledText(self.ventana1, width=100, height=20)
        self.scrolledtext1.grid(column=0,row=5, padx=10, pady=10)
        self.ventana1.mainloop() # Funcion para ejecutar un ciclo de eventos Tkinter

    def Eliminar(self): # Funcion para eliminar en entrada de texto y editor de texto
        self.entry.delete(0, "end")
        self.scrolledtext1.delete(1.0, "end")

    def agregar_menu(self): # Funcion para agregar menu de opciones
        menubar1 = tk.Menu(self.ventana1)
        self.ventana1.config(menu=menubar1)
        opciones1 = tk.Menu(menubar1, tearoff=0)
        opciones1.add_command(label="Recuperar archivo", command=self.abrir_txt)
        opciones1.add_separator()
        opciones1.add_command(label="Salir", command=self.salir)
        menubar1.add_cascade(label="Archivo", menu=opciones1)

    def salir(self): # Funcion para salir de aplicacion
        sys.exit()

    def abrir_txt(self): # Funcion para abrir archivo txt
        nombrearch=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
        if nombrearch!='':
            archi1=open(nombrearch, "r", encoding="utf-8")
            # variable para cadena del txt
            cadena_dic = ''
            # lectura del txt resultados del ejercicio anterior
            with open(archi1.name, 'r', encoding='utf-8') as archivo:
                for lines in archivo:
                    cadena_dic = lines
            # conversion de str a dict
            self.diccionario = ast.literal_eval(cadena_dic)
            self.valida_txt = True

    def func_busqueda(self): # Funcion principal de busqueda
        self.scrolledtext1.delete(1.0, "end")
        if self.valida_txt == True:
                # Inicializar funciones
                nlp = spacy.load('en_core_web_sm')
                nlp2 = spacy.load("es_core_news_sm")
                nlp2.replace_pipe("lemmatizer", "spanish_lemmatizer")
                palabras_buscar = []
                # Crea los token, los almacena en una lista y los lematiza
                for token in nlp(self.entry.get()):
                    palabras_buscar.append([token.text, token.lemma_])
                i=0
                # Recupera y saca informacion de una palabra
                for token in nlp2(self.entry.get()):
                    palabras_buscar[i].append(token.pos_)
                    i+=1
                palabras_por_urls = {}
                result = {}
                # Iniciar for para buscar palabras en el diccionario
                for palabra in palabras_buscar:
                    valor = 0
                    if self.diccionario.get(palabra[0]) != None or self.diccionario.get(palabra[1] != None):
                        if palabra[-1] != "ADP": # Omitir palabra si es un adjetivo
                            if palabra[-1] != "DET": # Omotir palabras si son determinantes
                                # Recupera urls de una palabra
                                urls = recovery_url.recupera_url(self.diccionario.get(palabra[0]))
                                # Recupera frecuencia de la palabra
                                frec = recovery_frec.recupera_frec(self.diccionario.get(palabra[0]))
                                for url in range(len(urls)): # For para agregar aun diccionario {url: [palabra frecuencia]}
                                    if result.get(urls[url]) == None:
                                        result[urls[url]] = [1]
                                        lista = result.get(urls[url])
                                        lista.append([palabra[0], frec[url]])
                                    else:
                                        lista = result.get(urls[url])
                                        lista[0] = lista[0]+1
                                        lista.append([palabra[0], frec[url]])
                # Ordenacion del diccionario conforme a la frecuencia de las palabras
                result = sorted(result.items(), key=operator.itemgetter(1))
                for resul in result: # For para recuperar titulos de urls
                    title = recovery_title.recupera_title(resul[0])
                    palabras_frec = resul[1][1:]
                    for pala in range(len(palabras_frec)): # For para insertar palabras y frecuecics conforme a urls
                        self.scrolledtext1.insert("1.0", f"{palabras_frec[pala][0]}, {palabras_frec[pala][1]} ")
                    # Insertar titulo de pagina, url, cantidad de palabras encontradas y etiqueta palabras y frecuencia
                    self.scrolledtext1.insert("1.0", f"\nTitulo de pagina: {title}\nUrl de pagina: {resul[0]}\n"
                                                     f"Cantidad de palabras encontradas: {resul[1][0]}\n"
                                                     f"Palabras y frecuencia:\n")
                    # Insertar salta de linea en el texto
                    self.scrolledtext1.insert("1.0", f"\n")

        else:
            # Mostrar mensaje de error si no ha cargado el txt
            mb.showerror("Error", "No se ha cargado el archivo que contiene el diccionario. \nVerifique que se haya cargado.")
        self.entry.delete(0, "end")

aplicacion1=Aplicacion() # Inicio de aplicacion mediante una clase