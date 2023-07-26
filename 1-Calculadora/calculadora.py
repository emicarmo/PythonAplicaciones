import tkinter as tk, os,sys
from tkinter import Button, Entry, StringVar, messagebox

expresion = ""

def presionar(numero):
    global expresion
    global equacion
    expresion = expresion + str(numero)
    equacion.set(expresion)

def resultadoExpresion():
    global expresion
    global equacion
    try:
        total = str(eval(expresion))
        equacion.set(total)
        expresion = total
    except ZeroDivisionError:
        equacion.set('0')
        expresion = ""
        messagebox.showerror(title="Error", message="No se puede dividir por cero")
    except Exception:
        equacion.set('0')
        expresion = ""
        messagebox.showerror(title="Error", message="Se produjo un error")

def limpiarCalculadora():
    global expresion
    global equacion
    expresion = ""
    equacion.set("0")

#Evento Enter

def on_Enter0(e):
    boton0.configure(bg='red')

def on_Enter1(e):
    boton1.configure(bg='red')

def on_Enter2(e):
    boton2.configure(bg='red')

def on_Enter3(e):
    boton3.configure(bg='red')

def on_Enter4(e):
    boton4.configure(bg='red')

def on_Enter5(e):
    boton5.configure(bg='red')

def on_Enter6(e):
    boton6.configure(bg='red')

def on_Enter7(e):
    boton7.configure(bg='red')

def on_Enter8(e):
    boton8.configure(bg='red')

def on_Enter9(e):
    boton9.configure(bg='red')

def on_Enter_Clear(e):
    boton_clear.configure(bg='red')

def on_Enter_Dividir(e):
    boton_dividir.configure(bg='red')

def on_Enter_Igual(e):
    boton_igual.configure(bg='red')

def on_Enter_Mas(e):
    boton_mas.configure(bg='red')

def on_Enter_Menos(e):
    boton_menos.configure(bg='red')

def on_Enter_Multiplicar(e):
    boton_multiplicar.configure(bg='red')

#Evento Leave

def on_Leave0(e):
    boton0.configure(bg='gray')

def on_Leave1(e):
    boton1.configure(bg='gray')

def on_Leave2(e):
    boton2.configure(bg='gray')

def on_Leave3(e):
    boton3.configure(bg='gray')

def on_Leave4(e):
    boton4.configure(bg='gray')

def on_Leave5(e):
    boton5.configure(bg='gray')

def on_Leave6(e):
    boton6.configure(bg='gray')

def on_Leave7(e):
    boton7.configure(bg='gray')

def on_Leave8(e):
    boton8.configure(bg='gray')

def on_Leave9(e):
    boton9.configure(bg='gray')

def on_Leave_Dividir(e):
    boton_dividir.configure(bg='gray')

def on_Leave_Mas(e):
    boton_mas.configure(bg='gray')

def on_Leave_Menos(e):
    boton_menos.configure(bg='gray')

def on_Leave_Multiplicar(e):
    boton_multiplicar.configure(bg='gray')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#Aplicacion

def calculadora():
    global boton0,boton1,boton2,boton3,boton4,boton5,boton6,boton7,boton8,boton9,boton_clear,boton_dividir,boton_igual,boton_mas,boton_menos,boton_multiplicar
    global equacion
    ventana_principal = tk.Tk()
    ventana_principal.title("Calculadora")
    ventana_principal.geometry("290x290")
    ventana_principal.configure(bg='black')
    ventana_principal.resizable(0,0)
    path = resource_path("calculadora.ico")
    ventana_principal.iconbitmap(path)

    equacion = StringVar()

    #Caja
    pantalla_calculadora = Entry(textvariable=equacion)
    pantalla_calculadora.configure(font='Montserrat 16',justify='right',state='disabled',disabledbackground='black',disabledforeground='white',border=0)
    pantalla_calculadora.grid(columnspan=4,ipadx=23,ipady=15)

    equacion.set('0')

    #Botones
    boton7 = Button(text=' 7 ', fg='black', bg='gray', height=3, width=7, command=lambda: presionar(7))
    boton7.grid(row=2, column=0)
    boton7.bind('<Enter>', on_Enter7)
    boton7.bind('<Leave>', on_Leave7)
    boton8 = Button(text=' 8 ', fg='black',bg='gray',height=3, width=7, command= lambda: presionar(8))
    boton8.grid(row=2, column=1)
    boton8.bind('<Enter>', on_Enter8)
    boton8.bind('<Leave>', on_Leave8)
    boton9 = Button(text=' 9 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(9))
    boton9.grid(row=2, column=2)
    boton9.bind('<Enter>', on_Enter9)
    boton9.bind('<Leave>', on_Leave9)
    
    boton4 = Button(text=' 4 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(4))
    boton4.grid(row=3, column=0)
    boton4.bind('<Enter>', on_Enter4)
    boton4.bind('<Leave>', on_Leave4)
    boton5 = Button(text=' 5 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(5))
    boton5.grid(row=3, column=1)
    boton5.bind('<Enter>', on_Enter5)
    boton5.bind('<Leave>', on_Leave5)
    boton6 = Button(text=' 6 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(6))
    boton6.grid(row=3, column=2)
    boton6.bind('<Enter>', on_Enter6)
    boton6.bind('<Leave>', on_Leave6)
    
    boton1 = Button(text=' 1 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(1))
    boton1.grid(row=4, column=0)
    boton1.bind('<Enter>', on_Enter1)
    boton1.bind('<Leave>', on_Leave1)
    boton2 = Button(text=' 2 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(2))
    boton2.grid(row=4, column=1)
    boton2.bind('<Enter>', on_Enter2)
    boton2.bind('<Leave>', on_Leave2)
    boton3 = Button(text=' 3 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(3))
    boton3.grid(row=4, column=2)
    boton3.bind('<Enter>', on_Enter3)
    boton3.bind('<Leave>', on_Leave3)
    
    boton_clear = Button(text=' C ',fg='black',bg='yellow',height=3, width=7, command=limpiarCalculadora)
    boton_clear.grid(row=5, column=0)
    boton0 = Button(text=' 0 ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar(0))
    boton0.grid(row=5, column=1)
    boton0.bind('<Enter>', on_Enter0)
    boton0.bind('<Leave>', on_Leave0)
    boton_igual = Button(text=' = ', fg='white',bg='blue',height=3, width=7, command=resultadoExpresion)
    boton_igual.grid(row=5, column=2)
    
    boton_mas = Button(text=' + ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar("+"))
    boton_mas.grid(row=2, column=3)
    boton_mas.bind('<Enter>', on_Enter_Mas)
    boton_mas.bind('<Leave>', on_Leave_Mas)
    boton_menos = Button(text=' - ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar("-"))
    boton_menos.grid(row=3, column=3)
    boton_menos.bind('<Enter>', on_Enter_Menos)
    boton_menos.bind('<Leave>', on_Leave_Menos)
    boton_multiplicar = Button(text=' X ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar("*"))
    boton_multiplicar.grid(row=4, column=3)
    boton_multiplicar.bind('<Enter>', on_Enter_Multiplicar)
    boton_multiplicar.bind('<Leave>', on_Leave_Multiplicar)
    boton_dividir = Button(text=' / ', fg='black',bg='gray',height=3, width=7, command=lambda: presionar("/"))
    boton_dividir.grid(row=5, column=3)
    boton_dividir.bind('<Enter>', on_Enter_Dividir)
    boton_dividir.bind('<Leave>', on_Leave_Dividir)
    
    ventana_principal.mainloop()

calculadora()