#import os
#from wopa.settings import BASE_DIR, PROJECT_PATH

#DATABASES = {
   # 'default': {
      #  'ENGINE': 'django.db.backends.sqlite3',
      #  'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
#}

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
LOGIN_URL = '/login/'
MEDIA_URL = '/media/'
#MEDIA_ROOT = PROJECT_PATH + '/media/'
#TEMPLATE_DIRS = (
    #os.path.join(PROJECT_PATH, 'templates/'),

#)
#STATICFILES_DIRS = (
    #os.path.join(PROJECT_PATH, 'static'),

#)

AWS_ACCESS_KEY_ID=            "AKIAIZVLQWPQFXQMTVKQ"
AWS_SECRET_ACCESS_KEY=        "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"
DATABASE_URL=                 "postgres://wvgcqruqurnjwv:Oqe6GbdwvoZ8UNKHjuxFNgmCj2@ec2-54-235-132-177.compute-1.amazonaws.com:5432/d6rs69sncgin15"
HEROKU_POSTGRESQL_COPPER_URL= "postgres://wvgcqruqurnjwv:Oqe6GbdwvoZ8UNKHjuxFNgmCj2@ec2-54-235-132-177.compute-1.amazonaws.com:5432/d6rs69sncgin15"