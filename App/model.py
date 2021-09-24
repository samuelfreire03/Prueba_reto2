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
    catalog = {'books': None,'Medios': None}

    catalog['books'] = lt.newList('SINGLE_LINKED', compareBookIds)

    catalog['Medios'] = mp.newMap(1000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareAuthorsByName)

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
    authors = book['Medium'].split(",")  # Se obtienen los autores
    for author in authors:
        addBookAuthor(catalog, author.strip(), book)

def addBookAuthor(catalog, authorname, book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = catalog['Medios']
    existauthor = mp.contains(authors, authorname)
    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newAuthor(authorname)
        mp.put(authors, authorname, author)
    lt.addLast(author['obras'], book)

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
    tecnica['obras'] = lt.newList('SINGLE_LINKED', compareAuthorsByName)
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
# Funciones de ordenamiento

def sortantiguas(catalog,size):
    sub_list = lt.subList(catalog, 1, size)
    sub_list = sub_list.copy()
    orden = merge.sort(sub_list, compareantiguas)
    return orden