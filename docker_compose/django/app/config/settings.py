import os
from pathlib import Path
from split_settings.tools import include
from dotenv import load_dotenv

load_dotenv()

include(
    "components/database.py",
    "components/debug.py",
    "components/i18n.py",
    "components/password-validation.py",
    "components/middleware.py",
    "components/templates.py",
    "components/applications.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = (os.environ.get("SECRET_KEY"),)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
LOCALE_PATHS = ["movies/locale"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
