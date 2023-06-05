import random
import tkinter as tk
from tkinter import messagebox

def roll_dice():
    return random.randint(0, 10)

def move_player(player, steps):
    player["position"] += steps
    if player["level"] <= 5:
        improve = player["level"] * 30
        if player["position"] >= improve:
            player["level"] += 1
            messagebox.showinfo("Awans na poziom", f"Gracz {player['name']} awansował na poziom {player['level']}")
    else:
        improve = (player["level"] * 30) + ((player["level"]-5)*20)
        


def process_event(player, players):
    event = random.choices(
        population=["Alkowalka", "Globalne", "Personalne", "Puste pole", "Bar"],
        weights=[0.1, 0.05, 0.25, 0.5, 0.1],
        k=1
    )[0]

    if event == "Alkowalka":
        messagebox.showinfo("Alkowalka!", f"Gracz {player['name']} musi stoczyć pojedynek z wybraną przez niego osobą.")
        player["score"] += 100
    elif event == "Globalne":
        messagebox.showinfo("Globalne!", f"Gracz {player['name']} natknął się na Globalne wydarzenie! Traci 50 punktów.")
        player["score"] -= 50
    elif event == "Personalne":
        messagebox.showinfo("Personalne!", f"Gracz {player['name']} spotyka osobiste wydarzenie! Otrzymuje dodatkowy ruch.")
        play_game(players)  # Wywołujemy rekurencyjnie funkcję play_game dla tego samego gracza
    elif event == "Puste pole":
        messagebox.showinfo("Puste pole!", f"Gracz {player['name']} wchodzi na puste pole. Nic się nie dzieje.")
    elif event == "Bar":
        messagebox.showinfo("Bar!", f"Gracz {player['name']} trafia do baru! Otrzymuje dodatkowe 50 punktów.")
        player["score"] += 50

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