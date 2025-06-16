import socket

# EV3Controller class - Til at håndtere kommunikationen mellem robotten (EV3 lego) og klienten (computer)
class EV3Controller:
    def __init__(self, ip, port=9999):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def send(self, command):
        try:
            self.sock.sendall(command.encode())
        except Exception as e:
            print("Fejl ved afsendelse:", e)

    def close(self):
        self.sock.close()
