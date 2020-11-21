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
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
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
                'graph': None,
                "llegadas":None,
                "id":None,
                "req5":None
                }

    citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                          directed=True,
                                          size=300,
                                          comparefunction=compareStopIds)
    citibike["llegadas"] = m.newMap(numelements=300,maptype="PROBING",loadfactor=0.4,comparefunction=comparellegada)
    citibike["id"] = m.newMap(numelements=300,maptype="PROBING",loadfactor=0.4,comparefunction=comparellegada)
    citibike["req5"]=m.newMap(numelements=300,maptype="PROBING",loadfactor=0.4,comparefunction=comparellegada)
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
    weight=int(weight)
    newweight=(((int(edge["weight"]))*(int(edge["count"])) + (weight)) / (int(edge["count"]+1)))
    edge["weight"]=int(newweight)
    edge["count"]+=1

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike ["graph"], origin, destination)
    if edge is None:
        gr.addEdge(citibike["graph"], origin, destination, duration)
    else:
        updateAverageWeight(edge,duration)
    return citibike

###FUNCIONES AGREGAR INFO A MAPS
###MAP LLEGADAS
def addllegada(citibike, llegada):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    exist_llegada = m.contains( citibike['llegadas'],llegada)
    if exist_llegada:
        entry = m.get( citibike['llegadas'],llegada)
        entry= me.getValue(entry)
        entry["value"]+=1
    else:
        llegada1 = Newllegada(llegada)
        m.put( citibike['llegadas'], llegada, llegada1)


def Newllegada(name):
    llegada = {'element': "", "value":0}
    llegada['element'] = name
    llegada['value'] = 1
    return llegada

#MAP ID-NOMBRE
def addid(citibike, trip):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    exist_id_start = m.contains( citibike,trip["start station id"])
    if exist_id_start is False:
        m.put( citibike, trip["start station id"], trip["start station name"])
    exist_id_end = m.contains( citibike,trip["end station id"])
    if exist_id_end is False:
        m.put( citibike, trip["end station id"], trip["end station name"])
####MAP REQ5
def addreq5(citibike, trip):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    rangostart={"vs0-10":0,
            "vs11-20":0,
            "vs21-30":0,
            "vs31-40":0,
            "vs41-50":0,
            "vs51-60":0,
            "vs60+":0,
            "ve0-10":0,
            "ve11-20":0,
            "ve21-30":0,
            "ve31-40":0,
            "ve41-50":0,
            "ve51-60":0,
            "ve60+":0
            }
    edad= 2020-int(trip["birth year"])
    exist_id_start = m.contains( citibike,trip["start station id"])
    if exist_id_start:  
        if edad<11:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs0-10"]=me.getValue(entry)["vs0-10"]+1
        elif edad<21:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs11-20"]=me.getValue(entry)["vs11-20"]+1

        elif edad<31:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs21-30"]=me.getValue(entry)["vs21-30"]+1
        elif edad<41:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs31-40"]=me.getValue(entry)["vs31-40"]+1
        elif edad<51:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs41-50"]=me.getValue(entry)["vs41-50"]+1
        elif edad<61:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs51-60"]=me.getValue(entry)["vs51-60"]+1
        else:
            entry=m.get(citibike,trip["start station id"])
            me.getValue(entry)["vs60+"]=me.getValue(entry)["vs60+"]+1
    else:
        if edad<11:
            rangostart["vs0-10"]=rangostart["vs0-10"]+1
        elif edad<21:
            rangostart["vs11-20"]=rangostart["vs11-20"]+1
        elif edad<31:
            rangostart["vs21-30"]=rangostart["vs21-30"]+1
        elif edad<41:
            rangostart["vs31-40"]=rangostart["vs31-40"]+1
        elif edad<51:
            rangostart["vs41-50"]=rangostart["vs41-50"]+1
        elif edad<61:
            rangostart["vs51-60"]=rangostart["vs51-60"]+1
        else:
            rangostart["vs60+"]=rangostart["vs60+"]+1
            
        m.put( citibike, trip["start station id"], rangostart)


    rangoend={"vs0-10":0,
            "vs11-20":0,
            "vs21-30":0,
            "vs31-40":0,
            "vs41-50":0,
            "vs51-60":0,
            "vs60+":0,
            "ve0-10":0,
            "ve11-20":0,
            "ve21-30":0,
            "ve31-40":0,
            "ve41-50":0,
            "ve51-60":0,
            "ve60+":0
            }

    
    exist_id_end = m.contains( citibike,trip["end station id"])
    if exist_id_end:
        if edad<11:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve0-10"]=me.getValue(entry)["ve0-10"]+1
        elif edad<21:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve11-20"]=me.getValue(entry)["ve11-20"]+1

        elif edad<31:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve21-30"]=me.getValue(entry)["ve21-30"]+1
        elif edad<41:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve31-40"]=me.getValue(entry)["ve31-40"]+1
        elif edad<51:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve41-50"]=me.getValue(entry)["ve41-50"]+1
        elif edad<61:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve51-60"]=me.getValue(entry)["ve51-60"]+1
        else:
            entry=m.get(citibike,trip["end station id"])
            me.getValue(entry)["ve60+"]=me.getValue(entry)["ve60+"]+1
    
    else:
        if edad<11:
            rangoend["ve0-10"]=rangoend["ve0-10"]+1
        elif edad<21:
            rangoend["ve11-20"]=rangoend["ve11-20"]+1
        elif edad<31:
            rangoend["ve21-30"]=rangoend["ve21-30"]+1
        elif edad<41:

            rangoend["ve31-40"]=rangoend["ve31-40"]+1
        elif edad<51:
            rangoend["ve41-50"]=rangoend["ve41-50"]+1
        elif edad<61:
            rangoend["ve51-60"]=rangoend["ve51-60"]+1
        else:
            rangoend["ve60+"]=rangoend["ve60+"]+1
            
        m.put( citibike, trip["end station id"], rangoend)
 
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

