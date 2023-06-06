import random
import pygame
import pygame_gui

# Inicjalizacja biblioteki pygame
pygame.init()

# Rozmiar okna gry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicjalizacja okna gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra planszowa")

clock = pygame.time.Clock()

def roll_dice():
    return random.randint(0, 10)

def move_player(player, steps):
    player["position"] += steps
    if player["level"] <= 5:
        improve = player["level"] * 30
        if player["position"] >= improve:
            player["level"] += 1
            print(f"Awans na poziom: Gracz {player['name']} awansował na poziom {player['level']}")
    else:
        improve = (player["level"] * 30) + ((player["level"]-5)*20)

def process_event(player, players):
    event = random.choices(
        population=["Alkowalka", "Globalne", "Personalne", "Puste pole", "Bar"],
        weights=[0.1, 0.05, 0.25, 0.5, 0.1],
        k=1
    )[0]

    if event == "Alkowalka":
        print(f"Alkowalka!: Gracz {player['name']} musi stoczyć pojedynek z wybraną przez niego osobą.")
        player["score"] += 100
    elif event == "Globalne":
        print(f"Globalne!: Gracz {player['name']} natknął się na Globalne wydarzenie! Traci 50 punktów.")
        player["score"] -= 50
    elif event == "Personalne":
        print(f"Personalne!: Gracz {player['name']} spotyka osobiste wydarzenie! Otrzymuje dodatkowy ruch.")
        play_game(players)  # Wywołujemy rekurencyjnie funkcję play_game dla tego samego gracza
    elif event == "Puste pole":
        print(f"Puste pole!: Gracz {player['name']} wchodzi na puste pole. Nic się nie dzieje.")
    elif event == "Bar":
        print(f"Bar!: Gracz {player['name']} trafia do baru! Otrzymuje dodatkowe 50 punktów.")
        player["score"] += 50

def play_game(players):
    for player in players:
        print(f"Tura gracza: {player['name']}")
        roll = roll_dice()
        print(f"Wyrzucono: {roll}")
        move_player(player, roll)
        current_position = player["position"]
        process_event(player, players)
        new_position = player["position"]
        if current_position < new_position:
            print(f"Dodatkowy ruch!: Gracz {player['name']} otrzymuje dodatkowy ruch.")
            play_game(players)  # Wywołujemy rekurencyjnie funkcję play_game dla tego samego gracza

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def game_loop():
    running = True
    start_game = False  # Flaga informująca, czy gra rozpoczęła się

    num_players = 2  # Domyślna liczba graczy
    players = []

    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Tworzenie elementów interfejsu użytkownika
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25), (100, 50)),
        text="Start",
        manager=manager
    )

    player_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100), (100, 30)),
        manager=manager
    )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        input_text = player_input.get_text()
                        if input_text.isdigit():
                            start_game = True
                            num_players = int(input_text)

    screen.fill(BLACK)

    if start_game:
        # Wyświetlanie statystyk graczy
        player_stats = ""
        for player in players:
            player_stats += f"Gracz: {player['name']}\n"
            player_stats += f"Punkty Życia: {player['score']}\n"
            player_stats += f"Pole: {player['position']}\n"
            player_stats += f"Poziom: {player['level']}\n"
            player_stats += "\n"

        font = pygame.font.Font(None, 24)
        draw_text(screen, player_stats, font, WHITE, 100, 100)

        play_game(players)

    else:
        # Wyświetlanie ekranu startowego
        manager.process_events(event)
        manager.update(pygame.time.get_ticks() / 1000)
        manager.draw_ui(screen)

    pygame.display.flip()
    clock.tick(60)

    pygame.quit()

# Uruchamianie pętli gry
game_loop()