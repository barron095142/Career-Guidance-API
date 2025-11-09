from api.config_static import (
    SECRET_KEY,
    OPENROUTER_API_KEY, OPENROUTER_MODEL,
    NEWS_API_KEY, DAILY_API_LIMIT,
)

AUTH_USER_MODEL = "api.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
CORS_ALLOW_ALL_ORIGINS = True
