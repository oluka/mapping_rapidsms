# Django settings for rapidsms_geo project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)


path=os.path.realpath(os.path.dirname('__file__'))
MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'gis'             # Or path to database file if using sqlite3.
DATABASE_USER = 'rapidsms_user'             # Not used with sqlite3.
DATABASE_PASSWORD = 'rapidpass'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i)7cjae@*%0_@3ppazw-amc2&^$_3^!cc#ozxd36srv)*1tazr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
     'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

)

ROOT_URLCONF = 'rapidsms_geo.urls'

TEMPLATE_DIRS = (
                # path+'/templates',###gets the servers root path / shd tweak
                '/home/mugisha/projects/django-projects/rapidsms_geo/templates'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.sites',
    'Map',
    
    'django_shapes.shapes',
)
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

ROOT_PROJECT_FOLDER = os.path.dirname(__file__)

DISK_CACHE = os.path.join(ROOT_PROJECT_FOLDER,'Media/cache')

MAPFILE_ROOT = os.path.join(ROOT_PROJECT_FOLDER,'mapfiles')

MAPNIK_MAPFILE =os.path.join( MAPFILE_ROOT ,'world.xml')
TILECACHE_CONF=os.path.join(ROOT_PROJECT_FOLDER,'config/tilecache.cfg')

GMAP_API_KEY = ''

MAPS_POSTGIS_HOST='localhost'

MAPS_POSTGIS_USER='rapidsms_user'

MAPS_POSTGIS_PASS='rapidpass'

MAPS_POSTGIS_DB='gis'

TILE_SIZE = 256

