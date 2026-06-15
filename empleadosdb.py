from pymongo import MongoClient
import os

conex=MongoClient("mongodb://localhost:27017")
db=conex["empresa"]
col=db["empleados"]

def ingresoemp():
    os.system("cls")
    rut=input("Ingrese RUT de empleado: ")
    nombre=input("Ingrese nombre de empleado: ")
    apellidos=input("Ingrese apellidos de empleado: ")
    sueldo=int(input("Ingrese sueldo de empleado: "))
    estatura=float(input("Ingrese estatura de empleado: "))
    hijos=input("¿Tiene hijos? (S/N): ")
    if hijos=="S":
        nuevoshijos=[]
        numhijos=int(input("Ingrese numero de hijos que desea registrar: "))
        count=0
        while True:
            count+=1
            print("Hijo N°",count)
            nhijo=input("Ingrese nombre del hijo: ")
            ehijo=int(input("Ingrese edad del hijo: "))
            shijo=input("Ingrese sexo del hijo (F/M): ")
            nuhijo={"nombre":nhijo, "edad":ehijo, "sexo":shijo}
            nuevoshijos.append(nuhijo)
            if count==numhijos:
                break
        nempleado=({"rut":rut, "nombre":nombre, "apellidos":apellidos, "sueldo":sueldo, "hijos":nuevoshijos, "estatura":estatura})
    elif hijos=="N":
        nempleado=({"rut":rut, "nombre":nombre, "apellidos":apellidos, "sueldo":sueldo, "estatura":estatura})
    col.insert_one(nempleado)
    print("Empleado ingresado!")
    input("Presione enter para continuar...")

def ingresonhijo():
    os.system("cls")
    nuevoshijos=[]
    remp=input("Ingrese RUT del empleado: ")
    numhijos=int(input("Ingrese numero de hijos que desea registrar: "))
    os.system("cls")
    count=0
    while True:
        count+=1
        print("Hijo N°",count)
        nhijo=input("Ingrese nombre del hijo: ")
        ehijo=int(input("Ingrese edad del hijo: "))
        shijo=input("Ingrese sexo del hijo (F/M): ")
        nuhijo={"nombre":nhijo, "edad":ehijo, "sexo":shijo}
        nuevoshijos.append(nuhijo)
        if count==numhijos:
            break
    col.update_one({"rut":remp},{"$push":{"hijos":{"$each":nuevoshijos}}})
    print("Hijos ingresados!")
    input("Presione enter para continuar...")

def mostrar():
    os.system("cls")
    salida=col.find({})
    for linea in salida:
        print("")
        print("------------------------------")
        print("")
        print(f"""RUT: {linea["rut"]}
Nombre: {linea["nombre"]}
Apellidos: {linea["apellidos"]}
Sueldo: {linea["sueldo"]}
Estatura: {linea["estatura"]}""")
        if "hijos" in linea:
            print("Hijos:")
            for hijo in linea["hijos"]:
                print(f"""    Nombre: {hijo["nombre"]}
    Edad: {hijo["edad"]}
    Sexo: {hijo["sexo"]}""")
                print("")
            print("------------------------------")
    input("Presione enter para continuar...")

while True:
    os.system("cls")
    print("-- BIENVENIDO AL SISTEMA --")
    print("")
    print("1. Ingresar nuevo empleado")
    print("2. Ingresar nuevo hijo a un empleado")
    print("3. Mostrar empleados+hijos")
    print("0. Salir")
    print("")
    op=int(input("Ingrese una opcion: "))
    if op==1:
        ingresoemp()
    elif op==2:
        ingresonhijo()
    elif op==3:
        mostrar()
    elif op==0:
        break
    else:
        print("Opcion invalida.")
        input("Presione enter para continuar...")