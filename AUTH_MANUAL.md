# Authentication Manual — Postman & DRF Browsable API

This document describes how to manually test the project's authentication
endpoints (register, login, token refresh) using Postman and the DRF
browsable API. Use `http://localhost:8000/` as the base URL when running
the development server locally.

Authentication system
- The project uses JSON Web Tokens (JWT) for authentication via the
  `djangorestframework-simplejwt` package. It issues a short-lived
  access token and a longer-lived refresh token.
- `Login` and `Register` endpoints return both `access` and `refresh` tokens.
- Protected endpoints require the access token in the `Authorization`
  header as `Bearer <access_token>`.
- Token refresh is handled at `/token/refresh/` (SimpleJWT's
  `TokenRefreshView`) which returns a new access token when given a
  valid refresh token.

Implementation notes
- `LoginSerializer` extends SimpleJWT's `TokenObtainPairSerializer` to
  include serialized user data in responses.
- `RegisterViewSet` creates a user through the custom manager and
  returns tokens using `RefreshToken.for_user(user)`.
- Token lifetimes and behaviour (rotation, blacklisting) are controlled
  by SimpleJWT settings in `settings.py`.

Prerequisites
- Project dependencies installed in the project virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Endpoints (summary)
- `POST /register/` — create a new user. Returns `user`, `refresh`, and `token` (access).
- `POST /login/` — authenticate and receive `user`, `refresh`, and `access` tokens.
- `POST /token/refresh/` — exchange a refresh token for a new access token.
- `GET /user/` and `GET /user/{public_id}/` — read user(s). Use `Authorization` header.

Request/Response examples

- Register (POST /register/)

Request JSON:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "s3curePass!"
}
```

Successful response (201):

```json
{
  "user": {
    "id": "<public-uuid>",
    "username": "alice",
    "first_name": "",
    "last_name": "",
    "email": "alice@example.com",
    "is_active": true,
    "created": "...",
    "updated": "..."
  },
  "refresh": "<refresh_token>",
  "token": "<access_token>"
}
```

- Login (POST /login/)

Request JSON (use the credentials you registered with):

```json
{
  "email": "alice@example.com",
  "password": "s3curePass!"
}
```

Successful response (200):

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "user": { ... }
}
```

- Refresh (POST /token/refresh/)

Request JSON:

```json
{ "refresh": "<refresh_token>" }
```

Response:

```json
{ "access": "<new_access_token>" }
```

Using the access token to call protected endpoints
- Add an HTTP header:

```
Authorization: Bearer <access_token>
```

Postman step-by-step
1. Create a new Postman collection and an environment with variables `base_url`, `access_token`, `refresh_token`.
2. Register request:
   - Method: POST
   - URL: `{{base_url}}/register/` (set `base_url` to `http://localhost:8000`)
   - Headers: `Content-Type: application/json`
   - Body (raw JSON): use the Register example above.
   - Save the response `refresh` and `token` into environment variables: `{{refresh_token}}`, `{{access_token}}`.
3. Login request:
   - Method: POST
   - URL: `{{base_url}}/login/`
   - Body: credentials JSON
   - Save `refresh` and `access` from the response into environment variables.
4. Refresh request:
   - Method: POST
   - URL: `{{base_url}}/token/refresh/`
   - Body: `{ "refresh": "{{refresh_token}}" }`
   - Store returned `access` into `{{access_token}}`.
5. Test protected endpoint (list users):
   - Method: GET
   - URL: `{{base_url}}/user/`
   - Header: `Authorization: Bearer {{access_token}}`

Notes for Postman
- Use environment variables to avoid copying tokens between requests.
- If you get 401 Unauthorized when hitting protected endpoints, ensure the
  `Authorization` header uses the exact string `Bearer ` followed by the token.

DRF Browsable API (in-browser)
1. Start the dev server: `python manage.py runserver`.
2. Open `http://localhost:8000/` — the API root lists available routes from the router.
3. Click the `register` or `login` endpoints to open the form; submit JSON via the form fields.
4. After login/register, copy the returned access token and use the "Authorize" button
   in the DRF UI (top-right) to set `Authorization: Bearer <access_token>` for subsequent requests.

Quick curl examples

Register:
```bash
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"s3curePass!"}'
```

Login:
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"s3curePass!"}'
```

Refresh:
```bash
curl -X POST http://localhost:8000/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

Troubleshooting
- 400 Bad Request from token endpoints: verify JSON field names and that tokens are unexpired.
- 401 Unauthorized on protected endpoints: ensure `Authorization` header is `Bearer <access_token>` and token is valid.

Example: running the included `client.py`
- The repository contains a small `client.py` which demonstrates a login request. Run it with:

```bash
./.venv/bin/python client.py
```

Replace credentials inside `client.py` with the values you registered.

If you want, I can also export a Postman collection JSON with example requests you can import.
