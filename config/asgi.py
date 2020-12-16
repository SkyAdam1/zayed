import os

from django.core.asgi import get_asgi_application

from .settings.settings import CONFIG

if CONFIG.settings == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')
elif CONFIG.settings == 'heroku':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.heroku')

application = get_asgi_application()
