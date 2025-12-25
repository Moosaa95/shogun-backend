from .base import *


AUTH_ACCESS_TOKEN_NAME = "access_token"
AUTH_REFRESH_TOKEN_NAME = "refresh_token"

# Cookie expiration time (in seconds)
AUTH_COOKIE_ACCESS_TOKEN_MAX_AGE = 60 * 15
AUTH_COOKIE_REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 * 7

# Common Cookie Settings
AUTH_COOKIE_PATH = "/"
AUTH_COOKIE_SECURE = True
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_SAMESITE = "Lax"
