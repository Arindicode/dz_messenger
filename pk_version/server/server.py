from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def getIncomingMesseges():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s присоединился к переписке" % client_address)
        client.send(bytes("Привет!" + " Введи своё имя и нажми Enter", "utf8"))
        addresses[client] = client_address
        Thread(target=clientHandler, args=(client,)).start()

def clientHandler(client):
    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = "Добро пожаловать, %s!" % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s Теперь в переписке" % name
    Broadcast(bytes(msg, "utf8"))

    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            Broadcast(msg, name + ": ")
        else:
            exit_msg = "покинул переписку."
            Broadcast(bytes(exit_msg, "utf8"))
            del clients[client]
            client.send(bytes("{quit}", "utf8"))
            client.close()
            break

def Broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

clients = {}
addresses = {}

HOST = ""
PORT = 8080
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("ожидание соединения")
    ACCEPT_THREAD = Thread(target=getIncomingMesseges)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()