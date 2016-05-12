from django.http import HttpResponse
from django.template import loader

from .models import Gif


def index(request):
	latest_gif_list = Gif.objects.all()
	template = loader.get_template('gif/index.html')
	context = {
		'latest_gif_list' : latest_gif_list,
	}
	return HttpResponse(template.render(context, request))

def post_gif(request):
	template = loader.get_template('gif/post_gif.html')
	return HttpResponse(template.render())