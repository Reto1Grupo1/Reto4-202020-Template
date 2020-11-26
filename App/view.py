"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import datetime
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import timeit
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Cantidad de clusters de Viajes ")
    print("4- Ruta turística Circular ")
    print("5- Estaciones críticas ")
    print("6- Ruta turística por resistencia ")
    print("7- Recomendador de Rutas  ")
    print("8- Ruta de interés turístico   ")
    print("9- Buscador de estaciones adyacentes ")  
    print("10-  Identificación de Bicicletas para Mantenimiento ")  


    print("0- Salir")
    print("*******************************************")

"-------------------------------------------------------------"
def optionTwo():
    print("\nCargando información de transporte de bicicleta ....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    elif int(inputs[0]) == 3:
        station1=str(input("Estacion 1: "))
        station2=str(input("Estacion 2: "))
        lo=controller.requerimiento1(cont["graph"],station1,station2)
        print("El total de componentes fuertemente conectados es: ")
        print(lt.firstElement(lo))
        print("Existe la conexion:")
        print(lt.lastElement(lo))

    elif int(inputs[0]) == 4:
        try:
            tiempo=int(input("Digite el tiempo disponible: "))
            idestacion=input("Digite la id de la estacion: ")
            retorno=controller.requerimiento2(cont,tiempo,idestacion)
            if retorno != False:
                print("-----------")
                print("Las rutas circulares que se cumplen dentro del rango de tiempo son: ")
                for i in range(1,lt.size(retorno)+1):
                    ciclo=lt.getElement(retorno,i)
                    for j in range(1,lt.size(ciclo)+1):
                        print(lt.getElement(ciclo,j))
                    print("------------")
            else:
                print("No hay ruta circular para volver a la estacion")
        except:
            print("Ocurrio un error ejecutando el programa")


    elif int(inputs[0]) == 5:
        try:
            lista1,lista2,lista3=controller.requerimiento3(cont["graph"],cont["llegadas"],cont["id"])
            print("Estaciones de salida:")
            for j in range(1,4):
                print((lt.getElement(lista1,j)))
            print("---------------------------------------------")
            print("Estaciones de Llegada:")
            for j in range(1,4):
                print(lt.getElement(lista2,j))
            print("---------------------------------------------")
            print("Estaciones menos usadas")
            for j in range(1,4):
                print(lt.getElement(lista3,j))
        except :
            print("Ha habido un erro intente de nuevo.")
    elif int(inputs[0]) == 6:
            station1=str(input("Estacion Inicial : "))
            Tiempo=int(input("Tiempo estimado en minutos:"))
            tr=controller.requemiento4(Tiempo,station1,cont)
            size=int(lt.size(tr))
            for i in range(0,size+1):
                info=lt.getElement(tr,i)
                peso=str(datetime.timedelta(seconds=int(info["weight"])))
                print("Estacion Inicial "+str(station1)+" Estacion Final "+str(info["vertexB"]) + " Duracion Estimada "+str(peso[2:7]))
    elif int(inputs[0]) == 7:
        try:
            edad=input("Dígite su edad:")

            retorno1,retorno2,ruta=controller.requerimiento5(edad,cont["req5"],cont["graph"],cont["id"])
            print("Salida:")
            print(retorno1)
            print("-----------------------------------")
            print("llegada:")
            print(retorno2)
            print("---------------------------------------------------")
            print("Ruta")
            print(ruta+" segundos")
        except:
            print("Ha habido un error intente de nuevo.")
    elif int(inputs[0]) == 8:
        try:
            latini=input(" Digite la latitud en la que se encuentra:")
            longini=input(" Digite la longitud en la que se encuentra:")
            latifin=input(" Digite la latitud en del sitio de su interés:")
            longfin=input(" Digite la longitud en del sitio de su interés:")
            retorno=controller.requerimiento6(latini,longini,latifin,longfin,cont["graph"],cont["coordenadas"],cont["id"])
            if type(retorno) is str:
                print (retorno)
            else:
                print("Estación más cercana a su ubicación "+retorno["estacioninicial"])
                print("Estación más cercana a su sitio de interés "+retorno["estacionfinal"])
                print("-------------------------------------------------------")
                print ("El tiempo estimado es: "+str(retorno["tiempo"])+" segundos.")
                print("-------------------------------------------------------")
                print("La ruta que debe seguir es:")
                (retorno["ruta"])
                for i in range(1,lt.size(retorno["ruta"])+1):
                    a=lt.getElement(retorno["ruta"],i)["vertexA"]
                    a=m.get(cont["id"],a)
                    a=me.getValue(a)
                    b=lt.getElement(retorno["ruta"],i)["vertexB"]
                    b=m.get(cont["id"],b)
                    b=me.getValue(b)
                    print(a+"   ->  "+b)
        except:
            print("Ha habido un error intente de nuevo.")

    elif int(inputs[0]) ==9 :
        print("Rango de edad :  ")
        IRango=input("Inicio Rango: ")
        FRango=input("Final Rango: ")
        controller.loadTripsAge(cont,IRango,FRango)
        A=controller.requerimiento7(cont)
        print("Las estaciones adyacentes que más utilizan las personas de este rango de edad son ")
        for k in range(1,lt.size(A)+1):
            print(str(lt.getElement(A,int(k))["vertexA"])+" hacia "+str(lt.getElement(A,int(k))["vertexB"]))
            print("Total de viajes: "+str(lt.getElement(A,int(k))["count"]))

    elif int(inputs) == 10:
        Dia=input("Digite el dia a investigar (AAAA-MM-DD): ")
        Id=input("Digite la id de la biccleta: ")
        controller.loadTripsDay(cont,Dia,Id)
        retorno=controller.requerimiento8(cont)
        print("--------------")
        print("Los segundos totales que se uso la bicicleta fueron: "+str(lt.getElement(retorno,1)))
        print("--------------")
        print("Los segundos totales que la bicicleta estuvo parqueada fueron: "+str(lt.getElement(retorno,2)))
        print("--------------")
        print("Las estaciones por las que paso la bicicleta fueron: ")
        vertices=lt.getElement(retorno,3)
        for i in range(1,lt.size(vertices)+1):
            elemento=lt.getElement(vertices,i)
            print(elemento)
    else:
        sys.exit(0)
sys.exit(0)