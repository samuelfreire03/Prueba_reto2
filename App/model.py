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
from datetime import date

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
    catalog = {'books': None,'Medios': None,'Artistas':None,'years':None,'Codigos_Artistas':None, 'AdquisicionFecha': None, 'Departamento': None}

    catalog['books'] = lt.newList('SINGLE_LINKED', compareBookIds)

    catalog['Artistas'] = mp.newMap(20000,
                                   maptype='PROBING',
                                   loadfactor=0.5, 
                                   comparefunction=compareAuthorsByName)

    catalog['Medios'] = mp.newMap(1000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareAuthorsByName)
    
    catalog['Departamento'] = mp.newMap(1000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareAuthorsByName)
                                
    catalog['years'] = mp.newMap(15000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapYear)
    
    catalog['Codigos_Artistas'] = mp.newMap(150000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareAuthorsByName)

    catalog['AdquisicionFecha'] = mp.newMap(150000,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapYear)
    catalog['Nombres_Artistas'] = mp.newMap(150000,
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
    
    artistas = book['ConstituentID'].replace("[","")
    artistas = artistas.replace("]","")
    artistas = artistas.split(",")

    for codigo in artistas:
        addBookAuthor(catalog, codigo.strip(), book)
    addDepartamento(catalog, book['Department'].strip(), book)
    addAdquisionFecha(catalog, book)

def addArtistas(catalog,book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    author = newartista(book['DisplayName'],book['ConstituentID'])
    mp.put(catalog['Artistas'], book['ConstituentID'], author)
    addBookYear(catalog, book)
    mp.put(catalog['Nombres_Artistas'], book['DisplayName'], book['ConstituentID'])

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

def addAdquisionFecha(catalog, book):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        years = catalog['AdquisicionFecha']
        if (book['DateAcquired'] != ''):
            pubyear = book['DateAcquired']
            pubyear = int((date.fromisoformat(pubyear)).strftime("%Y%m%d%H%M%S"))
        elif (book['DateAcquired'] == ''):
            pubyear = 0
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

def addDepartamento(catalog, authorname, book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = catalog['Departamento']
    existauthor = mp.contains(authors, authorname)
    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newdepartamento(authorname)
        mp.put(authors, authorname, author)
    lt.addLast(author['books'], book)

def newYear(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'year': "", "books": None}
    entry['year'] = pubyear
    entry['books'] = lt.newList('ARRAY_LIST', compareYears)
    return entry

def newdepartamento(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'Departamento': "", "books": None}
    entry['Departamento'] = pubyear
    entry['books'] = lt.newList('ARRAY_LIST', compareYears)
    return entry

def addBookAuthor(catalog, authorname, book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = catalog['Codigos_Artistas']
    existauthor = mp.contains(authors, authorname)
    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newAuthor(authorname)
        mp.put(authors, authorname, author)
    lt.addLast(author['obras'], book)

def addcodigoautor(catalog, authorname, book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = catalog['Artistas']
    author = newartista(authorname,book['ConstituentID'])
    mp.put(authors, authorname, author)

def addtecnica(catalog, authorname, book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """

    existauthor = mp.contains(catalog, authorname)
    if existauthor:
        entry = mp.get(catalog, authorname)
        author = me.getValue(entry)
    else:
        author = newTecnica_lista(authorname)
        mp.put(catalog, authorname, author)
    lt.addLast(author['obras'], book)

# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    artista = {'codigo': "",
              "obras": None,}
    artista['codigo'] = name
    artista['obras'] = lt.newList('ARRAY_LIST', compareAuthorsByName)
    return artista

def newartista(name,codigo):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    artista = {'Nombre': "",
              "Codigo": ''}
    artista['Nombre'] = name
    artista['Codigo'] = codigo
    return artista

def newTecnica(nombre_tecnica):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    tecnica = {'Tecnica': "", "Cantidad": 0}
    tecnica['Tecnica'] = nombre_tecnica
    tecnica['Cantidad'] = None
    return tecnica

def newTecnica_lista(nombre_tecnica):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    tecnica = {'Tecnica': "", "Cantidad": 0}
    tecnica['Tecnica'] = nombre_tecnica
    tecnica['obras'] = lt.newList('ARRAY_LIST')

def newCosto(codigo_obra,costo,peso,titulo,artistas,clasificacion,fecha,dimensiones,tecnica):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    artista = {'codigo': "", "costo": None, "peso": None}
    artista['codigo'] = codigo_obra
    artista['costo'] = costo
    artista['peso'] = peso
    artista['titulo'] = titulo
    artista['artistas'] = artistas
    artista['clasificacion'] = clasificacion
    artista['fecha'] = fecha
    artista['dimensiones'] = dimensiones
    artista['tecnica'] = tecnica
    return artista
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

def cantidad_tecnicas(artistas):

    cantidad_de_tecnicas_veces = lt.newList('ARRAY_LIST',cmpfunction=comparetecnicas)
    tecnicas_final = lt.newList('ARRAY_LIST')
    for partes in lt.iterator(artistas['obras']):
        lt.addLast(tecnicas_final,partes['Medium'])

    for i in lt.iterator(tecnicas_final):
        posauthor = lt.isPresent(cantidad_de_tecnicas_veces, i)
        if posauthor > 0:
            artista = lt.getElement(cantidad_de_tecnicas_veces, posauthor)
            artista['Cantidad'] += 1
        else:
            artista = newTecnica(i)
            artista['Cantidad'] = 1
            lt.addLast(cantidad_de_tecnicas_veces, artista)
        
    k = 0
    for p in lt.iterator(cantidad_de_tecnicas_veces):
        if int(p['Cantidad']) > k:
            k = p['Cantidad']
            maximo = p['Tecnica']
    
    return maximo,cantidad_de_tecnicas_veces,lt.size(cantidad_de_tecnicas_veces)

def calculo_de_transporte(catalog):

    obras = lt.newList('ARRAY_LIST')
    for obra in lt.iterator(catalog):

        peso = obra['Weight (kg)'] 
        altura = obra['Height (cm)'] 
        ancho = obra['Width (cm)'] 
        profundidad = obra['Depth (cm)']
        longitud = obra['Length (cm)']
        diametro = obra['Diameter (cm)']

        if (altura == 0 or altura == '') and (ancho == 0 or ancho == ''):
            costo = 48.00

        elif (longitud != 0 and longitud != '') and (ancho != 0 and ancho != '') and (altura == 0 or altura == ''):
            costo = (float(longitud)*float(ancho)*72)/10000 

        elif (altura != 0 and altura != '') and (ancho != 0 and ancho != ''):
            costo = (float(altura)*float(ancho)*72)/10000
            if (profundidad != 0 and profundidad != ''):
                costo = max((float(altura)*float(ancho)*72)/10000,(float(altura)*float(ancho)*72*float(profundidad))/1000000)
            if (peso != 0 and peso != '') and (profundidad != 0 and profundidad != ''):
                costo = max((float(peso) * 72),(float(altura)*float(ancho)*72)/10000,(float(altura)*float(ancho)*72*float(profundidad))/1000000)
            elif (peso != 0 and peso != '') and (profundidad == 0 or profundidad == ''):
                costo = max((float(peso) * 72),(float(altura)*float(ancho)*72)/10000)
        elif (peso != 0 and peso != ''):
            costo1 = (float(peso) * 72)
            costo = max(costo1,costo)

        if (diametro != 0 and diametro != '') and (altura != 0 and altura != ''):
            costo = (((float(diametro)/2)**2)*float(altura)*72*3.14)/1000000
        elif (diametro != 0 and diametro != '') and (altura == 0 and altura == ''):
            costo = (((float(diametro)/2)**2)*72*3.14)/10000 
            
        if (peso == 0 or peso == ''):
            pesar = 0
        else: 
            pesar = peso 
        precio = newCosto(obra['ObjectID'],costo,pesar,obra['Title'],obra['ConstituentID'],obra['Classification'],obra['Date'],obra['Dimensions'],obra['Medium'])

        if precio['costo'] == 0:
            precio['costo'] = 48.00
        lt.addLast(obras,precio)
    return obras

def suma_costo(catalog):

    suma = 0
    for p in lt.iterator(catalog):
        suma += p['costo']

    return float(suma)

def suma_peso(catalog):

    suma = 0
    for p in lt.iterator(catalog):
        suma += float(p['peso'])

    return float(suma)

def obtener_antiguas(catalog):
    """
    Retorna los tres ultimos artistas cargados
    """
    ordenadas = sortantiguasobras(catalog)
    con_fecha = lt.newList()
    orden = lt.newList()
    for obra in lt.iterator(ordenadas):
        if obra['fecha'] != '':
            lt.addLast(con_fecha, obra)
    orden = lt.subList(con_fecha,1,5)
    return orden

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

def compareantiguasobras(artista1, artista2):
    return ((artista1['fecha']) < (artista2['fecha']))

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

def comparetecnicas(tecnica1, tecnica):
    if (tecnica1.lower().strip() == tecnica['Tecnica'].lower().strip()):
        return 0
    return -1

def comparecanitdad(artista1, artista2):
    return (float(artista1['Cantidad']) > float(artista2['Cantidad']))

def comparacostos(artista1, artista2):
    return (float(artista1['costo']) > float(artista2['costo']))

def sortantiguasobras(catalog):
    orden = merge.sort(catalog, compareantiguasobras)
    return orden
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

def cmpArtworkByDateAcquired(artwork1, artwork2):

    if artwork1['DateAcquired'] == '':

        fecha1 = 0
    else: 
        fecha1 = int((date.fromisoformat(artwork1['DateAcquired'])).strftime("%Y%m%d%H%M%S"))

    if artwork2['DateAcquired'] == '':

        fecha2 = 0

    else:
        fecha2 = int((date.fromisoformat(artwork2['DateAcquired'])).strftime("%Y%m%d%H%M%S"))

    return fecha1 < fecha2

def sortCantidades(catalog):
    orden = merge.sort(catalog, comparecanitdad)
    return orden

def sortobras(catalog):

    sorted_list = merge.sort(catalog, cmpArtworkByDateAcquired)
    return sorted_list

def sortcostos(catalog):
    orden = merge.sort(catalog, comparacostos)
    return orden

#completas requerimientos

def primer_req(catalogo,año1,año2):
    nueva = lt.newList('ARRAY_LIST')
    años = mp.keySet(catalogo['years'])
    for c in lt.iterator(años):
        if int(c) >= int(año1) and int(c) <= int(año2):
            valor = mp.get(catalogo['years'],c)
            for i in lt.iterator(me.getValue(valor)['books']):
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

def tercer_req(catalog,Artista):

    valores = mp.get(catalog['Nombres_Artistas'],Artista)
    valores_especificos = mp.get(catalog['Codigos_Artistas'],me.getValue(valores))
    tecnicas = cantidad_tecnicas(me.getValue(valores_especificos))
    tecnicas_orden = sortCantidades(tecnicas[1])
    obras = lt.newList('ARRAY_LIST')
    for obra in lt.iterator(me.getValue(valores_especificos)['obras']):
        if obra['Medium'] == tecnicas[0]:
            lt.addLast(obras,obra)

    if lt.size(tecnicas_orden) <= 10:
        tecnicas_orden = tecnicas_orden
    elif lt.size(tecnicas_orden) > 10:
        primeros = lt.subList(tecnicas_orden, 1, 10)
        tecnicas_orden = primeros

    if lt.size(obras) <= 10:
        obras = obras
    elif lt.size(obras) > 10:
        primeros = lt.subList(obras, 1, 10)
        obras = primeros
    return obras,tecnicas_orden,lt.size(me.getValue(valores_especificos)['obras']),tecnicas[2],tecnicas[0]

def segundo_req(catalog,fecha_inicial,fecha_final):
    fecha1 = int((date.fromisoformat(fecha_inicial.replace('/','-'))).strftime("%Y%m%d%H%M%S"))
    fecha2 = int((date.fromisoformat(fecha_final.replace('/','-'))).strftime("%Y%m%d%H%M%S"))
    llaves = (mp.keySet(catalog['AdquisicionFecha']))
    nueva = lt.newList('ARRAY_LIST')
    for c in lt.iterator(llaves):
        if c >= fecha1 and c <= fecha2:
            valor = mp.get(catalog['AdquisicionFecha'],c)
            lista = me.getValue(valor)['books']
            for j in lt.iterator(lista):
                lt.addLast(nueva,j)
    orden = sortobras(nueva)
    if lt.size(orden) == 0:
        primeros = ''
        ultimos = ''
    elif lt.size(orden) < 6:
        primeros = orden
        ultimos = orden
    elif lt.size(orden) >= 6:
        primeros = lt.subList(orden, 1, 3)
        ultimos = lt.subList(orden, int(lt.size(orden)-2), 3)
    conteo = 0
    for k in lt.iterator(orden):
        if 'purchase' in k['CreditLine'].lower():
            conteo += 1
    return primeros,ultimos,lt.size(orden),conteo

def quinto_req(catalog,departamento):
    total_departamento = mp.get(catalog['Departamento'],departamento)
    obras_artista = me.getValue(total_departamento)['books']
    obras = calculo_de_transporte(obras_artista)
    costo = suma_costo(obras)
    peso = suma_peso(obras)
    ordenadas_costo = sortcostos(obras)
    primerascostosas = lt.subList(ordenadas_costo,1,5)
    orden_antiguas = sortantiguasobras(obras)
    ultimas_antiguas = obtener_antiguas(orden_antiguas)
    return primerascostosas,ultimas_antiguas,costo,peso,lt.size(obras)