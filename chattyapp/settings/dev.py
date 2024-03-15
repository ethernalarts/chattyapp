from .base import *
import dj_database_url

DEBUG = env('DEBUG')

DATABASES = {
    'default': dj_database_url.parse(
        env('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True
    )
}
