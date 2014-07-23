import os
from wopa.settings import BASE_DIR, PROJECT_PATH

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
wopa_submitter/views.py}

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
LOGIN_URL = '/login/'
MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_PATH + '/media/'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),

)
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),

)
