import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.134", 6000))

def main():
    while True:    
        msg = input("Inserisci istruzione: ")
        s.sendall(msg.encode())

if __name__ == "__main__":
    main()
