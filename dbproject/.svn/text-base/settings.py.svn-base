# Django settings for dbproject.

# Debugging. These settings should change when the project moves into the production server.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Administrators and Managers. These people will be informed via mail when the website encounters problems.
ADMINS = (('Nikolas Pontikos', 'n.pontikos@gmail.com'),
          ('Zhengzi Yi', 'zhengzi_kk@hotmail.com'),
          ('Tisham De', 'de.tisham@gmail.com'),
          ('Christos Gkekas', 'christos.gkekas08@imperial.ac.uk')
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL='kiphodb@dbproject.dyndns.org'
SERVER_EMAIL='kiphodb@dbproject.dyndns.org'

# Database.
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'kiphodb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'dbproject'             # Not used with sqlite3.
DATABASE_PASSWORD = '312032'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Default settings for http responses.
DEFAULT_CHARSET='utf-8'
DEFAULT_CONTENT_TYPE='text/html'

# Email Server Configuration.
EMAIL_HOST='localhost'
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=25
EMAIL_SUBJECT_PREFIX='[KiPhoDB] '
EMAIL_USE_TLS=False

# Handling of Files.
FILE_CHARSET='utf-8'
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880
FILE_UPLOAD_TEMP_DIR='/tmp'
FILE_UPLOAD_PERMISSIONS=0644

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/workspace/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$l^@6oxfss700y^j1gb=2-mw7(dl_q&2(!caj@82tm&50jj(go'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'dbproject.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "./web_site"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'dbproject.KiPhoDB',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.databrowse'
)
