# ui.py
import pygame

# ---- simple palette ----
UI_BG      = (0, 0, 0, 140)      # panel bg (alpha)
UI_PANEL   = (20, 20, 28, 200)
UI_BORDER  = (70, 70, 90)
TXT        = (220, 220, 230)

HP_BACK    = (60, 24, 32)
HP_FILL    = (220, 70, 90)

ST_BACK    = (22, 44, 56)
ST_FILL    = (80, 200, 255)

CD_OVERLAY = (0, 0, 0, 120)      # cooldown darken

def _draw_panel(surf, rect, bg=UI_PANEL, border=UI_BORDER):
    x, y, w, h = rect
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill(bg)
    surf.blit(panel, (x, y))
    pygame.draw.rect(surf, border, rect, 1)

def _draw_bar(surf, pos, size, value, max_value, back_col, fill_col, border_col=UI_BORDER):
    x, y = pos; w, h = size
    pygame.draw.rect(surf, back_col, (x, y, w, h))
    ratio = 0 if max_value <= 0 else max(0.0, min(1.0, value / max_value))
    fw = int(w * ratio)
    if fw > 0:
        pygame.draw.rect(surf, fill_col, (x, y, fw, h))
    pygame.draw.rect(surf, border_col, (x, y, w, h), 1)

def _label(surf, font, text, pos, color=TXT, center=False):
    img = font.render(text, True, color)
    r = img.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    surf.blit(img, r)

class AbilityPanel:
    """Shows ability slots (Q, E, Shift) with cooldown overlays."""
    def __init__(self, font, x, y, slot_w=56, slot_h=56, gap=10):
        self.font = font
        self.x, self.y = x, y
        self.slot_w, self.slot_h, self.gap = slot_w, slot_h, gap
        # default ordering/labels; works with the ability system we discussed
        self.slots = [("Q", "Shockwave"), ("E", "Blink"), ("⇧", "Dash")]  # labels only

    def draw(self, surf, player):
        x = self.x
        for label, ability_name in self.slots:
            rect = pygame.Rect(x, self.y, self.slot_w, self.slot_h)
            _draw_panel(surf, rect)
            _label(surf, self.font, label, (rect.x + 6, rect.y + 4))
            # cooldown overlay if ability exists
            ab = None
            # If you used a dict like {pygame.K_q: ShockwaveAbility(), ...}:
            # try to find by name instead; adapt if your structure differs
            if hasattr(player, "abilities"):
                for a in player.abilities.values():
                    if getattr(a, "name", "") == ability_name:
                        ab = a; break
            if ab:
                cd = getattr(ab, "timer", 0.0)
                max_cd = max(0.001, getattr(ab, "cooldown", 1.0))
                if cd > 0:
                    frac = max(0.0, min(1.0, cd / max_cd))
                    h = int(self.slot_h * frac)
                    overlay = pygame.Surface((self.slot_w-2, h), pygame.SRCALPHA)
                    overlay.fill(CD_OVERLAY)
                    surf.blit(overlay, (rect.x+1, rect.bottom - h - 1))
            x += self.slot_w + self.gap

class PowerupPanel:
    """Grid of tiny powerup icons/labels (active run-only)."""
    def __init__(self, font, x, y, cols=6, cell=28, gap=6):
        self.font = font
        self.x, self.y = x, y
        self.cols, self.cell, self.gap = cols, cell, gap

    def draw(self, surf, player):
        # Expect player.active_powerups: list of strings or objects with .short/.icon
        items = getattr(player, "active_powerups", [])
        if not items:
            return
        # panel bounds
        rows = (len(items) + self.cols - 1) // self.cols
        w = self.cols * self.cell + (self.cols - 1) * self.gap + 8
        h = rows * self.cell + (rows - 1) * self.gap + 8
        _draw_panel(surf, (self.x, self.y, w, h))
        # draw cells
        ox, oy = self.x + 4, self.y + 4
        for i, it in enumerate(items):
            r = pygame.Rect(
                ox + (i % self.cols) * (self.cell + self.gap),
                oy + (i // self.cols) * (self.cell + self.gap),
                self.cell, self.cell
            )
            pygame.draw.rect(surf, UI_BORDER, r, 1)
            # If you have icons, blit them here; otherwise label
            label = getattr(it, "short", None) or (str(it)[:2].upper())
            _label(surf, self.font, label, (r.centerx, r.centery), center=True)

class HUD:
    """Owns and draws all UI; call hud.draw(game_surface, player, score, credits, dt)."""
    def __init__(self, base_w, base_h, font=None):
        self.base_w, self.base_h = base_w, base_h
        self.font = font or pygame.font.Font(None, 24)

        # Layout anchors/margins (internal 1920x1080 space is fine)
        self.margin = 16

        # Bars sizes
        self.hp_size = (260, 18)
        self.st_size = (220, 12)

        # Panels
        self.abilities = AbilityPanel(self.font, x=self.margin, y=base_h - (56 + self.margin))
        self.powerups  = PowerupPanel(self.font, x=base_w - (6*28 + 5*6 + 8) - self.margin,
                                      y=base_h - (28 + 8 + self.margin), cols=6, cell=28, gap=6)

    def draw(self, surf, player, score=0, credits=0, dt=0.0):
        # Top-left: HP + Stamina/Energy
        hp_x, hp_y = self.margin, self.margin
        st_x, st_y = self.margin, hp_y + self.hp_size[1] + 8

        max_hp = getattr(player, "max_hp", 100)
        hp     = getattr(player, "health", max_hp)
        _draw_bar(surf, (hp_x, hp_y), self.hp_size, hp, max_hp, HP_BACK, HP_FILL)

        # Label
        _label(surf, self.font, f"HP {int(hp)}/{int(max_hp)}", (hp_x + 6, hp_y - 20))

        # Stamina/Energy (optional). If you don’t have stamina, comment this out.
        stamina    = getattr(player, "stamina", None)
        max_stam   = getattr(player, "max_stamina", 100)
        if stamina is not None:
            _draw_bar(surf, (st_x, st_y), self.st_size, stamina, max_stam, ST_BACK, ST_FILL)
            _label(surf, self.font, "Energy", (st_x + 6, st_y - 18))

        # Top-center: Score
        sc_text = self.font.render(str(int(score)), True, TXT)
        sc_rect = sc_text.get_rect(center=(self.base_w // 2, 22))
        surf.blit(sc_text, sc_rect)

        # Top-right: Credits (meta or run-currency)
        cred_text = self.font.render(f"Scrap {int(credits)}", True, TXT)
        cr = cred_text.get_rect(topright=(self.base_w - self.margin, self.margin))
        surf.blit(cred_text, cr)

        # Bottom-left: abilities with cooldown overlays
        self.abilities.draw(surf, player)

        # Bottom-right: active powerups grid
        self.powerups.draw(surf, player)
