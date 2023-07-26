import time

def ingreso_str(mensaje,error):
    dato = input(mensaje)
    while dato.strip() == "":
        print(error)
        dato = input(mensaje)
    return dato

def ingreso_int(mensaje,error):
    dato = input(mensaje)
    while True:
        try:
            dato = int(dato)
            break
        except ValueError:
            print(error)
        dato = input(mensaje)
    return dato

def ingreso_float(mensaje,error):
    dato = input(mensaje)
    while True:
        try:
            dato = float(dato)
            break
        except ValueError:
            print(error)
        dato = input(mensaje)
    return dato

def ingresar():
    print("Bienvenido a Hamburguesas IT")
    nombre = ingreso_str("Ingrese nombre del encargad@: ", "Error campo vacio")
    return nombre

def saludar(nombre):
    print("Hamburguesas IT")
    print(f'Encargad@ -> {nombre}')
    print("Recuerda, siempre hay que recibir al cliente con una sonrisa :)")

def menu():
    print("""
    Menu:
    1 - Ingreso de nuevo pedido
    2 - Cambio de turno
    3 - Apagar sistema
    """)

def calcular_precio(precios,pedido):
    total = 0
    total += pedido["ComboSimple"] * precios["ComboSimple"]
    total += pedido["ComboDoble"] * precios["ComboDoble"]
    total += pedido["ComboTriple"] * precios["ComboTriple"]
    total += pedido["McFlurby"] * precios["McFlurby"]
    return total

def confirmar():
    respuesta = ingreso_str("¿Confirma el pedido? Y/N: ", "Error campo vacio")
    while respuesta.lower() != "y" and respuesta.lower() != "n" and respuesta.lower() != "yes" and respuesta.lower() != "no":
        print("Ingrese unicamente Y o N")
        respuesta = ingreso_str("¿Confirma el pedido? Y/N: ", "Error campo vacio")
    if respuesta == "y" or respuesta == "yes":
        return True
    else:
        return False

def guardarVentas(data):
    venta = ""
    for n in data:
        if n == "total":
            venta += f'{str(data[n])}\n'
        else:
            venta += f'{str(data[n])},'
    f = open("ventas.txt", "a", encoding="utf8")
    f.write(venta)
    f.close()

def guardarEncargado(data):
    ingreso = f'IN {data["ingreso"]} Encargad@ {data["nombre"]}\n'
    egreso = f'OUT {data["egreso"]} Encargad@ {data["nombre"]} $ {str(data["facturado"])}\n'
    separador = ("#"*50)+"\n"
    f = open("registro.txt", "a", encoding="utf8")
    f.write(ingreso)
    f.write(egreso)
    f.write(separador)
    f.close()

precios = {
    "ComboSimple": 5,
    "ComboDoble": 6,
    "ComboTriple":7,
    "McFlurby": 2
}

salir = True

while salir:
    datosEncargado = {
        "nombre":"",
        "ingreso":"",
        "egreso":"",
        "facturado":0
    }
    encargado = ingresar()
    inicio = time.asctime()
    datosEncargado["nombre"] = encargado
    datosEncargado["ingreso"] = inicio
    caja = 0
    print("\n"*2)
    while True:
        saludar(encargado)
        menu()
        opcion = ingreso_str("Ingrese opcion de menu: ", "Error, ingreso vacio")
        if opcion == "1":
            print("\n"*2)
            pedido = {
                "cliente": "",
                "fecha": "",
                "ComboSimple": 0,
                "ComboDoble": 0,
                "ComboTriple": 0,
                "McFlurby": 0,
                "total": 0
            }
            pedido["cliente"] = ingreso_str("Ingreso nombre del cliente: ","Error campo vacio")
            pedido["ComboSimple"] = ingreso_int("Ingrese cantidad Combo S: ","Error solo numeros")
            pedido["ComboDoble"] = ingreso_int("Ingrese cantidad Combo D: ","Error solo numeros")
            pedido["ComboTriple"] = ingreso_int("Ingrese cantidad Combo T: ","Error solo numeros")
            pedido["McFlurby"] = ingreso_int("Ingrese cantidad McFlurby: ","Error solo numeros")
            costoTotal = calcular_precio(precios,pedido)
            print(f'Total $ {costoTotal}')
            pago = ingreso_float("Abona con $: ", "Error solo numeros")
            while costoTotal > pago:
                print("Ingrese un monto mayor, no alcanza.")
                pago = ingreso_float("Abona con $: ", "Error solo numeros")
            print(f'Vuelto $ {pago - costoTotal}')
            estado = confirmar()
            if estado:
                caja += costoTotal
                pedido["fecha"] = time.asctime()
                pedido["total"] = costoTotal
                guardarVentas(pedido)
            else:
                print("Pedido cancelado")
        elif opcion == "2":
            datosEncargado["egreso"] = time.asctime()
            datosEncargado["facturado"] = caja
            guardarEncargado(datosEncargado)
            break
        elif opcion == "3":
            datosEncargado["egreso"] = time.asctime()
            datosEncargado["facturado"] = caja
            guardarEncargado(datosEncargado)
            print("¡Muchas Gracias por usar nuestro programa de Hamburguesas IT!")
            salir = False
            break
        else:
            print("Opcion incorrecta, vuelva intentarlo")
            print("\n"*3)