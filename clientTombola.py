import socket, threading, customtkinter

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverPort: int = 1710
serverIp: str = "192.168.56.1"

client.connect((serverIp, serverPort))
numeri = []

def recive() -> None:
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            print(msg)
            numeri.append(msg)
        except:
            print("Connessione persa")
            client.close()
            break

def main() -> None:
    rcvT = threading.Thread(target=recive)
    rcvT.start()

if __name__ == '__main__':
    main()