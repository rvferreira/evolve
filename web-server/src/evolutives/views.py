from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader

from .models import Code, FitnessFunction, Parameter
from algorithms.EvolutiveStrategy import es_run

def index(request):

	fitness_list = FitnessFunction.objects.order_by('-name')

	template = loader.get_template('evolutives/index.html')
	context = RequestContext(request, {
		'page_title': 'Evolutives Algorithms',
		'fitness_list': fitness_list,
	})

	return HttpResponse(template.render(context))

def run_algorithm(request):
	population_size = request.GET.get('Population_Size')
	n_dimensions = request.GET.get('Dimensions')
	n_generations = request.GET.get('Max_Generation')

	print population_size, n_dimensions, n_generations

	template = loader.get_template('evolutives/results.html')
	best_fitness = es_run(int(population_size), int(n_dimensions), int(n_generations))
	
	context = RequestContext(request, {
		'best_fitness' : best_fitness
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
		return HttpResponse('')

	return HttpResponse(template.render(context))

def get_preloader(request):
	template = loader.get_template('evolutives/preloader.html')
	return HttpResponse(template.render())