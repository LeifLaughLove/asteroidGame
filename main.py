import os
import pygame
from game import Game
from menu import Menu
from shipselect import ShipSelect
from levelmanager import LevelManager
from shop import Shop
pygame.font.init()
from boss import Boss
from constants import *
from player import Player, get_player_name
from asteroid import Asteroid
from asteroidfield import AsteroidField
from powerupfield import PowerUpField
from powerup import PowerUp
from button import Button
from shot import Shot
from ui import HUD

from leaderboard import draw_leaderboard_panel, save_score
from leaderboard_client import post_score, get_leaderboard
import time

# ---- Display helpers (borderless/windowed/fullscreen) ----

def make_window(mode="borderless"):
    """Create the OS window. mode: 'windowed' | 'borderless' | 'fullscreen'."""
    flags = 0
    size = (1280, 720)  # default windowed size

    if mode == "borderless":
        # Borderless fullscreen at desktop resolution
        os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
        info = pygame.display.Info()
        size = (info.current_w, info.current_h)
        flags = pygame.NOFRAME
    elif mode == "fullscreen":
        # Exclusive fullscreen at current display mode
        size = (0, 0)
        flags = pygame.FULLSCREEN
    else:
        # Resizable windowed
        flags = pygame.RESIZABLE

    # vsync is best-effort; if not supported it is ignored
    try:
        return pygame.display.set_mode(size, flags, vsync=1)
    except TypeError:
        return pygame.display.set_mode(size, flags)

def blit_to_window(window, game_surf, base_w, base_h):
    """Scale + letterbox the internal canvas to the OS window."""
    ww, wh = window.get_size()
    scale = min(ww / base_w, wh / base_h)
    sw, sh = int(base_w * scale), int(base_h * scale)
    x = (ww - sw) // 2
    y = (wh - sh) // 2

    window.fill((0, 0, 0))
    # Nearest-neighbor keeps pixel art crisp
    scaled = pygame.transform.scale(game_surf, (sw, sh))
    window.blit(scaled, (x, y))
    pygame.display.flip()

def window_to_game(pos, window, base_w, base_h):
    """Map mouse coords from window space to internal game space."""
    ww, wh = window.get_size()
    scale = min(ww / base_w, wh / base_h)
    sw, sh = int(base_w * scale), int(base_h * scale)
    x_off = (ww - sw) // 2
    y_off = (wh - sh) // 2
    gx = (pos[0] - x_off) / scale
    gy = (pos[1] - y_off) / scale
    return pygame.Vector2(gx, gy)

# -------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    BASE_W, BASE_H = SCREEN_WIDTH, SCREEN_HEIGHT  # your internal resolution

    print(f"Starting Asteroids! \nInternal width: {BASE_W} \nInternal height: {BASE_H}")

    # Create OS window (start in borderless)
    mode = "borderless"  # 'windowed' | 'borderless' | 'fullscreen'
    window = make_window(mode)
    pygame.display.set_caption("Asteroids")

    # Internal canvas where the whole game renders
    game_surf = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA).convert_alpha()

    # Load and scale background to internal resolution
    background_lo = pygame.image.load("resources/background.png").convert_alpha()
    background = pygame.transform.scale(background_lo, (BASE_W, BASE_H))
    hud = HUD(BASE_W, BASE_H)

    font = pygame.font.Font(None, 36)

    score = 0
    game_state = "menu"
    open_shop = False
    running = True

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0

    # Construct game systems with the internal canvas
    game = Game(game_surf)
    menu = Menu(game_surf, background)
    shipselect = ShipSelect(game_surf, background)
    levelmanager = LevelManager()
    shop = Shop(game_surf, background)

    try:
        top_scores = get_leaderboard()
    except Exception as e:
        print(f"Warning: Could not connect to leaderboard server — {e}")
        top_scores = []

    # ----- MAIN LOOP -----
    while running:
        # Get all events ONCE
        events = pygame.event.get()

        # Handle global/window events here
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    mode = "windowed" if mode == "borderless" else "borderless"
                    window = make_window(mode)
                elif event.key == pygame.K_F10:
                    mode = "fullscreen"
                    window = make_window("fullscreen")
                elif event.key == pygame.K_F9:
                    mode = "windowed"
                    window = make_window("windowed")
            elif event.type == pygame.VIDEORESIZE:
                pass

        # ----- STATE MACHINE -----
        if game_state == "menu":
            # pass events and a coord-mapper
            to_game = lambda pos: window_to_game(pos, window, BASE_W, BASE_H)
            game_state = menu.menu_screen(game_surf, dt, game, events, to_game)
        elif game_state == "spaceship_select":
            to_game = lambda pos: window_to_game(pos, window, BASE_W, BASE_H)
            game_state = shipselect.selection_screen(game_surf, dt, game, events, to_game)
        elif open_shop:
            open_shop = shop.shop_screen()
        elif game_state == "playing":
            # Clear internal canvas & draw background
            game_surf.fill((0, 0, 0, 0))
            game_surf.blit(background, (0, 0))

            # GAME UPDATE
            current_level, open_shop = levelmanager.update(dt, game)
            game.update(dt, current_level)

            # GAME DRAW (draws onto game_surf)
            game.draw()

            # HUD: score (center top, internal coords)
            #score_text = font.render(f"{score}", True, (255, 255, 255))
            #text_rect = score_text.get_rect(center=(BASE_W / 2, 20))

            # Example: if you track credits in game.credits; otherwise pass 0
            hud.draw(game_surf, game.player, score=score, credits=getattr(game, "credits", 0), dt=dt)


            # Collisions & state changes
            score, game_state = game.handle_collisions(score, game_state)
            game_time += dt

        # Present: scale internal canvas to the OS window
        blit_to_window(window, game_surf, BASE_W, BASE_H)

        dt = clock.tick(60) / 1000.0  # 60 FPS cap

    pygame.quit()

# Entry
if __name__ == "__main__":
    main()