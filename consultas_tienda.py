from pymongo import MongoClient

# ==================== CONEXIÓN A MONGODB ====================
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["tienda"]
c_clientes = db["clientes"]
c_pedidos = db["pedidos"]

# ==================== FUNCIONES DE CONSULTAS ====================

def consulta_1_clientes_por_ciudad():
    """Opción 1: Filtros múltiples - Clientes por ciudad"""
    print("\n" + "="*70)
    print("OPCIÓN 1: Clientes por Ciudad (Filtros Múltiples)")
    print("="*70)
    
    try:
        # Extraer ciudades únicas
        ciudades_unicas = c_clientes.distinct("direccion")
        ciudades = list(set([c.split(", ")[-1] if ", " in c else c for c in ciudades_unicas]))
        
        print(f"\nCiudades disponibles: {', '.join(sorted(ciudades))}")
        ciudad_seleccionada = input("Selecciona una ciudad (ej: Valparaiso): ").strip()
        
        if not ciudad_seleccionada:
            ciudad_seleccionada = "Valparaiso"
            print(f"Usando ciudad por defecto: {ciudad_seleccionada}")
        
        # Filtro: clientes cuya dirección contiene la ciudad (insensible a mayúsculas)
        filtro = {"direccion": {"$regex": ciudad_seleccionada, "$options": "i"}}
        
        print(f"\n🔍 Buscando clientes en: {ciudad_seleccionada}")
        print("-" * 70)
        
        resultados = c_clientes.find(filtro)
        count = 0
        
        for doc in resultados:
            count += 1
            fecha = doc['fecha_registro']['$date'] if isinstance(doc['fecha_registro'], dict) else doc['fecha_registro']
            print(f"\n  Cliente #{count}:")
            print(f"    ID: {doc['_id']} | Nombre: {doc['nombre']}")
            print(f"    Email: {doc['email']}")
            print(f"    Teléfono: {doc['telefono']}")
            print(f"    Dirección: {doc['direccion']}")
            print(f"    Registro: {fecha}")
        
        print(f"\n  Total: {count} cliente(s) encontrado(s)" if count > 0 else "\n  No se encontraron resultados")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def consulta_2_buscar_nombre_email():
    """Opción 2: Expresiones regulares - Buscar por nombre o email"""
    print("\n" + "="*70)
    print("OPCIÓN 2: Buscar Clientes por Nombre o Email (Expresiones Regulares)")
    print("="*70)
    
    try:
        patron = input("\nIngresa el patrón de búsqueda (nombre o email): ").strip()
        
        if not patron:
            patron = "gmail"
            print(f"Usando búsqueda por defecto: '{patron}'")
        
        # Filtro: busca en nombre O email con patrón (insensible a mayúsculas)
        filtro = {
            "$or": [
                {"nombre": {"$regex": patron, "$options": "i"}},
                {"email": {"$regex": patron, "$options": "i"}}
            ]
        }
        
        print(f"\n🔍 Buscando: '{patron}' en nombres o emails")
        print("-" * 70)
        
        resultados = c_clientes.find(filtro)
        count = 0
        
        for doc in resultados:
            count += 1
            fecha = doc['fecha_registro']['$date'] if isinstance(doc['fecha_registro'], dict) else doc['fecha_registro']
            print(f"\n  Resultado #{count}:")
            print(f"    ID: {doc['_id']} | Nombre: {doc['nombre']}")
            print(f"    Email: {doc['email']}")
            print(f"    Registro: {fecha}")
        
        print(f"\n  Total: {count} cliente(s) encontrado(s)" if count > 0 else "\n  No se encontraron resultados")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def consulta_3_pedidos_por_monto():
    """Opción 3: Arrays/Subdocumentos - Pedidos por monto"""
    print("\n" + "="*70)
    print("OPCIÓN 3: Pedidos por Monto (Arrays y Subdocumentos)")
    print("="*70)
    
    try:
        monto_minimo = input("\nIngresa monto mínimo de pedido (ej: 500): ").strip()
        
        try:
            monto_minimo = float(monto_minimo) if monto_minimo else 500
        except ValueError:
            monto_minimo = 500
        
        print(f"Usando monto mínimo: ${monto_minimo}")
        
        # Filtro: pedidos con monto_total >= al ingresado
        filtro = {"monto_total": {"$gte": monto_minimo}}
        
        print(f"\n🔍 Buscando pedidos con monto >= ${monto_minimo}")
        print("-" * 70)
        
        resultados = list(c_pedidos.find(filtro).sort("monto_total", -1))
        count = 0
        
        for doc in resultados:
            count += 1
            fecha = doc['fecha_pedido']['$date'] if isinstance(doc['fecha_pedido'], dict) else doc['fecha_pedido']
            
            # Obtener datos del cliente
            cliente = c_clientes.find_one({"_id": doc['cliente_id']})
            nombre_cliente = cliente['nombre'] if cliente else "Desconocido"
            
            num_productos = len(doc['productos'])
            
            print(f"\n  Pedido #{count}:")
            print(f"    ID Pedido: {doc['_id']} | Cliente: {nombre_cliente}")
            print(f"    Fecha: {fecha}")
            print(f"    Monto Total: ${doc['monto_total']}")
            print(f"    Productos: {num_productos}")
            
            for prod in doc['productos']:
                print(f"      - Producto {prod['producto_id']}: {prod['cantidad']} unidades @ ${prod['precio']}")
        
        print(f"\n  Total: {count} pedido(s) encontrado(s)" if count > 0 else "\n  No se encontraron resultados")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def consulta_4_clientes_activos():
    """Opción 4: Operadores lógicos - Clientes activos"""
    print("\n" + "="*70)
    print("OPCIÓN 4: Clientes Activos (Operadores Lógicos: $or, $and)")
    print("="*70)
    
    try:
        print(f"\n🔍 Buscando clientes activos (registro reciente O pedidos en 2025)")
        print("-" * 70)
        
        # Obtener clientes con pedidos en 2025
        pedidos_2025 = c_pedidos.find({"fecha_pedido": {"$regex": "2025"}})
        clientes_con_pedidos_2025 = set(p['cliente_id'] for p in pedidos_2025)
        
        todos_clientes = list(c_clientes.find())
        clientes_activos = []
        
        for cliente in todos_clientes:
            # Verificar si tiene pedidos en 2025 O está registrado recientemente (2025/2024)
            tiene_pedido_2025 = cliente['_id'] in clientes_con_pedidos_2025
            fecha_str = str(cliente['fecha_registro'])
            es_registro_reciente = "2025" in fecha_str or "2024" in fecha_str
            
            if tiene_pedido_2025 or es_registro_reciente:
                clientes_activos.append(cliente)
        
        count = 0
        for cliente in sorted(clientes_activos, key=lambda x: x['_id']):
            count += 1
            fecha = cliente['fecha_registro']['$date'] if isinstance(cliente['fecha_registro'], dict) else cliente['fecha_registro']
            num_pedidos = c_pedidos.count_documents({"cliente_id": cliente['_id']})
            
            print(f"\n  Cliente #{count}:")
            print(f"    ID: {cliente['_id']} | Nombre: {cliente['nombre']}")
            print(f"    Registro: {fecha}")
            print(f"    Pedidos: {num_pedidos}")
        
        print(f"\n  Total: {count} cliente(s) activo(s)" if count > 0 else "\n  No se encontraron clientes activos")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def consulta_5_estadisticas():
    """Opción 5: Estadísticas y ranking de clientes"""
    print("\n" + "="*70)
    print("OPCIÓN 5: Estadísticas y Ranking de Clientes")
    print("="*70)
    
    try:
        print(f"\n📊 Generando estadísticas...")
        print("-" * 70)
        
        # Estadística 1: Calcular monto total por cliente
        estadisticas_cliente = {}
        for pedido in c_pedidos.find():
            cliente_id = pedido['cliente_id']
            monto = pedido['monto_total']
            
            if cliente_id not in estadisticas_cliente:
                estadisticas_cliente[cliente_id] = {'monto_total': 0, 'num_pedidos': 0}
            
            estadisticas_cliente[cliente_id]['monto_total'] += monto
            estadisticas_cliente[cliente_id]['num_pedidos'] += 1
        
        # Cliente con mayor gasto
        if estadisticas_cliente:
            cliente_top_id = max(estadisticas_cliente.items(), 
                                key=lambda x: x[1]['monto_total'])[0]
            cliente_top = c_clientes.find_one({"_id": cliente_top_id})
            stats_top = estadisticas_cliente[cliente_top_id]
            
            print(f"\n💎 Cliente con mayor gasto:")
            print(f"    {cliente_top['nombre']} (ID: {cliente_top_id})")
            print(f"    Monto total: ${stats_top['monto_total']}")
            print(f"    Pedidos: {stats_top['num_pedidos']}")
        
        # Ranking de clientes
        print(f"\n🏆 Ranking de clientes por monto gastado:")
        ranking = sorted(estadisticas_cliente.items(), 
                        key=lambda x: x[1]['monto_total'], 
                        reverse=True)
        
        for posicion, (cliente_id, stats) in enumerate(ranking, 1):
            cliente_info = c_clientes.find_one({"_id": cliente_id})
            promedio = stats['monto_total'] / stats['num_pedidos'] if stats['num_pedidos'] > 0 else 0
            print(f"  #{posicion}. {cliente_info['nombre']}")
            print(f"     Total: ${stats['monto_total']} | Pedidos: {stats['num_pedidos']} | Promedio: ${promedio:.2f}")
        
        # Resumen global
        print(f"\n📈 Resumen Global:")
        total_clientes = c_clientes.count_documents({})
        total_pedidos = c_pedidos.count_documents({})
        monto_total_vendido = sum(p['monto_total'] for p in c_pedidos.find())
        promedio_pedido = monto_total_vendido / total_pedidos if total_pedidos > 0 else 0
        
        print(f"    Total de clientes: {total_clientes}")
        print(f"    Total de pedidos: {total_pedidos}")
        print(f"    Monto total vendido: ${monto_total_vendido}")
        print(f"    Promedio por pedido: ${promedio_pedido:.2f}")
        
        # Clientes sin pedidos
        clientes_con_pedidos = set(p['cliente_id'] for p in c_pedidos.find())
        clientes_sin_pedidos = [c for c in c_clientes.find() if c['_id'] not in clientes_con_pedidos]
        
        if clientes_sin_pedidos:
            print(f"\n⚠️  Clientes sin pedidos ({len(clientes_sin_pedidos)}):")
            for cliente in clientes_sin_pedidos:
                print(f"    - {cliente['nombre']} (ID: {cliente['_id']})")
        else:
            print(f"\n✓ Todos los clientes tienen al menos un pedido")
    
    except Exception as e:
        print(f"✗ Error: {e}")


