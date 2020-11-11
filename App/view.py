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
import timeit
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
    print("9- Identificación de Estaciones para Publicidad ")  
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

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    elif int(inputs[0]) == 3:
        station1=input("Estacion 1: ")
        station2=input("Estacion 2: ")
        lo=controller.requerimiento1(cont["graph"],station1,station2)
        print("El total de componentes fuertemente conectados es ")
        print(lt.firstElement(lo))
        print("Existe la conexion")
        print(lt.lastElement(lo))

    elif int(inputs[0]) == 4:
        x

    elif int(inputs[0]) == 5:
        x

    elif int(inputs[0]) == 6:
        x

    elif int(inputs[0]) == 7:
        x
    elif int(inputs[0]) == 8:
        x
    elif int(inputs[0]) == 9:
        x
    elif int(inputs[0]) == 10:
       x
    else:
        sys.exit(0)
sys.exit(0)