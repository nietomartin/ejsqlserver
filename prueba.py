import pyodbc 
# Ojo , este script no se ejecuta en el contexto web, debe ejecutarse en linea de comandos
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# server = 'tcp:myserver.database.windows.net' 
server="DESKTOP-1P539GB\SQLEXPRESS"
database = 'bodega' 
username = 'martinieto' 
password = 'martinieto' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#Sample select query
print ("SELECT @@version")
cursor.execute("SELECT @@version;") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()

#Sample insert query
print("Hacemos un insert en la tabla herramientas")
cursor.execute("""
INSERT INTO dbo.herramientas (code,nombre,cantidad) 
VALUES (?,?,?)""",
3, 'Motor 4 válvulas para Renault Sandero', 4) 
cnxn.commit()
row = cursor.fetchone()

while row: 
    print('Inserted Product key is ' + str(row[0]))
    row = cursor.fetchone()