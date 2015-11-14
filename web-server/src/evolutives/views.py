from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Code, FitnessFunction

def index(request):

	fitness_list = FitnessFunction.objects.order_by('-name')

	template = loader.get_template('evolutives/index.html')
	context = RequestContext(request, {
		'page_title': 'Evolutives Algorithms',
		'fitness_list': fitness_list,
	})

	return HttpResponse(template.render(context))

def new_algorithm(request):

	template = loader.get_template('evolutives/algorithm_in_workspace.html')
	code_list = Code.objects.order_by('-language')
	context = RequestContext(request, {
		'index'	: request.GET.get('index'),
		'code_list': code_list,
	})

	return HttpResponse(template.render(context))