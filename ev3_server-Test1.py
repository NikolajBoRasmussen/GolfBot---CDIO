import socket
import json
from Navigation.main import runflow

HOST, PORT = '', 9999

def start_server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    print("EV3-server lytter på port", PORT)
    while True:
        conn, addr = s.accept()
        print("Forbindelse fra", addr)
        data = conn.recv(8192).decode().strip()

        # Ignorer tomme beskeder
        if not data:
            print("Modtaget tom besked – ignorerer.")
            conn.close()
            continue

        # Prøv at parse JSON
        try:
            req = json.loads(data)
            coords = req["coords"]
        except Exception as e:
            print("Ugyldigt input fra", addr, ":", repr(data), "(", e, ")")
            conn.close()
            continue

        # Kør dit runflow og send ACK
        print("Starter runflow med coords:", coords)
        runflow(coords)
        conn.sendall(b"done")
        conn.close()

if __name__ == "__main__":
    start_server()
