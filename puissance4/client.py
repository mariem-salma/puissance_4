import socket
import threading

# Connexion au serveur
def start_network_connection(on_receive_move):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))  # L'IP du serveur ici, localhost pour les tests
    player_id = client_socket.recv(1024).decode()
    print(f"Connecté comme {player_id}")

    # Lancer un thread pour recevoir les coups de l'adversaire
    def receive_move():
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    col = int(data.decode())
                    on_receive_move(col)  # Appeler la fonction de callback pour jouer le coup adverse
            except:
                break

    thread = threading.Thread(target=receive_move, daemon=True)
    thread.start()

    return client_socket, player_id

# Envoyer un coup au serveur
def send_move(client_socket, col):
    try:
        client_socket.sendall(str(col).encode())
    except:
        print("Erreur réseau lors de l'envoi du coup")


