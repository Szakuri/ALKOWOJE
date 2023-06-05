import random
import tkinter as tk
from tkinter import messagebox

def roll_dice():
    return random.randint(0, 10)

def move_player(player, steps):
    player["position"] += steps
    if player["position"] >= 50:
        player["level"] += 1
        messagebox.showinfo("Awans na poziom", f"Gracz {player['name']} awansował na poziom {player['level']}")
        player["position"] -= 50

def process_event(player, players):
    event = random.randint(1, 3)
    if event == 1:
        messagebox.showinfo("Skarb!", f"Gracz {player['name']} znalazł skarb! Otrzymuje dodatkowe 100 punktów.")
        player["score"] += 100
    elif event == 2:
        messagebox.showinfo("Przeciwnik!", f"Gracz {player['name']} natknął się na przeciwnika! Traci 50 punktów.")
        player["score"] -= 50
    elif event == 3:
        messagebox.showinfo("Dodatkowy ruch!", f"Gracz {player['name']} wejdzie na pole 31 i otrzymuje dodatkowy ruch.")
        play_game(players)  # Wywołujemy rekurencyjnie funkcję play_game dla tego samego gracza
    else:
        messagebox.showinfo("Kontynuacja podróży", f"Gracz {player['name']} kontynuuje podróż.")

def play_game(players):
    for player in players:
        messagebox.showinfo("Tura gracza", f"Tura gracza {player['name']}")
        roll = roll_dice()
        messagebox.showinfo("Wyrzucono", f"Wyrzucono: {roll}")
        move_player(player, roll)
        current_position = player["position"]
        process_event(player, players)
        new_position = player["position"]
        messagebox.showinfo("Aktualny poziom", f"Aktualny poziom gracza {player['name']}: {player['level']}")
        messagebox.showinfo("Aktualny wynik", f"Aktualny wynik gracza {player['name']}: {player['score']}")
        if current_position < new_position:
            messagebox.showinfo("Dodatkowy ruch!", f"Gracz {player['name']} otrzymuje dodatkowy ruch.")
            play_game(players)  # Wywołujemy rekurencyjnie funkcję play_game dla tego samego gracza

def start_game():
    num_players = int(num_players_var.get())
    players = []

    for i in range(num_players):
        player_name = f"Gracz {i + 1}"
        player = {"name": player_name, "level": 1, "position": 0, "score": 0}
        players.append(player)

    play_game(players)

# Tworzenie GUI
window = tk.Tk()
window.title("Gra planszowa")
window.geometry("300x200")

num_players_label = tk.Label(window, text="Liczba graczy (1-8):")
num_players_label.pack()

num_players_var = tk.StringVar(window)
num_players_var.set("2")

num_players_menu = tk.OptionMenu(window, num_players_var, "1", "2", "3", "4", "5", "6", "7", "8")
num_players_menu.pack()

start_button = tk.Button(window, text="Rozpocznij grę", command=start_game)
start_button.pack()

window.mainloop()