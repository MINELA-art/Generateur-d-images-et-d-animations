"""
dessin.py — Générateur d'images pixel art
Même principe que test.py : on place des pixels sur une grille.
La fonction Dessiner(nom_dessin) retourne les pixels sous forme de liste
pour être envoyée au frontend via l'API Flask.
"""

import math

# ─────────────────────────────────────────────
#  DIMENSIONS DE LA GRILLE
# ─────────────────────────────────────────────
COLS = 72
ROWS = 36

# ─────────────────────────────────────────────
#  COULEURS  (tuples RGB — équivalent des codes ANSI de test.py)
# ─────────────────────────────────────────────
def rgb(r, g, b):
    return (int(r), int(g), int(b))

JAUNE      = rgb(255, 220, 0)
ORANGE     = rgb(255, 140, 0)
JAUNE_CLAR = rgb(255, 255, 150)
ROUGE      = rgb(220, 50,  50)
ROSE       = rgb(255, 110, 160)
VERT       = rgb(60,  180, 60)
BLEU_CIEL  = rgb(100, 190, 255)
BLANC      = rgb(240, 240, 255)
GRIS       = rgb(160, 160, 170)
GRIS_CLAIR = rgb(210, 210, 215)
MARRON     = rgb(139, 90,  43)
BEIGE      = rgb(240, 220, 180)
NEIGE      = rgb(220, 235, 255)
GLACE      = rgb(170, 210, 255)

# ─────────────────────────────────────────────
#  GRILLE & PLACEMENT DE PIXELS
# ─────────────────────────────────────────────
def make_grid():
    """Crée une grille vide ROWS x COLS."""
    return [[None] * COLS for _ in range(ROWS)]


def Placer_pixel(grille, x, y, char, couleur):
    """
    Place un caractère coloré à la position (x, y).
    Identique à Placer_pixel() dans test.py.
    couleur : tuple (r, g, b)
    """
    x, y = round(x), round(y)
    if 0 <= x < COLS and 0 <= y < ROWS:
        grille[y][x] = (char, couleur)


def grille_vers_pixels(grille):
    """
    Convertit la grille en liste de dicts {x, y, c, r, g, b}
    pour la sérialisation JSON vers le frontend.
    """
    pixels = []
    for y, row in enumerate(grille):
        for x, cell in enumerate(row):
            if cell:
                char, (r, g, b) = cell
                pixels.append({"x": x, "y": y, "c": char, "r": r, "g": g, "b": b})
    return pixels


# ═══════════════════════════════════════════════════════════
#  IMAGES STATIQUES
# ═══════════════════════════════════════════════════════════

def image_soleil():
    grille = make_grid()
    cx, cy = COLS // 2, ROWS // 2

    # Rayons — 8 rayons espaces de 45 degres
    for i in range(8):
        a = i * math.pi / 4
        for r in range(8, 16):
            rx = cx + r * math.cos(a) * 2   # *2 : compensation aspect ratio
            ry = cy + r * math.sin(a)
            Placer_pixel(grille, rx, ry, "✦", ORANGE)

    # Corps du soleil — ellipse remplie
    for dy in range(-6, 7):
        for dx in range(-14, 15):
            if (dx / 2) ** 2 + dy ** 2 <= 36:
                Placer_pixel(grille, cx + dx, cy + dy, "█", JAUNE)

    # Reflet lumineux
    for dy in range(-2, 2):
        for dx in range(-4, 2):
            if (dx / 2) ** 2 + dy ** 2 <= 4:
                Placer_pixel(grille, cx + dx - 4, cy + dy - 2, "█", JAUNE_CLAR)

    return grille


def image_coeur():
    grille = make_grid()
    cx, cy = COLS // 2, ROWS // 2 + 2

    # Formule mathematique du coeur : (x2+y2-1)3 - x2*y3 <= 0
    for dy in range(-11, 10):
        for dx in range(-22, 23):
            nx = dx / 2.4
            ny = -dy + 2
            if (nx ** 2 + ny ** 2 - 1) ** 3 - nx ** 2 * ny ** 3 <= 0:
                couleur = ROSE if dy < -4 else ROUGE
                Placer_pixel(grille, cx + dx, cy + dy, "♥", couleur)

    return grille


