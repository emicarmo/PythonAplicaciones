import tkinter as tk, sqlite3, requests
from tkinter import ttk, messagebox

def llamarBaseDeDatos():
    try:
        conn = sqlite3.connect('productos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        tabla = cursor.fetchall()
    except sqlite3.OperationalError:
        messagebox.showerror(title="Error",message="La tabla no pudo ser traida con exito de la base de datos")
    else:
        messagebox.showinfo(title="Informacion",message="Tabla traida con exito de la base de datos")
    conn.commit()
    conn.close
    return tabla

def cotizacionDolar():
    try:
        r = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
        estado = r.status_code
        if estado == 200:
            cotizacion_dolar_oficial = r.json()
    except Exception:
        messagebox.showerror(title="Error de conexion", message="Las peticion de la cotizacion del dolar no pudo ser realizada")
    return cotizacion_dolar_oficial

def agregarProductos():
    nombre_producto = caja_producto.get()
    precio_usd = caja_precio_usd.get()
    if not nombre_producto.strip() and not precio_usd.strip():
        messagebox.showerror(title="Error",message="Los campos producto y precio (usd) deben llenarse")
    precio_usd = int(precio_usd)
    precio_pesos = float(round(precio_usd * precio_venta,2))
    tabla_productos.insert("",tk.END, text=nombre_producto,values=(f'${precio_usd}',f'${precio_pesos}'))
    productos = [nombre_producto, precio_usd]
    try:
        conn = sqlite3.connect('productos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos VALUES (?,?)', productos)
    except sqlite3.OperationalError:
        messagebox.showerror(title="Error",message="El producto no pudo ser insertado a la base de datos")
    else:
        messagebox.showinfo(title="Informacion",message="El producto fue insertado con exito a la base de datos")
    conn.commit()
    conn.close()
    caja_producto.delete(0,tk.END)
    caja_precio_usd.delete(0,tk.END)

def eventoReturn():
    agregarProductos()

def gestorProductosApp():
    global tabla_productos, precio_venta, caja_producto, caja_precio_usd
    # Ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Gestor de productos")
    ventana_principal.geometry("550x420")
    ventana_principal.resizable(0,0)
    
    # Label
    label_producto = ttk.Label(text="Producto:")
    label_producto.place(x=10, y=10)
    label_precio_usd = ttk.Label(text="Precio (USD):")
    label_precio_usd.place(x=210,y=10)

    # Caja
    caja_producto = ttk.Entry()
    caja_producto.place(x=70, y=10)
    caja_precio_usd = ttk.Entry()
    caja_precio_usd.place(x=287, y=10)

    #Boton
    btn_agregar_producto = ttk.Button(text="Agregar",command=agregarProductos)
    btn_agregar_producto.place(x=450,y=10)
    btn_agregar_producto.bind_all("<Return>",eventoReturn)

    #Treeview
    tabla_productos = ttk.Treeview(columns=("precio_usd", "precio_pesos"))
    tabla_productos.place(x=10,y=55,width=530, height=355)
    tabla_productos.column("#0",width=176)
    tabla_productos.heading("#0",text="Producto")
    tabla_productos.column('#1',width=176)
    tabla_productos.heading("precio_usd",text="Precio (USD)")
    tabla_productos.column('#2',width=176)
    tabla_productos.heading("precio_pesos", text="Precio (Pesos)")

    # Insertar datos al treeview
    tabla = llamarBaseDeDatos()
    cotizacion = cotizacionDolar()
    precio_venta = cotizacion[0]["casa"]["venta"]
    precio_venta = precio_venta.replace(",", ".")
    precio_venta = float(precio_venta)
    for t in tabla:
        precio_pesos = round(t[1] * precio_venta,2)
        tabla_productos.insert("",tk.END, text=t[0],values=(f'$ {t[1]}',f'$ {precio_pesos}'))

    ventana_principal.mainloop()

gestorProductosApp()