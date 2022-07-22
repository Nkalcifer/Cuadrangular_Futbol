from itertools import combinations
from numpy import equal
import pymongo
from pymongo import MongoClient
from tabulate import tabulate
# Ejecutar pip install pymongo
# Ejecutar pip install tabulate
cluster = MongoClient("mongodb+srv://neider:1234@neiderpuentes.kxb2kxz.mongodb.net/?retryWrites=true&w=majority")
db = cluster.ejercicio
collection = db.equipos
collectionEnfrentamientos= db.enfrentamientos
# Lista de Equipos
post ={"_id": 0, "equipo": "a", "puntos": 0}
# post1 ={"_id": 1, "equipo": "b", "puntos": 0}
# post2 ={"_id": 2, "equipo": "c", "puntos": 0}
# post3 ={"_id": 3, "equipo": "d", "puntos": 0}
# collection.insert_one(post) #Insersion Simple
# collection.insert_many([post, post1, post2, post3]) #Insersion Multiple
# Consulta datos ordenada
# results = list(collection.find({"puntos":0}).sort("_id"))
# print(tabulate(results))
# for result in results:
#     print(result["_id"])
# Eliminado de registros
# results = collection.delete_one({"_id":0})

# Update de Registros
# results = collection.update_one({"_id":0}, {"$set":{"equipo":"a"}})

# post_count = collection.count_documents({})
# print(post_count)

# Funciones
def lista_equipos():
    try:
        result =list(collection.find({}))
    except Exception as ex:
        return "Error"
    return result 

def buscar_equipo(id):
    try:
        result =list(collection.find({"_id":id}))
    except Exception as ex:
        return "Error"
    return result 

def modificar_equipo(id, equipo, puntos):
    try:
        result = collection.update_one({"_id":id}, {"$set":{"equipo":equipo}})
    except Exception as ex:
        return "Error"
    return "Equipo Modificado"

def cambiar_puntaje(id, puntos):
    try:
        puntaje=buscar_equipo(id)["puntos"]
        puntaje=puntaje+puntos
        result = collection.update_one({"_id":id}, {"$set":{"puntos":puntaje}})
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
        result = collection.delete_one({"_id":id})
    except Exception as ex:
        return "Error Eliminando Equipo"
    return "Equipo Elimnado"

def iniciar_juego():
    if collectionEnfrentamientos.count_documents!=0:
        collectionEnfrentamientos.delete_many({})
    equipos = lista_equipos()
    cont=0
    lista=[]
    for i in equipos:
        lista.insert(cont, str(equipos[cont]["_id"]))
        cont=cont+1
    juegos=list(combinations(lista, 2))
    cont=0
    for i in juegos:
        print(i)
        print(i[0]+" "+i[1])
        partido ={"_id":cont,"_idE1": i[0], "_idE2": i[1]}
        collectionEnfrentamientos.insert_one(partido)
        cont=cont+1
    print("Juego Iniciado")

# Menu App
while True:
    print(type(post))
    print(f"""*** CUADRANGULARES  ****
            1. Ver Equipos
            2. Registrar Equipo
            3. Iniciar Juegos
            4. Modifcar Equipo
            5. Eliminar Equipo
            5. Ver tabla de Enfrentamientos
            6. Registrar Marcador Enfrentamiento
            """)
    opcion = input("Que desea Hacer: ")
    if opcion == '1':
        print("Equipos")
        equipos=lista_equipos()
        print(tabulate(equipos, headers="keys"))
    elif opcion == '2':
        id=input("Ingrese el Id del Equipo: ")
        nombre= input("Ingrese el nombre del equipo: ")
        result=agregar_equipo(id, nombre)
        print(result)
    elif opcion == '3':
        print("El juego iniciara con los Equipos que han sido registrados : ")
        equipos=lista_equipos()
        print("Equipos en Juego")
        for row in equipos:
            print(row["equipo"])
        iniciar_juego()
    elif opcion == '4':
        print("proceso")
    elif opcion == '5':
        id = input("Ingrese el id del equipo que desea eliminar: ")
        result= eliminar_equipo(id)
        print(result)
    elif opcion== '*':
        break