# PET_internet_shop
PET Project for students

### Environment variables
```
export SECRET_KEY=your_secret_key
export DB_NAME=your_production_db_name
export DB_USER=your_production_db_user
export DB_PASSWORD=your_production_db_password
export DB_HOST=your_production_db_host
export DB_PORT=your_production_db_port
```

### Local Database configuration
#### create file local_settings.py in folder with django settings and configure it like in example:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': your_local_db_name,
        'USER': your_local_db_user,
        'PASSWORD': your_local_db_password,
        'HOST': your_local_db_host,
        'PORT': your_local_db_port,
    }
}
```