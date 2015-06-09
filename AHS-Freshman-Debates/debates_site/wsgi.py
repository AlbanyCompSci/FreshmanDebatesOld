#!/usr/bin/env python3.4
#file: wsgi.py

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debates.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
