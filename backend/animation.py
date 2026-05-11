"""
animation.py — Generateur d'animations pixel art
Meme principe que la boucle while True de test.py :
chaque appel a Animer(nom, frame) calcule et retourne une frame.
Le frontend appelle cette fonction en boucle pour animer.
"""

import math

# On importe les utilitaires de dessin.py
# (grille, Placer_pixel, couleurs, dimensions)
from dessin import (
    COLS, ROWS, rgb,
    JAUNE, ORANGE, JAUNE_CLAR,
    ROUGE, ROSE, VERT, BLEU_CIEL,
    BLANC, GRIS, GRIS_CLAIR, MARRON, BEIGE, NEIGE, GLACE,
    make_grid, Placer_pixel, grille_vers_pixels,
)

# ═══════════════════════════════════════════════════════════
#  ANIMATIONS  (une fonction par animation)
#  Chaque fonction prend `frame` (entier incrementé par le frontend)
#  et retourne une grille representant cet instant.
# ═══════════════════════════════════════════════════════════

def anim_soleil(frame):
    """
    Soleil tournant — directement issu de test.py.
    Les rayons pivotent autour du centre a chaque frame.
    """
    grille = make_grid()
    cx, cy = COLS // 2, ROWS // 2
    angle  = frame * 0.05

    # Rayons qui tournent
    for i in range(8):
        a = angle + i * (math.pi / 4)
        for r in range(8, 16):
            rx = cx + r * math.cos(a) * 2
            ry = cy + r * math.sin(a)
            Placer_pixel(grille, rx, ry, "✦", ORANGE)

    # Corps du soleil
    for dy in range(-6, 7):
        for dx in range(-14, 15):
            if (dx / 2) ** 2 + dy ** 2 <= 36:
                Placer_pixel(grille, cx + dx, cy + dy, "█", JAUNE)

    # Reflet
    for dy in range(-2, 2):
        for dx in range(-4, 2):
            if (dx / 2) ** 2 + dy ** 2 <= 4:
                Placer_pixel(grille, cx + dx - 4, cy + dy - 2, "█", JAUNE_CLAR)

    return grille


def anim_pluie(frame):
    """
    Pluie style Matrix.
    Chaque colonne a une trainee de caracteres verts qui tombent.
    """
    grille = make_grid()

    for x in range(0, COLS, 2):
        phase = (x * 7 + frame) % (ROWS * 2)
        for traine in range(9):
            y = (phase - traine + ROWS * 2) % (ROWS * 2)
            if y < ROWS:
                lum  = 1 - traine / 9
                char = "█" if traine == 0 else ("▓" if traine < 3 else "░")
                Placer_pixel(grille, x, y, char, rgb(0, 50 + 210 * lum, 0))

    return grille


def anim_vague(frame):
    """
    Vagues de mer avec ciel, surface animee et profondeur.
    Deux ondes sinusoidales superposees creent un mouvement naturel.
    """
    grille = make_grid()

    for x in range(COLS):
        # Superposition de deux vagues
        v1  = math.sin(x * 0.22 - frame * 0.11) * 5
        v2  = math.sin(x * 0.11 - frame * 0.07 + 1) * 3
        sur = int(ROWS / 2 + v1 + v2)   # niveau de la surface

        for y in range(ROWS):
            if y < sur:
                # Ciel
                t = y / sur if sur > 0 else 0
                Placer_pixel(grille, x, y, " ", rgb(55 + t * 35, 75 + t * 45, 145))
            elif y == sur:
                # Surface scintillante
                wc = 155 + 60 * math.sin(frame * 0.1 + x * 0.18)
                Placer_pixel(grille, x, y, "~", rgb(110, 190, wc))
            elif y == sur + 1:
                Placer_pixel(grille, x, y, "≈", rgb(65, 155, 205))
            else:
                # Profondeur — s'assombrit vers le bas
                d = (y - sur) / max(1, ROWS - sur)
                Placer_pixel(grille, x, y, "░", rgb(0, 55 + d * 20, 138 - d * 75))

        # Cretes blanches sur les bosses de vague
        if math.sin(x * 0.45 - frame * 0.18) > 0.65 and 1 <= sur < ROWS:
            Placer_pixel(grille, x, sur - 1, "˜", BLANC)

    return grille


def anim_feu(frame):
    """
    Feu anime — chaleur sinusoidale qui monte depuis le bas.
    L'intensite de chaque pixel est calculee par des ondes qui
    se combinent pour simuler le scintillement des flammes.
    """
    grille = make_grid()

    for y in range(ROWS):
        for x in range(COLS):
            # Chaleur de base + scintillement
            base      = math.sin(x * 0.3  + frame * 0.2)  * 0.3 + 0.7
            scintille = math.sin(x * 1.7  + frame * 0.5)  * 0.15 \
                      + math.sin(x * 3.1  + frame * 0.8)  * 0.10
            # La chaleur diminue en montant
            montee    = (ROWS - 1 - y) / (ROWS - 1)
            chaleur   = max(0, (base + scintille) * montee - 0.04 - montee * 0.28)

            if   chaleur > 0.65:
                Placer_pixel(grille, x, y, "█", rgb(255, min(255, chaleur * 330), 0))
            elif chaleur > 0.45:
                Placer_pixel(grille, x, y, "▓", rgb(255, chaleur * 200, 0))
            elif chaleur > 0.27:
                Placer_pixel(grille, x, y, "▒", rgb(chaleur * 580, 28, 0))
            elif chaleur > 0.11:
                Placer_pixel(grille, x, y, "░", rgb(58, 10, 0))

    return grille


def anim_flocon(frame):
    """
    Flocons de neige qui tombent doucement en se balancant.
    Chaque flocon a sa propre vitesse et trajectoire sinusoidale.
    """
    grille = make_grid()

    for i in range(35):
        vitesse     = 0.22 + (i % 5) * 0.11
        balancement = math.sin(frame * 0.04 + i * 1.2) * 2
        x = round(((i * 13 + 7) % COLS + balancement + COLS) % COLS)
        y = round((i * 4 + int(frame * vitesse)) % ROWS)

        chars = ["❄", "✦", "·", "*"]
        Placer_pixel(grille, x,     y,     chars[i % 4], BLANC)
        if i % 4 > 0:
            Placer_pixel(grille, x - 1, y,     "·", GLACE)
            Placer_pixel(grille, x + 1, y,     "·", GLACE)
        if i % 4 > 1:
            Placer_pixel(grille, x,     y - 1, "·", NEIGE)
            Placer_pixel(grille, x,     y + 1, "·", NEIGE)

    # Accumulation de neige au sol
    for x in range(COLS):
        Placer_pixel(grille, x, ROWS - 1, "▓", NEIGE)

    return grille


# ─────────────────────────────────────────────
#  CATALOGUE  &  POINT D'ENTREE
# ─────────────────────────────────────────────
CATALOGUE = {
    "soleil"  : anim_soleil,
    "pluie"   : anim_pluie,
    "vague"   : anim_vague,
    "feu"     : anim_feu,
    "flocons" : anim_flocon,
}


def Animer(nom_anim, frame):
    """
    Calcule et retourne la frame demandee de l'animation choisie.
    Retourne une liste de dicts {x, y, c, r, g, b} prête pour JSON.

    Appelee par Flask via :  GET /api/animer/<nom>/<frame>
    """
    if nom_anim not in CATALOGUE:
        raise ValueError(f"Animation inconnue : '{nom_anim}'. "
                         f"Disponibles : {list(CATALOGUE)}")
    grille = CATALOGUE[nom_anim](frame)
    return grille_vers_pixels(grille)
