import socket, threading, random, customtkinter

host = socket.gethostbyname(socket.gethostname())  # Hosta sulla macchina locale
port: int = 1710

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # parametri: usa ip v4, con connessione
server.bind((host, port))
server.listen()

clients = []

numeri = []
for number in range (1, 91) :
    numeri.append(number)

def brodcast(msg) -> None:
    for client in clients:
        client.send(msg)


def handle(client) -> None:
    global numeri
    while True:
        try:
            if len(numeri) > 0:
                input("Inviare per generare")
                msg = str(estrai())
                brodcast(msg.encode("utf-8"))
            else :
                brodcast("Fine".encode("utf-8"))
                clients.remove(client)
                client.close()
                break
        except:
            clients.remove(client)
            client.close()
            break


def recive() -> None:
    print("Il server attivo")
    while True:
        client, addr = server.accept()
        print(f"Connessione da {str(addr)}")

        clients.append(client)

        client.send("Connesso al server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def estrai() -> int :
    global numeri
    value = random.choice(numeri)
    numeri.remove(value)
    return value


if __name__ == '__main__':
    print(f"Server Ip: {host}")
    recive()
