import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from tkinter import ttk
import sqlite3
import uuid
from customtkinter import *
from tkinter import messagebox
import openpyxl
from datetime import datetime
from tkinter import scrolledtext
from datetime import datetime
import random
import string



class FormularioMaestroDesing(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/logo.png",(560,136))
        self.perfil = util_img.leer_imagen("./imagenes/perfil.png",(100,100))
        self.menu_burger = util_img.leer_imagen("./imagenes/menu-burger.png",(20,20))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()
        self.editando_producto_id = None
     
    def config_window(self):
        self.title('Punto de Venta')
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self,w,h)    

    def paneles(self):
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR,height=50)
        self.barra_superior.pack(side=tk.TOP,fill="both")

        self.menu_lateral = tk.Frame(self,bg=COLOR_MENU_LATERAL,width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill="both", expand=False)

        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL,width=150)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill="both",expand=True)
        
    def controles_barra_superior(self):

        self.labelTitulo =  tk.Label(self.barra_superior,text="Menu Principal")
        
        self.labelTitulo.config(fg="#fff",font=("Roboto",15), bg=COLOR_BARRA_SUPERIOR,
        pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = CTkButton(self.barra_superior, text='\uf0c9',
                                           command=self.toggle_panel,fg_color=COLOR_BARRA_SUPERIOR,font=("Arial",20),hover_color=COLOR_BARRA_SUPERIOR)
        self.buttonMenuLateral.pack(side=tk.LEFT)


        self.labelTitulo = tk.Label(
            self.barra_superior,text="@bacosoluciones")
        self.labelTitulo.config(
            fg="#fff",font=("Roboto",10),bg=COLOR_BARRA_SUPERIOR,padx=10,width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        ancho_menu = 24
        alto_menu = 2
        font_awesome = font.Font(family='OCR A Extended',size=14)

        self.labelPerfil =tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP,pady=10)

        self.buttonInventario = tk.Button(self.menu_lateral,command=self.Inventario) 
        self.buttonIngresoVentas = tk.Button(self.menu_lateral,command=self.ventas) 
        self.buttonHistorialVentas = tk.Button(self.menu_lateral) 
       # self.buttonProveedores= tk.Button(self.menu_lateral) 
       # self.buttonClientes = tk.Button(self.menu_lateral,command=self.mostrar_clientes)  
       # self.buttonDatosNegocio = tk.Button(self.menu_lateral,command=self.datos_negocio)
        self.buttonUsuarios = tk.Button(self.menu_lateral)
     
        buttons_info = [
        ("INVENTARIO", "\uf494", self.buttonInventario), 
        ("CAJA REGISTRADORA", "\uf788", self.buttonIngresoVentas), 
        ("HISTORIAL VENTAS", "\uf073", self.buttonHistorialVentas), 
        #("Proveedores", "\ue58d", self.buttonProveedores),
        #("CLIENTES", "\uf007", self.buttonClientes),
        #("DATOS NEGOCIO", "\uf54e", self.buttonDatosNegocio),
        ("USUARIOS", "\ue594", self.buttonUsuarios),
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)
    
    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
             self.menu_lateral.pack_forget()
           
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def bind_hover_events(self,button):
        button.bind("<Enter>", lambda event: self.on_enter(event,button))
        button.bind("<Leave>", lambda event: self.on_leave(event,button))
    
    def on_enter(self,event,button):
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA,fg='white')
    
    def on_leave(self,event,button):
        button.config(bg=COLOR_MENU_LATERAL,fg='white')
    
    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu): 
        button.config(text=f" {icon} {text}", anchor="w", font=font_awesome,
        bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu) 
        button.pack(side=tk.TOP) 
        self.bind_hover_events(button)

    def controles_cuerpo(self):
        label = tk.Label(self.cuerpo_principal,image=self.logo,
                         bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0,y=0,relwidth=1,relheight=1)
    

#---------------------funciones para el inventario-------------------------------------------------
    
    def Inventario(self):
       

        # Limpiar cualquier widget existente en el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
          # Definir el estilo general para los botones
        
        ESTILO_CTKBOTONES_DATOS_INVENTARIO = {
            'width': 30,
            'height': 30,
            'text_color': 'black',
            'font': ("OCR A Extended", 12)
        }

        ESTILO_TITULO_LABEL_DATOS_INVENTARIO = {
            'text_color': 'black',
            'font': ("OCR A Extended", 15, "bold"),  
        }

        ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO = {
            'text_color': 'black',
            'font': ("OCR A Extended", 14),
               
        }
        
        ALINEACION_FORMULARIO = {
        'padx': 5,
        'pady': 5,
        'sticky': 'w'
        }
