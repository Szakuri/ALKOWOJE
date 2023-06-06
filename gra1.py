import random
import pygame
import pygame_gui

# Rozmiar okna gry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

def roll_dice():
    return random.randint(1, 6)

def move_player(player, steps):
    player["position"] += steps
    if player["level"] < 5:
        if player["position"] >= (player["level"] + 1) * 30:
            player["level"] += 1
            print(f"Aktualizacja poziomu: Gracz {player['name']} awansował na poziom {player['level']}")
    else:
        if player["position"] >= 200 + (player["level"] - 5) * 50:
            player["level"] += 1
            print(f"Aktualizacja poziomu: Gracz {player['name']} awansował na poziom {player['level']}")

def process_event(player):
    event = random.choices(
        population=["Puste pole", "Coś"],
        weights=[0.7, 0.3],
        k=1
    )[0]

    if event == "Puste pole":
        print(f"Puste pole!: Gracz {player['name']} wchodzi na puste pole. Nic się nie dzieje.")
    elif event == "Coś":
        print(f"Coś!: Gracz {player['name']} spotyka wydarzenie! Otrzymuje dodatkowe punkty życia.")
        player["score"] += 10

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def game_loop(num_players):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gra planszowa")

    running = True
    start_game = False  # Flaga informująca, czy gra rozpoczęła się

    players = create_players(num_players)
    current_player_index = 0

    start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25), (100, 50))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if start_game:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_player = players[current_player_index]
                        roll = roll_dice()
                        print(f"Wyrzucono: {roll}")
                        move_player(current_player, roll)
                        current_position = current_player["position"]
                        process_event(current_player)
                        new_position = current_player["position"]
                        if current_position < new_position:
                            print(f"Dodatkowy ruch!: Gracz {current_player['name']} otrzymuje dodatkowy ruch.")
                        current_player_index = (current_player_index + 1) % len(players)

            else:
                # Obsługa interfejsu startowego
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        start_game = True

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

        pygame.draw.rect(screen, WHITE, start_button_rect)  # Rysowanie prostokąta przycisku

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def create_players(num_players):
    players = []
    for i in range(num_players):
        player = {
            "name": f"Gracz {i+1}",
            "score": 10,
            "position": 0,
            "level": 0
        }
        players.append(player)
    return players

# Uruchamianie pętli gry
def start_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gra planszowa")

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLACK)
        manager.process_events(event)
        manager.update(pygame.time.get_ticks() / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)

        if start_button.check_pressed():
            num_players_text = player_input.get_text()
            num_players = int(num_players_text) if num_players_text.isdigit() else 2
            pygame.quit()
            game_loop(num_players)

start_game()
