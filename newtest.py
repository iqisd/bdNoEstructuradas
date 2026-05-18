import pymongo
from pymongo import MongoClient
import os
cliente=MongoClient("mongodb://localhost:27017")
db=cliente["ejemplos"]
col=db["alumnos"]

def insertar():
    col.insert_one({"nombre":"Fran","edad":18})

