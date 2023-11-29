# author: Nayeli Itzel Dominguez Avila
#modificado por: Alexi vasquez rodriguez

# El programa recoje url de un txt y manda a llamar a esa pagina para poder recuperar las palabras y hacer un conteo
# una vez que el conteo este echo e guarda en un diccionario y se guarda en un txt.

# librerias necesarias
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

diccionario = {}
url = []

# optencion de las urls que estan en un txt
with open("50Urls.txt",'r',encoding='utf-8') as archivo:
    for lines in archivo:
        url.append(lines) # guardado de links en una lista de string

# for para ir de una en una url
for i in url:
    frecuencia_palabras = []
    results = []
    print(i)
    html = urlopen(i).read()
    soup = BeautifulSoup(html,features="lxml")
    # matar todos los elementos de estilo y guión
    for script in soup(["script", "style"]):
        script.extract()    # extraccion

    # recupera texto
    text = soup.get_text()

    # dividir en líneas y eliminar el espacio inicial y final en cada
    lines = (line.strip() for line in text.splitlines())
    # dividir varios titulares en una línea cada uno
    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
    # soltar líneas en blanco
    text = ' '.join(chunk for chunk in chunks if chunk)

    texto = text.split(' ') # separar string por palabras

    for w in texto: # for que recupera el numero de palbras que hay
        frecuencia_palabras.append([w,texto.count(w)])

    for w in frecuencia_palabras:
        w[0] = re.sub(r'[^\w\s]','',w[0])
        w[0] = w[0].lower()
    frecuencia_palabras2 = []

    for w in frecuencia_palabras:
        frecuencia_palabras2.append((w[0],w[1]))

    for item in frecuencia_palabras2: # for para elimilar palabras repetidas sin borrar el numero de palabras
        if item not in results:
            if len(item[0])>2:
                if len(item[0])<20:
                    if not item[0].isdigit():
                        results.append(item)

    diccionario[i] = results # guardado de los resultados en el diccionario

# 2da parte, invertir diccionario
new_diccionario = {} # nuevo diccionario
lista = []

for item in diccionario:
    for palab in diccionario[item]:
            lista.append([palab[0],item, palab[1]])

indi = len(lista)
palabras = []
for i in range(indi):
    if lista[i][0] not in palabras:
        palabras.append([lista[i][0]])

for i in palabras:
    for j in lista:
        if j[0] in i:
            if j[1] not in i:
                i.append(j[1])
                i.append(j[2])

results = []
for item in palabras:
    if item not in results:
        results.append(item)

for i in results:
    if len(i) == 3:
        new_diccionario[i[0]] = (i[1],i[2])
    elif len(i) == 5:
        new_diccionario[i[0]] = (i[1],i[2],i[3],i[4])
    elif len(i) == 7:
        new_diccionario[i[0]] = (i[1],i[2],i[3],i[4],i[5],i[6])
# impresion del nuevo diccionario de una forma estetica
#print(json.dumps(new_diccionario, sort_keys=False, indent=4))

# escritura del nuevo diccionario en un nuevo txt
with open("raiz_ind_inv.txt", 'w', encoding='utf-8') as archivo: # guardado del dicconario en txt
    archivo.write(str(new_diccionario))




