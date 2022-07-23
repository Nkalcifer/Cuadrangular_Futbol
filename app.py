from itertools import combinations
from numpy import equal, intp
import pymongo
from pymongo import MongoClient
from tabulate import tabulate

cluster = MongoClient("mongodb+srv://neider:1234@neiderpuentes.kxb2kxz.mongodb.net/?retryWrites=true&w=majority")
db = cluster.ejercicio
collection = db.equipos
collectionEnfrentamientos= db.enfrentamientos
estadoJuego=0

def lista_equipos():
    try:
        result = collection.find({})
    except Exception as ex:
        result= str("Error"+ex)
    return result 

def lista_enfrentamientos():
    try:
        result = list(collectionEnfrentamientos.find({}))
    except Exception as ex:
        result= str("Error"+ex)
    return result 

def enfrentamiento(id):
    try:
        result =collectionEnfrentamientos.find({"_id":int(id)})
    except Exception as ex:
        return "Error"
    return result

def buscar_equipo(id):
    try:
        result =collection.find({"_id":int(id)})
    except Exception as ex:
        return "Error"
    return result

def modificar_equipo(id, equipo):
    try:
        result = collection.update_one({"_id":int(id)}, {"$set":{"equipo":equipo}})
    except Exception as ex:
        return "Error"
    return "Equipo Modificado"

def cambiar_puntaje(id, puntos):
    try:
        puntaje=buscar_equipo(id)
        for i in puntaje:
            puntaje=i['puntos']
        puntaje=int(puntaje)+int(puntos)
        result = collection.update_one({"_id":int(id)}, {"$set":{"puntos":puntaje}})
    except Exception as ex:
        return "Error"
    return "Puntaje Modificado"

def agregar_equipo(id, equipo):
    try:
        post={"_id":int(id), "equipo": equipo, "puntos": 0}
        result = collection.insert_one(post)
    except Exception as ex:
        return "Error"
    return "Equipo Guardado"

def eliminar_equipo(id):
    try:
        result = collection.delete_one({"_id":int(id)})
    except Exception as ex:
        return "Error Eliminando Equipo"
    return "Equipo Elimnado"

def reiniciar_juego():
    collectionEnfrentamientos.delete_many({})
    collection.update_many({}, {"$set":{"puntos":0}})

def iniciar_juego():
    if collectionEnfrentamientos.count_documents!=0:
        collectionEnfrentamientos.delete_many({})
        collection.update_many({}, {"$set":{"puntos":0}})
    equipos = list(lista_equipos())
    cont=0
    lista=[]
    for i in equipos:
        lista.insert(cont, str(equipos[cont]["_id"]))
        cont=cont+1
    juegos=list(combinations(lista, 2))
    cont=0
    for i in juegos:
        partido ={"_id":cont,"_idE1": i[0], "_idE2": i[1], "golesE1":0, "golesE2":0, "ganador":0}
        collectionEnfrentamientos.insert_one(partido)
        cont=cont+1

def Eliminar_todo():
    try:
        print("Eliminando...")
        collection.delete_many({})
        collectionEnfrentamientos.delete_many({})
    except Exception as ex:
        return "Error"
    return "Base de Datos Vaciada"

def agregar_marcador(id, golE1, golE2):
    try:
        partido=enfrentamiento(id)
        E1=int(golE1)
        E2=int(golE2)
        for i in partido:
            idE1=int(i['_idE1'])
            idE2=int(i['_idE2'])
        if E1>E2:
            result= collectionEnfrentamientos.update_one({"_id":int(id)},{"$set":{"golesE1":E1, "golesE2":E2, "ganador":idE1}})
            result2= cambiar_puntaje(idE1, 3)
        elif E1==E2:
            result= collectionEnfrentamientos.update_one({"_id":int(id)},{"$set":{"golesE1":E1, "golesE2":E2, "ganador":"Empate"}})
            result2= cambiar_puntaje(idE1, 1)
            result2= cambiar_puntaje(idE2, 1)
        else:
            result= collectionEnfrentamientos.update_one({"_id":int(id)},{"$set":{"golesE1":E1, "golesE2":E2, "ganador":idE2}})
            result2= cambiar_puntaje(idE2, 3)
    except Exception as ex:
        return "Error"
    return "Ok"
# Menu App
while True:
    print(f"""*** CUADRANGULARES  ****
            1. Ver Equipos
            2. Registrar Equipo
            3. Iniciar Juegos
            4. Modificar Equipo
            5. Eliminar Equipo
            6. Ver tabla de Enfrentamientos
            7. Registrar Marcador Enfrentamiento
            8. Vacias Todas Las Tablas
            * Para Terminar App""")
    opcion = input("Que desea Hacer: ")
    if opcion == '1':
        print("Equipos")
        equipos=list(lista_equipos().sort('puntos'))
        print(tabulate(equipos, headers="keys"))
    elif opcion == '2':
        id=input("Ingrese el Id del Equipo: ")
        nombre= input("Ingrese el nombre del equipo: ")
        result=agregar_equipo(id, nombre)
        print(result)
    elif opcion == '3':
        print(estadoJuego)
        if estadoJuego==1:
            print("El juego ya ha sido Iniciado")
        else:
            print("El juego iniciara con los Equipos que han sido registrados : ")
            equipos=lista_equipos()
            print("Equipos en Juego")
            for row in equipos:
                print(row["equipo"])
            iniciar_juego()
            print("juego Iniciado")
            estadoJuego=1
    elif opcion == '4':
        id=input("Ingrese el id del Equipo que desea Modificar: ")
        print(list(buscar_equipo(id)))
        equipo=input("Ingrese el nuevo nombre del equipo: ")
        print(modificar_equipo(id, equipo))
    elif opcion == '5':
        id = input("Ingrese el id del equipo que desea eliminar: ")
        result= eliminar_equipo(id)
        print(result)
    elif opcion== '6':
        partidos=lista_enfrentamientos()
        print(tabulate(partidos, headers="keys"))
    elif opcion== '7':
        idPartido=input("Ingrese el partido al cual digitar el marcador: ")
        print(list(enfrentamiento(idPartido)))
        golE1=input("Goles Equipo 1: ")
        golE2=input("Goles Equipo 2: ")
        agregar_marcador(idPartido, golE1, golE2)
    elif opcion== '8':
        confirmacion=input("Digite S para borrar Todo o R para reiniciar el cuadrangular")
        if confirmacion=='S':
            Eliminar_todo()
            estadoJuego=0
            print("Base de Datos Vaciada")
        elif confirmacion=='R':
            reiniciar_juego()
            estadoJuego=0
            print("Juego Reiniciado")
    elif opcion== '*':
        break