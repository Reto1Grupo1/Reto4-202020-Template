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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    citibike = {
                'graph': None
                }

    citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=True,
                                          size=14000,
                                          comparefunction=compareStopIds)
    return citibike

# Funciones para agregar informacion al grafo

def addTrip(citibike, trip):
    """
    """
    try:
        origin = trip['start station id']
        destination = trip['end station id']
        duration = int(trip['tripduration'])
        addStation(citibike, origin)
        addStation(citibike, destination)
        addConnection(citibike, origin, destination, duration)
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')


def addStation(citibike, stationid):
    """
    Adiciona un viaje como un vertice del grafo
    """
    try:
        if not gr.containsVertex(citibike['graph'], stationid):
            gr.insertVertex(citibike['graph'], stationid)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:addStation')

def updateAverageWeight(edge,weight):
    newweight=float(float(edge["weight"])*float(edge["count"])+ float(weight) / float(edge["count"]+1))
    edge["weight"]=newweight
    edge["count"]+=1

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike ["graph"], origin, destination)
    if edge is None:
        gr.addEdge(citibike["graph"], origin, destination, duration)
    else:
        updateAverageWeight(edge,destination)
    return citibike


# ==============================
# Funciones de consulta
# ==============================
def totalStops(citibike):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(citibike['graph'])


def totalConnections(citibike):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(citibike['graph'])


def requerimiento1(graph,station1,station2):
    sc=scc.KosarajuSCC(graph)
    MaxGraph=numSCC(graph)
    MaxStations=sameCC(sc,station1,station2)
    retorno=lt.newList("ARRAY_LIST",compareIds)
    lt.addLast(retorno,MaxGraph)
    lt.addLast(retorno,MaxStations)
    return retorno

def numSCC(graph):
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def sameCC(sc, station1, station2):
    return scc.stronglyConnected(sc, station1, station2)


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
