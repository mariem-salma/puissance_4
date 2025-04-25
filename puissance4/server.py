import socket
import threading

HOST = '0.0.0.0'  # Use localhost for testing
PORT = 12345

clients = []

def handle_client(conn, addr, player_id):
    print(f"Connexion de {addr} en tant que {player_id}")
    conn.sendall(player_id.encode())
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            for c in clients:
                if c != conn:
                    c.sendall(data)
        except:
            break
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Serveur en attente de connexions...")

    while len(clients) < 2:
        conn, addr = server.accept()
        clients.append(conn)
        player_id = "PLAYER_1" if len(clients) == 1 else "PLAYER_2"
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()

start_server()