def requerimiento3(graph,mapallegadas,mapaid):
    vertices= gr.vertices(graph)
    lista1=lt.newList('SINGLE_LINKED')
    for i in range(1,(lt.size(vertices)+1)):
        elements1={}
        element1 =lt.getElement(vertices,i)
        adyacentes= gr.adjacents(graph,element1)
        valuetotal1=0
        for j in range (1,(lt.size(adyacentes)+1)):
            adjacent1= lt.getElement(adyacentes,j)
            valuetotal1+=gr.getEdge(graph,element1,adjacent1)["count"]
        name=m.get(mapaid,element1)
        name=me.getValue(name)
        if valuetotal1!=0:
            elements1["element"]=name
            elements1["value"]=float(valuetotal1)
            lt.addLast(lista1,elements1)
    mg.mergesort(lista1,greater_station)
    lista1r=lt.newList('SINGLE_LINKED')
    
    for j in range(1,4):
        elemento=((lt.getElement(lista1,j)["element"])+" , salidas:"+str(lt.getElement(lista1,j)["value"]))
        lt.addLast(lista1r,elemento)

    
    lista2=lt.newList('SINGLE_LINKED')
    #print(mapallegadas)
    vert= m.keySet(mapallegadas)
    for i in range(1, (lt.size(vert)+1)):
        vertice=lt.getElement(vert,i)
        entry= m.get(mapallegadas,vertice)
        entry= me.getValue(entry)
        lt.addLast(lista2,entry)
    
    mg.mergesort(lista2,greater_station)
    lista2r=lt.newList('SINGLE_LINKED')
    for j in range(1,4):
        elemento=lt.getElement(lista2,j)["element"]+" , llegadas:"+str(lt.getElement(lista2,j)["value"])
        lt.addLast(lista2r,elemento)

    lista3=lt.newList('SINGLE_LINKED')
    for i in range(1,(lt.size(vertices)+1)):
        elements1={}
        element1 =lt.getElement(vertices,i)
        adyacentes= gr.adjacents(graph,element1)
        valuetotal1=0
        for j in range (1,(lt.size(adyacentes)+1)):
            adjacent1= lt.getElement(adyacentes,j)
            valuetotal1+=gr.getEdge(graph,element1,adjacent1)["count"]
        name=m.get(mapaid,element1)
        name=me.getValue(name)
        entry= m.get(mapallegadas,name)
        entry= me.getValue(entry)["value"]
        
        if valuetotal1!=0:
            elements1["element"]=name
            elements1["value"]=float(valuetotal1+int(entry))
            lt.addLast(lista3,elements1)

    mg.mergesort(lista3,less_station)
    
    lista3r=lt.newList('SINGLE_LINKED')
    for j in range(1,4):
        elemento=lt.getElement(lista3,j)["element"]+" , Salidas:"+str(lt.getElement(lista3,j)["value"])
        lt.addLast(lista3r,elemento)
    return lista1r,lista2r,lista3r
