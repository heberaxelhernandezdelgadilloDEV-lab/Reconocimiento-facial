from os import name
import mysql.connector as db
import json

with open('conexion.json') as json_file:
    keys = json.load(json_file)
#Define una función convertir datos binarios que lee un archivo en modo binario y devuelve sus datos binarios.
# esto se usa para convertir un archivo de imagen en formato binario para almacenarlo en la base de datos.

def convertToBinaryData(filename):
    # convierte los datos a binario
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except:
        return 0
    
#Define una función write_file que escribe datos binarios en un archivo en modo binario.
#Esta función probablemente se usa para guardar una imagen recuperada de la base de datos
def write_file(data, path):
    
    with open(path, 'wb') as file:
        file.write(data)

#Define una función registerUser que intenta registrar un usuario en la base de datos con un nombre y una foto.
#Abre una conexión a la base de datos, prepara una consulta SQL para insertar los datos del usuario y convierte la foto en datos binarios.
#Ejecuta la consulta SQL y confirma los cambios si tiene éxito.
#Devuelve un diccionario con información sobre el proceso de registro.
def registerUser(name, photo):
    id = 0
    inserted = 0

    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "INSERT INTO `user`(name, photo) VALUES (%s,%s)"
        pic = convertToBinaryData(photo)

        if pic:
            cursor.execute(sql, (name, pic))
            con.commit()
            inserted = cursor.rowcount
            id = cursor.lastrowid
    except db.Error as e:
        print(f"Failed inserting image: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected":inserted}
#Define una función getUser que recupera datos de usuario de la base de datos en función del nombre proporcionado.
#Abre una conexión de base de datos, prepara una consulta SQL para recuperar datos de usuario y la ejecuta.
#Recorre en iteración los registros obtenidos, escribe los datos de la foto en un archivo mediante la función write_file y cuenta el número de registros.
#Devuelve un diccionario con información sobre el proceso de recuperación.
#En general, este fragmento de código parece ser un módulo para interactuar con una base de datos MySQL para registrar y recuperar información del usuario, particularmente fotos, usando almacenamiento de datos binarios.

def getUser(name, path):
    id = 0
    rows = 0

    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "SELECT * FROM `user` WHERE name = %s"

        cursor.execute(sql, (name,))
        records = cursor.fetchall()

        for row in records:
            id = row[0]
            write_file(row[2], path)
        rows = len(records)
    except db.Error as e:
        print(f"Failed to read image: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected": rows}

