#Aquí, está importando varias bibliotecas y módulos necesarios para su aplicación, como Tkinter para GUI, OpenCV para procesamiento de imágenes, 
# MTCNN para detección de rostros, conector MySQL para operaciones de base de datos y más.

from tkinter import *
from tkinter import messagebox as msg
import os
import tkinter
from unittest.case import _AssertRaisesContext
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import mysql.connector
from mysql.connector import Error
import database as db
import tensorflow as tf
import datetime
import openpyxl
import pandas as pd


# CONFIGURACIONES
#Las siguientes líneas definen varias constantes y ajustes de configuración para su aplicación:

entrada =  datetime.datetime.now()
salida =  datetime.datetime.now()

path = "C:/Users/elbot/OneDrive/Escritorio/proyectodereconocimientofacialtesis/Recognition/" # Aqui insertamos la direccion de nuestro path
txt_login = "Registra asistencia con detección facial"
txt_register = "Registrar usuario"
txt_salida="Registrar salida"

color_white = "#f4f5f4"
color_black = "#846e23"

color_black_btn = "#202020"
color_background = "#75151e"

font_label = "Century Gothic"
size_screen = "500x400"

# COLORES
color_success = "\033[1;32;40m"
color_error = "\033[1;31;40m"
color_normal = "\033[0;37;40m"

res_bd = {"id": 0, "affected": 0} # variable de base de datos

# GENERAL
#Estas variables configuran varias configuraciones y elementos de la interfaz de usuario para su aplicación, 
# incluidas etiquetas de texto, colores, fuentes y más.
#La función getEnter crea una etiqueta vacía con el color de fondo especificado.
def getEnter(screen):
    ''' Entrada dentro de la pantalla '''
    Label(screen, text="", bg=color_background).pack()
    
#La función printAndShow muestra un mensaje tanto en la consola como en un cuadro de mensaje emergente. 
# Destruye el widget de pantalla dado si la bandera es Verdadera.
def printAndShow(screen, text, flag):
    ''' imprime y muestra el texto'''
    if flag:
        print(color_success + text + color_normal)
        screen.destroy()
        msg.showinfo(message=text, title="¡Éxito!")
    else:
        print(color_error + text + color_normal)
        Label(screen, text=text, fg="red", bg=color_background, font=(font_label, 12)).pack()

#La función configure_screen configura la apariencia de un widget de pantalla dado configurando su título, tamaño y color de fondo. 
# También agrega una etiqueta en la parte superior de la pantalla con un mensaje de bienvenida.
def configure_screen(screen, text):
    ''' configuracion de estilos globales'''
    screen.title(text)
    screen.geometry(size_screen)
    screen.configure(bg=color_background)
    Label(screen, text=f"¡{text}!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

#La función de credenciales crea campos de entrada y botones para la interacción del usuario. 
# Crea una etiqueta, un widget de entrada y botones basados en el valor de la bandera.
def credentials(screen, var, flag):
    ''' Configuración de la entrada del usuario '''
    Label(screen, text="Usuario:", fg=color_white, bg=color_background, font=(font_label, 12)).pack()
    entry = Entry(screen, textvariable=var, justify=CENTER, font=(font_label, 12))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=30, ipady=6)

    getEnter(screen)
    if flag:
        Button(screen, text=txt_salida, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login_salidas).pack()
       
    
    if flag:        
        Button(screen, text="Registrar entrada", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login_capture).pack()

    else:
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register_capture).pack()
    return entry

#La función de cara procesa una imagen extrayendo caras utilizando el modelo MTCNN y OpenCV. Cambia el tamaño y guarda la cara detectada.
#El código continúa con varias funciones relacionadas con el registro de usuarios, inicio de sesión y seguimiento de asistencia,
#utilizando las capacidades de OpenCV, MTCNN y MySQL para reconocimiento facial, captura de imágenes e interacciones con bases de datos.
def face(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1,len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])

# REGISTRO DE USUARIO #

def register_face_db(img):
    name_user = img.replace(".jpg","").replace(".png","")
    res_bd = db.registerUser(name_user, path + img)

    getEnter(screen1)
    if(res_bd["affected"]):
        printAndShow(screen1, "¡Éxito! Se ha registrado correctamente", 1)
    else:
        printAndShow(screen1, "¡Error! No se ha registrado correctamente", 0)
    os.remove(img)

def register_capture():
    cap = cv2.VideoCapture(0)
    user_reg_img = user1.get()
    img = f"{user_reg_img}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Registro Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry1.delete(0, END)
    
    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)
    face(img, faces)
    register_face_db(img)

def register():
    global user1
    global user_entry1
    global screen1

    screen1 = Toplevel(root)
    user1 = StringVar()

    configure_screen(screen1, txt_register)
    user_entry1 = credentials(screen1, user1, 0)

# LOGIN #
def compatibility(img1, img2):
    orb = cv2.ORB_create()

    kpa, dac1 = orb.detectAndCompute(img1, None)
    kpa, dac2 = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(dac1, dac2)

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar)/len(matches)


