from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader

from .models import Code, FitnessFunction, Parameter
from algorithms.EvolutiveStrategy import es_run
from algorithms.GeneticAlgorithm import ga_run
from algorithms.fitness import rastrigin, ackley

def index(request):

	fitness_list = FitnessFunction.objects.order_by('-name')

	template = loader.get_template('evolutives/index.html')
	context = RequestContext(request, {
		'page_title': 'Evolutives Algorithms',
		'fitness_list': fitness_list,
	})

	return HttpResponse(template.render(context))

def run_algorithm(request):
	print request

	population_size = int(request.GET.get('Population_Size'))
	n_dimensions = int(request.GET.get('Dimensions'))
	n_generations = int(request.GET.get('Max_Generation'))
	mutation_rate = float(request.GET.get('Mutation_Rate', 0))/100.0
	
	if request.GET.get('fitness') == 'ackley':
		fitness_function = ackley
	elif request.GET.get('fitness') == 'rastrigin':
		fitness_function = rastrigin
	else:
		return HttpResponse('')

	metrics = ['best_fitness', 'convergence_generation', 'processing_time', 'best_fitness_vector']

	if request.GET.get('alg_type') == 'PY_GA':
		language, algorithm = "Python", "GeneticAlgorithm"
		results = ga_run(population_size, n_dimensions, n_generations, 0.0, fitness_function, metrics)
	elif request.GET.get('alg_type') == 'PY_ES':
		language, algorithm = "Python", "EvolutiveStrategy"
		results = es_run(population_size, n_dimensions, n_generations, fitness_function, metrics)
	else:
		return HttpResponse('')

	template = loader.get_template('evolutives/results.html')	
	
	context = RequestContext(request, {
		'best_fitness' : results[0],
		'convergence_generation' : results[1],
		'processing_time' : results[2],
		'best_fitness_vector' : results[3],
		'in_language' : language,
		'in_algorithm' : algorithm,
		'in_population_size' : request.GET.get('Population_Size'),
		'in_n_dimensions' : request.GET.get('Dimensions'),
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
	print request
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