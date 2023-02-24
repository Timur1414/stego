import os, sys
activate_this = '/home/f0783237/python/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})
sys.path.insert(0, os.path.join('/home/f0783237/domains/trtemirov.ru/stego'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'stego.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()