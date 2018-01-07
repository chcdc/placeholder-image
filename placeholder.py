import sys
import os

from io import BytesIO

from django.conf import settings

SECRET_KEY = os.environ.get('SECRET_KEY', '&yl06#la7^3b$f6_f=4@5c=%g@c892v@6ts-q62xx&reyee2^t')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
	DEBUG=DEBUG,
	SECRET_KEY=SECRET_KEY,
	ALLOWED_HOSTS=ALLOWED_HOSTS,
	ROOT_URLCONF=__name__,
	MIDDLEWARE_CLASSES=(
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	),
	INSTALLED_APPS=(
		'django.contrib.staticfiles',
		'django.contrib.contenttypes',
		'django.contrib.sites',
		'django.contrib.auth',
		),
	TEMPLATE_DIRS=(
		os.path.join(BASE_DIR, 'templates'),
		),
	STATICFILES_DIRS=(
		os.path.join(BASE_DIR, 'static'),
		),
	STATIC_URL = '/static/',
)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest

def index(request):
	return HttpResponse('Initial')

urlpatterns = (
	url(r'^$', index),
)

application = get_wsgi_application()

if __name__ == "__main__":
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
