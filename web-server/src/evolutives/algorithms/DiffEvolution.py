from fitness import ackley, rosenbrock
from random import seed, randrange
from operator import attrgetter
from time import clock


POPULATION_SIZE = 100 #min 4!
DIMENSIONS= 2

MAX_X_RANGE = 5.0
MIN_X_RANGE = -5.0

INITIAL_FITNESS = 50.0
CR = 0.5

F = 0.5

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
				print "DEBUG x_array:", len(x_array), "n_dimensions:", n_dimensions
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
		(self.elements).sort(key=attrgetter('fitness')) #sorts the array elements
	
	def printFitness(self):
		print self.elements[0].x, " ", self.elements[0].fitness

	def mutation(self):
		population_size = len(self.elements)
		donor_population = []

		for i in range(population_size):
			#print "old", self.elements[i].x
			#print "i:", i
			self.elements[i].computeElementFitness(ackley)
			#print "fitness old", self.elements[i].fitness

			r1 = i
			while (r1 == i):
				r1 = randrange(0, population_size)
			r2 = i
			#print "r1:", r1
			while (r2 == i or r2 == r1):
				r2 = randrange(0, population_size)
			r3 = i
			#print "r2:", r2
			while (r3 == i or r3 == r2 or r3 == r1):
				r3 = randrange(0, population_size)
			#print "r3:", r3

			x_array = []
			individual_r1 = self.elements[r1]
			individual_r2 = self.elements[r2]
			individual_r3 = self.elements[r3]
			#print "individups:", individual_r1.x, individual_r2.x, individual_r3.x

			for j in range(self.n_dimensions):
				x_array.append(round(individual_r1.x[j]+F*(individual_r2.x[j]-individual_r3.x[j]), 2))
			
			new_element = Element(self.n_dimensions, x_array)
			new_element.computeElementFitness(ackley)
			#print "new", new_element.fitness

			donor_population.append(new_element)


		return donor_population

	def recombination(self, donor_population):

		population_size = len(self.elements)
		trial_population = []

		for i in range(population_size):
			self.elements[i].computeElementFitness(ackley)
			#print "old", self.elements[i].x, "fitness:", self.elements[i].fitness
			x_array = []
			for j in range(self.n_dimensions):
				random_number = randrange(0, 100)/100.0
				if (random_number<= CR):
					x_array.append(donor_population[i].x[j])
				else:
					x_array.append(self.elements[i].x[j])
			new_element = Element(self.n_dimensions, x_array)
			new_element.computeElementFitness(ackley)
			#print "new", new_element.x, "fitness:", new_element.fitness
			trial_population.append(Element(self.n_dimensions, x_array));

		return trial_population

	def selection(self, trial_population, fitness_function):
		population_size = len(self.elements)
		new_generation = []

		for i in range(population_size):
			self.elements[i].computeElementFitness(fitness_function)
			trial_population[i].computeElementFitness(fitness_function)
			#print "old fitness:", self.elements[i].fitness, "new fitness:", trial_population[i].fitness
			if (self.elements[i].fitness >= trial_population[i].fitness):
				#print "novo eh melhor"
				new_generation.append(trial_population[i])
			else:
				new_generation.append(self.elements[i])
			#print new_generation[i].x
		self.elements = new_generation

	def evolve(self, fitness_function):
		self.selection(self.recombination(self.mutation()), fitness_function)
		self.computeFitness(fitness_function)

	def run_generation(self, number_of_generations, fitness_function):
		best_fitness_vector = []
		for i in range(number_of_generations):
			self.evolve(fitness_function)
			best_fitness_vector.append(self.elements[0].fitness)
			if self.elements[0].fitness == 0.0:
				convergency_generation = i;
				break

		for i in range(number_of_generations - len(best_fitness_vector)):
			best_fitness_vector.append(0.0)

		convergency_generation = -1;
		convergency_fitness = INITIAL_FITNESS

		for i in range(len(best_fitness_vector)):
			if best_fitness_vector[i] != convergency_fitness:
				convergency_fitness = best_fitness_vector[i]
				convergency_generation = i

		return best_fitness_vector, convergency_generation


def de_run(population_size, n_dimensions, n_generations, metrics):
	time = clock()

	pop = Population(population_size, n_dimensions)
	best_fitness_vector, convergency_generation = pop.run_generation(n_generations, ackley)

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

