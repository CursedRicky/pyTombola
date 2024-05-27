import customtkinter
import random
import socket
import threading
from CTkMessagebox import CTkMessagebox

host = socket.gethostbyname(socket.gethostname())  # Hosta sulla macchina locale
port: int = 1710

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Parametri: usa ip v4, con connessione
server.bind((host, port)) # Associa il server all'IP della macchina e alla porta scelta prima
server.listen()  # Il server è in ascolto

clients = []  # Lista dei client connessi
ultimoNumeroA = []

tabelle = []  # Matrice contenente tutte le tabelle
tabella1 = [[1, 2, 3, 4, 5], [11, 12, 13, 14, 15], [21, 22, 23, 24, 25]]
tabelle.append(tabella1)
tabella2 = [[6, 7, 8, 9, 10], [16, 17, 18, 19, 20], [26, 27, 28, 29, 30]]
tabelle.append(tabella2)
tabella3 = [[31, 32, 33, 34, 35], [41, 42, 43, 44, 45], [51, 52, 53, 54, 55]]
tabelle.append(tabella3)
tabella4 = [[36, 37, 38, 39, 40], [46, 47, 48, 49, 50], [56, 57, 58, 59, 60]]
tabelle.append(tabella4)
tabella5 = [[61, 62, 63, 64, 65], [71, 72, 73, 74, 75], [81, 82, 83, 84, 85]]
tabelle.append(tabella5)
tabella6 = [[66, 67, 68, 69, 70], [76, 77, 78, 79, 80], [86, 87, 88, 89, 90]]
tabelle.append(tabella6)

numeri = []   # Numeri pescabili
for number in range(1, 91):
    numeri.append(number)
numeriL = []  # Lista di tutte le label dei numeri


def brodcast(msg) -> None:
    # Manda un messaggio contenuto in 'msg' a tutti i client
    for client in clients:
        client.send(msg)


def handle(client) -> None:
    global numeri
    while True:
        try:
            if len(numeri) <= 0:  # Se non ci sono più numeri da pescare allora chiudi la comunicazione con il client
                brodcast("Fine".encode("utf-8"))
                clients.remove(client)
                client.close()
                break
        except:
            # Se non riesci a comunicare con il client allora togli il client dallla lista di client
            clients.remove(client)
            client.close()
            break


def recive() -> None:
    print("Server attivo e in ascolto")
    while True:
        client, addr = server.accept()  # Prendi l'indirizzo IpV4 del client che ha effettuato la richiesta
        print(f"Connessione da {str(addr)}")

        clients.append(client)  # Aggiungi client alla lista dei client connessi

        # Crea un nuovo thread per ogni client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def estrai() -> None:
    global numeri, numeriL, ultimoNumeroA, tabelle
    value = random.choice(numeri)  # Estrai un numero casuale dalla lista di numeri disponibili
    numeri.remove(value)  # Rimuovi il valore estratto dalla lista di numeri disponibili
    numeriL[value - 1].configure(text_color="lime green")  # Cambia colore della casella con quel valore
    ultimoNumeroA[0].configure(text=f"Ultimo numero: {value}")  # Cambia valore ultimo numero uscito
    brodcast(str(value).encode("utf-8"))  # Comunica ai client quale valore è stato estratto

    # Gestione ambo, terna, quaterna e cinquina
    for tabella in tabelle:
        tombola = True
        for riga in tabella:
            if len(riga) != 0:
                tombola = False
            if not tombola:
                for n in riga:
                    if n == value:
                        riga.remove(n)  # Rimuovi il valore uscito dalla tabella
                        # Fai apparire un pop-up nel caso ci sia un ambo, una terna, una quaterna o una cinquina
                        if len(riga) == 3:
                            CTkMessagebox(title="Ambo", message=f"Ambo!", icon="warning")
                        elif len(riga) == 2:
                            CTkMessagebox(title="Terna", message=f"Terna!", icon="warning")
                        elif len(riga) == 1:
                            CTkMessagebox(title="Quaterna", message=f"Quaterna!", icon="warning")
                        elif len(riga) == 0:
                            CTkMessagebox(title="Cinquina", message=f"Cinquina!", icon="warning")
            # CTkMessagebox(title="Tombola", message=f"Tombola!", icon="check")


def resetta() -> None:
    global numeriL, numeri, ultimoNumeroA, tabelle

    # Rimetti tutte le caselle bianche
    for label in numeriL:
        label.configure(text_color="white")

    # Reset lista dei numeri disponibili
    numeri.clear()  # Cancella tutti i valori nella lista di numeri estraibili
    for numbe in range(1, 91):  # Inserisci nella lista di numeri estraibili tutti i valori tra 1 e 90
        numeri.append(numbe)

    brodcast("Reset".encode("utf-8"))  # Comunica ai client che la partita è stata resettata
    ultimoNumeroA[0].configure(text="Ultimo numero: -")  # Resetta ultimo numero uscito
    # Resetta i valori della matrice delle tabelle
    tabelle[0] = [[1, 2, 3, 4, 5], [11, 12, 13, 14, 15], [21, 22, 23, 24, 25]]
    tabelle[1] = [[6, 7, 8, 9, 10], [16, 17, 18, 19, 20], [26, 27, 28, 29, 30]]
    tabelle[2] = [[31, 32, 33, 34, 35], [41, 42, 43, 44, 45], [51, 52, 53, 54, 55]]
    tabelle[3] = [[36, 37, 38, 39, 40], [46, 47, 48, 49, 50], [56, 57, 58, 59, 60]]
    tabelle[4] = [[61, 62, 63, 64, 65], [71, 72, 73, 74, 75], [81, 82, 83, 84, 85]]
    tabelle[5] = [[66, 67, 68, 69, 70], [76, 77, 78, 79, 80], [86, 87, 88, 89, 90]]


def graf() -> None:
    global numeriL, numeri, ultimoNumeroA
    root = customtkinter.CTk()
    root.title("Tabellone")
    root.geometry("900x725")
    root.resizable(False, False)
    customtkinter.set_default_color_theme("green")
    
    # Frame contenente tuttele tabelle
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=10)

    # Frame contenente tutti i pulsanti
    frame_btn = customtkinter.CTkFrame(master=root, width=200, height=50)
    frame_btn.pack()
    
    # Bottone per l'estrazione del numero
    estrai_btn = customtkinter.CTkButton(master=frame_btn, text="Estrai", width=200, height=50, command=estrai)
    estrai_btn.grid(pady=10, padx=10, column=0, row=0)
    
    # Pulsante di reset
    reset_btn = customtkinter.CTkButton(master=frame_btn, text="Resetta", width=200, height=50, command=resetta, fg_color="red", hover_color="maroon")
    reset_btn.grid(pady=10, padx=10, column=1, row=0)
    
    # Mostra ultimo numero uscito
    ultimo_numero = customtkinter.CTkLabel(master=root, text="Ultimo numero: -", font=("Verdana", 20))
    ultimoNumeroA.append(ultimo_numero)
    ultimoNumeroA[0].pack(pady=5)
    
    # Crea tutte le tabelle vuote
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

    # Riempi le tabelle
    i = 0  # Colonne
    y = 0  # Righe
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
    reciveT = threading.Thread(target=recive)
    reciveT.start()
