# Muziart Backend

Django 5.2 REST API. Session-based auth with CSRF protection. Talks to a Vue 3 SPA frontend.

## Commands

```bash
python manage.py runserver          # dev server
python manage.py migrate            # apply migrations
python manage.py makemigrations     # generate migrations after model changes
python manage.py createsuperuser    # create admin user
python manage.py shell              # Django shell
```

## Architecture

```
muziart/          # project settings + root urls.py
core/             # auth views, User Profile model, CSRF endpoint
games/            # game logic, ScrollingGame, Track, Instrument models
cards/            # card collection and reward system
lessons/          # lesson content
quests/           # daily and persistent quests
daily/            # daily challenge activities
```

Each Django app follows the standard layout: `models.py`, `views.py`, `urls.py`, `serializers.py` (if needed), `admin.py`, `migrations/`.

## Key conventions

### Apps
- Each feature domain is its own Django app. Do not add models to `core` unless they belong to user identity/auth.
- Register new apps in `INSTALLED_APPS` in `settings.py`.

### Models
- Always define `__str__` on every model.
- Use `related_name` on all ForeignKey/ManyToMany fields.
- Add `db_index=True` on fields used in `filter()` or `order_by()` calls.
- Never use `null=True` on string fields (`CharField`, `TextField`) — use `blank=True` and an empty string default instead.
- Always run `makemigrations` after changing a model. Never edit migration files by hand.

### Views
- Use function-based views with `@require_http_methods` for simple endpoints.
- Return `JsonResponse`. Do not use DRF unless the endpoint is complex enough to justify it.
- Authenticate with `@login_required` or check `request.user.is_authenticated` explicitly. Never trust client-provided user IDs.
- All state-modifying endpoints must be POST (or PUT/PATCH/DELETE). Never use GET for writes.

### Auth & CSRF
- Auth is session-based. No JWT.
- The frontend calls `/api/set-csrf-token` on startup to receive the CSRF cookie.
- All mutating requests from the frontend send `X-CSRFToken` header — Django's `CsrfViewMiddleware` validates it.
- Do not use `@csrf_exempt` unless the endpoint is explicitly public and read-only.

### CORS
- Allowed origins are set dynamically from the `FRONTEND_URL` env var. Do not hardcode origins.
- `CORS_ALLOW_CREDENTIALS = True` is required for session cookies to work cross-domain.

### API responses
- Return consistent JSON shapes: `{"status": "ok", ...data}` for success, `{"error": "message"}` for errors.
- Use appropriate HTTP status codes: 400 for bad input, 401 for unauthenticated, 403 for unauthorized, 404 for not found.
- Never leak stack traces or internal details in error responses (set `DEBUG=False` in production).

### Business logic
- Put business logic in dedicated functions/modules (e.g. `quests/progress.py`, `daily/progress.py`), not inside views.
- Views should only handle HTTP concerns: parse input, call logic, return response.

### Progression system
- XP and keys are on `core.Profile`. Always use `profile.add_xp()` / `profile.add_keys()` helpers rather than direct field assignments to avoid race conditions.
- Quest and daily progress checks are side effects of game completion — call `check_quest_progress` and `complete_daily_activity` at the end of relevant game endpoints.

### Environment
- Never commit secrets. All sensitive config lives in environment variables: `SECRET_KEY`, `DATABASE_URL`, `FRONTEND_URL`, `CSRF_COOKIE_DOMAIN`.
- `DEBUG=True` only in development. Static files are served by Whitenoise in production.
- Database: SQLite for local dev, PostgreSQL in production.
