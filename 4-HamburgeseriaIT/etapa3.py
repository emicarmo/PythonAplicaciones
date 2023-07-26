import sqlite3, requests, os, time, sys, tkinter as tk
from tkinter import ttk, messagebox
from os import path

def cotizacion():
    try:
        r = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        respuesta = r.json()
        valorVentaDolar = respuesta[0]["casa"]["venta"]
        valorVentaDolar = valorVentaDolar.replace(",", ".")
        valorVentaDolar = round(float(valorVentaDolar))
        return valorVentaDolar
    except:
        messagebox.showerror(title="Error de conexion", message="Sin internet para cotizar")

def guardarEncargado(data):
    datosIn = (data['nombre'],data['ingreso'],'IN',0)
    datosOut = (data['nombre'],data['egreso'],'OUT',data['facturado'])
    conn = sqlite3.connect('comercio.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO registro VALUES (NULL,?,?,?,?)',datosIn)
        cursor.execute('INSERT INTO registro VALUES (NULL,?,?,?,?)',datosOut)
    except sqlite3.OperationalError:
        cursor.execute("""CREATE TABLE registro
        (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Encargado TEXT,
            Fecha TEXT,
            Evento TEXT,
            Caja REAL
        )
        """)
        cursor.execute('INSERT INTO registro VALUES (NULL,?,?,?,?)',datosIn)
        cursor.execute('INSERT INTO registro VALUES (NULL,?,?,?,?)',datosOut)
    conn.commit()
    conn.close()

def guardarVentas(data):
    datos = tuple(data)
    conn = sqlite3.connect('comercio.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO ventas VALUES (NULL,?,?,?,?,?,?,?)',datos)
    except sqlite3.OperationalError:
        cursor.execute(""" CREATE TABLE ventas 
        (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, 
            Cliente TEXT, 
            Fecha TEXT, 
            ComboS INT, 
            ComboD INT, 
            ComboT INT, 
            Flurby INT, 
            Total REAL
        )
        """)
        cursor.execute('INSERT INTO Ventas VALUES (NULL,?,?,?,?,?,?,?)',datos)
    conn.commit()
    conn.close()

def validar(dato):
    try:
        dato = int(dato)
        return dato
    except ValueError:
        messagebox.showerror(title="Error de valor", message="Solo numeros enteros")

def borrar():
    c_comboS.delete(0, tk.END)
    c_comboD.delete(0, tk.END)
    c_comboT.delete(0, tk.END)
    c_postre.delete(0, tk.END)
    c_nombreCliente.delete(0, tk.END)

def cancelarPedido():
    cancelar = messagebox.askyesno(title="Pregunta", message="¿Desesa cancelar el pedido?")
    if cancelar:
        borrar()

def pedido():
    comboS = c_comboS.get()
    comboS = validar(comboS)
    comboD = c_comboD.get()
    comboD = validar(comboD)
    comboT = c_comboT.get()
    comboT = validar(comboT)
    postre = c_postre.get()
    postre = validar(postre)
    dolar = cotizacion()
    if comboS>=0 and comboD>=0 and comboT>=0 and postre>=0:
        cliente = c_nombreCliente.get()
        encargado = c_nombreEncargado.get()
        if cliente and encargado:
            respuesta = messagebox.askyesno(title="Pregunta", message="¿Confirmar pedido?")
            if respuesta:
                costoTotal = ((comboS*precioMenu['ComboSimple'])+(comboD*precioMenu['ComboDoble'])+(comboT*precioMenu['ComboTriple'])+(postre*precioMenu['McFlurby']))
                total_en_pesos = costoTotal * dolar
                fecha = time.asctime()
                pedido = [cliente,fecha,comboS,comboD,comboT,postre,total_en_pesos]
                messagebox.showinfo(title="A pagar", message="$"+str(total_en_pesos))
                guardarVentas(pedido)
                messagebox.showinfo(title="Estado del pedido", message="Pedido exitoso")
                if datosEncargados['nombre'] != encargado and datosEncargados['egreso'] == '':
                    datosEncargados['nombre'] = encargado
                    datosEncargados['egreso'] = "Sin fecha"
                    datosEncargados['facturado'] += total_en_pesos
                elif datosEncargados['nombre'] == encargado:
                    datosEncargados['facturado'] += total_en_pesos
                else:
                    datosEncargados['egreso'] = fecha
                    guardarEncargado(datosEncargados)
                    datosEncargados['nombre'] = encargado
                    datosEncargados['ingreso'] = fecha
                    datosEncargados['facturado'] = 0
                    datosEncargados['facturado'] += total_en_pesos
                borrar()
            else:
                messagebox.showinfo(title="Informacion", message="Pedido en pausa")
        else:
            messagebox.showwarning(title="¡Atencion!", message="Error, ingrese bien los datos")
    else:
        messagebox.showwarning(title="¡Atencion!", message="Error, ingrese los datos correctos")

