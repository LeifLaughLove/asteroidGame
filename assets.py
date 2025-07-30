import pygame

# Global cache to avoid reloading images
_image_cache = {}

def load_image(path):
    if path not in _image_cache:
        _image_cache[path] = pygame.image.load(path).convert_alpha()
    return _image_cache[path]


# ----SHIP SPRITES- SPACESHIP SPRITE FRAMES ARE RETURNED IN A LIST FROM THIS FUNCTION ------
def get_phazer_sprite():
    spritesheet = load_image("resources/PhazerSprite.png")
    frame_width = 56
    frame_height = 56
    columns = 2
    rows = 2

    max_frames = 4

    frames = []
    for row in range(rows):
        for col in range(columns):
            if len(frames) >= max_frames:
                break
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                spritesheet,
                (0, 0),
                pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            )
            frames.append(frame_surface)
    return frames


# ----EXPLOSION SPRITES - BIG EXPLOSION SPRITE FRAMES ARE RETURNED IN A LIST FROM THIS FUNCTION ------
def get_explosion_frames():
    spritesheet = load_image("resources/explosion.png")
    frame_width = 128
    frame_height = 128
    columns = 2
    rows = 3
    max_frames = 5

    frames = []
    for row in range(rows):
        for col in range(columns):
            if len(frames) >= max_frames:
                break
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                spritesheet,
                (0, 0),
                pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            )
            frames.append(frame_surface)
    return frames

# ----EXPLOSION SPRITES - SMALL EXPLOSION SPRITE FRAMES ARE RETURNED IN A LIST FROM THIS FUNCTION ------
def get_small_explosion_frames():
    spritesheet = load_image("resources/Small_explosion.png")
    frame_width = 38
    frame_height = 34
    columns = 2
    rows = 3
    max_frames = 6

    frames = []
    for row in range(rows):
        for col in range(columns):
            if len(frames) >= max_frames:
                break
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                spritesheet,
                (0, 0),
                pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            )
            frames.append(frame_surface)
    return frames   

def get_powerup_sprite():
    return load_image("resources/powerup.png")