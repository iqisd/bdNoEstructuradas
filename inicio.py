import json
from pymongo import MongoClient
import os
cliente=MongoClient("mongodb://localhost:27017/")
db=cliente["instituto"]
coleccion=db["alumnos"]

def cargar_json():
    with open("alumnos.json","r", encoding="utf-8") as archivo:
        datos=json.load(archivo)
    coleccion.insert_many(datos)
    print("Datos cargados correctamente")
    input("Presione Enter para continuar...")

def mostrar_datos():
        os.system("cls")
        resultado=coleccion.find()
        for doc in resultado:
            print(f"Nombre: {doc['nombre']} Edad: {doc['edad']} Carrera: {doc['carrera']}")
        input("Presione Enter para continuar...")

def buscar_datos():
    os.system("cls")
    varbus=input("Ingrese la variable que desea buscar (nombre, edad, carrera): ")
    valor=input("Ingrese el valor que desea buscar: ")
    resultado=coleccion.find({varbus:valor})
    for doc in resultado:
        print(f"""Nombre: {doc['nombre']} 
Edad: {doc['edad']} 
Carrera: {doc['carrera']}""")
    input("Presione enter para continuar...")

def insertar_documento():
    os.system("cls")
    nombre=input("Ingrese el nombre del alumno: ")
    edad=input("Ingrese la edad del alumno: ")
    carrera=input("Ingrese la carrera del alumno: ")
    coleccion.insert_one({'nombre':nombre, 'edad':edad, 'carrera':carrera})
    print(f"Datos: {nombre}, {edad}, {carrera} ingresados con exito!")
    input("Presione Enter para continuar...")

def actualizar_documento():
    os.system("cls")
    varbus=input("Ingrese la variable que desea buscar (nombre, edad, carrera): ")
    valor=input("Ingrese el valor que desea buscar: ")
    nuevovalor=input("Ingrese el nuevo valor: ")
    coleccion.update_one({varbus:valor}, {"$set":{varbus:nuevovalor}})
    print(f"Valor actualizado correctamente: {varbus} = {nuevovalor}")
    input("Presione Enter para continuar...")

def eliminar_documento():
    os.system("cls")
    varbus=input("Ingrese la variable que desea buscar (nombre, edad, carrera): ")
    valor=input("Ingrese el valor que desea buscar: ")
    coleccion.delete_one({varbus:valor})
    print(f"Documento con {varbus} = {valor} eliminado correctamente")
    input("Presione Enter para continuar...")

while True:
    os.system("cls")
    print("1. Cargar JSON")
    print("2. Mostrar datos")
    print("3. Buscar datos")
    print("4. Insertar documento")
    print("5. Actualizar documento")
    print("6. Eliminar documento")
    print("7. Salir")
    opcion=input("Seleccione una opción: ")
    if opcion=="1":
        cargar_json()
    elif opcion=="2":   
        mostrar_datos()
    elif opcion=="3":
        buscar_datos()
    elif opcion=="4":  
        insertar_documento()
    elif opcion=="5":
        actualizar_documento()
    elif opcion=="6":
        eliminar_documento()
    elif opcion=="7":
        print("Saliendo del programa...")
        break