def salir():
    salir_del_programa = messagebox.askyesno(title="Pregunta", message="¿Desea salir del programa?")
    if salir_del_programa:
        datosEncargados['egreso'] = time.asctime()
        guardarEncargado(datosEncargados)
        sys.exit()

# Precios menu
precioMenu = {
    'ComboSimple': 5,
    'ComboDoble': 6,
    'ComboTriple': 7,
    'McFlurby': 2
}

# Datos encargados
datosEncargados = {"nombre": "", "ingreso": time.asctime(), "egreso": "", "facturado": 0}

# Funciones eventos

def salirEnter(event=None):
    salir()

def cancelarEnter(event=None):
    cancelarPedido()

def pedidoEnter(event=None):
    pedido()

# Funcion para generar unico archivo

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Hamburgesas IT")
ventana_principal.configure(width=400, height=400)
#ventana_principal.iconphoto(False, tk.PhotoImage(file='icono3.png'))
ventana_principal.resizable(0,0)
path = resource_path("icono3.ico")
ventana_principal.iconbitmap(path)

# Etiqueta titulo
ebienvenido = ttk.Label(text="------ Pedidos ------")
ebienvenido.place(x=140, y=20)

# Etiquetas 
e_nombreEncargado = ttk.Label(text='Nombre Encargado:')
e_nombreEncargado.place(x=50, y=70)
e_comboS = ttk.Label(text='Combo S Cantidad:')
e_comboS.place(x=50, y=110)
e_comboD = ttk.Label(text='Combo D Cantidad:')
e_comboD.place(x=50, y=150)
e_comboT = ttk.Label(text='Combo T cantidad:')
e_comboT.place(x=50, y=190)
e_postre = ttk.Label(text='Postre Cantidad:')
e_postre.place(x=50, y=230)
e_nombreCliente = ttk.Label(text='Nombre Cliente:')
e_nombreCliente.place(x=50, y=270)

# Cajas
c_nombreEncargado = ttk.Entry()
c_nombreEncargado.place(x=230, y=70)
c_comboS = ttk.Entry()
c_comboS.place(x=230, y=110)
c_comboD = ttk.Entry()
c_comboD.place(x=230, y=150)
c_comboT = ttk.Entry()
c_comboT.place(x=230, y=190)
c_postre = ttk.Entry()
c_postre.place(x=230, y=230)
c_nombreCliente = ttk.Entry()
c_nombreCliente.place(x=230, y=270)

# Botones
b_salir = ttk.Button(text="Salir seguro",command=salir)
b_salir.place(x=30, y=330, width=100, height=40)
b_salir.bind('<Return>', salirEnter)
b_cancelar = ttk.Button(text="Cancelar pedido",command=cancelarPedido)
b_cancelar.place(x=150, y=330, width=100, height=40)
b_cancelar.bind('<Return>', cancelarEnter)
b_pedido = ttk.Button(text="Hacer pedido", command=pedido)
b_pedido.place(x=270, y=330, width=100, height=40)
b_pedido.bind('<Return>', pedidoEnter)

ventana_principal.mainloop()