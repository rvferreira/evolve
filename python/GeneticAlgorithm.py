from random import seed, randrange
from fitness import ackley
from operator import attrgetter
from math import cos, exp, sqrt, pi, fsum
from time import clock

DECIMAL_APPROX = 6

NUMBER_OF_GENERATIONS = 10

INITIAL_FITNESS = 50.0
POPULATION_SIZE = 100
DIMENSIONS = 3

MUTATION_INTENSITY = 0.1
CROSSOVER_POINT = DIMENSIONS/2
MUTATION_RATE = 0.2


#individual generation parameters
MIN_X_RANGE = -5.0
MAX_X_RANGE = 5.0

class Element:

	@property
	def x():
		return self.x

	def __init__(self, n_dimensions, x_array=[]):
		seed()
		
		self.x = []
		self.fitness = INITIAL_FITNESS

		if not x_array:	
			for i in range(n_dimensions):
				(self.x).append(randrange(MIN_X_RANGE*100.0, MAX_X_RANGE*100.0) / 100.0)
		else:
			if (len(x_array)!=n_dimensions):
				print "Array given is not the same size as array wanted"
			(self.x) = x_array

	def computeElementFitness(self, fitness_function):
		self.fitness = fitness_function(self.x)

class Population:
	def __init__(self, initial_population_size, n_dimensions):
		self.n_dimensions = n_dimensions
		self.elements = []

		for i in range(initial_population_size):
			self.elements.append(Element(n_dimensions))

	def computeFitness(self, fitness_function):
		for element in self.elements:
			element.computeElementFitness(fitness_function)
		(self.elements).sort(key=attrgetter('fitness'))

	def printFitness(self):
		print self.elements[0].x, " ", self.elements[0].fitness

	def parents_select(self):
		#Type of selection: Prioritizes best parents.
		#Returns 2 vectors, with the chromossomes of each selected parent
		first_parent_roll = 0.8 ** (randrange(0, 100)/(-5.077) - 1) - 1.2
		second_parent_roll = 0.8 ** (randrange(0, 100)/(-5.077) - 1) - 1.2

		# normalizing for population size
		first_parent_roll = int((first_parent_roll / 100.0) * len(self.elements))
		second_parent_roll = int((second_parent_roll / 100.0) * len(self.elements))

		first_parent = self.elements[first_parent_roll]
		second_parent = self.elements[second_parent_roll]

		return first_parent.x, second_parent.x

	def crossover(self, crossover_point):
		parent = [None] * 2
		child_chromossomes = []
		parent[0], parent[1] = self.parents_select()

		for chromossome in range(crossover_point):
			child_chromossomes.append(round((parent[0][chromossome] + parent[1][chromossome])/2, 2))

		child_chromossomes += parent[0][crossover_point:self.n_dimensions]

		child = Element(self.n_dimensions, child_chromossomes)
		return child

	def createChildren(self, crossover_point, mutation_rate, mutation_intensity):
		population_size = len(self.elements)
		children = []
		for i in range(population_size):
			children.append(self.crossover(crossover_point))
		self.mutation(children, mutation_rate, mutation_intensity)

		return children

	def mutation(self, children, mutation_rate, mutation_intensity):
		#Mutation Mode: Plus_Minus
		temporary_population = []

		for element in children:
			new_element_chromossomes = []

			for chromossome in range(self.n_dimensions):
				chance = randrange(0, 100)/100.0
				if chance <= mutation_rate: #ocorre mutacao
					if randrange(0,2)==1:
						new_element_chromossomes.append(round(element.x[chromossome]+mutation_intensity*element.x[chromossome], DECIMAL_APPROX))
					else:
						new_element_chromossomes.append(round(element.x[chromossome]-mutation_intensity*element.x[chromossome], DECIMAL_APPROX))
				else:
					new_element_chromossomes.append(element.x[chromossome])

			temporary_population.append(Element(self.n_dimensions, new_element_chromossomes))
		children = temporary_population

	def evolve(self, fitness_function, crossover_point, mutation_rate, mutation_intensity):
		self.computeFitness(fitness_function)
		self.elements += self.createChildren(crossover_point, mutation_rate, mutation_intensity)
		self.computeFitness(fitness_function)
		self.elements = self.elements[0:(len(self.elements)/2)]

	def run_generation(self, number_of_generations, fitness_function, crossover_point, mutation_rate, mutation_intensity):
		best_fitness_vector = []
		for i in range(number_of_generations):
			self.evolve(fitness_function, crossover_point, mutation_rate, mutation_intensity)
			best_fitness_vector.append(self.elements[0].fitness)
			if self.elements[0].fitness == 0.0:
				convergency_generation = i;
				break

		if i==number_of_generations-1:
			j = number_of_generations-1
			while best_fitness_vector[j] == best_fitness_vector[j-1]:
				j-=1
			convergency_generation = j

		while i<number_of_generations-1:
			i += 1
			best_fitness_vector.append(0.0)


		return best_fitness_vector, convergency_generation

def main():
	metrics = ['BEST_FITNESS_VECTOR', 'CONVERGENCY_GENERATION', 'PROCESSING_TIME']

	result = ga_run(POPULATION_SIZE, DIMENSIONS, NUMBER_OF_GENERATIONS, MUTATION_RATE, metrics)

	print result[0][result[1]], result[1], result[2]


def ga_run(population_size, n_dimensions, n_generations, mutation_rate, metrics):
	time = clock()

	pop = Population(population_size, n_dimensions)
	best_fitness_vector, convergency_generation = pop.run_generation(n_generations, ackley, CROSSOVER_POINT, mutation_rate, MUTATION_INTENSITY)

	time = clock() - time

	results = []

	for request in metrics:
		if request == 'BEST_FITNESS_VECTOR':
			results.append(best_fitness_vector)
		elif request == 'CONVERGENCY_GENERATION':
			results.append(convergency_generation)
		elif request == 'PROCESSING_TIME':
			results.append(time)

	return results

if __name__ == '__main__': main()