def requerimiento5(edad,req5,graph,mapid):
    verticeinicial=""
    verticefinal=""
    vertices=gr.vertices(graph)
    contador1=0
    idverticeinicial=0
    for i in range(lt.size(vertices)):
        
        vertice=lt.getElement(vertices,i)
        entry= m.get(req5,vertice)
       
        entry2=me.getValue(entry)
        
        if int(edad)<11:
            personas=entry2["vs0-10"]
        elif int(edad)<21:
            personas=entry2["vs11-20"]
        elif int(edad)<31:
            personas=entry2["vs21-30"]
        elif int(edad)<41:
            personas=entry2["vs31-40"]
        elif int(edad)<51:
            personas=entry2["vs41-50"]
        elif int(edad)<61:
            personas=entry2["vs51-60"]
        else:
            personas=entry2["vs60+"]
        if personas>contador1:
            contador1= personas
            idverticeinicial= me.getKey(entry)
    nombre=m.get(mapid,idverticeinicial)
    nombre=me.getValue(nombre)
    retorno1={}
    retorno1["Nombre estacion salida"]=nombre
    retorno1["Numero de personas en ese rango"]=contador1


    contador2=0
    idverticefinal=0
    for i in range(lt.size(vertices)):
        
        vertice=lt.getElement(vertices,i)
        entry= m.get(req5,vertice)
       
        entry2=me.getValue(entry)
        
        if int(edad)<11:
            personas=entry2["ve0-10"]
        elif int(edad)<21:
            personas=entry2["ve11-20"]
        elif int(edad)<31:
            personas=entry2["ve21-30"]
        elif int(edad)<41:
            personas=entry2["ve31-40"]
        elif int(edad)<51:
            personas=entry2["ve41-50"]
        elif int(edad)<61:
            personas=entry2["ve51-60"]
        else:
            personas=entry2["ve60+"]
        if personas>contador2:
            contador2= personas
            idverticefinal= me.getKey(entry)
    nombre2=m.get(mapid,idverticefinal)
    nombre2=me.getValue(nombre2)
    retorno2={}
    retorno2["Nombre estacion llegada: "]=nombre2
    retorno2["Numero de personas en ese rango: "]=contador2

    source=(djk.Dijkstra(graph,idverticeinicial))
    exist=djk.hasPathTo(source,idverticefinal)
    if exist:
        ruta=("El costo minimo de entre estos dos vertices es de: "+str(djk.distTo(source,idverticefinal)))
    else:
        ruta=(" no existe camino entre"+nombre+" y "+nombre2)
    return retorno1,retorno2,ruta







def requerimiento4(time,InitialS,citibike):
    time=int(time)*60
    rango=int(gr.outdegree(citibike["graph"],str(InitialS)))
    listD=gr.adjacentEdges(citibike["graph"],str(InitialS))
    Lista=lt.newList("ARRAY_LIST",compareIds)
    for i in range(1,int(rango+1)):
        Arco=lt.getElement(listD,i)
        MaxTime=int(Arco["weight"])
        if MaxTime <= time:
            lt.addLast(Lista,Arco)
    return Lista















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
    
def comparellegada(keyname,vertice):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    verticentry = me.getKey(vertice)
    if (keyname == verticentry):
        return 0
    elif (keyname > verticentry):
        return 1
    else:
        return -1
def greater_station(element1, element2):
    if (element1['value']) > (element2['value']):
        return True
    return False

def less_station(element1, element2):
    if (element1['value']) < (element2['value']):
        return True
    return False