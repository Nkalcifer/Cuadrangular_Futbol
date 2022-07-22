import pymongo
from pymongo import MongoClient
# Ejecutar pip install pymongo
cluster = MongoClient("mongodb+srv://neider:1234@neiderpuentes.kxb2kxz.mongodb.net/?retryWrites=true&w=majority")
db = cluster.ejercicio
collection = db.equipos

post ={"_id": 3, "equipo": "d", "puntos": 0}
collection.insert_one(post)