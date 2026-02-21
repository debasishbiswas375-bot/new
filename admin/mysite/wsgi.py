import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for your project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# This is the only line needed to start the web server
application = get_wsgi_application()
