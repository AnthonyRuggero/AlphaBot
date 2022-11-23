import socket
import time
import AlphaBot
import sqlite3

def comandiDaDB(messaggio, comandi):
    for elemento in messaggio:
            stringa = elemento.split(",")
            tempo = float(stringa[1])
            istruzione = comandi[stringa[0]]()
            time.sleep(tempo)


def main():
    robot = AlphaBot.AlphaBot()
    comandi = {"f" : robot.forward, "l" : robot.left, "r": robot.right, "b" : robot.backward, "s" : robot.stop}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 6000))
    sock.listen()
    connection, address = sock.accept()
    con = sqlite3.connect("./movimentiAB.db")
    cur = con.cursor()

    while True:
        msg = connection.recv(4096)
        messaggio = str(msg.decode())
        if(messaggio[0] in comandi):
            istruzione = messaggio.split(",")
            tempo = float(istruzione[1])
            comandi[istruzione[0]]()
            time.sleep(tempo)
            robot.stop()
        else:
            id = int(messaggio)
            res = cur.execute(f"SELECT movimento FROM MOVIMENTI WHERE ID = {id}")
            istruzione = (res.fetchone()[0]).split(";")      
            comandiDaDB(istruzione, comandi)

    con.close()

if __name__ == "__main__":
    main()