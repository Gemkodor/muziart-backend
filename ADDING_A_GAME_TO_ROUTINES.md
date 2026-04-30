# Adding a new mini-game to daily routines — Backend

> See also: `ADDING_A_GAME_TO_ROUTINES.md` in `muziart-frontend` for the frontend steps.

---

## 1. Register the game in the generator

**File:** `daily/generator.py`

Add an entry to the `GAMES` list:

```python
GAMES = [
    {'type': 'notes_reading',  'title': 'Lecture de notes',       'minutes': 3, 'auto': True},
    {'type': 'blind_test',     'title': 'Blind test',             'minutes': 2, 'auto': False},
    {'type': 'scales_builder', 'title': 'Construction de gammes', 'minutes': 3, 'auto': False},
    # Add your game here:
    {'type': 'my_game',        'title': 'Mon nouveau jeu',        'minutes': 3, 'auto': False},
]
```

Fields:
- `type` — internal snake_case key, used everywhere to identify the game.
- `title` — displayed in the program activity list.
- `minutes` — estimated duration; controls how many activities fit in the user's time budget.
- `auto` — set to `True` if the backend marks this activity complete automatically when the session ends (see step 2). Set to `False` if the user completes it manually via "J'ai terminé".

---

## 2. Mark the activity complete when the game session ends

**File:** `games/views.py` (or wherever your game's API endpoint lives)

Call `complete_daily_activity` at the end of a session so the routine advances:

```python
from daily.progress import complete_daily_activity

def end_my_game_session(request):
    # ... your scoring logic ...
    complete_daily_activity(profile, 'my_game')
    return JsonResponse({'success': True})
```

`complete_daily_activity(profile, activity_type)` finds the first uncompleted activity of that type in today's program and marks it done. If the user has no active program it does nothing safely.

If your game has no server-side session endpoint (fully client-side), skip this step and set `auto: False` in the generator — the user completes it manually.

---

## Checklist

- [ ] Entry added to `GAMES` in `daily/generator.py`
- [ ] `complete_daily_activity(profile, 'my_game')` called in the game's API endpoint (if `auto: True`)
