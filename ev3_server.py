import socket
import json
from Navigation.main import runflow

HOST, PORT = '', 9999

def handle_client(conn, addr):
    print("Forbindelse fra", addr)
    try:
        while True:
            data = conn.recv(8192).decode().strip()
            if not data:
                print("Klient lukkede forbindelsen.")
                break

            try:
                req = json.loads(data)
                coords = req["coords"]
            except Exception as e:
                print("Ugyldigt input:", repr(data), "(", e, ")")
                # sende fejl-ack her
                continue

            print("Kører runflow med coords:", coords)
            runflow(coords)
            print("coords from pictures: " , coords)
            conn.sendall(b"done")
            
            print("→ sendt ACK, venter på næste coords…")

    finally:
        conn.close()
        print("Lukker forbindelse til", addr)


def start_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print("EV3-server lytter på port", PORT)
    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)


if __name__ == "__main__":
    start_server()
