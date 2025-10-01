
''' Para iniciar o servidor no terminal usar:
    python -m Pyro5.nameserver
'''

import Pyro5.api
from Pyro5.server import Daemon
import threading
import time

RESOURCE_MAX_TIME=10#ACHO Q DA P GENTE USAR ESSA MACRO P CONTROLAR O TEMPO DO RECURSO NA SEÇÃO CRÍTICA

@Pyro5.api.expose
class Peer(object):
    def __init__(self,name):
        self.name=name
        self.state="RELESEAD"
        self.resource_time=0

    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
               "Tomorrow's lucky number is 12345678.".format(name)
    
    def solicitar_recurso(self,resource):
        with self.lock:
            self.state="WANTED"
        print("I want to enter the critical section and access resource {resource} ")
        #Mandar msg pra cada peer, exceto pra ele próprio
        contador=0
        #verificar isso aqui!
        for peer_name in ns.list().keys():
            if peer_name==self.name:
                continue
            uri=ns.lookup(peer_name)
            peer=Pyro5.api.Proxy(uri)

            print("Solicitando recurso para {peer_name}")
            resposta=peer.receber_pedido(self.name)
            if resposta==True:
                contador+=1
            #TINHAMOS FEITO ASSIM ANTES, MAS ACHO Q ESSA LOGICA E LA NA FUNCAO DE RECEBER PEDIDO
            """ if peer.state=="WANTED" | peer.state=="HELD":
                return False
            else:
                contador+=1"""
            
        if contador == len(ns.list())-1:
            #lógica pra contar o tempo max q pode usar o recurso
            return True
        
    def receber_pedido(self, requester_name):
        #aqui precisamos verificar a questão do tempo tb, e adicionar o tempo na fila, eu n quis mexer por enquanto
        if self.state=="WANTED" | self.state=="HELD":
            self.request_queue.append(requester_name)
            return False
        else:
           return True
        
    def liberar_recurso(self):#INCOMPLETA SÓ ADICIONEI PRA GENTE N ESQUECER
        with self.lock:
            self.state="RELESEAD"

name = input("What is your name? ").strip()

daemon = Pyro5.server.Daemon()         # make a Pyro daemon
ns = Pyro5.api.locate_ns()             # find the name server

if name not in ns.list().keys():
    uri = daemon.register(Peer)   # register the greeting maker as a Pyro object
    ns.register(name, uri)   # register the object with a name in the name server

print("Ready.")
threading.Thread(target=daemon.requestLoop, daemon=True).start()    # start the event loop of the server to wait for calls    

while True:
    opcao = input(
        "\nSelecione a opção desejada:\n"
        "1. Solicitar recurso\n"
        "2. Listar peers ativos\n"
        "3. Liberar recurso\n"
        "4. Sair\n> "
    )

    if opcao == "1":
        print("Solicitar recurso\n")
        resource=input("Qual recurso?")
        #solicitar_recurso(resource)
    elif opcao == "2":
        print("Listar peers ativos")
        print(ns.list())  # exemplo: mostra peers registrados
    elif opcao == "3":
        print("Liberar recurso")
    elif opcao == "4":
        print("Encerrando...")
        ns.remove(name)   # remove peer do NameServer
        break
    else:
        print("Opção inválida")
    


    
