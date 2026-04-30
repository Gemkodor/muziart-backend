# Muziart — Backend

API Django REST pour la plateforme d'apprentissage musicale Muziart.

**Frontend :** [muziart-frontend](../muziart-frontend)

---

## Stack

| | |
|---|---|
| Framework | Django 5 + Python 3.11 |
| API | Django REST Framework |
| Base de données | MySQL (prod) / SQLite (dev) |
| Serveur | Gunicorn + Nginx |
| Déploiement | Docker + CapRover |

---

## Installation

```bash
cp .env.example .env
# → voir la section "Variables d'environnement" ci-dessous

uv sync
# ou : pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # optionnel
python manage.py runserver        # http://localhost:8000
```

### Variables d'environnement

```env
SECRET_KEY=change-me-generate-a-strong-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite en local
DATABASE_URL=sqlite:///db.sqlite3

# URL du frontend (CORS et CSRF)
FRONTEND_URL=http://localhost:5173
CSRF_COOKIE_DOMAIN=
```

> **Production (CapRover)** : les variables sont définies dans l'interface CapRover, pas dans un fichier `.env`. `DATABASE_URL` pointe vers MySQL (`mysql://user:pass@host/db`).

---

## Scripts

| Commande | Description |
|---|---|
| `python manage.py runserver` | Serveur de développement |
| `python manage.py migrate` | Appliquer les migrations |
| `python manage.py makemigrations` | Créer de nouvelles migrations |
| `python manage.py collectstatic` | Rassembler les fichiers statiques |
| `python manage.py createsuperuser` | Créer un admin |

---

## Structure

```
muziart-backend/
├── core/          # Authentification, profil utilisateur, XP, clés
├── games/         # Endpoints et modèles des jeux
├── lessons/       # Endpoints et modèles des leçons
├── daily/         # Routines quotidiennes (générateur, progression)
│   ├── generator.py   # Génération des activités
│   ├── progress.py    # complete_daily_activity()
│   ├── models.py      # DailyProgram, DailyActivity
│   └── views.py       # API /api/daily/
├── cards/         # Cartes compositeurs et instruments
└── quests/        # Système de quêtes
```

---

## API

### Authentification
```
GET  /api/set-csrf-token
POST /api/register
POST /api/login
POST /api/logout
GET  /api/user
```

### Progression
```
POST /api/keys/add_keys/
POST /api/keys/add_xp/
```

### Routines quotidiennes
```
GET  /api/daily/today/           — programme du jour (null si inexistant)
POST /api/daily/today/           — générer un programme { time_goal: 5|10|15|20 }
POST /api/daily/activities/:id/complete/  — complétion manuelle d'une activité
POST /api/daily/extra/           — ajouter une activité bonus
```

### Autres
```
/api/games/    — endpoints des jeux
/api/lessons/  — endpoints des leçons
/api/cards/    — endpoints des cartes
/admin/        — interface d'administration Django
```

---

## Routines quotidiennes

Le générateur (`daily/generator.py`) alterne jeux et leçons pour remplir le temps de pratique choisi par l'utilisateur. Quand un jeu se termine, son endpoint doit appeler `complete_daily_activity(profile, 'game_type')` pour faire avancer la routine.

→ Voir [ADDING_A_GAME_TO_ROUTINES.md](./ADDING_A_GAME_TO_ROUTINES.md) pour intégrer un nouveau jeu.

---

## Déploiement

```bash
docker build -t muziart-backend .
docker run -p 8000:8000 \
  -e SECRET_KEY=<clé-secrète> \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=mondomaine.com \
  -e DATABASE_URL=mysql://user:pass@host/db \
  -e FRONTEND_URL=https://mondomaine.com \
  muziart-backend
```

Le Dockerfile exécute automatiquement `collectstatic`, `migrate` puis démarre Gunicorn avec 3 workers.

Déploiement continu via **CapRover** (`captain-definition` à la racine).
Production : https://muziart-api.arthania.fr
