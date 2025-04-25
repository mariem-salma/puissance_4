
Ce projet est une implémentation de Puissance 4 en Python avec plusieurs modes : local, en ligne et contre une IA.

## Modes de jeu

- **Local** : Deux joueurs sur le même PC.
- **En ligne** : Un joueur héberge comme serveur, l'autre se connecte.
- **Solo** : Contre une IA entraînée.

## Structure

- `interface.py` : Interface graphique.
- `server.py` : Serveur pour le mode en ligne.
- `client.py` : Client réseau.
- `PPO.py` : Entraînement de l'IA.
- `game_logic.py` : Logique du jeu.

## Installation

1. **Cloner le project** :
   ```bash
   git clone https://github.com/mariem-salma/puissance_4.git
   cd puissance4
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel** :
     ```bash
     venv\Scripts\activate
     ```

4. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```


## Utilisation

1. **Lancer le serveur** (pour le mode en ligne) :
   ```bash
   python server.py
   ```
2. **Lancer le jeu** :
   ```bash
   python interface.py
   ```


