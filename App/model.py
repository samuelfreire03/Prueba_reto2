"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'books': None,'Medios': None,'Artistas':None,'years':None}

    catalog['books'] = lt.newList('SINGLE_LINKED', compareBookIds)

    catalog['Artistas'] = lt.newList('SINGLE_LINKED', compareBookIds)

    catalog['Medios'] = mp.newMap(1000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareAuthorsByName)
                                
    catalog['years'] = mp.newMap(15000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapYear)

    return catalog

# Funciones para agregar informacion al catalogo

def addBook(catalog, book):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de autores, una referencia
    al libro.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    lt.addLast(catalog['books'], book)

def addBookAuthor(catalog,book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    lt.addLast(catalog['Artistas'], book)
    addBookYear(catalog, book)

def addBookYear(catalog, book):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        years = catalog['years']
        if (book['BeginDate'] != ''):
            pubyear = book['BeginDate']
            pubyear = int(float(pubyear))
        else:
            pubyear = 2020
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['books'], book)
    except Exception:
        return None

def newYear(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'year': "", "books": None}
    entry['year'] = pubyear
    entry['books'] = lt.newList('ARRAY_LIST', compareYears)
    return entry

# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    tecnica = {'Tecnica': "",
              "obras": None,}
    tecnica['Tecnica'] = name
    tecnica['obras'] = lt.newList('ARRAY_LIST', compareAuthorsByName)
    return tecnica

# Funciones de consulta

def getBooksByAuthor(catalog, authorname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    author = mp.get(catalog['Medios'], authorname)
    if author:
        return me.getValue(author)
    return None

def getBooksByYear(catalog, year):
    """
    Retorna los libros publicados en un año
    """
    year = mp.get(catalog['years'], year)
    if year:
        return me.getValue(year)['books']
    return None

# Funciones utilizadas para comparar elementos dentro de una lista

def compareAuthorsByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareBookIds(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareantiguas(artista1, artista2):
    return ((artista1['Date']) < (artista2['Date']))

def compareMapYear(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0

def comparenacidos(artista1, artista2):
    return ((artista1['BeginDate']) < (artista2['BeginDate']))
# Funciones de ordenamiento

def sortantiguas(catalog,size):
    sub_list = lt.subList(catalog, 1, size)
    sub_list = sub_list.copy()
    orden = merge.sort(sub_list, compareantiguas)
    return orden

def sortnacidos(catalog):
    orden = merge.sort(catalog, comparenacidos)
    return orden

def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

#completas requerimientos

def primer_req(catalogo,año1,año2):
    llaves = mp.keySet(catalogo['years'])
    nueva = lt.newList('ARRAY_LIST')
    for c in lt.iterator(llaves):
            if int(c) >= int(año1) and int(c) <= int(año2):
                valor = mp.get(catalogo['years'],c)
                for i in lt.iterator(valor['value']['books']):
                    lt.addLast(nueva,i)
    orden = sortnacidos(nueva)
    medida = str(lt.size(orden))
    if lt.size(orden) == 0:
        primeros = ''
        ultimos = ''
    elif lt.size(orden) < 6:
        primeros = orden
        ultimos = orden
    elif lt.size(orden) >= 6:
        primeros = lt.subList(orden, 1, 3)
        ultimos = lt.subList(orden, int(lt.size(orden)-2), 3)
    return primeros,ultimos,orden,medida