"""
    COMPILADORES 3CV11
    Pérez Bravo Isaac Ulises
    Práctica 1. Traductor inglés-español
"""

#Orientandolo a a objetos
class Traductor:
    #Creando el archivo primera vez
    def creandoArchivo():
        try:
            with open("diccionarioDatos.txt", "x") as dicDatos:
                #Ingresando primeras traducciones al archivo
                dicDatos.write("abrir = open\n")
                dicDatos.write("ir = go\n")
                dicDatos.write("cargar = upload\n")
                dicDatos.write("quieto = stay\n")
                dicDatos.write("azul = blue\n")
                return dicDatos
        except FileExistsError:
            with open("diccionarioDatos.txt", "r") as dicDatos:
                return dicDatos #El archivo ya existe

    #Agregando una nueva traducción
    def agregaP(palabra, traduccion):
        
        diccionario = open("diccionarioDatos.txt", "a+")
        linea = palabra+" = "+traduccion+"\n"
        print(linea)
        diccionario.write(linea)
        diccionario.close()
        print("\n****PALABRA AÑADIDA AL DICCIONARIO****\n")

    #Leyendo el archivo
    def leerDic(diccionario):
        diccionario = open("diccionarioDatos.txt", "r")
        print("\n*******TABLA DE TRADUCCIONES*******\n\n")
        for linea in diccionario:
            linea = linea.rstrip("\\n")
            print(linea)
        diccionario.close()

    #Sacando listas en español e inglés
    def listasTabla(diccionario):
        
        listaEspañol = []
        listaIngles = []
        diccionario = open("diccionarioDatos.txt", "r")
        for linea in diccionario:
            linea = linea.rstrip()
            #Limpiando el signo = y buscando linea por linea
            tuplaPalabras = linea.partition(" = ")
            espa, aux, ing = tuplaPalabras
            #print("Español: "+espa+", inglés: "+ing)
            listaEspañol.append(espa)
            listaIngles.append(ing)
        diccionario.close()

        return listaEspañol, listaIngles

    # Definimos una función para calcular la distancia de Levenshtein entre dos palabras
    def distancia_levenshtein(palabra1, palabra2):
        # Si la primera palabra es más corta que la segunda, intercambiamos las palabras para simplificar el cálculo
        if len(palabra1) < len(palabra2):
            return Traductor.distancia_levenshtein(palabra2, palabra1)

        # Si la segunda palabra es vacía, la distancia es igual a la longitud de la primera palabra
        if len(palabra2) == 0:
            return len(palabra1)

        # Inicializamos una lista llamada "anteriores" con valores desde 0 hasta la longitud de la segunda palabra
        anteriores = range(len(palabra2) + 1)

        # Recorremos cada carácter de la primera palabra
        for i, c1 in enumerate(palabra1):
            # Inicializamos una lista llamada "actuales" con el primer valor igual a la posición actual más 1
            actuales = [i + 1]

            # Recorremos cada carácter de la segunda palabra
            for j, c2 in enumerate(palabra2):
                # Calculamos tres posibles operaciones: inserción, eliminación y sustitución
                insercion = anteriores[j + 1] + 1
                eliminacion = actuales[j] + 1
                sustitucion = anteriores[j] + (c1 != c2)

                # Agregamos el mínimo de las tres operaciones a la lista "actuales"
                actuales.append(min(insercion, eliminacion, sustitucion))

            # Actualizamos la lista "anteriores" con los valores de "actuales" para la siguiente iteración
            anteriores = actuales

        # El último valor de la lista "anteriores" es la distancia de Levenshtein entre las palabras
        return anteriores[-1]

    # Definimos una función para calcular el porcentaje de similitud entre dos palabras
    def porcentaje_similitud(palabra1, palabra2):
        # Calculamos la distancia de Levenshtein entre las palabras
        distancia = Traductor.distancia_levenshtein(palabra1, palabra2)
        
        # Calculamos la longitud máxima de las dos palabras
        longitud_maxima = max(len(palabra1), len(palabra2))
        
        # Calculamos el porcentaje de similitud restando la distancia de Levenshtein al 100%
        similitud = 100 - (distancia / longitud_maxima * 100)
        
        return similitud

    #Buscando la traducción de la palabra dada
    def buscarTrad(palabra, listEspa, listIng):
        flag = 0
        similitudEsp = []
        similitudIng = []
        list1 = listEspa
        list2 = listIng
        for indice in range(len(listEspa)): #En español e ingles tiene el mismo tamaño la lista
            porceEsp = Traductor.porcentaje_similitud(palabra, listEspa[indice])
            porceIng = Traductor.porcentaje_similitud(palabra, listIng[indice])
            if(palabra == listEspa[indice]):
                print("La traducción para "+palabra+" es: "+ listIng[indice])
                flag = 1
            if (palabra == listIng[indice]):
                print("La traducción para "+palabra+" es: "+ listEspa[indice])
                flag = 1
            similitudEsp.append(porceEsp)
            similitudIng.append(porceIng)    
        if (flag == 0):    
            print("\n\nERROR. No hay traducción para esta palabra")    
            Traductor.erroresLista(similitudEsp, similitudIng, list1, list2, palabra)

    #Manejo de errores (75% de concordancia)
    def erroresLista(similitudEsp, similitudIng, listEspa, listIng, palabra):
        #Comprobando palabras
        print("\nQuiza quiso decir: ")
        print("\n0 : NO ESTA EN LA LISTA")
        print("\n***ESPAÑOL***")
        for indice in range(len(listEspa)):
            if ((similitudEsp[indice] >= 75) and (similitudEsp[indice] <= 100)):
                print(f"{(indice+1)} : {listEspa[indice]}\n")
        print("\n***INGLES***")
        for indice in range(len(listIng)):
            if ((similitudIng[indice] >= 75) and (similitudIng[indice] <= 100)):
                print(f"{(indice+1)}: {listIng[indice]}\n")         
        opcion = input("\nIngrese una opción: ")
        opc = int(opcion)
        if(opc == 0):
            idioma = input("¿En qué idioma esta la palabra? 1=Esp 2=Ing : ")
            idioma = int(idioma)
            traduccion = input("¿Y se traduce como?: ")
            if(idioma == 1):
                Traductor.agregaP(palabra, traduccion)
            if(idioma == 2):
                Traductor.agregaP(traduccion, palabra)    
        else:
            idioma = input("¿En qué idioma esta la palabra de la lista? 1=Esp 2=Ing : ")    
            idioma = int(idioma)
            if(idioma == 1):
                print(f"La palabra {listEspa[opc-1]} se traduce como {listIng[opc-1]}")
            if(idioma == 2):
                print(f"La palabra {listIng[opc-1]} se traduce como {listEspa[opc-1]}")

"""
#Menu principal en consola
diccionario = Traductor.creandoArchivo()
def menu(diccionario):
    print("***********TRADUCTOR EN PYTHON (ES/EN)***********\n")
    ingreso = input("- Ingrese la palabra: ")
    palabra = ingreso.rstrip(" ")
    Traductor.leerDic(diccionario)
    #Obtener la lista en español y en inglés
    listEspa, listIng = Traductor.listasTabla(diccionario)
    #Comparar palabra con las listas (75% de concordancia)
    Traductor.buscarTrad(palabra, listEspa, listIng)

continuar = ""
while(True):
    menu(diccionario)
    opc = input("--¿Deseas ingresar otra palabra? Y/N: ")
    continuar = opc.lower()
    if(continuar != 'y'):
        break
print("BYE BYEEEEEEEE")    
"""
