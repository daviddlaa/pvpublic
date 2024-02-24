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



class FormularioMaestroDesing(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/logo.png",(560,136))
        self.perfil = util_img.leer_imagen("./imagenes/perfil.png",(100,100))
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

       
        self.labelTitulo = tk.Label(
            self.barra_superior,text="@bacosoluciones")
        self.labelTitulo.config(
            fg="#fff",font=("Roboto",10),bg=COLOR_BARRA_SUPERIOR,padx=10,width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAweson',size=15)

        self.labelPerfil =tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP,pady=10)

        self.buttonInventario = tk.Button(self.menu_lateral,command=self.Inventario) 
        self.buttonIngresoVentas = tk.Button(self.menu_lateral) 
        self.buttonHistorialVentas = tk.Button(self.menu_lateral) 
        self.buttonProveedores= tk.Button(self.menu_lateral) 
        self.buttonClientes = tk.Button(self.menu_lateral)
        self.buttonDatosNegocio = tk.Button(self.menu_lateral)
        self.buttonUsuarios = tk.Button(self.menu_lateral)
     
        buttons_info = [
        ("Inventario", "\uf494", self.buttonInventario), 
        ("Ingreso Ventas", "\uf788", self.buttonIngresoVentas), 
        ("Historial Ventas", "\uf07a", self.buttonHistorialVentas), 
        ("Proveedores", "\ue58d", self.buttonProveedores),
        ("Clientes", "\uf007", self.buttonClientes),
        ("Datos Negocio", "\uf54e", self.buttonDatosNegocio),
        ("Usuarios", "\ue594", self.buttonUsuarios),
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)
    
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
    


    #funciones para el inventario
    
    def Inventario(self):
        # Limpiar cualquier widget existente en el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()
            
        # Crear un formulario para agregar nuevos elementos al inventario
        formulario_inventario = tk.Frame(self.cuerpo_principal, bg=COLOR_CUERPO_PRINCIPAL)
        formulario_inventario.pack(padx=20, pady=20, fill='both', expand=True)

        # Etiquetas y campos de entrada para el formulario_inventario
        CTkLabel(formulario_inventario,text="INGRESO DE PRODUCTOS",font=("Roboto",17)).grid(row=0,column=0,sticky="ns",padx=5,pady=5,columnspan=2)

        #dentry para id OCULTO
        id_producto_entry = tk.Entry(formulario_inventario,)
        id_producto_entry.grid(row=1, column=1, padx=5, pady=5)
        id_producto_entry.grid_remove()
      
        CTkLabel(formulario_inventario, text="Nombre:",font=("Roboto",16)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        nombre_producto_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        nombre_producto_entry.grid(row=2, column=1, padx=5, pady=5)

        CTkLabel(formulario_inventario, text="Descripción:",font=("Roboto",16)).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        descripcion_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        descripcion_entry.grid(row=3, column=1, padx=5, pady=5)

        CTkLabel(formulario_inventario, text="Precio venta:",font=("Roboto",16)).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        precio_venta_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        precio_venta_entry.grid(row=4, column=1, padx=5, pady=5)

        CTkLabel(formulario_inventario, text="Precio compra:",font=("Roboto",16)).grid(row=5, column=0, sticky='w', padx=5, pady=5)
        precio_compra_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        precio_compra_entry.grid(row=5, column=1, padx=5, pady=5)

        CTkLabel(formulario_inventario, text="Existencias:",font=("Roboto",16)).grid(row=6, column=0, sticky='w', padx=5, pady=5)
        existencias_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        existencias_entry.grid(row=6, column=1, padx=5, pady=5)

        CTkLabel(formulario_inventario, text="Stock Min:",font=("Roboto",16)).grid(row=7, column=0, sticky='w', padx=5, pady=5)
        stock_minimo_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        stock_minimo_entry.grid(row=7, column=1, padx=5, pady=5)

        CTkLabel(formulario_inventario, text="Codigo de barras:",font=("Roboto",16)).grid(row=8, column=0, sticky='w', padx=5, pady=5)
        codigo_barras_entry = CTkEntry(formulario_inventario,font=("Roboto",16))
        codigo_barras_entry.grid(row=8, column=1, padx=5, pady=5)

        # Actualizar la descripción al principio
    
      # Botón para agregar el producto al inventario
        agregar_button = CTkButton(formulario_inventario, text="\uf055 Agregar Producto", 
                                    command=lambda: self.agregar_producto(tree_inventario, nombre_producto_entry, descripcion_entry, 
                                                                        precio_venta_entry, precio_compra_entry, existencias_entry, 
                                                                        stock_minimo_entry, codigo_barras_entry, id_producto_entry), text_color="black")
        agregar_button.grid(row=9, column=1, padx=5, pady=5)

        # Botón para limpiar el formulario
    
        limpiar_formulario_button = CTkButton(formulario_inventario, text="\uf87d Limpiar formulario", text_color="black", command=lambda: self.limpiar_formulario(id_producto_entry,nombre_producto_entry,descripcion_entry,precio_venta_entry,precio_compra_entry,existencias_entry,stock_minimo_entry,codigo_barras_entry))
        limpiar_formulario_button.grid(row=9, column=0, padx=5, pady=5)

        # Crear y empaquetar el label para la descripción del producto
        self.descripcion_info_producto = tk.Label(formulario_inventario,font=("Roboto", 16),wraplength=500,background=COLOR_CUERPO_PRINCIPAL,justify="left")
        self.descripcion_info_producto.place(relx=0.5, rely=0.3, anchor='nw')

        # Crear y empaquetar el label para la notificación de existencias bajas
        self.notificacion_existencias_bajas = tk.Label(formulario_inventario,font=("Roboto", 14), fg="red", background=COLOR_CUERPO_PRINCIPAL,wraplength=300)

        self.lbl_buscar = CTkLabel(formulario_inventario,text="Buscar producto:",font=("Roboto",16))
        self.lbl_buscar.place(relx=0.60, rely=0.85, anchor='e')

        self.entry_buscar = CTkEntry(formulario_inventario,height=30,width=150,font=("Roboto",16),placeholder_text="\uf002")
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
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Roboto', 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Roboto', 11, 'bold'))  # Modify the font of the headings
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
        
        for producto in productos:
            self.agregar_producto_a_treeview(producto, tree_inventario)

        self.actualizar_descripcion(None, tree_inventario)

        # Obtener la descripción seleccionada
        descripcion_seleccionada = "Descripción seleccionada"

        # Crear o actualizar la descripción
        self.actualizar_descripcion(descripcion_seleccionada, tree_inventario)
        self.notificar_existencias_bajas(productos)

        buttons_frame = tk.Frame(treeview_frame,background=COLOR_CUERPO_PRINCIPAL)
        buttons_frame.grid(row=0, column=2, sticky="ns")

        # Crear los botones de editar y eliminar
        editar_button = CTkButton(buttons_frame, text="\uf044"" Editar",text_color="black", command=lambda: self.editar_producto(tree_inventario, nombre_producto_entry, descripcion_entry, precio_venta_entry, precio_compra_entry, existencias_entry, stock_minimo_entry, codigo_barras_entry, id_producto_entry))
        editar_button.pack(side="top", padx=5, pady=5)

        eliminar_button = CTkButton(buttons_frame, text="\uf056"" Eliminar",text_color="black", command=lambda: self.eliminar_producto(tree_inventario))
        eliminar_button.pack(side="top", padx=5, pady=5)

        cargar_button = CTkButton(buttons_frame, text="\uf093"" Cargar Excel",text_color="black",command=lambda: self.cargar_excel(tree_inventario))
        cargar_button.pack(side="top", padx=5, pady=5)

        descargar_button = CTkButton(buttons_frame, text="\uf019 Respaldo", text_color="black", command=self.descargar_productos_excel)
        descargar_button.pack(side="top", padx=5, pady=5)

        # Verificar si hay existencias mínimas en la lista de productos
        existencias_minimas = any(producto[5] < producto[6] for producto in productos)

        # Crear el botón con la opción de habilitarlo o deshabilitarlo según la condición
        informe_stock_min_button = CTkButton(buttons_frame, text="\uf15b"" Informe Mín. Stock", text_color="black", command=lambda: self.mostrar_informe_min_stock(productos))
        if existencias_minimas:
            informe_stock_min_button.configure(state="normal")  # Habilitar el botón si hay existencias mínimas
        else:
            informe_stock_min_button.configure(state="disabled")  # Deshabilitar el botón si no hay existencias mínimas
        informe_stock_min_button.pack(side="top", padx=5, pady=5)


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
        self.agregar_producto_a_treeview  # No estoy seguro de qué hace esta línea, así que la he mantenido

    def mostrar_informe_min_stock(self, productos):
        # Crear una nueva ventana
        informe_window = tk.Toplevel(self.cuerpo_principal, background=COLOR_CUERPO_PRINCIPAL)
        informe_window.title("INFORME")
        informe_window.iconbitmap("./imagenes/logo.ico")
        informe_window.geometry("300x200")

        # Crear un Frame para contener el Treeview y el Scrollbar
        tree_frame = tk.Frame(informe_window)
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configurar el estilo
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Roboto', 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Roboto', 11, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        # Crear un Treeview en el frame con el estilo configurado
        informe_treeview = ttk.Treeview(tree_frame, style="mystyle.Treeview")
        informe_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un Scrollbar para el Treeview
        treeview_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=informe_treeview.yview)
        treeview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el comando de desplazamiento del Treeview
        informe_treeview.configure(yscrollcommand=treeview_scrollbar.set)

        # Configurar las columnas del Treeview
        informe_treeview["columns"] = ("Nombre", "Existencias")
        informe_treeview.heading("#0", text="ID", anchor="center")  # Oculta la columna de índice
        informe_treeview.heading("Nombre", text="Nombre")
        informe_treeview.heading("Existencias", text="Existencias")

        # Ajustar el ancho de las columnas
        informe_treeview.column("#0", width=0, stretch=tk.NO)  # Oculta la columna de índice
        informe_treeview.column("Nombre", width=150, anchor="center")
        informe_treeview.column("Existencias", width=100, anchor="center")

        # Obtener y agregar los productos al Treeview con existencias mínimas
        for producto in productos:
            if producto[5] < producto[6]:  # Verificar si las existencias son menores al stock mínimo
                informe_treeview.insert("", "end", values=(producto[1], producto[5]))

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
                    id_producto INTEGER,
                    id_cliente  INTEGER, 
                    cantidad INTEGER,
                    precio_unitario REAL,
                    total REAL,
                    metodo_pago TEXT,
                    fecha_venta DATE,
                    hora_venta INTEGER,    
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