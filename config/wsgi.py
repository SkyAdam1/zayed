import os

from django.core.wsgi import get_wsgi_application

from .settings.settings import CONFIG

if CONFIG.settings == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')
elif CONFIG.settings == 'heroku':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.heroku')

application = get_wsgi_application()
