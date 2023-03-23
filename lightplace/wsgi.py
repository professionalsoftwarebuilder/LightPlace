import os
from django.core.wsgi import get_wsgi_application

os.environ['HTTPS'] = "on"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lightplace.settings.development')

application = get_wsgi_application()
