# Mon Application React + Flask + Turtle

## Structure du projet

```
projet/
├── backend/
│   ├── app.py           ← Flask (API)
│   ├── phrase.py        ← Générateur Markov (inchangé)
│   ├── dessin.py        ← Turtle (inchangé)
│   ├── requirements.txt
│   └── poemes.txt       ← à placer ici
└── frontend/
    ├── src/
    │   ├── App.jsx      ← Interface React
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Lancement

### 1. Backend Flask (terminal 1)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

→ Flask tourne sur http://localhost:5000

### 2. Frontend React (terminal 2)

```bash
cd frontend
npm install
npm run dev
```

→ React tourne sur http://localhost:5173

## Comment ça fonctionne

- React envoie des requêtes HTTP vers Flask (`fetch`)
- Flask appelle `Creer_Phrase()` ou `dessiner_forme()` en Python
- Turtle s'ouvre dans une **fenêtre séparée** sur votre machine
- `flask-cors` autorise la communication entre les deux serveurs
