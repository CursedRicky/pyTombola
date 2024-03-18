import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverPort: int = 1710
serverIp: str = "192.168.8.82"

numeri = []

def recive() -> None:
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg == "Fine":
                client.close()
                print("Partita conclusa")
            else :
                print(msg)
            numeri.append(msg)
        except:
            print("Comunicazione interrotta")
            client.close()
            break

def main() -> None:
    rcvT = threading.Thread(target=recive)
    rcvT.start()

if __name__ == '__main__':
    # serverIp = input("Inserire Ip Server:\n")
    try:
        client.connect((serverIp, serverPort))
        print("Connessione al server avvenuta")
        main()
    except:
        print("Errore, nessuna connessione")
