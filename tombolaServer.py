import socket, threading, random, customtkinter

host = socket.gethostbyname(socket.gethostname())  # Hosta sulla macchina locale
port: int = 1710

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # parametri: usa ip v4, con connessione
server.bind((host, port))
server.listen()

clients = []

numeri = []
for number in range(1, 91):
    numeri.append(number)
numeriL = []


def brodcast(msg) -> None:
    for client in clients:
        client.send(msg)


def handle(client) -> None:
    global numeri
    while True:
        try:
            if len(numeri) <= 0:
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


def estrai() -> None:
    global numeri, numeriL
    value = random.choice(numeri)
    numeri.remove(value)
    numeriL[value-1].configure(text_color="lime green")
    brodcast(str(value).encode("utf-8"))

def resetta() -> None:
    global numeriL, numeri
    for label in numeriL :
        label.configure(text_color="white")
    numeri.clear()
    for number in range(1, 91):
        numeri.append(number)
    brodcast("Reset".encode("utf-8"))

def graf() -> None:
    global numeriL, numeri
    root = customtkinter.CTk()
    root.title("Tabellone")
    root.geometry("900x690")
    root.resizable(False, False)
    customtkinter.set_default_color_theme("green")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=10)

    frameBtn = customtkinter.CTkFrame(master=root, width=200, height=50)
    frameBtn.pack()

    estraiBtn = customtkinter.CTkButton(master=frameBtn, text="Estrai", width=200, height=50, command=estrai)
    estraiBtn.grid(pady=10, padx=10, column=0, row=0)

    resetBtn = customtkinter.CTkButton(master=frameBtn, text="Resetta", width=200, height=50, command=resetta, fg_color="red", hover_color="maroon")
    resetBtn.grid(pady=10, padx=10, column=1, row=0)

    frame1 = customtkinter.CTkFrame(master=frame, width=400)
    frame1.grid(pady=10, padx=10, column=0, row=0)
    frame2 = customtkinter.CTkFrame(master=frame, width=400)
    frame2.grid(pady=10, padx=10, column=1, row=0)
    frame3 = customtkinter.CTkFrame(master=frame, width=400)
    frame3.grid(pady=10, padx=10, column=0, row=1)
    frame4 = customtkinter.CTkFrame(master=frame, width=400)
    frame4.grid(pady=10, padx=10, column=1, row=1)
    frame5 = customtkinter.CTkFrame(master=frame, width=400)
    frame5.grid(pady=10, padx=10, column=0, row=2)
    frame6 = customtkinter.CTkFrame(master=frame, width=400)
    frame6.grid(pady=10, padx=10, column=1, row=2)

    i = 0  # Col
    y = 0  # Row
    for numero in numeri:
        if i < 5 and y < 3:
            label = customtkinter.CTkLabel(text=str(numero), master=frame1, font=("Verdana", 40))
            label.grid(row=y, column=i, padx=10, pady=5)
            numeriL.append(label)
        elif i >= 5 and y < 3:
            label = customtkinter.CTkLabel(text=str(numero), master=frame2, font=("Verdana", 40))
            label.grid(row=y, column=i, padx=10, pady=5)
            numeriL.append(label)
        elif i < 5 and y < 6:
            label = customtkinter.CTkLabel(text=str(numero), master=frame3, font=("Verdana", 40))
            label.grid(row=y, column=i, padx=10, pady=5)
            numeriL.append(label)
        elif i >= 5 and y < 6:
            label = customtkinter.CTkLabel(text=str(numero), master=frame4, font=("Verdana", 40))
            label.grid(row=y, column=i, padx=10, pady=5)
            numeriL.append(label)
        elif i < 5:
            label = customtkinter.CTkLabel(text=str(numero), master=frame5, font=("Verdana", 40))
            label.grid(row=y, column=i, padx=10, pady=5)
            numeriL.append(label)
        elif i >= 5:
            label = customtkinter.CTkLabel(text=str(numero), master=frame6, font=("Verdana", 40))
            label.grid(row=y, column=i, padx=10, pady=5)
            numeriL.append(label)

        if i < 9:
            i += 1
        else:
            i = 0
            y += 1

    root.mainloop()


if __name__ == '__main__':
    print(f"Server Ip: {host}")
    grafica = threading.Thread(target=graf)
    grafica.start()
    reciveT = threading.Thread(target=recive())
    reciveT.start()
