import sys
import os
import hashlib

from io import BytesIO
from PIL import Image, ImageDraw

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

from django import forms
from django.conf.urls import url
from django.core.cache import cache
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag


class ImageForm(forms.Form):
	height = forms.IntegerField(min_value=1, max_value=2000)
	width = forms.IntegerField(min_value=1, max_value=2000)
	
	def generate(self,image_format='PNG'):
		# Gera uma imagem do tipo especificado e retorna em forma de bytes puros
		height = self.cleaned_data['height']
		width = self.cleaned_data['width']
		key = (f"{width}.{height}.{image_format}" )
		content = cache.get(key)
		if content is None:
			image = Image.new('RGB', (width, height))
			draw = ImageDraw.Draw(image)
			text = (f"{width} x {height}")
			textwidth, textheight = draw.textsize(text)
			if textwidth < width and textheight < height:
				texttop = (height - textheight) // 2
				textleft = (width - textwidth) // 2 
				draw.text((textleft, texttop), text, fill=(255, 255, 255))
			content = BytesIO()
			image.save(content, image_format)
			content.seek(0)
			cache.set(key, content, 60*60)
		return content

def generate_etag(request, width, height):
	content = (f"Placeholder: {width} x {height}")
	return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(request, width, height):
	form = ImageForm({'height': height, 'width': width})
	if form.is_valid():
		image = form.generate()
		return HttpResponse(image, content_type='image/png')
	else:
		return HttpResponseBadRequest('Invalid Image Request')

def index(request):
	return HttpResponse('Initial')


urlpatterns = (
	url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,
		name='placeholder'),
	url(r'^$', index, name="homepage"),
	)

application = get_wsgi_application()

if __name__ == "__main__":
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
