# Evolutive Strategy Algorithm made by Valeska Paroni and Raphael Ferreira for Evolutive Algorithms classes.
# 11/12/2015

from random import seed, randrange, gauss
from fitness import ackley
from operator import attrgetter
from math import exp, sqrt

DECIMAL_APPROX = 6

NUMBER_OF_GENERATIONS = 20

INITIAL_FITNESS = 50.0
POPULATION_SIZE = 200
DIMENSIONS = 4
CROSSOVER_METHOD = 'LOCAL_INTERMEDIARY' #two fixed parents, child_chromossome = (parent1_chromossome + parent2_chromossome)/2 
#CROSSOVER_METHOD = 'LOCAL_DISCRETE' #two fixed parents, child_chromossome = chromossome of a random parent
#CROSSOVER_METHOD = 'GLOBAL_INTERMEDIARY' #parents are not the same for all chromossomes. child_chromossome = (parent1_chromossome + parent2_chromossome)/2 
#CROSSOVER_METHOD = 'GLOBAL_DISCRETE' #parents are not the same for all chromossomes. child_chromossome = chromossome of a random parent


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
		self.sigma = []
		self.fitness = INITIAL_FITNESS

		for i in range(n_dimensions):
			(self.sigma).append(1.0)

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

	def parents_select(self):
		#Type of selection: Uniform random.
		#Returns 2 vectors, with the chromossomes of each selected parent
		first_parent_roll = randrange(0, len(self.elements))
		second_parent_roll = randrange(0, len(self.elements))

		first_parent = self.elements[first_parent_roll]
		second_parent = self.elements[second_parent_roll]

		return first_parent.x, second_parent.x

	def crossover(self, crossover_method):
		seed()

		parent = [None] * 2
		child_chromossomes = []

		if crossover_method == 'LOCAL_DISCRETE':
			#Two fixed parents:
			parent[0], parent[1] = self.parents_select()
			#Each chromossome of child is a copy of parent's chromossome, parent randomly chosen:
			for chromossome in range(self.n_dimensions):
				dice = randrange(0, 2)
				child_chromossomes.append(parent[dice][chromossome])

		if crossover_method == 'LOCAL_INTERMEDIARY':
			#Two fixed parents:
			parent[0], parent[1] = self.parents_select()
			#Each chromossome is calculated (mean of parents' chromossomes):
			for chromossome in range(self.n_dimensions):
				child_chromossomes.append(round((parent[0][chromossome] + parent[1][chromossome])/2, 2))

		if crossover_method == 'GLOBAL_DISCRETE':
			#Parents chosen for each chromossome:
			for chromossome in range(self.n_dimensions):
				parent[0], parent[1] = self.parents_select()
				#Each chromossome of child is a copy of parent's chromossome, parent randomly chosen:
				dice = randrange(0, 2)
				child_chromossomes.append(parent[dice][chromossome])

		if crossover_method == 'GLOBAL_INTERMEDIARY':
			#Parents chosen for each chromossome:
			for chromossome in range(self.n_dimensions):
				parent[0], parent[1] = self.parents_select()
				#Each chromossome is calculated (mean of parents' chromossomes):
				child_chromossomes.append(round((parent[0][chromossome] + parent[1][chromossome])/2, 2))

		child = Element(self.n_dimensions, child_chromossomes)
		return child

	def mutation(self, children):
		#Mutation Mode: Gaussian Perturbation
		temporary_population = []

		for element in children:
			new_element_chromossomes = []

			for chromossome in range(self.n_dimensions):
				element.sigma[chromossome] *= exp(1/sqrt(self.n_dimensions) * gauss(0.0, 1.0))
				new_element_chromossomes.append(element.x[chromossome] + gauss(0.0, element.sigma[chromossome]))

			temporary_population.append(Element(self.n_dimensions, new_element_chromossomes))
		children = temporary_population

	def createChildren(self, crossover_method):
		population_size = len(self.elements)
		children = []
		for i in range(population_size):
			children.append(self.crossover(crossover_method))
		self.mutation(children)

		return children

	def evolve(self, fitness_function, crossover_method):
		self.elements += self.createChildren(crossover_method)
		self.computeFitness(fitness_function)
		self.elements = self.elements[0:(len(self.elements)/2)]

	def run_generation(self, number_of_generations, fitness_function, crossover_method):
		for i in range(number_of_generations):
			self.evolve(fitness_function, crossover_method)
			print i
			self.printFitness()
			if self.elements[0].fitness == 0.0:
				break

def main():
	test = Population(POPULATION_SIZE, DIMENSIONS)

	test.run_generation(NUMBER_OF_GENERATIONS, ackley, CROSSOVER_METHOD)

if __name__ == '__main__': main()