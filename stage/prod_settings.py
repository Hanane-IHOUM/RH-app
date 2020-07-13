import dj_database_url

from .settings import *


DATABASES['default'] = dj_database_url.config()


MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = False
TEMPLATE_DEBUG = False



ALLOWED_HOSTS = ['rh-selection.herokuapp.com']
