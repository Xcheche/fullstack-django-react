# Fullstack Django REST API

This repository contains a Django REST API focused on user authentication
and simple user management. It uses Django, Django REST Framework and
SimpleJWT for JWT-based authentication.

<!-- ![Project Image](docs/project-image.png) -->



## What this project provides
- JWT-based authentication (access + refresh tokens) via
  `djangorestframework-simplejwt`.
- Endpoints for user registration, login, token refresh and basic user
  retrieval.
- A small `user` app that includes a custom `User` model, manager,
  serializers, and viewsets.

## Quick start (development)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://localhost:8000/` to view the DRF browsable API and test
endpoints manually. See `AUTH_MANUAL.md` for Postman, curl and DRF UI
instructions.

## Important endpoints
- `POST /register/` — create a new user (returns user + tokens)
- `POST /login/` — obtain `access` and `refresh` tokens
- `POST /token/refresh/` — exchange a refresh token for a new access token
- `GET /user/` and `GET /user/{public_id}/` — list or retrieve users

## Notes for maintainers
- Token behaviour (lifetimes, rotation, blacklisting) is configured in
  `settings.py` via SimpleJWT settings.
- The user model exposes a `public_id` UUID used for API lookups. Use
  `UserManager.get_object_by_public_id()` to resolve safely.

## Contributing
1. Create a feature branch.
2. Add tests for new features (unit + integration).
3. Open a PR with a clear description.

## License
Add your project license here.
