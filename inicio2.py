from pymongo import MongoClient
cliente=MongoClient("mongodb://localhost:27017/")
db=cliente["Ejemplos"]
c_alumnos=db["alumnos"]
c_ramos=db["ramos"]

def ingreso():
    nombre=input("Ingrese el nombre del alumno: ")
    edad=int(input("Ingrese la edad del alumno: "))
    carrera=input("Ingrese la carrera del alumno: ")
    correo=input("Ingrese el correo del alumno: ")
    documento={"nombre":nombre, "edad":edad, "carrera":carrera, "correo":correo}

    c_alumnos.insert_one(documento)

ingreso()

def mostrar():
    salida = c_alumnos.find({}, {"nombre": 1, "_id": 0})
    for linea in salida:
        print(linea["nombre"])

while True:
    print("1 ingresar alumno")
    print("2 mostrar alumnos")
    opcion=int(input("Ingrese una opcion: "))
    if opcion == 1:    ingreso()
    elif opcion == 2:    mostrar()
    elif opcion == 0:    break
    else:    print("Opción no válida")