def image_maison():
    grille = make_grid()
    cx, cy = COLS // 2, ROWS - 4
    LG, HT = 17, 13

    # Sol herbeux
    for x in range(COLS):
        for y in range(cy + 1, ROWS):
            Placer_pixel(grille, x, y, "▓", VERT)

    # Murs
    for dy in range(HT):
        for dx in range(-LG, LG + 1):
            if dy == 0 or dy == HT - 1 or abs(dx) == LG:
                Placer_pixel(grille, cx + dx, cy - dy, "█", MARRON)
            else:
                Placer_pixel(grille, cx + dx, cy - dy, "▒", BEIGE)

    # Toit pointu
    for h in range(HT + 7):
        w = round((LG + 3) * (1 - h / (HT + 6)))
        for dx in range(-w, w + 1):
            Placer_pixel(grille, cx + dx, cy - HT - h,
                         "█", GRIS_CLAIR if h < 3 else ROUGE)

    # Porte
    for dy in range(7):
        for dx in range(-3, 4):
            if dy == 0 or abs(dx) == 3:
                Placer_pixel(grille, cx + dx, cy - dy, "█", MARRON)

    # Fenetres (deux cotes)
    for cote in [-1, 1]:
        for dy in range(5, 11):
            for dx in range(-3, 4):
                if dy == 5 or dy == 10 or abs(dx) == 3:
                    Placer_pixel(grille, cx + cote * 12 + dx, cy - dy, "█", MARRON)
                else:
                    Placer_pixel(grille, cx + cote * 12 + dx, cy - dy, "░", BLEU_CIEL)

    # Cheminee
    for dy in range(6):
        for dx in range(-1, 2):
            Placer_pixel(grille, cx + 9 + dx, cy - HT - 4 - dy, "█", GRIS)

    return grille


def image_montagne():
    grille = make_grid()

    # Ciel degrade nuit
    for y in range(ROWS):
        for x in range(COLS):
            t = y / ROWS
            Placer_pixel(grille, x, y, " ", rgb(10 + t * 35, 15 + t * 40, 65 + t * 75))

    base = ROWS - 2
    for x in range(COLS):
        Placer_pixel(grille, x, ROWS - 1, "█", NEIGE)
        Placer_pixel(grille, x, ROWS - 2, "░", NEIGE)

    # Grande montagne
    h1, cx1 = 28, int(COLS * 0.62)
    for h in range(h1):
        w = round((h1 - h) * 0.72)
        for dx in range(-w, w + 1):
            col = NEIGE if h < 5 else (GRIS_CLAIR if h < 11 else GRIS)
            Placer_pixel(grille, cx1 + dx, base - h, "█", col)

    # Petite montagne
    h2, cx2 = 20, int(COLS * 0.30)
    for h in range(h2):
        w = round((h2 - h) * 0.60)
        for dx in range(-w, w + 1):
            Placer_pixel(grille, cx2 + dx, base - h, "█", NEIGE if h < 3 else GRIS)

    # Sapins
    for i in range(4):
        tx = 5 + i * 5
        for h in range(7):
            larg = max(0, 4 - h)
            for dx in range(-larg, larg + 1):
                Placer_pixel(grille, tx + dx, base - h - 1, "▲", VERT)
        Placer_pixel(grille, tx, base, "█", MARRON)

    # Etoiles et lune
    for x, y in [(3,1),(16,3),(30,0),(45,2),(59,1),(65,4),(8,5),(50,0)]:
        Placer_pixel(grille, x, y, "·", BLANC)
    Placer_pixel(grille, 62, 3, "◯", JAUNE_CLAR)

    return grille


def image_flocon():
    grille = make_grid()
    cx, cy = COLS // 2, ROWS // 2

    # 6 branches principales + branches secondaires
    for i in range(6):
        a = i * math.pi / 3
        for r in range(13):
            rx = cx + r * math.cos(a) * 2
            ry = cy + r * math.sin(a)
            col = BLANC if r < 3 else (GLACE if r < 8 else NEIGE)
            Placer_pixel(grille, rx, ry, "█", col)

            if 4 <= r <= 9:
                for cote in [-1, 1]:
                    ba = a + cote * math.pi / 3
                    for br in range(1, 5):
                        bx = cx + r * math.cos(a) * 2 + br * math.cos(ba) * 1.6
                        by = cy + r * math.sin(a) + br * math.sin(ba)
                        Placer_pixel(grille, bx, by, "·", GLACE)

    # Centre etoile
    for dy in range(-1, 2):
        for dx in range(-2, 3):
            Placer_pixel(grille, cx + dx, cy + dy, "✦", BLANC)

    return grille


# ─────────────────────────────────────────────
#  CATALOGUE  &  POINT D'ENTREE
# ─────────────────────────────────────────────
CATALOGUE = {
    "soleil"   : image_soleil,
    "coeur"    : image_coeur,
    "maison"   : image_maison,
    "montagne" : image_montagne,
    "flocon"   : image_flocon,
}


def Dessiner(nom_dessin):
    """
    Genere l'image demandee et retourne ses pixels sous forme de
    liste de dicts {x, y, c, r, g, b} prête pour etre serialisee en JSON.

    Appelee par Flask via :  GET /api/dessiner/<nom>
    """
    if nom_dessin not in CATALOGUE:
        raise ValueError(f"Image inconnue : '{nom_dessin}'. "
                         f"Disponibles : {list(CATALOGUE)}")
    grille = CATALOGUE[nom_dessin]()
    return grille_vers_pixels(grille)
