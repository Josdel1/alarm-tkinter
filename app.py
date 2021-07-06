#encoding: utf-8
 
'''
AUTOR: Josdel Páez
Versión: 1.5 beta
Nombre: Alarma de Eventos
'''
 
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date, datetime
import sqlite3
 
class Ventana():
 
    def __init__( self ):
        self.raiz = Tk( )
        self.raiz.config(bg="turquoise2")
        self.raiz.title( "Proyecto: Josdel Páez" )
 
        #Etiqueta referente al titulo de la ventana principal
        Label( self.raiz, text = "Alarma de Eventos", bg="turquoise2", font=( "Arial", 30 ) ).pack( side=TOP, padx=10, pady=10 )
 
        #Botón para crear un evento
        ttk.Button( self.raiz, text = "Planificar", command = self.__planificar ).pack(
            side=LEFT, expand=True, padx=10, pady=10)
 
        #Botón para ver los eventos ya creados 
        ttk.Button( self.raiz, text= "Eventos", command = self.__verEventos ).pack( 
            side=RIGHT, expand=True, padx=10, pady=10 )
 
        #Sección de la base de datos
        try:
            conexion = sqlite3.connect( "sqlite3/Guardado.sqlite3" )
            consulta = conexion.cursor( )
 
            Query = '''
                    CREATE TABLE IF NOT EXISTS Proyecto(
                    id integer primary key autoincrement not null,
                    Nombre varchar( 50 ) not null,
                    Fecha date not null,
                    Hora varchar( 5 ) not null,
                    Nota varchar( 50 ) not null,
                    Estado varchar( 10 ) not null
                )'''
 
            if( consulta.execute( Query ) ): print( "Tabla creada correctamente." )
            else: print( "Ha ocurrido un error." )
 
            consulta.close( )
            conexion.commit( )
            conexion.close( )
 
            self.__avisar()
 
        except sqlite3.OperationalError:
            messagebox.showwarning("ERROR", "Ha ocurrido un error, puede que no exista el directorio sqlite3")
            print("No existe la carpeta sqlite3 donde se almacenará el guardado.")
        
        #Esto sirve para mantener la ventana abierta y no desaparesca al ejecutar los códigos de arriba.
        self.raiz.mainloop( )
    
    def __avisar(self):
 
        #Almacenar el ID del evento entrante
        self.__IDEvento = IntVar()
 
        conexion = sqlite3.connect( "sqlite3/Guardado.sqlite3" )
        consulta = conexion.cursor( )
 
        Query = "SELECT * FROM Proyecto"
        if( consulta.execute( Query ) ):
            Datos = consulta.fetchall( )
 
            for DatosI in Datos:
                if DatosI[ 2 ] == datetime.now( ).strftime( "%Y-%m-%d" ) and DatosI[ 3 ] == datetime.now( ).strftime( "%H:%M") and DatosI[ 5 ] == "Sin Avisar":
                    self.__IDEvento.set( DatosI[ 0 ] )
                    self.__mandarVentana( )
                    
        consulta.close( )
        conexion.commit( )
        conexion.close( )
 
    def __mandarVentana(self):
 
        self.raiz = Toplevel( )
 
        conexion = sqlite3.connect( "sqlite3/Guardado.sqlite3" )
        consulta = conexion.cursor( )
 
        if( consulta.execute( "SELECT * FROM Proyecto WHERE id = %d" %(self.__IDEvento.get()) ) ):
            Datos = consulta.fetchall( )
 
            for DatosI in Datos:
                Label( self.raiz, text =  DatosI[ 1 ].upper( ), font=("Arial", 15), bg="red" ).pack( )
 
                Button( self.raiz, text = "Pulsa para detener!", command=self.__parar, height=10, width=45, bg='red', fg='white', bd=8).pack( )
 
                Label( self.raiz, text = DatosI[ 4 ].upper( ), font=("Arial", 15), bg="red" ).pack( )
        consulta.close( )
        conexion.commit( )
        conexion.close( )
 
        self.raiz.config( bg="red" )
 
        self.raiz.mainloop( )
 
    def __parar( self ):
        conexion = sqlite3.connect( "sqlite3/Guardado.sqlite3" )
        consulta = conexion.cursor( )
 
        if( consulta.execute( "UPDATE Proyecto SET Estado='Finalizado' WHERE id = %d" %( self.__IDEvento.get( ) ) ) ):
            print("Valor actualizado correctamente.")
 
        consulta.close( )
        conexion.commit( )
        conexion.close( )
 
        self.raiz.destroy( )
 
    def __planificar( self ):
        self.raiz = Toplevel( )
        self.raiz.title( "Planificar Evento" )
        self.raiz.geometry( "200x420" )
 
        #Variables de Control
        self.__Nombre = StringVar( )
        self.__Dia = IntVar( value = 1 )
        self.__Mes = IntVar( value = 1 )
        self.__Anio = IntVar( value = 2017 )
        self.__Hora = StringVar( )
        self.__Nota = StringVar( )
        self.__Estado = StringVar( )
 
        #Etiqueta que se refiere al nombre de la ventana
        Label( self.raiz, text="Planificar", font=( "Arial", 15 ) ).pack( )
 
        #Etiqueta & Entry referente al nombre del evento
        Label( self.raiz, text="Nombre del Evento:").pack( side = TOP, padx = 10, pady = 10 )
        Entry( self.raiz, textvariable=self.__Nombre ).pack( side = TOP, padx = 10, pady = 10 )
 
        self.Frame0 = Frame( self.raiz )
        self.Frame0.pack( side = TOP )
 
        #Sección de Etiquetas (Widgets "Padres")
        self.Frame1 = Frame( self.Frame0 )
        Label( self.Frame1, text="Día: " ).pack( padx = 5, pady = 5 )
        Label( self.Frame1, text="Mes: " ).pack( padx = 5, pady = 5 )
        Label( self.Frame1, text="Año: " ).pack( padx = 5, pady = 5 )
        Label( self.Frame1, text="Hora: " ).pack( padx = 5, pady = 5 )
        self.Frame1.pack( side = LEFT )
 
        #Sección de Spinbox (Widgets "Hijos")
        self.Frame2 = Frame( self.Frame0 )
        Spinbox( self.Frame2, from_ = 1, to = 31, wrap = True, state = 'readonly', width = 4, textvariable = self.__Dia ).pack( padx = 5, pady = 5 )
        Spinbox( self.Frame2, from_ = 1, to = 12, wrap = True, state = 'readonly', width = 4, textvariable = self.__Mes ).pack( padx = 5, pady = 5 )
        Spinbox( self.Frame2, from_ = 2017, to = 2020, wrap = True, state = 'readonly', width = 5, textvariable = self.__Anio ).pack( padx = 5, pady = 5 )
        Spinbox( self.Frame2,
            value = (   "00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
                        "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                        "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30" ),
            wrap = True, state = 'readonly', width = 5, textvariable = self.__Hora ).pack( 
            padx = 5, pady = 5 )
        self.Frame2.pack( side = RIGHT )
 
        #Nota a ingresar para recordar algo extra
        Label( self.raiz, text = "NOTA:" ).pack( side = TOP, padx = 10, pady = 10 )
        Entry( self.raiz, textvariable = self.__Nota ).pack( side = TOP )
 
        #Botones para Vacior & Guardar
        ttk.Button( self.raiz, text="Vaciar", command=self.__vaciar ).pack( side = LEFT, padx = 10, pady = 10 )
        ttk.Button( self.raiz, text="Guardar", command = self.__confirmar ).pack( side = RIGHT, padx = 10, pady = 10 )
 
    def __vaciar( self ):
        self.__Nombre.set( "" )
        self.__Dia.set( 1 )
        self.__Mes.set( 1 )
        self.__Anio.set( 2017 )
        self.__Hora.set("00:00")
        self.__Nota.set( "" )
        print("Todo se ha vaciado correctamente")
 
    def __confirmar( self ):
 
        #Craer lista para crear la fecha para la base de datos
        self.__Fecha = str( self.__Anio.get( ) ) + "-" + str( self.__Mes.get( ) ) + "-" + str( self.__Dia.get( ) )
        
        #Asignar valor a Estado del evento
        self.__Estado.set("Sin Avisar")
 
        #Verificar que no haya ningún problema
        if( self.__Nombre.get( ).isspace( ) or len( self.__Nombre.get( ) ) == 0 ):
            messagebox.showwarning( "ALERTA", "El nombre esta vacio." )
        elif( self.__Mes.get( ) < date.today( ).month and self.__Anio.get( ) == date.today( ).year ):
            messagebox.showwarning( "ALERTA", "No puedes colocar una mes menor al actual durante este año." )
        elif( self.__Anio.get( ) == date.today( ).year and self.__Mes.get( ) == date.today( ).month and self.__Dia.get( ) < date.today( ).day ):
            messagebox.showwarning( "ALERTA", "No puedes colocar un día menor durante este mes." )
        elif( self.__Dia.get( ) == date.today( ).day and self.__Hora.get( ) < datetime.now( ).strftime( "%H:%M" ) ):
            messagebox.showwarning( "ALERTA", "No puees colocar una hora menor\na la actual durante este día." )
        else:
            conexion = sqlite3.connect( "sqlite3/Guardado.sqlite3" )
            consulta = conexion.cursor( )
 
            Query = "SELECT * FROM Proyecto"
 
            self.__Chequear = False
 
            if( consulta.execute( Query ) ):
                Datos = consulta.fetchall( )
                for DatosI in Datos:
                    if( DatosI[ 1 ] == self.__Nombre.get( ) and DatosI[ 2 ] == self.__Fecha and DatosI[ 3 ] == self.__Hora.get( ) ):
                        self.__Chequear = True
            if( self.__Chequear ):
                messagebox.showwarning( "ALERTA", "Ya hay un evento con los mismo datos en curso." )
            else:
                self.__Confir = messagebox.askokcancel( "CONFIRMAR", "¿Seguro que quieres confirmar?" )
 
                if( self.__Confir ):
                    Datos = ( self.__Nombre.get( ), self.__Fecha, self.__Hora.get( ), self.__Nota.get( ), self.__Estado.get( ) )
 
                    Query2 = "insert into Proyecto ( Nombre, Fecha, Hora, Nota, Estado ) values( ?, ?, ?, ?, ? )"
 
                    if( consulta.execute( Query2, Datos ) ): print( "Datos insertados correctamente." )
                    else: print( "Ha ocurrido un error." )
 
                    self.__FechaE = str( self.__Dia.get( ) ) + "/" + str( self.__Mes.get( ) ) + "/" + str( self.__Anio.get( ) )
                    messagebox.showinfo("Información", "Evento creado, se te notificará el %s a las %s" %( self.__FechaE, self.__Hora.get( ) ) )
 
                    self.raiz.destroy( )
 
            consulta.close( )
            conexion.commit( )
            conexion.close( )
 
 
    def __verEventos( self ):
        self.raiz = Toplevel( )
        self.raiz.title( "Ver Eventos" )
 
        conexion = sqlite3.connect( "sqlite3/Guardado.sqlite3" )
        consulta = conexion.cursor( )
 
        Query = "SELECT * FROM Proyecto"
 
        self.Frame0 = Frame( self.raiz )
        self.Frame0.pack( side = TOP )
 
        self.Frame1 = Frame( self.Frame0 )
        Label( self.Frame1, text = "#" ).pack( )
        self.Frame1.pack( side = LEFT, padx = 10, pady = 10 )
 
        self.Frame2 = Frame( self.Frame0 )
        Label( self.Frame2, text = "Nombre" ).pack( )
        self.Frame2.pack( side = LEFT, padx = 10, pady = 10 )
 
        self.Frame3 = Frame( self.Frame0 )
        Label( self.Frame3, text = "Fecha" ).pack( )
        self.Frame3.pack( side = LEFT, padx = 10, pady = 10 )
 
        self.Frame4 = Frame( self.Frame0 )
        Label( self.Frame4, text = "Nota" ).pack( )
        self.Frame4.pack( side = LEFT, padx = 10, pady = 10 )
 
        self.Frame5 = Frame( self.Frame0 )
        Label( self.Frame5, text = "Hora" ).pack( )
        self.Frame5.pack( side = LEFT, padx = 10, pady = 10 )
 
        self.Frame6 = Frame( self.Frame0 )
        Label( self.Frame6, text = "Estado" ).pack( )
        self.Frame6.pack( side = LEFT, padx = 10, pady = 10 )
 
        if( consulta.execute( Query ) ):
            Datos = consulta.fetchall( )
 
            self.__Verificar = True
 
            for DatosI in Datos:
                if( DatosI[ 0 ] >= 1 ):
                    self.__Verificar = False
                Label( self.Frame1, text = DatosI[ 0 ] ).pack( )
                Label( self.Frame2, text = DatosI[ 1 ] ).pack( )
                Label( self.Frame3, text = DatosI[ 2 ] ).pack( )
                Label( self.Frame5, text = DatosI[ 3 ] ).pack( )
                Label( self.Frame4, text = DatosI[ 4 ] ).pack( )
                Label( self.Frame6, text = DatosI[ 5 ] ).pack( )
 
 
            if( self.__Verificar ):
                Label( self.raiz, text = "No existen eventos creados." ).pack( )
        
        consulta.close( )
        conexion.commit( )
        conexion.close( )
 
def main( ):
    App = Ventana( )
 
if __name__ == '__main__':
    main( )