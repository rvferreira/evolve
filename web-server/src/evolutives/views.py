from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader

from .models import Code, FitnessFunction, Parameter

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

def get_parameter(request):
	p = Parameter.objects.get(name = request.GET.get('query'))
	short_name = '_'.join(p.name.split(' '))

	if (request.GET.get('is_metric') == "false") and p.c_is_metric == False:
	
		template = loader.get_template('evolutives/parameter.html')
		context = RequestContext(request, {
			'p' : p,
			'alg_index' : request.GET.get('alg_index'),
			'short_name': short_name
		})

	elif (request.GET.get('is_metric') == "true") and p.c_is_metric == True:

		template = loader.get_template('evolutives/metric.html')
		context = RequestContext(request, {
			'p' : p,
			'alg_index' : request.GET.get('alg_index'),
			'short_name': short_name,
		})

	else:
	
		return HttpResponseNotFound('404')


	return HttpResponse(template.render(context))

	# 	template = loader.get_template('evolutives/parameter.html')
	# 	p = Parameter.objects.get(name = request.GET.get('query'))
	# 	context = RequestContext(request, {
	# 		'p' : p,
	# 		'alg_index' : request.GET.get('alg_index'),
	# 		'short_name': p.name.split(' ', 1)[0]
	# 	})
	# 	return HttpResponse(template.render(context))
		
	# else return HttpResponse("oi")