def login_capture():
    cap = cv2.VideoCapture(0)
    user_login = user2.get()
    img = f"{user_login}_login.jpg"
    img_user = f"{user_login}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry2.delete(0, END)
    
    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)

    face(img, faces)
    getEnter(screen2)

    res_db = db.getUser(user_login, path + img_user)
    if(res_db["affected"]):
        my_files = os.listdir()
        if img_user in my_files:
            face_reg = cv2.imread(img_user, 0)
            face_log = cv2.imread(img, 0)

            comp = compatibility(face_reg, face_log)
            
            if comp >= 0.70:
                print("{}Compatibilidad del {:.1%}{}".format(color_success, float(comp), color_normal))
                printAndShow(screen2, f"Bienvenido, {user_login}, {entrada}", 1)
  
                try:
                    entra_da=datetime.datetime.now()
                    conexion = mysql.connector.connect(
                        host="localhost",
                        port="3306",
                        user="root",
                        password="",
                        db="prueba"
                    )
                    if conexion.is_connected():
                        print("Conexion exitosa")
                        cursor=conexion.cursor()
                        hora_in=entra_da
                        name=user_login
                        sentencia= "INSERT INTO registro (name, entrada) VALUES (%s,%s)"
                        valores=(name, hora_in)
                        cursor.execute(sentencia, valores)
                        conexion.commit()
                        print("Registro realizado")
                except Error as ex:
                    print("error en la conexion")
                finally:
                    if conexion.is_connected():
                        conexion.close()
                        print("La conexion finalizo.") 
            else:
                print("{}Compatibilidad del {:.1%}{}".format(color_error, float(comp), color_normal))
                printAndShow(screen2, "¡Error! Incopatibilidad de datos", 0)
            os.remove(img_user)
    
        else:
            printAndShow(screen2, "¡Error! Usuario no encontrado", 0)
    else:
        printAndShow(screen2, "¡Error! Usuario no encontrado", 0)
    os.remove(img)

def login():
    global screen2
    global user2
    global user_entry2


    screen2 = Toplevel(root)
    user2 = StringVar()

    configure_screen(screen2, txt_login,)
    user_entry2 = credentials(screen2, user2, 1)

def login_salidas():
    cap = cv2.VideoCapture(0)
    user_login = user2.get()
    img = f"{user_login}_login.jpg"
    img_user = f"{user_login}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry2.delete(0, END)
    
    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)

    face(img, faces)
    getEnter(screen2)

    res_db = db.getUser(user_login, path + img_user)
    if(res_db["affected"]):
        my_files = os.listdir()
        if img_user in my_files:
            face_reg = cv2.imread(img_user, 0)
            face_log = cv2.imread(img, 0)

            comp = compatibility(face_reg, face_log)
            
            if comp >= 0.70:
                print("{}Compatibilidad del {:.1%}{}".format(color_success, float(comp), color_normal))
                printAndShow(screen2, f"Hasta luego, {user_login}, {salida}", 1)
  
                try:
                    sali_da=datetime.datetime.now()
                    conexion = mysql.connector.connect(
                        host="localhost",
                        port="3306",
                        user="root",
                        password="",
                        db="prueba"
                    )
                    if conexion.is_connected():
                        print("Conexion exitosa")
                        cursor=conexion.cursor()
                        hora_out=sali_da
                        name=user_login
                        sentencia= "INSERT INTO registro (name, salida) VALUES (%s,%s)"
                        valores=(name, hora_out)
                        cursor.execute(sentencia, valores)
                        conexion.commit()
                        print("Registro de salida realizado")
                except Error as ex:
                    print("error en la conexion")
                finally:
                    if conexion.is_connected():
                        conexion.close()
                        print("La conexion finalizo.") 
            else:
                print("{}Compatibilidad del {:.1%}{}".format(color_error, float(comp), color_normal))
                printAndShow(screen2, "¡Error! Incopatibilidad de datos", 0)
            os.remove(img_user)
    
        else:
            printAndShow(screen2, "¡Error! Usuario no encontrado", 0)
    else:
        printAndShow(screen2, "¡Error! Usuario no encontrado", 0)
    os.remove(img)

def salidas():
    global screen2
    global user2
    global user_entry2


    screen2 = Toplevel(root)
    user2 = StringVar()

    configure_screen(screen2, txt_salida,)
    user_entry2 = credentials(screen2, user2, 1)
    
def idb():
        
            conn = mysql.connector.connect(
                host="localhost",
                port="3306",
                user="root",
                password="",
                db="prueba"
                )    
            cursor = conn.cursor()

                # Obtener la fecha actual
            fecha_actual = datetime.datetime.now()

                # Consulta SQL para obtener los registros de la tabla "registro" del día actual
            query = "SELECT * FROM registro"
            cursor.execute(query)
            datos = cursor.fetchall()

                # Crear un DataFrame con los datos
            df = pd.DataFrame(datos)

                # Guardar el DataFrame en un archivo Excel
            df.to_excel('informe.xlsx', index=False)
            
                #abrir el archivo excel
            workbook =openpyxl.load_workbook('informe.xlsx')
                # Obtener la hoja de cálculo predeterminada
            worksheet = workbook.active
            # Agregar la fórmula en la celda B2
            worksheet['E3'] = '=D3-C2'
            worksheet['F3'] = '=SUM(E3:E500)'

                # Guardar los cambios en el archivo de Excel
            workbook.save('informe.xlsx')

                # Borrar los registros de la tabla "registro"
            cursor.execute("DELETE FROM registro ")
            conn.commit()

                # Mostrar un mensaje de confirmación
            tkinter.messagebox.showinfo('Exportar Informe', 'El informe se ha exportado correctamente y los registros se han borrado.')

                # Cerrar la conexión a la base de datos
            cursor.close()
            conn.close()


root = Tk()
root.geometry(size_screen)
root.title("Registro de asistencia")
root.configure(bg=color_background)
Label(text="¡Bienvenido(a)!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()

getEnter(root)
Button(text=txt_login, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()

getEnter(root)
Button(text="Registro facial de usuario", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register).pack()

getEnter(root)
Button(text="Reporte del día", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=idb).pack()
root.mainloop()