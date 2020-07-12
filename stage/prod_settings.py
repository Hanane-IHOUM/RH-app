import dj_database_url

from .settings import *


DATABASES['default'] = dj_database_url.config()

DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = '_!pjrhz8suvg%o7ufwhqg-ymy14q-n9*f^(8#c97v#$m822m@s'

ALLOWED_HOSTS = ['rh-selection.herokuapp.com']
