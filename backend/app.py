"""
app.py — Serveur Flask
Expose deux routes qui appellent Dessiner() et Animer()
depuis les fichiers dessin.py et animation.py.
"""

from flask import Flask, jsonify
from flask_cors import CORS

from dessin   import Dessiner, COLS, ROWS
from animation import Animer

app = Flask(__name__)
CORS(app)   # autorise les requetes depuis le frontend React (localhost:5173)


# ─────────────────────────────────────────────
#  ROUTE : générer une image statique
#  Appel frontend : GET /api/dessiner/<nom>
#  Retour         : { "pixels": [...], "cols": 72, "rows": 36 }
# ─────────────────────────────────────────────
@app.route("/api/dessiner/<nom>")
def route_dessiner(nom):
    try:
        pixels = Dessiner(nom)
        return jsonify({"pixels": pixels, "cols": COLS, "rows": ROWS})
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 404


# ─────────────────────────────────────────────
#  ROUTE : obtenir une frame d'animation
#  Appel frontend : GET /api/animer/<nom>/<frame>
#  Retour         : { "pixels": [...], "cols": 72, "rows": 36 }
# ─────────────────────────────────────────────
@app.route("/api/animer/<nom>/<int:frame>")
def route_animer(nom, frame):
    try:
        pixels = Animer(nom, frame)
        return jsonify({"pixels": pixels, "cols": COLS, "rows": ROWS})
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 404


# ─────────────────────────────────────────────
#  ROUTE : liste des images et animations disponibles
# ─────────────────────────────────────────────
@app.route("/api/catalogue")
def route_catalogue():
    from dessin    import CATALOGUE as CAT_IMG
    from animation import CATALOGUE as CAT_ANIM
    return jsonify({
        "images"     : list(CAT_IMG.keys()),
        "animations" : list(CAT_ANIM.keys()),
    })


if __name__ == "__main__":
    print("Pixel Art Studio — backend Flask")
    print(f"  Grille : {COLS} x {ROWS} cellules")
    print("  API disponible sur http://localhost:5000")
    app.run(debug=True, port=5000)