# ==================== MENÚ PRINCIPAL ====================

print("\n╔══════════════════════════════════════════════════════════════════════╗")
print("║     CONSULTAS AVANZADAS EN MONGODB - BASE DE DATOS: TIENDA          ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

# Verificar conexión
try:
    cliente.admin.command('ping')
    print("✓ Conexión a MongoDB exitosa")
except:
    print("✗ Error: No se pudo conectar a MongoDB")
    exit()

# Menú interactivo
while True:
    print("\n" + "="*70)
    print("MENÚ - CONSULTAS AVANZADAS EN MONGODB (Base de datos TIENDA)")
    print("="*70)
    print("\n1. Clientes por ciudad (Filtros múltiples)")
    print("2. Buscar por nombre/email (Expresiones regulares)")
    print("3. Pedidos por monto (Arrays y subdocumentos)")
    print("4. Clientes activos (Operadores lógicos)")
    print("5. Estadísticas y ranking")
    print("0. Salir")
    print("-" * 70)
    
    opcion = input("\nSelecciona una opción (0-5): ").strip()
    
    if opcion == "1":
        consulta_1_clientes_por_ciudad()
    elif opcion == "2":
        consulta_2_buscar_nombre_email()
    elif opcion == "3":
        consulta_3_pedidos_por_monto()
    elif opcion == "4":
        consulta_4_clientes_activos()
    elif opcion == "5":
        consulta_5_estadisticas()
    elif opcion == "0":
        print("\n✓ ¡Hasta luego!")
        break
    else:
        print("\n✗ Opción no válida. Por favor, ingresa un número entre 0 y 5.")
