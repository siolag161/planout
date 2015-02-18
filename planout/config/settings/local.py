DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'planout-dev',
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST': 'localhost', 
        'PORT': '5432', 
    } 
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kikoha04@gmail.com'
EMAIL_HOST_PASSWORD = 'kikoha89'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#PIPELINE_ENABLED = True
 
