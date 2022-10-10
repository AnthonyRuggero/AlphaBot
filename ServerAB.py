import socket
import AlphaBot

def main():
    robot = AlphaBot.AlphaBot()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 6000))
    sock.listen()
    connection, address = sock.accept()
    while True:
        msg = connection.recv(4096)
        istruzione = str(msg.decode())
        print(istruzione)

        if(istruzione == "forward"):
            robot.forward()
        elif(istruzione == "stop"):
            robot.stop()
        elif(istruzione == "backward"):
            robot.backward()
        elif(istruzione == "left"):
            robot.left()
        elif(istruzione == "right"):
            robot.right() 
        
    

if __name__ == "__main__":
    main()