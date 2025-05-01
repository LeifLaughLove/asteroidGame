import os
import pygame
import requests
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from dotenv import load_dotenv

load_dotenv()
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:5000")  

def get_top_scores(limit=5):
    try:
        response = requests.get(f"{SERVER_URL}/get-leaderboard")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve leaderboard: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error retrieving leaderboard: {e}")
        return []

def draw_leaderboard_panel(screen, top_scores):
    panel_width = 400
    panel_height = 300
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = (SCREEN_HEIGHT - panel_height) // 2

    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surface.fill((0, 0, 0, 180))
    screen.blit(panel_surface, (panel_x, panel_y))

    font = pygame.font.Font(None, 36)
    title = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(title, (panel_x + 110, panel_y + 20))

    header_font = pygame.font.Font(None, 28)
    screen.blit(header_font.render("Name", True, (255, 255, 255)), (panel_x + 40, panel_y + 70))
    screen.blit(header_font.render("Score", True, (255, 255, 255)), (panel_x + 250, panel_y + 70))

    for i, entry in enumerate(top_scores):
        name = entry["name"]
        score = entry["score"]
        y_offset = 100 + i * 35
        screen.blit(header_font.render(str(name), True, (200, 200, 200)), (panel_x + 40, panel_y + y_offset))
        screen.blit(header_font.render(str(score), True, (200, 200, 200)), (panel_x + 250, panel_y + y_offset))

def save_score(name, score):
    from datetime import date
    try:
        payload = {
            "name": name,
            "score": score,
            "date": date.today().isoformat()
        }
        response = requests.post(f"{SERVER_URL}/submit-score", json=payload)
        if response.status_code == 201:
            print("Score submitted successfully!")
        else:
            print(f"Failed to submit score: {response.status_code}")
    except Exception as e:
        print(f"Error submitting score: {e}")