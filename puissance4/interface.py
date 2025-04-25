import socket
import threading
import tkinter as tk
import numpy as np  
import client
from game_logic import Connect4

CELL_SIZE = 100
ROWS, COLS = 6, 7
client_socket = None
player_id = None  # "PLAYER_1" ou "PLAYER_2"

current_player = 1
mode = None
game = None

def draw_board():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            x0 = c * CELL_SIZE
            y0 = r * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            # Always draw the cell background (blue)
            canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black")
            # Then draw the circle (the token)
            canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=get_color(game.board[r][c]))

def get_color(value):
    if value == 1:
        return "red"
    elif value == 2:
        return "yellow"
    else:
        return "white"  # empty cells
def on_receive_action(col):
    
    jouer_coup_adverse(col) 

def start_game():
    global game  # Assure-toi que `game` est une variable globale
    
    # Utilisation de VecEnv : reset() renvoie un tuple (observation, info)
    game.obs, _ = game.env.reset()  # On garde seulement l'observation
    draw_board()  # Met à jour le plateau de jeu

def handle_click(event):
    global current_player

    col = event.x // CELL_SIZE

    # Empêche un coup invalide (colonne pleine)
    if not game.make_move(col):
        return

    draw_board()

    # Vérifie victoire ou match nul après le coup
    if game.winner:
        winner_text = (
            "🎉 Tu as gagné !" if mode == "pve"
            else f"🎉 Joueur {current_player} a gagné !"
        )
        status_label.config(text=winner_text)
        canvas.unbind("<Button-1>")
        return

    elif game.is_draw():
        status_label.config(text="🤝 Match nul !")
        canvas.unbind("<Button-1>")
        return

    # 🎮 Mode Humain vs Humain en ligne
    if mode == "pvp_online":
        # Vérifie si c’est le bon joueur
        if ((player_id == "PLAYER_1" and current_player != 1) or
            (player_id == "PLAYER_2" and current_player != 2)):
            return

        try:
            client.send_move(client_socket, col)  # Envoie le coup au serveur
        except:
            status_label.config(text="❌ Erreur réseau")
            return

        current_player = 2 if current_player == 1 else 1
        status_label.config(text="🕒 En attente de l'autre joueur")

    # 🤖 Mode Humain vs IA
    elif mode == "pve":
        current_player = 2
        status_label.config(text="🤖 L'IA réfléchit...")
        root.after(500, jouer_ia)  # Ajoute un petit délai pour l'effet

    # 👥 Mode Humain vs Humain local (sur le même PC)
    elif mode == "pvp_local":
        current_player = 2 if current_player == 1 else 1
        status_label.config(
            text=f"🔴 Joueur {current_player}, à toi de jouer" if current_player == 1 else f"🟡 Joueur {current_player}, à toi de jouer"
        )

def jouer_ia():
    global current_player
    
    try:
        # Update env board with current game state
        game.env.board = np.array(game.board)  
        obs = np.copy(game.env.board) 
        
        # Get AI prediction
        ai_action, _ = game.model.predict(obs, deterministic=True)
        
        # Check if the move is valid
        if not (0 <= ai_action < COLS) or game.board[0][int(ai_action)] != 0:
            # AI tried an invalid move, find a valid one instead
            print(f"AI tried invalid column {ai_action}, finding alternative...")
            for col in range(COLS):
                if game.board[0][col] == 0:  # Check if column has space
                    ai_action = col
                    print(f"AI will play column {col} instead")
                    break
            else:
                print("No valid moves found!")
                return
        
        # Apply the move in the game
        if not game.make_move(int(ai_action)):
            print(f"Failed to make AI move in column {ai_action}")
            return
            
        # Update the environment too
        obs, reward, done, truncated, info = game.env.step(int(ai_action))
        
        draw_board()
        
        if game.winner:
            status_label.config(text="🤖 L'IA a gagné!")
            canvas.unbind("<Button-1>")
        elif game.is_draw():
            status_label.config(text="🤝 Match nul!")
            canvas.unbind("<Button-1>")
        else:
            current_player = 1
            status_label.config(text="🔴 Ton tour")
    except Exception as e:
        print(f"AI Error: {e}")
        # Make sure we always return to player's turn if there's an error
        current_player = 1
        status_label.config(text="🔴 Ton tour")

def start_network_connection():
    global client_socket, player_id

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("172.31.240.1", 12345))  # ⚠️ mets l’IP du serveur ici si en réseau
    player_id = client_socket.recv(1024).decode()
    print("Connecté comme", player_id)

    thread = threading.Thread(target=receive_move, daemon=True)
    thread.start()

def receive_move():
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                col = int(data.decode())
                print("Coup adverse reçu :", col)
                root.after(100, lambda: jouer_coup_adverse(col))
        except:
            break

def jouer_coup_adverse(col):
    global current_player
    if not game.make_move(col):
        return
    draw_board()

    if game.winner:
        status_label.config(text=f"🎉 L'adversaire a gagné !")
        canvas.unbind("<Button-1>")
    elif game.is_draw():
        status_label.config(text="🤝 Match nul !")
        canvas.unbind("<Button-1>")
    else:
        current_player = 1 if current_player == 2 else 2
        status_label.config(text="🔴 À ton tour" if current_player == 1 else "🟡 À ton tour")


def lancer_jeu():
    global canvas, status_label, game, current_player

    canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.pack()

    status_label = tk.Label(root)
    status_label.pack()

    game = Connect4(root)
    # Mode Humain vs IA
    if mode == "pve":
        current_player = 1
        status_label.config(text="🔴 Ton tour (Humain)")
        canvas.bind("<Button-1>", handle_click)

    # Mode Humain vs Humain local
    elif mode == "pvp_local":
        current_player = 1
        status_label.config(text="🔴 Joueur 1 commence")
        canvas.bind("<Button-1>", handle_click)

    # Mode en ligne
    elif mode == "pvp_online":
        # current_player est déterminé dynamiquement
        status_label.config(text=f"Connecté comme {player_id}, en attente...")
        canvas.bind("<Button-1>", handle_click)

    draw_board()


def start_network_game():
    """ Cette fonction démarre le jeu réseau en établissant une connexion avec le serveur et en configurant les rappels pour recevoir les coups. """
    global client_socket, player_id

    # Appeler la fonction de connexion au réseau et passer `on_receive_action` pour gérer les coups adverses
    client_socket, player_id = client.start_network_connection(on_receive_action)

    # Afficher que le joueur est connecté
    print(f"Connecté comme {player_id}")
    
    # Mets à jour le statut du jeu si nécessaire
    status_label.config(text=f"Connecté comme {player_id}, à toi de jouer.")

def choisir_mode(selected_mode):
    global mode
    mode = selected_mode
    menu_window.destroy()
    lancer_jeu()

    if mode == "pvp_online":
        start_network_game()


# Interface principaley
root = tk.Tk()
root.title("Puissance 4")

# Menu de choix de mode
menu_window = tk.Toplevel(root)
menu_window.title("Choisir le mode de jeu")

tk.Button(menu_window, text="👥 Humain vs Humain (même PC)", command=lambda: choisir_mode("pvp_local")).pack(pady=5)
tk.Button(menu_window, text="🌐 Humain vs Humain (en ligne)", command=lambda: choisir_mode("pvp_online")).pack(pady=5)
tk.Button(menu_window, text="🤖 Humain vs IA (PPO)", command=lambda: choisir_mode("pve")).pack(pady=5)

root.mainloop()




