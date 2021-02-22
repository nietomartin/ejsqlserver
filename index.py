"""
aplicación : ddextprop (Data Dictionary Extended Properties)
Utilidad   : Permite registrar propiedades extendidas para tablas de BD de SQL Server
Desarrolló : Ing. Martin Nieto
             DBA
Fecha : Febrero de 2021
Observaciones : Esta es una aplicación python flask, es decir, es una aplicación en arquitectura Cliente/Servidor
               para su ejecución siga estos pasos:
                a) para el servidor
                c:\CARPETA_DE_LA_APLICACION\> set FLASK_APP = index
                c:\CARPETA_DE_LA_APLICACION\> set FLASK_ENV = development  (production cuando se hayan hecho las pruebas
                esto es para que se active el modo depuración y poder ver en pantalla lo que está pasando, posibles errores)
                c:\>CARPETA_DE_LA_APLICACION\> flask run

                b) para el cliente (ejecutar la aplicación)
                en el navegador http://IP_SERVIDOR/ejsqlserver
"""
import pyodbc 
import json
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# cambiar a los respectivos valores de su ambiente
server="DESKTOP-1P539GB\SQLEXPRESS"
database = 'bodega' 
username = 'martinieto' 
password = 'martinieto' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

@app.route('/')
def index():   
   return redirect(url_for('search'))

@app.route('/search')
def search():   
   data = cursor.execute('SELECT * FROM dbo.herramientas')  
   return render_template('search.html' , data=data)

@app.route('/edit', methods=["GET", "POST"])
def edit():
   if request.method == 'POST':  
      Id = request.form.get('Id')
      code = request.form.get('code')
      nombre = request.form.get('nombre')
      cantidad = request.form.get('cantidad')
      cursor.execute("UPDATE dbo.herramientas SET code = ?, nombre = ?, cantidad = ? WHERE Id = ?", code, nombre, cantidad, Id )
      cnxn.commit()
      return redirect(url_for('search'))
   else:
      post_id = request.args.get('id')
      data = cursor.execute('SELECT * FROM dbo.herramientas WHERE Id=?', post_id)
      return render_template('editForm.html' , data=data)

@app.route('/add', methods=["GET", "POST"])
def add():
   return render_template('add.html')

@app.route('/insertar', methods=["GET", "POST"])
def insertar():
   if request.method == 'POST':  
      code = request.form.get('code')
      nombre = request.form.get('nombre')
      cantidad = request.form.get('cantidad')
      cursor.execute("INSERT INTO dbo.herramientas (code,nombre,cantidad) VALUES (?,?,?)", code, nombre, cantidad )
      cnxn.commit()
   else:
      post_id = request.args.get('id')
      data = cursor.execute('SELECT * FROM dbo.herramientas WHERE Id=?', post_id)
   return redirect(url_for('search'))

@app.route('/salir')
def salir():
   cnxn.close()   
   return render_template('salida.html')

if __name__ == '__main__':   
   app.run(debug = True)
   cnxn.close()