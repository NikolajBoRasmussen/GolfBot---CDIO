# ev3_controller.py

import socket

class EV3Controller:
    def __init__(self, host: str, port: int = 9999, timeout: float = 5.0):
        """
        Opretter en TCP-forbindelse til EV3-serveren.
        host:   IP-adresse på EV3
        port:   Portnummer (samme som ev3_server.py lytter på)
        timeout: Socket-timeout i sekunder
        """
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        self.s.connect((host, port))

    def send(self, msg: str):
        """Sender en streng til EV3."""
        self.s.sendall(msg.encode('utf-8'))

    def recv(self, bufsize: int = 1024) -> str:
        """Læser op til bufsize bytes og returnerer det som UTF-8-tekst."""
        data = self.s.recv(bufsize)
        return data.decode('utf-8')

    def close(self):
        """Lukker forbindelsen."""
        self.s.close()