#Creando la ventana de D
            
        # Crear un formulario para agregar nuevos elementos al inventario
        formulario_inventario = tk.Frame(self.cuerpo_principal, bg=COLOR_CUERPO_PRINCIPAL)
        formulario_inventario.pack(padx=20, pady=20, fill='both', expand=True)

        # Etiquetas y campos de entrada para el formulario_inventario
        CTkLabel(formulario_inventario,text="INGRESO DE PRODUCTOS",**ESTILO_TITULO_LABEL_DATOS_INVENTARIO).grid(row=0,column=0,sticky="ns",padx=5,pady=5,columnspan=2)

        #dentry para id OCULTO
        id_producto_entry = tk.Entry(formulario_inventario,)
        id_producto_entry.grid(row=1, column=1, padx=5, pady=5)
        id_producto_entry.grid_remove()
      
        CTkLabel(formulario_inventario, text="Nombre:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=2, column=0,**ALINEACION_FORMULARIO)
        nombre_producto_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        nombre_producto_entry.grid(row=2, column=1,**ALINEACION_FORMULARIO)

        CTkLabel(formulario_inventario, text="Descripción:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=3, column=0,**ALINEACION_FORMULARIO)
        descripcion_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        descripcion_entry.grid(row=3, column=1,**ALINEACION_FORMULARIO)

        CTkLabel(formulario_inventario, text="Precio venta:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=4, column=0,**ALINEACION_FORMULARIO)
        precio_venta_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        precio_venta_entry.grid(row=4, column=1,**ALINEACION_FORMULARIO)

        CTkLabel(formulario_inventario, text="Precio compra:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=5, column=0,**ALINEACION_FORMULARIO)
        precio_compra_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        precio_compra_entry.grid(row=5, column=1,**ALINEACION_FORMULARIO)

        CTkLabel(formulario_inventario, text="Existencias:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=6, column=0,**ALINEACION_FORMULARIO)
        existencias_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        existencias_entry.grid(row=6, column=1,**ALINEACION_FORMULARIO)

        CTkLabel(formulario_inventario, text="Stock Min:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=7, column=0,**ALINEACION_FORMULARIO)
        stock_minimo_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        stock_minimo_entry.grid(row=7, column=1,**ALINEACION_FORMULARIO)

        CTkLabel(formulario_inventario, text="Codigo de barras:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO).grid(row=8, column=0,**ALINEACION_FORMULARIO)
        codigo_barras_entry = CTkEntry(formulario_inventario,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        codigo_barras_entry.grid(row=8, column=1,**ALINEACION_FORMULARIO)

        # Actualizar la descripción al principio
    
      # Botón para agregar el producto al inventario
        agregar_button = CTkButton(formulario_inventario, text="\uf055 Agregar\nProducto", 
                                    command=lambda: self.agregar_producto(tree_inventario, nombre_producto_entry, descripcion_entry, 
                                                                        precio_venta_entry, precio_compra_entry, existencias_entry, 
                                                                        stock_minimo_entry, codigo_barras_entry, id_producto_entry),**ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        agregar_button.grid(row=9, column=1, padx=5, pady=5)

        # Botón para limpiar el formulario
    
        limpiar_formulario_button = CTkButton(formulario_inventario, text="\uf1b8 Limpiar\nformulario", 
                                              command=lambda: self.limpiar_formulario(id_producto_entry,nombre_producto_entry,descripcion_entry,
                                                                                      precio_venta_entry,precio_compra_entry,existencias_entry,
                                                                                      stock_minimo_entry,codigo_barras_entry),**ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        limpiar_formulario_button.grid(row=9, column=0, padx=5, pady=5)

        # Crear y empaquetar el label para la descripción del producto
        self.descripcion_info_producto = tk.Label(formulario_inventario,font = ("OCR A Extended", 13),wraplength=300,background=COLOR_CUERPO_PRINCIPAL,justify="left")
        self.descripcion_info_producto.place(relx=0.5, rely=0.3, anchor='nw')

        # Crear y empaquetar el label para la notificación de existencias bajas
        self.notificacion_existencias_bajas = tk.Label(formulario_inventario,font = ("OCR A Extended", 14), fg="red", background=COLOR_CUERPO_PRINCIPAL,wraplength=300)

        self.lbl_buscar = CTkLabel(formulario_inventario,text="Buscar producto:",**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO)
        self.lbl_buscar.place(relx=0.60, rely=0.85, anchor='e')

        self.entry_buscar = CTkEntry(formulario_inventario,height=30,width=150,**ESTILO_ENTRYS_LABEL_DATOS_INVENTARIO,placeholder_text="\uf3eb")
        self.entry_buscar.place(relx=0.80, rely=0.85, anchor='e')

        self.entry_buscar.bind("<KeyRelease>", lambda event: self.filtrar_productos(event, tree_inventario, self.entry_buscar))
             
        # CREAR EL TREEVIEW -------------------------------------------------
        treeview_frame = tk.Frame(self.cuerpo_principal)
        treeview_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configurar el Grid para que el frame se expanda con la ventana
        treeview_frame.grid_rowconfigure(0, weight=1)
        treeview_frame.grid_columnconfigure(0, weight=1)

        # Configurar el estilo
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font = ("OCR A Extended", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font = ("OCR A Extended", 9,"bold"))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        # Crear el TreeView con el estilo configurado y limitar el número máximo de filas
        tree_inventario = ttk.Treeview(treeview_frame, style="mystyle.Treeview", 
                                        columns=("id","Nombre", "Descripción", "Precio Venta", "Precio Compra", "Existencias", "Stock Mínimo", "Código Barras"), 
                                        show="headings")

        tree_inventario.heading("id", text="ID")
        tree_inventario.heading("Nombre", text="NOMBRE")
        tree_inventario.heading("Descripción", text="DESCRIPCION")
        tree_inventario.heading("Precio Venta", text="PVP")
        tree_inventario.heading("Precio Compra", text="P. COMPRA")
        tree_inventario.heading("Existencias", text="EXISTENCIAS")
        tree_inventario.heading("Stock Mínimo", text="STOCK MIN")
        tree_inventario.heading("Código Barras", text="COD BARRAS")
        
        # Asociar la función de actualización al evento de selección en el TreeView
        tree_inventario.bind("<<TreeviewSelect>>", lambda event: self.actualizar_descripcion(event, tree_inventario))  

        # Agregar un Scrollbar para el TreeView
        scrollbar = CTkScrollbar(treeview_frame, command=tree_inventario.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree_inventario.configure(yscrollcommand=scrollbar.set)

        # Ajustar el ancho de las columnas al cambiar el tamaño de la ventana
        for col in ("Nombre", "Descripción", "Precio Venta", "Precio Compra", "Existencias", "Stock Mínimo", "Código Barras"):
            tree_inventario.column(col, width=60, anchor="center")  # Ajusta el ancho según sea necesario
            tree_inventario.column("id", width=0, stretch=tk.NO) #OCULTAR LA COLUMNA ID

        # Configurar el Grid para que el TreeView se expanda con el frame
        tree_inventario.grid(row=0, column=0, sticky="nsew")

        # Obtener datos de productos de la base de datos
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conn.close()
        
        
        # Obtener la descripción seleccionada
        descripcion_seleccionada = "Descripción seleccionada"

        # Crear o actualizar la descripción
        self.actualizar_descripcion(descripcion_seleccionada, tree_inventario)
        self.notificar_existencias_bajas(productos)

        buttons_frame = tk.Frame(treeview_frame,background=COLOR_CUERPO_PRINCIPAL)
        buttons_frame.grid(row=0, column=2, sticky="ns")

        # Crear los botones de editar y eliminar
        editar_button = CTkButton(buttons_frame, text="\uf044"" Editar", 
                                  command=lambda: self.editar_producto(tree_inventario, nombre_producto_entry, 
                                                                       descripcion_entry, precio_venta_entry, precio_compra_entry, 
                                                                       existencias_entry, stock_minimo_entry, codigo_barras_entry, 
                                                                       id_producto_entry),**ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        editar_button.pack(side="top", padx=5, pady=5)

        eliminar_button = CTkButton(buttons_frame, text="\uf056"" Eliminar", command=lambda: self.eliminar_producto(tree_inventario)
                                    ,**ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        eliminar_button.pack(side="top", padx=5, pady=5)

        cargar_button = CTkButton(buttons_frame, text="\uf093"" Cargar\nExcel",command=lambda: self.cargar_excel(tree_inventario)
                                  ,**ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        cargar_button.pack(side="top", padx=5, pady=5)

        descargar_button = CTkButton(buttons_frame, text="\uf019 Respaldo", command=self.descargar_productos_excel,**ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        descargar_button.pack(side="top", padx=5, pady=5)

        # Verificar si hay existencias mínimas en la lista de productos
        existencias_minimas = any(producto[5] < producto[6] for producto in productos)

        # Crear el botón con la opción de habilitarlo o deshabilitarlo según la condición
        informe_stock_min_button = CTkButton(buttons_frame, text="\uf15b"" Informe\nStock\nminimo", command=lambda: self.mostrar_informe_min_stock(productos),
                                             **ESTILO_CTKBOTONES_DATOS_INVENTARIO)
        if existencias_minimas:
            informe_stock_min_button.configure(state="normal")  # Habilitar el botón si hay existencias mínimas
        else:
            informe_stock_min_button.configure(state="disabled")  # Deshabilitar el botón si no hay existencias mínimas
        informe_stock_min_button.pack(side="top", padx=5, pady=5)

        for producto in productos:
            self.agregar_producto_a_treeview(producto, tree_inventario)

        self.actualizar_descripcion(None, tree_inventario)

    def actualizar_descripcion(self, event, tree_inventario):
        try:
            # Obtener el índice del item seleccionado en el TreeView
            item_seleccionado = tree_inventario.focus()
            
            # Obtener los valores del item seleccionado
            valores = tree_inventario.item(item_seleccionado, 'values')
            
            # Verificar si hay valores en la fila seleccionada
            if valores:
                # Obtener la descripción del producto
                descripcion_producto = valores[2]  # Suponiendo que la descripción está en la segunda columna
                # Actualizar el texto del label con la descripción del producto
                self.descripcion_info_producto.config(text="Información General: " + descripcion_producto)
            else:
                # Si no hay valores en la fila seleccionada, mostrar un mensaje de error
                self.descripcion_info_producto.config(text="Información General: Seleccione un producto para  ver su información.")

        except Exception as e:
            # Mostrar mensaje de error
            messagebox.showerror("Error", f"Ha ocurrido un error al actualizar la descripción: {str(e)}")
  
    def filtrar_productos(self, event, tree_inventario, entry_buscar):

        # Obtener el texto ingresado en el Entry de búsqueda
        texto_busqueda = entry_buscar.get().lower()  # Convertir a minúsculas para una búsqueda sin distinción entre mayúsculas y minúsculas

        # Limpiar el TreeView antes de aplicar el filtro
        for row in tree_inventario.get_children():
            tree_inventario.delete(row)

        # Obtener los datos de productos de la base de datos
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        # Filtrar los productos que coinciden con la búsqueda
        for producto in productos:
            # Convertir todos los campos a minúsculas para una búsqueda sin distinción entre mayúsculas y minúsculas
            if any(texto_busqueda in str(valor).lower() for valor in producto):
                precio_venta = f"${producto[3]}"  # El índice 3 corresponde al precio de venta
                precio_compra = f"${producto[4]}"  # El índice 4 corresponde al precio de compra
                tree_inventario.insert("", "end", text="", values=(producto[0],producto[1], producto[2], precio_venta, precio_compra, producto[5], producto[6], producto[7]))

        # Cerrar la conexión a la base de datos
        conn.close()

    def agregar_producto(self, tree_inventario, nombre_producto_entry, descripcion_entry, precio_venta_entry, precio_compra_entry, existencias_entry, stock_minimo_entry, codigo_barras_entry, id_producto_entry):
        try:
            # Obtener los valores de los campos del formulario
            nombre = nombre_producto_entry.get()
            descripcion = descripcion_entry.get()
            precio_venta = precio_venta_entry.get()
            precio_compra = precio_compra_entry.get()
            existencias = existencias_entry.get()
            stock_minimo = stock_minimo_entry.get()
            codigo_barras = codigo_barras_entry.get()
            id_producto = id_producto_entry.get()

            # Validar que no haya campos vacíos
            if not all([nombre, descripcion, precio_venta, precio_compra, existencias, stock_minimo, codigo_barras]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Convertir los valores de precio y existencias a números
            precio_venta = float(precio_venta.replace('$', ''))
            precio_compra = float(precio_compra.replace('$', ''))
            existencias = int(existencias)
            stock_minimo = int(stock_minimo)

            # Validar que los precios y existencias sean valores válidos
            if precio_venta <= 0 or precio_compra <= 0 or existencias < 0 or stock_minimo < 0:
                messagebox.showerror("Error", "Los precios y existencias deben ser mayores que cero, y las existencias no pueden ser negativas")
                return

            # Conectar a la base de datos
            conn = sqlite3.connect('farmacia.db')
            cursor = conn.cursor()

            # Verificar si el código de barras ya existe en la base de datos
            cursor.execute("SELECT * FROM productos WHERE codigo_barras=?", (codigo_barras,))
            existing_product = cursor.fetchone()

            # Verificar si ya existe un producto con el mismo código de barras, nombre, descripción y ID
            if existing_product:
                existing_nombre = existing_product[1]
                existing_descripcion = existing_product[2]
                existing_id = existing_product[0]
                if existing_nombre == nombre and existing_descripcion == descripcion and existing_id == id_producto:
                    # Permitir la edición si se modifican otros campos
                    cursor.execute("UPDATE productos SET precio_venta=?, precio_compra=?, existencias=?, stock_minimo=? WHERE id=?",
                                    (precio_venta, precio_compra, existencias, stock_minimo, id_producto))
                    messagebox.showinfo("Éxito", "El producto se ha actualizado correctamente")
                    conn.commit()
                else:
                    messagebox.showinfo("Info", "Ya existe un producto con el mismo código de barras, nombre y descripción en la base de datos")
                    return

            # Verificar si estamos editando un producto existente o agregando uno nuevo
            if self.editando_producto_id:  # Si hay un ID de producto en modo de edición
                # Actualizar los datos del producto existente
                cursor.execute("UPDATE productos SET nombre=?, descripcion=?, precio_venta=?, precio_compra=?, existencias=?, stock_minimo=?, codigo_barras=? WHERE id=?",
                                (nombre, descripcion, precio_venta, precio_compra, existencias, stock_minimo, codigo_barras, self.editando_producto_id))
                messagebox.showinfo("Éxito", "El producto se ha actualizado correctamente")
                conn.commit()
            else:
                # Generar un id único de 8 caracteres alfanuméricos
                producto_id = str(uuid.uuid4())[:8]  # Obtiene los primeros 8 caracteres del id generado

                # Insertar los datos en la tabla de productos
                cursor.execute("INSERT INTO productos (id, nombre, descripcion, precio_venta, precio_compra, existencias, stock_minimo, codigo_barras) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (producto_id, nombre, descripcion, precio_venta, precio_compra, existencias, stock_minimo, codigo_barras))
                messagebox.showinfo("Éxito", "El producto se ha agregado correctamente")
                conn.commit()

            # Limpiar el TreeView antes de volver a cargar los datos
            tree_inventario.delete(*tree_inventario.get_children())

            # Obtener los datos actualizados de productos de la base de datos
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            for producto in productos:
                precio_venta = f"${producto[3]}"  # El índice 3 corresponde al precio de venta
                precio_compra = f"${producto[4]}"  # El índice 4 corresponde al precio de compra
                tree_inventario.insert("", "end", values=(producto[0], producto[1], producto[2], precio_venta, precio_compra, producto[5], producto[6], producto[7]))

        except ValueError:
            # Mostrar mensaje de error si los campos de precio y existencias no son números válidos
            messagebox.showerror("Error", "Los campos de precio y existencias deben ser números")
        except sqlite3.Error as e:
            # Mostrar mensaje de error específico de SQLite
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
        except Exception as e:
            # Mostrar mensaje de error genérico
            messagebox.showerror("Error", f"Ha ocurrido un error al agregar el producto: {str(e)}")
        finally:
            # Cerrar la conexión a la base de datos si está abierta
            if conn:
                conn.close()

        # Limpiar el formulario independientemente del resultado
        self.limpiar_formulario(id_producto_entry, nombre_producto_entry, descripcion_entry, precio_venta_entry, precio_compra_entry, existencias_entry, stock_minimo_entry, codigo_barras_entry)
        self.notificar_existencias_bajas(productos)

    def eliminar_producto(self, tree_inventario):
        try:
            # Obtener el índice del item seleccionado en el TreeView
            item_seleccionado = tree_inventario.focus()

            if item_seleccionado:
                # Mostrar un cuadro de diálogo de confirmación
                confirmar_eliminar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este producto?")

                if confirmar_eliminar:
                    # Obtener los valores de la fila seleccionada
                    valores = tree_inventario.item(item_seleccionado, 'values')

                    # Obtener el ID del producto seleccionado (asumiendo que el ID está en la primera columna)
                    id_producto = valores[0]  # Suponiendo que el ID del producto está en la primera columna

                    # Conectar a la base de datos
                    conn = sqlite3.connect('farmacia.db')
                    cursor = conn.cursor()

                    # Eliminar el producto de la tabla de productos
                    cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))

                    # Confirmar los cambios en la base de datos
                    conn.commit()

                    # Eliminar el producto seleccionado del TreeView
                    tree_inventario.delete(item_seleccionado)

                    # Mostrar mensaje de éxito
                    messagebox.showinfo("Éxito", "El producto se ha eliminado correctamente")
            else:
                # Si no se selecciona ningún elemento, mostrar un mensaje de advertencia
                messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para eliminar")

        except sqlite3.Error as e:
            # Mostrar mensaje de error específico de SQLite
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
        except Exception as e:
            # Mostrar mensaje de error genérico
            messagebox.showerror("Error", f"Ha ocurrido un error al eliminar el producto: {str(e)}")
        finally:
            # Cerrar la conexión a la base de datos si está abierta
            if conn:
                conn.close()

    def editar_producto(self, tree_inventario, nombre_producto_entry, descripcion_entry, precio_venta_entry, precio_compra_entry, existencias_entry, stock_minimo_entry, codigo_barras_entry, id_producto_entry):
        try:
            # Obtener el índice del item seleccionado en el TreeView
            item_seleccionado = tree_inventario.focus()

            if item_seleccionado:
                # Obtener los valores de la fila seleccionada
                valores = tree_inventario.item(item_seleccionado, 'values')

                # Actualizar self.editando_producto_id con el ID del producto que se está editando
                self.editando_producto_id = valores[0]

                # Llenar los campos del formulario con los valores obtenidos
                nombre_producto_entry.delete(0, 'end')
                nombre_producto_entry.insert(0, valores[1])
                descripcion_entry.delete(0, 'end')
                descripcion_entry.insert(0, valores[2])
                precio_venta_entry.delete(0, 'end')
                precio_venta_entry.insert(0, valores[3])
                precio_compra_entry.delete(0, 'end')
                precio_compra_entry.insert(0, valores[4])
                existencias_entry.delete(0, 'end')
                existencias_entry.insert(0, valores[5])
                stock_minimo_entry.delete(0, 'end')
                stock_minimo_entry.insert(0, valores[6])
                codigo_barras_entry.delete(0, 'end')
                codigo_barras_entry.insert(0, valores[7])

                # Llenar el campo de ID del producto
                id_producto_entry.delete(0, 'end')
                id_producto_entry.insert(0, self.editando_producto_id)
            else:
                # Si no se selecciona ningún elemento, mostrar un mensaje de advertencia
                messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para editar")

        except Exception as e:
            # Mostrar mensaje de error
            messagebox.showerror("Error", f"Ha ocurrido un error al editar el producto: {str(e)}")

    def limpiar_formulario(self,id_producto_entry,nombre_producto_entry,descripcion_entry,precio_venta_entry,precio_compra_entry,existencias_entry,stock_minimo_entry,codigo_barras_entry):
        # Limpiar todos los campos de entrada
        id_producto_entry.delete(0,'end')
        nombre_producto_entry.delete(0, 'end')
        descripcion_entry.delete(0, 'end')
        precio_venta_entry.delete(0, 'end')
        precio_compra_entry.delete(0, 'end')
        existencias_entry.delete(0, 'end')
        stock_minimo_entry.delete(0, 'end')
        codigo_barras_entry.delete(0, 'end')

    def actualizar_treeview(self, tree_inventario):
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('farmacia.db')
            cursor = conn.cursor()

            # Obtener los datos actualizados de productos de la base de datos
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            # Limpiar el TreeView antes de volver a cargar los datos
            tree_inventario.delete(*tree_inventario.get_children())

            # Insertar los nuevos datos en el TreeView
            for producto in productos:
                precio_venta = f"${producto[3]}"  # El índice 3 corresponde al precio de venta
                precio_compra = f"${producto[4]}"  # El índice 4 corresponde al precio de compra
                tree_inventario.insert("", "end", text="", values=(producto[0],producto[1], producto[2], precio_venta, precio_compra, producto[5], producto[6], producto[7]))

        except Exception as e:
            # Mostrar mensaje de error
            messagebox.showerror("Error", f"Ha ocurrido un error al actualizar el TreeView: {str(e)}")
        finally:
            # Cerrar la conexión a la base de datos
            if conn:
                conn.close()

    def cargar_excel(self, tree_inventario):
        try:
            # Abrir el cuadro de diálogo para seleccionar un archivo Excel
            filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

            # Conectar a la base de datos
            conn = sqlite3.connect('farmacia.db')
            cursor = conn.cursor()

            # Leer el archivo Excel directamente con openpyxl
            wb = openpyxl.load_workbook(filepath)
            sheet = wb.active

            # Contadores para el informe
            filas_procesadas = 0
            productos_insertados = 0

            # Iterar sobre cada fila del archivo Excel
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Obtener los valores de cada columna
                producto_id = row[0].strip() if row[0] and row[0].strip() else str(uuid.uuid4())[:8]  # Suponiendo que la primera columna es el ID
                nombre = row[1]
                descripcion = row[2]
                precio_venta = row[3]
                precio_compra = row[4]
                existencias = row[5]
                stock_minimo = row[6]
                codigo_barras = row[7]

                # Insertar los datos en la tabla de productos
                cursor.execute("INSERT INTO productos (id, nombre, descripcion, precio_venta, precio_compra, existencias, stock_minimo, codigo_barras) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (producto_id, nombre, descripcion, precio_venta, precio_compra, existencias, stock_minimo, codigo_barras))

                # Incrementar el contador de productos insertados
                productos_insertados += 1

                # Incrementar el contador de filas procesadas
                filas_procesadas += 1

            # Confirmar los cambios en la base de datos
            conn.commit()

            # Mostrar mensaje de éxito con el informe
            messagebox.showinfo("Éxito", f"Se procesaron {filas_procesadas} archivo(s) y se insertaron {productos_insertados} productos correctamente desde el (los) archivo Excel.")

            # Actualizar el TreeView con los nuevos datos
            self.actualizar_treeview(tree_inventario)

        except Exception as e:
            # Mostrar mensaje de error
            messagebox.showerror("Error", f"Ha ocurrido un error al cargar los productos desde el archivo Excel: {str(e)}")
        finally:
            # Cerrar la conexión a la base de datos
            if conn:
                conn.close()

    def descargar_productos_excel(event=None):
        try:
            # Conectar a la base de datos y obtener los datos de productos
            conn = sqlite3.connect('farmacia.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            
            # Crear un nuevo libro de Excel
            libro_excel = openpyxl.Workbook()
            hoja_excel = libro_excel.active
            hoja_excel.title = "productos"
            
            # Agregar encabezados de columna (asegúrate de que los nombres coincidan con los nombres de las columnas en la base de datos)
            hoja_excel.append(["id", "nombre", "descripcion", "precio_venta", "precio_compra", "existencias", "stock_minimo", "codigo_barras"])
            
            # Agregar datos de productos a las filas
            for producto in productos:
                hoja_excel.append(producto)
            
            # Crear una carpeta para el backup si no existe
            backup_folder = 'backup_productos'
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            
            # Generar el nombre del archivo con la fecha y hora del backup
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"productos_{timestamp}.xlsx"
            filepath = os.path.join(backup_folder, filename)
            
            # Guardar el archivo Excel en la carpeta de backup
            libro_excel.save(filepath)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"La tabla de productos se ha descargado correctamente como {filename}")
        except Exception as e:
            # Mostrar mensaje de error
            messagebox.showerror("Error", f"Ha ocurrido un error al descargar la tabla de productos: {str(e)}")
        finally:
            # Cerrar la conexión a la base de datos
            conn.close()

    def notificar_existencias_bajas(self, productos):
        # Verificar si hay algún producto con existencias menores a 10
        existencias_bajas = any(producto[5] < 10 for producto in productos)  # El índice 5 corresponde a las existencias

        # Actualizar la visibilidad y el texto de la etiqueta
        if existencias_bajas:
            self.notificacion_existencias_bajas.config(text="\uf06a Existencias Bajas, revisar botón: informe stock mínimo \uf06a", fg="red")
            self.notificacion_existencias_bajas.place(relx=0.7, rely=0.05, anchor='n')
            self.notificacion_existencias_bajas.lift()  # Traer la etiqueta al frente
        else:
            self.notificacion_existencias_bajas.place_forget()  # Ocultar la etiqueta si no hay existencias bajas

    def mostrar_informe_min_stock(self, productos):
        # Verificar si la ventana ya está abierta
        if hasattr(self, "informe_window") and self.informe_window.winfo_exists():
            self.informe_window.deiconify()  # Enfocar ventana existente si está abierta
            self.actualizar_informe_min_stock(productos)  # Actualizar contenido
            return
        
        # Crear una nueva ventana
        self.informe_window = tk.Toplevel(self.cuerpo_principal, background=COLOR_CUERPO_PRINCIPAL)
        self.informe_window.title("INFORME")
        self.informe_window.iconbitmap("./imagenes/logo.ico")
        self.informe_window.geometry("300x200")

        # Crear un Frame para contener el Treeview y el Scrollbar
        tree_frame = tk.Frame(self.informe_window)
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configurar el estilo
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font = ("OCR A Extended", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font = ("OCR A Extended", 9,"bold"))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        # Crear un Treeview en el frame con el estilo configurado
        self.informe_treeview = ttk.Treeview(tree_frame, style="mystyle.Treeview")
        self.informe_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar para el Treeview
        treeview_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.informe_treeview.yview)
        treeview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el comando de desplazamiento del Treeview
        self.informe_treeview.configure(yscrollcommand=treeview_scrollbar.set)

        # Configurar las columnas del Treeview
        self.informe_treeview["columns"] = ("Nombre", "Existencias")
        self.informe_treeview.heading("#0", text="ID", anchor="center")  # Oculta la columna de índice
        self.informe_treeview.heading("Nombre", text="Nombre")
        self.informe_treeview.heading("Existencias", text="Existencias")

        # Ajustar el ancho de las columnas
        self.informe_treeview.column("#0", width=0, stretch=tk.NO)  # Oculta la columna de índice
        self.informe_treeview.column("Nombre", width=150, anchor="center")
        self.informe_treeview.column("Existencias", width=100, anchor="center")

        # Obtener y agregar los productos al Treeview con existencias mínimas
        for producto in productos:
            if producto[5] < producto[6]:  # Verificar si las existencias son menores al stock mínimo
                self.informe_treeview.insert("", "end", values=(producto[1], producto[5]))
    
    def actualizar_informe_min_stock(self, productos):
        # Limpiar contenido anterior
        for item in self.informe_treeview.get_children():
            self.informe_treeview.delete(item)

        # Obtener y agregar los productos al Treeview con existencias mínimas
        for producto in productos:
            if producto[5] < producto[6]:  # Verificar si las existencias son menores al stock mínimo
                self.informe_treeview.insert("", "end", values=(producto[1], producto[5]))

    def agregar_producto_a_treeview(self, producto, tree_inventario):
        # Agregar el signo "$" al precio de venta y de compra
        precio_venta = f"${producto[3]}"
        precio_compra = f"${producto[4]}"

        # Configurar el ícono y los tags dinámicamente según las existencias
        if producto[5] < 10:
            existencias = f"\uf243 {producto[5]}"  # Agregar el icono correspondiente si existencias son menores que 10
            tags = ("rojo",)  # Marcar la fila con el tag "rojo"
        else:
            existencias = producto[5]  # No se agrega ningún icono si las existencias son mayores o iguales a 10
            tags = ()  # No se aplica ningún tag si las existencias son mayores o iguales a 10

        # Insertar el producto en el Treeview con los valores y tags correspondientes
        tree_inventario.insert("", "end", text="", values=(producto[0], producto[1], producto[2], precio_venta, precio_compra, existencias, producto[6], producto[7]), tags=tags)
        

#---------------------FUNCIONES PARA VENTAS--------------------------------

    def ventas(self):
        # Limpiar cualquier widget existente en el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

#-----------------------FRAMES -----------------------------------------------------------------------------------
        botones_accesos_rapidos = tk.LabelFrame(self.cuerpo_principal, background=COLOR_CUERPO_PRINCIPAL)
        botones_accesos_rapidos.pack(fill='x', padx=10, pady=(10, 0))
        

        filtrado_productos_venta = tk.LabelFrame(self.cuerpo_principal, text="BUSQUEDA PRODUCTOS", 
                                                 background=COLOR_CUERPO_PRINCIPAL, font=("OCR A Extended",12))
        filtrado_productos_venta.pack(fill='x', padx=10, pady=10)
       

        detalles_venta = tk.LabelFrame(self.cuerpo_principal, text="DETALLES", 
                                       background=COLOR_CUERPO_PRINCIPAL, font=("OCR A Extended",12))
        detalles_venta.pack(fill="x",side="left", padx=10, pady=(10, 0))
       

        detalles_acciones = tk.LabelFrame(self.cuerpo_principal, 
                                       background=COLOR_CUERPO_PRINCIPAL, font=("OCR A Extended",12))
        detalles_acciones.pack(fill="none",side="left", padx=10, pady=(10, 0))
       

        detalles_totales_frame = tk.LabelFrame(self.cuerpo_principal,text="TOTALES",
                                               background=COLOR_CUERPO_PRINCIPAL, font=("OCR A Extended",12))
        detalles_totales_frame.pack(fill="none",side="left", padx=10, pady=(10, 0))
       

        # Crear los botones de acceso rápido
        boton_nueva_venta = CTkButton(botones_accesos_rapidos, text="NUEVA\nVENTA",width=70,height=70,text_color='black',font=("OCR A Extended",12))
        boton_nueva_venta.grid(column=0, row=0, padx=10, pady=10)
        boton_nueva_venta.configure(command=lambda: self.restablecer_valores(entry_busqueda_producto, treeview, lbl_pro_sel, lbl_pro_descripcion,
                                                                     entry_precio_venta, entry_cantidad, lbl_subtotal_venta,
                                                                     detalles_treeview,entry_nombre_producto_noinv, entry_precio_producto_detalle, entry_cantidad_producto_detalle, lbl_total_venta))


        inicio_caja = CTkButton(botones_accesos_rapidos, text="INICIO\nDE\nOPERACIONES",width=70, height=70, text_color='black',font=("OCR A Extended",12))
        inicio_caja.grid(column=2,row=0, padx=10, pady=10)

        cierre_caja = CTkButton(botones_accesos_rapidos, text="CIERRE\nDE\nCAJA",width=70, height=70, text_color='black',font=("OCR A Extended",12))
        cierre_caja.grid(column=3,row=0, padx=10, pady=10)
        

        # Entry para ingresar el término de búsqueda
        entry_busqueda_producto = CTkEntry(filtrado_productos_venta, bg_color=COLOR_CUERPO_PRINCIPAL, width=300, 
                                        placeholder_text="\uf02a Ingrese Cod barras, Nombre o Descripcion",font=("OCR A Extended",14))
        entry_busqueda_producto.grid(column=0, row=0, padx=(10, 5), pady=10, sticky='ew')
        # Vincular la función de actualización al evento de modificación del Entry
        entry_busqueda_producto.bind('<KeyRelease>', lambda event: self.actualizar_filtrado(event, entry_busqueda_producto, treeview, lbl_pro_sel,lbl_pro_descripcion))

        # Crear el estilo para el Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('OCR A Extended', 10))
        style.configure("mystyle.Treeview.Heading", font=('OCR A Extended', 11, 'bold'))
        

        # Aplicar el estilo al Treeview
        treeview = ttk.Treeview(filtrado_productos_venta, columns=('id','Nombre', 
                                                                   'Descripción', 
                                                                   'Precio',
                                                                   'Existencias',
                                                                   'Codigo Barras'), height=5, style="mystyle.Treeview")
        treeview.grid(column=0, row=1, columnspan=1, padx=10, pady=10, sticky='nsew')
        
        # Ocultar las columnas
        for col in ['#0','#1', '#3', '#4', '#6']:
           treeview.column(col, width=0, stretch=tk.NO)
        for col in  ['#2','#5']:
           treeview.column(col, anchor="center")
       

        # Asignar los encabezados
        treeview.heading('#0', text="")
        treeview.heading('#1', text="id")
        treeview.heading('#2', text='Nombre')
        treeview.heading('#3', text='Descripción')
        treeview.heading('#4', text='Precio')
        treeview.heading('#5', text='Existencias')
        treeview.heading('#6', text='Codigo Barras')

        treeview.grid(column=0, row=1, columnspan=1)
                    
       # Fondo deseado
        fondo = "#F9F9FA"

        # Crear los widgets ScrolledText con el fondo deseado
        lbl_pro_sel = scrolledtext.ScrolledText(filtrado_productos_venta, wrap="word", width=20, height=2, font=('OCR A Extended', 13))
        lbl_pro_sel.grid(column=2, row=0, padx=(0, 10), pady=10, sticky='w')
        lbl_pro_sel.config(bg=fondo)  # Establecer el fondo

        lbl_pro_descripcion = scrolledtext.ScrolledText(filtrado_productos_venta, wrap="word", width=20, height=7, font=('OCR A Extended', 13))
        lbl_pro_descripcion.grid(column=2, row=1, columnspan=2, padx=(0, 10), pady=10, sticky='w')
        lbl_pro_descripcion.config(bg=fondo)  # Establecer el fondo

        separador1 = ttk.Separator(filtrado_productos_venta, orient="vertical")
        separador1.grid(column=3, row=0,rowspan=3, sticky="ns",padx=5,pady=5)
        
        entry_id_producto=tk.Entry(filtrado_productos_venta)
        entry_id_producto.grid_forget
        
        entry_nombre_producto_noinv = CTkEntry(filtrado_productos_venta, placeholder_text="INGRESE NOMBRE PRODUCTO",font=("OCR A Extended", 12),width=230)
        entry_nombre_producto_noinv.grid(column=4, row=0,columnspan=2)
        entry_nombre_producto_noinv.bind("<Button-1>",lambda event: self.deselect_item(event,lbl_pro_sel,lbl_pro_descripcion,treeview,
                                                                                       entry_precio_venta,entry_cantidad,entry_busqueda_producto,lbl_subtotal_venta))
        
        descripcion = 0

        entry_precio_venta = CTkEntry(filtrado_productos_venta, placeholder_text="PRECIO $", width=90, height=70, font=("OCR A Extended", 14))
        entry_precio_venta.grid(column=4, row=1)#, sticky="w", padx=5, pady=5)
        entry_precio_venta.bind('<KeyRelease>', lambda event: self.actualizar_precio_cantidad(event, entry_precio_venta, entry_cantidad, lbl_subtotal_venta))

        entry_cantidad = CTkEntry(filtrado_productos_venta, placeholder_text="CANTIDAD", width=90, height=70, font=("OCR A Extended", 14))
        entry_cantidad.grid(column=5, row=1)#, sticky='W', padx=5, pady=5)

        entry_cantidad.bind('<KeyRelease>', lambda event: self.actualizar_precio_cantidad(event, entry_precio_venta, entry_cantidad, lbl_subtotal_venta))
        entry_cantidad.bind("<Return>", lambda event: self.agregar_articulo(treeview, entry_cantidad, entry_precio_venta, entry_nombre_producto_noinv, detalles_treeview, lbl_total_venta))
        entry_cantidad.bind("<space>", lambda event: self.agregar_articulo(treeview, entry_cantidad, entry_precio_venta, entry_nombre_producto_noinv, detalles_treeview, lbl_total_venta))

        lbl_subtotal_venta = CTkLabel(filtrado_productos_venta, text="subtotal\n$", width=70, height=50, font=("OCR A Extended", 20), anchor="center", bg_color="#F9F9FA")
        lbl_subtotal_venta.grid(column=6, row=1,sticky='nwse', padx=10, pady=10)

        
        btn_agregar_articulo = CTkButton(filtrado_productos_venta, text="\uf217 Agregar\narticulo", width=70, height=70, font=("OCR A Extended", 14), 
                                         text_color='black', command=lambda: self.agregar_articulo(treeview, entry_cantidad, entry_precio_venta, entry_nombre_producto_noinv, detalles_treeview, lbl_total_venta))
        btn_agregar_articulo.grid(column=6, row=0,sticky='nwse', padx=10, pady=10)

        # Vincular la función de actualización del precio al evento de selección en el Treeview
        treeview.bind("<<TreeviewSelect>>", lambda event: self.actualizar_precio_venta(event, entry_precio_venta, treeview, 
                                                                                       entry_cantidad, lbl_subtotal_venta, lbl_pro_sel, descripcion, lbl_pro_descripcion,entry_id_producto))

        # Actualizar el filtrado para mostrar todos los productos inicialmente
        self.actualizar_filtrado(None, entry_busqueda_producto, treeview, lbl_pro_sel,lbl_pro_descripcion,entry_id_producto)
        # Llamar a actualizar_precio_venta al final de la función ventas
        self.actualizar_precio_venta(None, entry_precio_venta, treeview, entry_cantidad, lbl_subtotal_venta, lbl_pro_sel,entry_id_producto, None, None)

        # Crear el estilo para el Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('OCR A Extended', 10), background="#F9F9FA")
        style.configure("mystyle.Treeview.Heading", font=('OCR A Extended', 11, 'bold'), background="#F9F9FA")

        # Aplicar el estilo al Treeview
        detalles_treeview = ttk.Treeview(detalles_venta, columns=("id","Producto", "Cantidad", "Precio", "SubTotal"), 
                                        height=9, style="mystyle.Treeview")

        # Ocultar la primera columna
        detalles_treeview.column("#0", width=0, stretch=tk.NO)
        detalles_treeview.column("#1", width=0,stretch=tk.NO)
        # Configurar las columnas del Treeview
        detalles_treeview.heading("#0", text="")
        detalles_treeview.heading("#1", text="ID")
        detalles_treeview.heading("#2", text="Producto")
        detalles_treeview.heading("#3", text="Precio")
        detalles_treeview.heading("#4", text="Cantidad")
        detalles_treeview.heading("#5", text="Subtotal")

        # Ajustar el ancho de las columnas
        detalles_treeview.column("Producto", width=130, anchor="center")
        detalles_treeview.column("Cantidad", width=90, anchor="center")
        detalles_treeview.column("Precio", width=90, anchor="center")
        detalles_treeview.column("SubTotal", width=90, anchor="center")

        detalles_treeview.grid(column=0, row=0, columnspan=1, padx=10, pady=10, sticky='nsew')
        id_det=0
        detalles_treeview.bind("<<TreeviewSelect>>", lambda event: self.on_treeview_select(event, detalles_treeview, id_det, entry_id_producto_detalle, entry_precio_producto_detalle, entry_cantidad_producto_detalle, lbl_pro_sel, lbl_pro_descripcion, treeview, entry_precio_venta, entry_cantidad, entry_busqueda_producto, lbl_subtotal_venta))
        
        lbl_precio_producto_detalle =CTkLabel(detalles_acciones,text="PRECIO",font=("OCR A Extended",15))
        lbl_precio_producto_detalle.grid(column=2,row=0,padx=10,pady=10)

        entry_id_producto_detalle = tk.Entry(detalles_acciones)
        entry_id_producto_detalle.grid_forget

        entry_cantidad_producto_detalle = CTkEntry(detalles_acciones,placeholder_text="\uf53d", 
                                                 width=70,height=70,font=("OCR A Extended",20))
        entry_cantidad_producto_detalle .grid(column=2, row=1, padx=10, pady=10)

        lbl_cantidad_producto_detalle = CTkLabel(detalles_acciones,text="CANTIDAD",font=("OCR A Extended",15))
        lbl_cantidad_producto_detalle.grid(column=3, row=0, padx=10, pady=10)


        entry_precio_producto_detalle = CTkEntry(detalles_acciones,placeholder_text="\ue43c", 
                                                   width=70,height=70,font=("OCR A Extended",20))                                              
        entry_precio_producto_detalle.grid(column=3, row=1, padx=10, pady=10)

        
        boton_editar_detalle_venta = CTkButton(detalles_acciones, text="REALIZAR\nCAMBIO", 
                                       width=70, height=50, text_color='black', 
                                       font=("OCR A Extended", 12))
        boton_editar_detalle_venta.grid(column=3, row=2, padx=10, pady=10)
        producto=0
        boton_editar_detalle_venta.configure(command=lambda: self.editar_detalle_venta(detalles_treeview, entry_id_producto_detalle, 
                                                                                       entry_precio_producto_detalle, 
                                                                                       entry_cantidad_producto_detalle, lbl_total_venta))

        boton_borrar_detalle_venta = CTkButton(detalles_acciones, text="ELIMINAR\nPRODUCTO\nDE LA VENTA", 
                                        width=70, height=50, text_color='black', font=("OCR A Extended", 12),
                                        command=lambda: self.borrar_detalle_seleccionado(detalles_treeview,lbl_total_venta))
        boton_borrar_detalle_venta.grid(column=2, row=2, padx=10, pady=10)      


        separador1 = ttk.Separator(detalles_acciones, orient="vertical")
        separador1.grid(column=4, row=0,rowspan=3, sticky="ns",padx=5,pady=5)

        lbl_titulo01 = CTkLabel(detalles_acciones, text="TOTALES",
                                   font=("OCR A Extended",15),anchor="center")
        lbl_titulo01.grid(column=5, row=0,padx=5,pady=5)

        total_venta=0
        lbl_total_venta = CTkLabel(detalles_acciones, text="A pagar:\n${}".format(total_venta),
                           width=70, height=50, font=("OCR A Extended", 25),
                           anchor="center", bg_color="#F9F9FA", corner_radius=32)
        
        lbl_total_venta.grid(column=5, row=1,padx=5,pady=5)

        boton_grabar_venta = CTkButton(detalles_acciones, text="GRABAR\nVENTA",
                                       width=70, height=50, text_color='black',
                                       font=("OCR A Extended", 12),
                                       command=lambda: self.boton_grabar_venta(entry_busqueda_producto, treeview, lbl_pro_sel, lbl_pro_descripcion,
                       entry_precio_venta, entry_cantidad, lbl_subtotal_venta,
                       detalles_treeview, entry_precio_producto_detalle,
                       entry_nombre_producto_noinv, entry_cantidad_producto_detalle, lbl_total_venta))
        boton_grabar_venta.grid(column=5, row=2,padx=5,pady=5)
        
        self.calcular_total_venta(detalles_treeview,lbl_total_venta)


    def calcular_total_venta(self,detalles_treeview,lbl_total_venta):
            # Obtener todas las filas del Treeview de detalles de venta
            filas = detalles_treeview.get_children()

            # Inicializar el total de la venta
            total_venta = 0

            # Iterar sobre todas las filas y sumar los subtotales
            for fila in filas:
                subtotal = float(detalles_treeview.item(fila, 'values')[-1])
                total_venta += subtotal
                total_venta = round(total_venta,2)

            # Mostrar el total de la venta en la etiqueta
            lbl_total_venta.configure(text="A pagar:\n${}".format(total_venta))

    def actualizar_precio_cantidad(self, event=None, entry_precio_venta=None, entry_cantidad=None, lbl_subtotal_venta=None):
        if entry_precio_venta and entry_cantidad and lbl_subtotal_venta:
            precio = entry_precio_venta.get()
            cantidad = entry_cantidad.get()

            try:
                if precio and cantidad:  
                    precio_float = float(precio)
                    cantidad_int = int(cantidad)
                    subtotal = precio_float * cantidad_int
                    subtotal = round(subtotal, 2)  # limite decimales
                    lbl_subtotal_venta.configure(text=f'subtotal\n$ {subtotal}')
                else:
                    lbl_subtotal_venta.configure(text='subtotal\n$ 0.0')
            except ValueError:
                lbl_subtotal_venta.configure(text='')
      
    def actualizar_precio_venta(self, event, entry_precio_venta, treeview, entry_cantidad, lbl_subtotal_venta, lbl_pro_sel, descripcion, lbl_pro_descripcion,entry_id_producto):
        # Obtener el ítem seleccionado en el Treeview
        selected_item = treeview.focus()
        if selected_item:
            # Obtener los valores de la fila seleccionada
            values = treeview.item(selected_item)['values']
            # El nombre del producto está en la primera posición (índice 0)
            id_producto = values[0]
            nombre_producto = values[1]
            # El precio está en la tercera posición (índice 2)
            precio = values[3]
            descripcion = values[2]

            entry_id_producto.delete(0,tk.END)
            entry_id_producto.insert(tk.END,id_producto)

            # Actualizar el entry de precio con el valor seleccionado
            entry_precio_venta.delete(0, tk.END)
            entry_precio_venta.insert(0, precio)

            # Actualizar la etiqueta con el nombre del producto seleccionado
            lbl_pro_sel.delete("1.0",tk.END)
            lbl_pro_sel.insert(tk.END,nombre_producto)

            # Limpiar el ScrolledText y luego insertar la nueva descripción
            lbl_pro_descripcion.delete("1.0", tk.END)  # Limpiar el ScrolledText
            lbl_pro_descripcion.insert(tk.END, descripcion)  # Insertar la nueva descripción

             # Hacer que el cursor caiga en el entry de cantidad
            entry_cantidad.focus()

            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, "1")
            # Calcular el subtotal y actualizar la etiqueta
            self.actualizar_precio_cantidad(event, entry_precio_venta, entry_cantidad, lbl_subtotal_venta)

    def actualizar_filtrado(self, event, entry_busqueda_producto, treeview, lbl_pro_sel, lbl_pro_descripcion, entry_id_producto):
        # Obtener el texto de búsqueda
        texto_busqueda = entry_busqueda_producto.get()

        # Conectar a la base de datos y realizar la consulta
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Limpiar el Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Consultar la base de datos
        cursor.execute("SELECT id, nombre, descripcion, precio_venta, existencias, codigo_barras FROM productos WHERE nombre LIKE ? OR descripcion LIKE ? OR codigo_barras LIKE ?", ('%' + texto_busqueda + '%', '%' + texto_busqueda + '%', '%' + texto_busqueda + '%'))
        productos = cursor.fetchall()

        # Insertar los datos en el Treeview
        for producto in productos:
            treeview.insert('', 'end', values=producto)

        # Cerrar la conexión a la base de datos
        conn.close()

        # Verificar si hay algún producto seleccionado en el Treeview
        if not treeview.selection():
            # Si no hay ningún producto seleccionado, actualizar lbl_pro_sel y lbl_pro_descripcion
            lbl_pro_sel.delete("1.0", tk.END)  # Eliminar cualquier texto actual en lbl_pro_sel
            lbl_pro_sel.insert(tk.END, "NOMBRE")

            lbl_pro_descripcion.delete("1.0", tk.END)  # Limpiar el ScrolledText
            lbl_pro_descripcion.insert(tk.END, "DESCRIPCION")

            # También puedes limpiar el entry_id_producto si no hay selección
            entry_id_producto.delete(0, tk.END)
        else:
            # Si hay un producto seleccionado, obtener los valores y asignarlos a los widgets correspondientes
            selected_item = treeview.selection()
            values = treeview.item(selected_item)['values']

            # Asignar valores a los widgets
            entry_id_producto.delete(0, tk.END)
            entry_id_producto.insert(0, values[1])  # Asignar el ID al entry_id_producto

            lbl_pro_sel.delete("1.0", tk.END)
            lbl_pro_sel.insert(tk.END, values[2])  # Asignar el Nombre a lbl_pro_sel

            lbl_pro_descripcion.delete("1.0", tk.END)
            lbl_pro_descripcion.insert(tk.END, values[3])  # Asignar la Descripción a lbl_pro_descripcion

    def agregar_articulo(self, treeview, entry_cantidad, entry_precio_venta, entry_nombre_producto_noinv, detalles_treeview, lbl_total_venta):
        # Obtener el índice seleccionado en el Treeview de productos
        seleccion = treeview.selection()

        # Verificar si se ha seleccionado un producto desde el Treeview
        if seleccion:
            # Obtener los datos del producto seleccionado
            item = treeview.item(seleccion)
            id_producto_detalle = item['values'][0]
            nombre_producto = item['values'][1]
            precio_producto = float(item['values'][3])  # Convertir a float
        else:
            # Obtener los datos ingresados manualmente
            id_producto_detalle = self.generar_codigo_aleatorio()
            nombre_producto = entry_nombre_producto_noinv.get()
            precio_producto = entry_precio_venta.get()

        # Verificar si se proporcionó un nombre de producto y un precio válido
        if nombre_producto and precio_producto:
            try:
                # Verificar si el precio es un número positivo
                precio_producto = float(precio_producto)
                if precio_producto > 0:
                    # Obtener la cantidad especificada por el usuario
                    cantidad = entry_cantidad.get()

                    # Verificar si la cantidad es válida (es un número entero positivo)
                    if cantidad.isdigit() and int(cantidad) > 0:
                        # Verificar si el producto ya existe en el Treeview de detalles
                        productos_detalles = detalles_treeview.get_children()
                        producto_existente = False

                        for producto in productos_detalles:
                            valores = detalles_treeview.item(producto, 'values')
                            if valores[0] == id_producto_detalle:  # Comparar por ID en lugar de por nombre
                                producto_existente = True
                                break

                        if not producto_existente:
                            # Calcular el subtotal para el producto agregado
                            subtotal = int(cantidad) * float(precio_producto)
                            subtotal = round(subtotal, 2)

                            # Agregar una nueva fila al Treeview de detalles de venta con la información del producto y la cantidad
                            detalles_treeview.insert("", "end", values=(id_producto_detalle, nombre_producto, precio_producto, cantidad, subtotal))

                            # Limpiar los campos de entrada
                            entry_cantidad.delete(0, 'end')
                            entry_nombre_producto_noinv.delete(0, 'end')
                            entry_precio_venta.delete(0, 'end')

                            # Calcular y mostrar el total de la venta
                            self.calcular_total_venta(detalles_treeview, lbl_total_venta)
                        else:
                            # Mostrar un mensaje de error si el producto ya existe en detalles_treeview
                            messagebox.showerror("Error", "El producto ya existe en la lista de detalles, puedes editar ahí el precio y la cantidad a vender.")
                    else:
                        # Mostrar un mensaje de error si la cantidad no es válida
                        messagebox.showerror("Error", "La cantidad ingresada no es válida o no es un número entero positivo.")
                else:
                    # Mostrar un mensaje de error si el precio no es positivo
                    messagebox.showerror("Error", "El precio ingresado debe ser un número positivo.")
            except ValueError:
                # Mostrar un mensaje de error si el precio no es un número válido
                messagebox.showerror("Error", "El precio ingresado no es válido.")
        else:
            # Mostrar un mensaje de error si no se proporcionó nombre de producto o precio
            messagebox.showerror("Error", "Por favor, ingrese nombre de producto y precio antes de agregarlo a la venta.")

    def actualizar_campos_entrada(self, detalles_treeview,id_det,entry_id_producto_detalle, entry_precio_producto_detalle, entry_cantidad_producto_detalle):
        selected_item = detalles_treeview.focus()

        if selected_item:
            values = detalles_treeview.item(selected_item)['values']
            id_det = values[0]
            nombre_producto = values[1]
            cantidad = values[2]
            precio = values[3]


            entry_id_producto_detalle.delete(0, 'end')
            entry_cantidad_producto_detalle.delete(0, 'end')
            entry_precio_producto_detalle.delete(0, 'end')

            entry_id_producto_detalle.insert(0, id_det)
            entry_cantidad_producto_detalle.insert(0, cantidad)
            entry_precio_producto_detalle.insert(0, precio)

    def borrar_detalle_seleccionado(self, detalles_treeview,lbl_total_venta):
        selected_item = detalles_treeview.selection()

        if selected_item:
            detalles_treeview.delete(selected_item)
            
            self.calcular_total_venta(detalles_treeview,lbl_total_venta)
    
    def editar_detalle_venta(self, detalles_treeview, entry_id_producto_detalle, entry_precio_producto_detalle, entry_cantidad_producto_detalle, lbl_total_venta):
        # Obtener la fila seleccionada en el Treeview de detalles
        selected_item = detalles_treeview.selection()

        if selected_item:
            try:
                # Obtener los nuevos valores desde los campos de entrada
                id_producto_detalle = entry_id_producto_detalle.get()
                producto_original = detalles_treeview.item(selected_item, 'values')[1]
                cantidad = entry_cantidad_producto_detalle.get()
                precio = float(entry_precio_producto_detalle.get())

                # Validar que los nuevos valores sean válidos
                if cantidad and isinstance(float(cantidad), float) and float(cantidad) > 0 and precio > 0:

                    # Actualizar los valores en el Treeview de detalles
                    subtotal = round(float(cantidad) * precio, 2)
                    detalles_treeview.item(selected_item, values=(id_producto_detalle, producto_original, cantidad, precio, subtotal))

                    self.calcular_total_venta(detalles_treeview,lbl_total_venta)

                    # Limpiar los campos de entrada
                    entry_id_producto_detalle.delete(0, 'end')
                    entry_cantidad_producto_detalle.delete(0, 'end')
                    entry_precio_producto_detalle.delete(0, 'end')
                else:
                    # Mostrar un mensaje de error si los nuevos valores no son válidos
                    messagebox.showerror("Error", "Por favor, ingrese valores válidos para la cantidad y el precio.")
            except ValueError:
                # Mostrar un mensaje de error si los nuevos valores no son números válidos
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para la cantidad y el precio.")
        else:
            # Mostrar un mensaje de error si no se seleccionó ninguna fila para editar
            messagebox.showerror("Error", "Por favor, seleccione una fila para editar en el Treeview de detalles.")


   









    def boton_grabar_venta(self, entry_busqueda_producto, treeview, lbl_pro_sel, lbl_pro_descripcion,
                       entry_precio_venta, entry_cantidad, lbl_subtotal_venta,
                       detalles_treeview, entry_precio_producto_detalle,
                       entry_nombre_producto_noinv, entry_cantidad_producto_detalle, lbl_total_venta):
        # Obtener la fecha y hora actual
        fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #id_venta = self.generar_codigo_aleatorio()
        id_cliente = self.generar_codigo_aleatorio()
        metodo_pago = "Contado"
        
        # Conectar a la base de datos
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        try:
            # Crear la tabla de ventas si no existe
            cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                    id TEXT PRIMARY KEY,
                    id_producto TEXT,
                    producto TEXT,
                    id_cliente TEXT,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    total REAL,
                    metodo_pago TEXT,
                    fecha_hora DATE,
                    FOREIGN KEY (id_producto) REFERENCES productos (id)
                )''')

            # Obtener todas las filas del Treeview de detalles de venta
            filas = detalles_treeview.get_children()

            # Iterar sobre todas las filas y grabar cada detalle de venta en la base de datos
            for fila in filas:
                valores = detalles_treeview.item(fila, 'values')
                id_detalle_venta = self.generar_codigo_aleatorio()  # Generar un nuevo ID de venta para cada detalle
                id_producto = valores[0]  # Obtener el ID del producto
                nombre_producto = valores[1]
                cantidad = float(valores[3])  # Obtener la cantidad
                precio_unitario = float(valores[2])
                subtotal = float(valores[4])  # Obtener el subtotal

                # Insertar el detalle de venta en la tabla de ventas
                cursor.execute('''
                    INSERT INTO ventas (id, id_producto, producto, id_cliente, cantidad, precio_unitario, total, metodo_pago, fecha_hora)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (id_detalle_venta, id_producto, nombre_producto, id_cliente, cantidad, precio_unitario, subtotal, metodo_pago, fecha_venta))

            # Confirmar la transacción y cerrar la conexión
            conn.commit()
            conn.close()

            # Limpiar el Treeview de detalles de venta después de grabar la venta
            detalles_treeview.delete(*filas)
            
            # Restablecer valores
            self.restablecer_valores(entry_busqueda_producto, treeview, lbl_pro_sel, lbl_pro_descripcion,
                                entry_precio_venta, entry_cantidad, lbl_subtotal_venta,
                                detalles_treeview, entry_precio_producto_detalle,
                                entry_nombre_producto_noinv, entry_cantidad_producto_detalle, lbl_total_venta)

            # Mostrar un mensaje de éxito
            messagebox.showinfo("Venta grabada", "La venta se ha grabado exitosamente en la base de datos.")

        except sqlite3.Error as e:
            # Manejar cualquier error en la operación de la base de datos
            messagebox.showerror("Error", f"No se pudo grabar la venta en la base de datos.\nError: {e}")

            # Cerrar la conexión en caso de error
            conn.close()








    def generar_codigo_aleatorio(self):
        # Definir la longitud del código
        longitud = 8

        # Crear una lista que contenga dígitos y letras
        caracteres = string.digits + string.ascii_letters

        # Generar el código aleatorio utilizando random.choice
        codigo_aleatorio = ''.join(random.choice(caracteres) for _ in range(longitud))

        return codigo_aleatorio

    def deselect_item(self,event,lbl_pro_sel,lbl_pro_descripcion,treeview,entry_precio_venta,entry_cantidad,entry_busqueda_producto,lbl_subtotal_venta):
        treeview.selection_remove(treeview.selection())
        lbl_pro_sel.delete(1.0, tk.END)
        lbl_pro_sel.insert(tk.END,"NOMBRE")
        lbl_pro_descripcion.delete(1.0, tk.END)
        lbl_pro_descripcion.insert(tk.END, "DESCRIPCION")
        entry_precio_venta.delete(0, tk.END)
        entry_precio_venta._activate_placeholder()  
        entry_cantidad.delete(0, tk.END)
        entry_cantidad._activate_placeholder()  
        entry_busqueda_producto.delete(0, tk.END)
        entry_busqueda_producto._activate_placeholder()
        lbl_subtotal_venta.configure(text="subtotal\n$")

    def restablecer_valores(self, entry_busqueda_producto, treeview, lbl_pro_sel, lbl_pro_descripcion,
                        entry_precio_venta, entry_cantidad, lbl_subtotal_venta,
                        detalles_treeview, entry_precio_producto_detalle,entry_nombre_producto_noinv, entry_cantidad_producto_detalle, lbl_total_venta):
        # Restablecer valores de Entry

        entry_busqueda_producto.delete(0, tk.END)
        entry_precio_venta.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_cantidad._activate_placeholder()
        
        entry_precio_producto_detalle.delete(0, tk.END)
        entry_cantidad_producto_detalle.delete(0, tk.END)
        entry_precio_producto_detalle._activate_placeholder()
        entry_cantidad_producto_detalle._activate_placeholder()
        # Restablecer valores 
        lbl_pro_sel.delete(1.0, tk.END)
        lbl_pro_sel.insert(tk.END,"NOMBRE")
        lbl_pro_descripcion.delete(1.0, tk.END)
        lbl_pro_descripcion.insert(tk.END, "DESCRIPCION")
        lbl_subtotal_venta.configure(text="subtotal\n$")
        
        treeview.selection_remove(treeview.selection())    

        # Restablecer valores de Treeview de detalles
        detalles_treeview.delete(*detalles_treeview.get_children())
        entry_busqueda_producto._activate_placeholder()
        entry_precio_venta._activate_placeholder()
        # Restablecer valores de lbl_total_venta
        lbl_total_venta.configure(text="A pagar:\n$")  # Puedes establecer otro valor por defecto si es necesario
        entry_nombre_producto_noinv._activate_placeholder()

    def on_treeview_select(self, event, detalles_treeview, id_det, entry_id_producto_detalle, entry_precio_producto_detalle, entry_cantidad_producto_detalle, lbl_pro_sel, lbl_pro_descripcion, treeview, entry_precio_venta, entry_cantidad, entry_busqueda_producto, lbl_subtotal_venta):
        # Update entry fields with selected item data
        self.actualizar_campos_entrada(detalles_treeview, id_det, entry_id_producto_detalle, entry_precio_producto_detalle, entry_cantidad_producto_detalle)
        
        # Deselect item and update related fields
        self.deselect_item(event, lbl_pro_sel, lbl_pro_descripcion, treeview, entry_precio_venta, entry_cantidad, entry_busqueda_producto, lbl_subtotal_venta)

    

""""

#------------------------FUNCIONES PARA CLIENTE-------------------------------

    def mostrar_clientes(self):
        # Definir el estilo general para los botones
        ESTILO_CTKBOTONES = {
            'width': 70,
            'height': 70,
            'text_color': 'black',
            'font': ("OCR A Extended", 13,"bold")
        }
        # Función para mostrar la lista de clientes
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
        

        frame_tree_clientes = tk.Frame(self.cuerpo_principal,bg=COLOR_CUERPO_PRINCIPAL)
        frame_tree_clientes.pack(pady=10, padx=10, side="right", fill="both", expand=True)
        
        # Crear el estilo para el Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('OCR A Extended', 10))
        style.configure("mystyle.Treeview.Heading", font=('OCR A Extended', 11, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Aplicar el estilo al Treeview
        tabla_cliente = ttk.Treeview(frame_tree_clientes, columns=("Cédula", "Nombre", "Teléfono", "Dirección", "Email"), displaycolumns=("Cédula", "Nombre", "Teléfono", "Dirección", "Email"), style="mystyle.Treeview")
        tabla_cliente.heading("#0", text="", anchor="center")  # Eliminar encabezado de índice
        tabla_cliente.heading("Cédula", text="CEDULA")
        tabla_cliente.heading("Nombre", text="NOMBRE")
        tabla_cliente.heading("Teléfono", text="TELEFONO")
        tabla_cliente.heading("Dirección", text="DIRECCION")
        tabla_cliente.heading("Email", text="EMAIL")
        tabla_cliente.column("#0", width=0, stretch=tk.NO)  # Hacer que la columna de índice no sea visible
        tabla_cliente.column("Cédula", width=70)
        tabla_cliente.column("Nombre", width=110)
        tabla_cliente.column("Teléfono", width=70)
        tabla_cliente.column("Dirección", width=120)
        tabla_cliente.column("Email", width=150)
        tabla_cliente.pack(side="top", expand=True, fill="both")

        # Botón Editar
        btn_editar = CTkButton(frame_tree_clientes, text="Editar", **ESTILO_CTKBOTONES)
        btn_editar.pack(side="left", padx=5, pady=5)

        # Botón Eliminar
        btn_eliminar = CTkButton(frame_tree_clientes, text="Eliminar", **ESTILO_CTKBOTONES)
        btn_eliminar.pack(side="left", padx=5, pady=5)

        # Formulario de ingreso de cliente
        frame_formulario_cliente = tk.Frame(self.cuerpo_principal,bg=COLOR_CUERPO_PRINCIPAL)
        frame_formulario_cliente.pack(pady=10, side="left")

        lbl_titulo = CTkLabel(frame_formulario_cliente, text="Ingreso de Clientes", font=("OCR A Extended", 12, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        lbl_id = CTkLabel(frame_formulario_cliente, text="id:",font=("OCR A Extended", 10, "bold"))
        lbl_id.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_id = CTkEntry(frame_formulario_cliente,font=("OCR A Extended", 10, "bold"))
        entry_id.grid(row=2, column=1, padx=5, pady=5)
    
        lbl_cedula = CTkLabel(frame_formulario_cliente, text="Cédula:",font=("OCR A Extended", 10, "bold"))
        lbl_cedula.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_cedula = CTkEntry(frame_formulario_cliente,font=("OCR A Extended", 10, "bold"))
        entry_cedula.grid(row=3, column=1, padx=5, pady=5)

        lbl_nombre = CTkLabel(frame_formulario_cliente, text="Nombre:",font=("OCR A Extended", 10, "bold"))
        lbl_nombre.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        entry_nombre = CTkEntry(frame_formulario_cliente,font=("OCR A Extended", 10, "bold"))
        entry_nombre.grid(row=4, column=1, padx=5, pady=5)

        lbl_telefono = CTkLabel(frame_formulario_cliente, text="Teléfono:",font=("OCR A Extended", 10, "bold"))
        lbl_telefono.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        entry_telefono = CTkEntry(frame_formulario_cliente,font=("OCR A Extended", 10, "bold"))
        entry_telefono.grid(row=5, column=1, padx=5, pady=5)

        lbl_direccion = CTkLabel(frame_formulario_cliente, text="Dirección:",font=("OCR A Extended", 10, "bold"))
        lbl_direccion.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        entry_direccion = CTkEntry(frame_formulario_cliente,font=("OCR A Extended", 10, "bold"))
        entry_direccion.grid(row=6, column=1, padx=5, pady=5)

        lbl_email = CTkLabel(frame_formulario_cliente, text="Email:",font=("OCR A Extended", 10, "bold"))
        lbl_email.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        entry_email = CTkEntry(frame_formulario_cliente,font=("OCR A Extended", 10, "bold"))
        entry_email.grid(row=7, column=1, padx=5, pady=5)

        btn_guardar = CTkButton(frame_formulario_cliente, text="Guardar",**ESTILO_CTKBOTONES)
        btn_guardar.grid(row=8, column=1, padx=5, pady=5, sticky="ns")
        
#--------------------------FUNCIONES PARA DATOS DEL NEGOCIO--------------------------------
    def datos_negocio(self):

        # Definir el estilo general para los botones
        ESTILO_CTKBOTONES_DATOS_NEGO = {
            'width': 50,
            'height': 50,
            'text_color': 'black',
            'font': ("OCR A Extended", 13,"bold")
        }

        ESTILO_TITULO_LABEL_DATOS_NEGO = {
            'text_color': 'black',
            'font': ("OCR A Extended", 15, "bold"),  
        }

        ESTILO_ENTRYS_LABEL_DATOS_NEGO = {
            'text_color': 'black',
            'font': ("OCR A Extended", 13),
            'width': 200      
        }

        global conexion, cursor
        conexion = sqlite3.connect('farmacia.db')
        cursor = conexion.cursor()
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        def generar_clave():
            caracteres = string.ascii_letters + string.digits
            return ''.join(random.choice(caracteres) for _ in range(8))

        def insertar_datos(conexion):
            try:
                # Obtener los valores de los campos de entrada
                datos = (nombre_negocio.get(), ruc.get(), direccion.get(), telefono.get(), email.get())

                # Verificar si hay datos existentes
                cursor.execute('SELECT COUNT(*) FROM datos_negocio')
                count = cursor.fetchone()[0]

                if count == 0:
                    # Si no hay registros, insertar uno nuevo
                    cursor.execute('INSERT INTO datos_negocio (nombre_negocio, ruc, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)', datos)
                else:
                    # Si ya hay un registro, actualizarlo
                    cursor.execute('UPDATE datos_negocio SET nombre_negocio=?, ruc=?, direccion=?, telefono=?, email=?', datos)

                conexion.commit()
                mostrar_datos_actuales()
                messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron guardar los datos. Error: {str(e)}")



                # Función para llenar los entrys con los datos actuales del negocio
        def llenar_entrys():
            cursor.execute('SELECT * FROM datos_negocio')
            datos = cursor.fetchone()
            if datos:
                # Obtener el id del registro actual para su posterior actualización
                id_registro = datos[0]

                # Actualizar los campos de entrada con los datos recuperados de la base de datos
                nombre_negocio.delete(0, 'end')
                nombre_negocio.insert(0, datos[1])
                ruc.delete(0, 'end')
                ruc.insert(0, datos[2])
                direccion.delete(0, 'end')
                direccion.insert(0, datos[3])
                telefono.delete(0, 'end')
                telefono.insert(0, datos[4])
                email.delete(0, 'end')
                email.insert(0, datos[5])

                # Retornar el id del registro actual para su posterior uso en la actualización
                return id_registro
            else:
                messagebox.showerror("Error", "No hay datos para mostrar.")
                return None


        # Función para mostrar los datos actuales del negocio sin llenar los entrys
        def mostrar_datos_actuales():
            cursor.execute('SELECT * FROM datos_negocio')
            datos = cursor.fetchone()
            if datos:
                lbl_nombre.configure(text=datos[1])
                lbl_ruc.configure(text=datos[2])
                lbl_direccion.configure(text=datos[3])
                lbl_telefono.configure(text=datos[4])
                lbl_email.configure(text=datos[5])

        # Crear Frames
        frame_formulario = tk.Frame(self.cuerpo_principal,bg=COLOR_CUERPO_PRINCIPAL)
        frame_formulario.grid(row=0,columnspan=2,column=0, padx=10, pady=10)

        frame_datos_actuales = tk.Frame(self.cuerpo_principal,bg=COLOR_CUERPO_PRINCIPAL)
        frame_datos_actuales.grid(row=1, column=0, padx=10, pady=10)

        # Crear etiquetas y entradas para el formulario
        lbl_titulo_formulario_nego = CTkLabel(frame_formulario, text="I N G R E S O   D E   D A T O S",**ESTILO_TITULO_LABEL_DATOS_NEGO )
        lbl_titulo_formulario_nego.grid(row=0, columnspan=2, padx=5, pady=5, sticky="w")

        CTkLabel(frame_formulario, text="Nombre del Negocio:",**ESTILO_ENTRYS_LABEL_DATOS_NEGO).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        nombre_negocio = CTkEntry(frame_formulario,**ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        nombre_negocio.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        CTkLabel(frame_formulario, text="RUC:",**ESTILO_ENTRYS_LABEL_DATOS_NEGO).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ruc = CTkEntry(frame_formulario,**ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        ruc.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        CTkLabel(frame_formulario, text="Dirección:",**ESTILO_ENTRYS_LABEL_DATOS_NEGO).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        direccion = CTkEntry(frame_formulario,**ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        direccion.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        CTkLabel(frame_formulario, text="Teléfono:",**ESTILO_ENTRYS_LABEL_DATOS_NEGO).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        telefono = CTkEntry(frame_formulario,**ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        telefono.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        CTkLabel(frame_formulario, text="Email:",**ESTILO_ENTRYS_LABEL_DATOS_NEGO).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        email = CTkEntry(frame_formulario,**ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        email.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        # Botón para guardar los datos
        btn_guardar = CTkButton(frame_formulario, text="Guardar Datos", **ESTILO_CTKBOTONES_DATOS_NEGO, command=lambda: insertar_datos(conexion))
        btn_guardar.grid(row=6, columnspan=2, padx=5, pady=5)
        
        # Crear etiquetas para mostrar los datos actuales del negocio
        lbl_nombre = CTkLabel(frame_datos_actuales, text="", **ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        lbl_nombre.grid(row=0, padx=5, pady=5, sticky="nsew")

        lbl_ruc = CTkLabel(frame_datos_actuales, text="", **ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        lbl_ruc.grid(row=1, padx=5, pady=5, sticky="nsew")

        lbl_direccion = CTkLabel(frame_datos_actuales, text="", **ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        lbl_direccion.grid(row=2, padx=5, pady=5, sticky="nsew")

        lbl_telefono = CTkLabel(frame_datos_actuales, text="", **ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        lbl_telefono.grid(row=3, padx=5, pady=5, sticky="nsew")

        lbl_email = CTkLabel(frame_datos_actuales, text="", **ESTILO_ENTRYS_LABEL_DATOS_NEGO)
        lbl_email.grid(row=4, padx=5, pady=5, sticky="nsew")

        # Crear botón "Editar" para llenar los entrys con los datos actuales
        btn_editar = CTkButton(frame_datos_actuales, text="Editar Datos", **ESTILO_CTKBOTONES_DATOS_NEGO, command=llenar_entrys)
        btn_editar.grid(row=5, padx=5, pady=5, sticky="nsew")

        mostrar_datos_actuales()
   

"""




# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('farmacia.db')
cursor = conn.cursor()

# Crear la tabla de productos
cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio_venta REAL,
                    precio_compra REAL,
                    existencias INTEGER,
                    stock_minimo INTEGER,
                    codigo_barras TEXT        
                )''')

# Crear la tabla de ventas
cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                    id TEXT PRIMARY KEY,
                    id_producto TEXT,
                    producto TEXT,
                    id_cliente TEXT,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    total REAL,
                    metodo_pago TEXT,
                    fecha_hora DATE,
                    FOREIGN KEY (id_producto) REFERENCES productos (id)
                )''')



# Crear la tabla de proveedores
cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    contacto TEXT
                )''')

# Crear la tabla de clientes
cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    cedula TEXT,
                    direccion TEXT,
                    telefono TEXT,
                    Email TEXT
                )''')

# Crear la tabla de datos negocio
cursor.execute('''CREATE TABLE IF NOT EXISTS datos_negocio (
                    id TEXT PRIMARY KEY,
                    nombre_negocio TEXT NOT NULL,
                    ruc TEXT,
                    direccion TEXT,
                    telefono TEXT,
                    Email TEXT
                )''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()