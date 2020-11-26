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

import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    citibike= model.newAnalyzer()
    return citibike
# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(citibike):
    viajes=0
    for filename in os.listdir(cf.data_dir):
        
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            viajes+=loadFile(citibike, filename)
    print("viajes totales: "+str(viajes))
    return citibike
def loadTripsAge(citibike,IRango,FRango):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            loadFileAge(citibike, filename,IRango,FRango)
    return citibike
def loadFileAge(citibike, tripfile,IRango,FRango):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTripAge(citibike, trip,IRango,FRango)
        
def loadTripsDay(citibike,Dia,Id):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            loadFileDia(citibike,filename,Dia,Id)
    return citibike
def loadFileDia(citibike,tripfile,Dia,Id):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTripDia(citibike,trip,Dia,Id)

def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    viajes=0
    for trip in input_file:
        viajes+=1
        model.addTrip(citibike, trip)
        model.addllegada(citibike,trip["end station name"])
        model.addid(citibike["id"],trip)
        model.addreq5(citibike["req5"],trip)
        model.addcoordenadas(citibike["coordenadas"],trip)

    return viajes

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

def requerimiento1(catalog,station1,station2):
    return model.requerimiento1(catalog,station1,station2)

def requerimiento2(catalog,tiempo,idestacion):
    return model.requerimiento2(catalog,tiempo,idestacion)

def requerimiento3(graph,mapallegadas,mapaid):
    return model.requerimiento3(graph,mapallegadas,mapaid)

def requemiento4(tiempo,StationI,catalog):
    return model.requerimiento4(tiempo,StationI,catalog)

def requerimiento5(edad,req5,graph,mapid):
    return model.requerimiento5(edad,req5,graph,mapid)

def requerimiento6(paralati,paralongi,paralatf,paralongf,graph,maplongla,mapid):
    return model.requerimiento6(paralati,paralongi,paralatf,paralongf,graph,maplongla,mapid)

def requerimiento7(catalog):
    return model.requerimiento7(catalog)

def requerimiento8(catalog):
    return model.requerimiento8(catalog)