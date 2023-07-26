"""  
Ejercicio 1: Dólar II
Hacer un programa que con un botón de consulta
muestre el precio de compra y venta del dólar.
"""

import tkinter as tk, requests, os, sys
from tkinter import ttk, messagebox

import threading
import queue


def worker(q: queue.Queue):
    r = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    if r.status_code == 200:
        respuesta = r.json()
        # No se puede retornar desde un hilo, así que hay que usar
        # una cola vía el módulo queue, que es una estructura
        # que se puede compartir entre hilos.
        q.put(respuesta)


def check_if_done(t, q: queue.Queue, index_respuesta):
    if not t.is_alive():
        respuesta = q.get_nowait()
        borrar()
        dolar_datos = respuesta[index_respuesta]
        dolar_compra = dolar_datos['casa']['compra']
        caja_compra.insert(0,dolar_compra)
        dolar_venta = dolar_datos['casa']['venta']
        caja_venta.insert(0,dolar_venta)
        # Rehabilitar los botones.
        for btn in (btn_dolar_blue,
                    btn_dolar_bolsa,
                    btn_dolar_liqui,
                    btn_dolar_oficial):
            btn["state"] = "normal"
    else:
        schedule_check(t, q, index_respuesta)


def schedule_check(t, q, index_respuesta):
    """
    Programar la ejecución de la función `check_if_done()` dentro de 
    un segundo.
    """
    ventana_principal.after(1000, check_if_done, t, q, index_respuesta)


def llamadaRequest():
    try:
        r = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        if r.status_code == 200:
            respuesta = r.json()
            return respuesta
    except Exception:
        messagebox.showerror(title="Error de conexion", message="No se puede obtener la cotizacion, intente mas tarde")
        caja_compra.insert(0,"NAN")
        caja_venta.insert(0,"NAN")

def borrar():
    caja_compra.delete(0,tk.END)
    caja_venta.delete(0,tk.END)


def obtener_cotizacion_con_hilo(index_respuesta):
    # Deshabilitar todos los botones mientras se obtiene la cotización.
    for btn in (btn_dolar_blue,
        btn_dolar_bolsa,
        btn_dolar_liqui,
        btn_dolar_oficial):
        btn["state"] = "disabled"
    # Crear la cola donde el hilo va a guardar el resultado
    # de la petición.
    q = queue.Queue()
    # Iniciar la petición en un nuevo hilo.
    t = threading.Thread(target=worker, args=(q,))
    t.start()
    # Comenzar a chequear periódicamente si el hilo ha finalizado.
    schedule_check(t, q, index_respuesta)


def cotizacionDolarOficial():
    obtener_cotizacion_con_hilo(0)


def cotizacionDolarBlue():
    obtener_cotizacion_con_hilo(1)


def cotizacionDolarLiqui():
    obtener_cotizacion_con_hilo(3)


def cotizacionDolarBolsa():
    obtener_cotizacion_con_hilo(4)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Ventana principal
ventana_principal = tk.Tk()
ventana_principal.title('Cotizaciones del dolar')
ventana_principal.configure(width=640, height=260)
ventana_principal.resizable(0,0)
path = resource_path('logo-dolares.ico')
ventana_principal.iconbitmap(path)

# Botones 

btn_dolar_oficial = ttk.Button(text="Cotizacion dolar oficial",command=cotizacionDolarOficial)
btn_dolar_oficial.place(x=10, y=50, width=140, height=40)
btn_dolar_blue = ttk.Button(text='Cotizacion dolar blue',command=cotizacionDolarBlue)
btn_dolar_blue.place(x=170, y=50, width=140, height=40)
btn_dolar_liqui = ttk.Button(text='Cotizacion dolar liqui',command=cotizacionDolarLiqui)
btn_dolar_liqui.place(x=330, y=50, width=140, height=40)
btn_dolar_bolsa = ttk.Button(text='Cotizacion dolar bolsa',command=cotizacionDolarBolsa)
btn_dolar_bolsa.place(x=490, y=50, width=140, height=40)

# Caja

caja_compra = ttk.Entry(font=('Arial Bold',15),foreground='red')
caja_compra.place(x=100, y=170, width=100, height=40)
caja_venta = ttk.Entry(font=('Arial Bold',15),foreground='green')
caja_venta.place(x=430, y=170, width=100, height=40)

# Label

label_compra = ttk.Label(text='Compra:')
label_compra.place(x=100, y=140)
label_compra.config(font=("Arial Bold",15),foreground='red')
label_venta = ttk.Label(text='Venta:')
label_venta.place(x=430, y=140)
label_venta.config(font=("Arial Bold",15),foreground='green')

ventana_principal.mainloop()