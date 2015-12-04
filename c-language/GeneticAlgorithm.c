#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include "fitness.h"

#define DECIMAL_APPROX 6

#define NUMBER_OF_GENERATIONS 10

#define INITIAL_FITNESS 50.0
#define POPULATION_SIZE 100
#define DIMENSIONS 3

#define MUTATION_INTENSITY 0.1
#define CROSSOVER_POINT DIMENSIONS/2
#define MUTATION_RATE 0.2


//individual generation parameters
#define MIN_X_RANGE -5.0
#define MAX_X_RANGE 5.0


struct Element {
	float *x;
	int tam_x;
	float fitness;
};

struct Population {
	int n_dimensions;
	struct Element *elements; 
	int n_elements;
};

struct Results {
	float *best_fitness_vector;
	int convergency_generation;
	float time;
};

struct Element initElement(int n_dimensions, float *x_array, int tam_array) {
	struct Element element;
	int i;

	element.fitness = INITIAL_FITNESS;

	//if(x_array[0] == -100) {
	//	element.x = (float*)realloc(sizeof(float));
	//}
	//else {
		element.x = (float*)malloc(tam_array * sizeof(float));
	//}

	//seed
	srand( (unsigned)time( NULL ) );
	
	if(x_array[0] == -100) {
		for(i = 0; i < n_dimensions; i++) {
			element.x[i] = (float)rand()/(float)(RAND_MAX) * (MAX_X_RANGE - MIN_X_RANGE);	
			element.x[i] = element.x[i] + MIN_X_RANGE;
		}
	}
	else {
		if (tam_array!=n_dimensions) {
			printf("Array given is not the same size as array wanted");
		}
		element.x = x_array;
	}
	
	return element;
}

void freeElement(struct Element element) {
	free(element.x);	
}

struct Population initPopulation(int initial_population_size, int n_dimensions) {
	struct Population population;
	float x_array[n_dimensions];
	int i;

	population.n_dimensions = n_dimensions;

	population.elements = (struct Element*)malloc(initial_population_size * sizeof(struct Element));

	for (i = 0; i < initial_population_size; i++) {
		population.elements[i] = initElement(n_dimensions, x_array, n_dimensions);
	}

	population.n_elements = initial_population_size;
	
	return population;
}

void freePopulation(struct Population population) {
	int i;

	free(population.elements);
}

float computeElementFitness(struct Element element, char* fitness_function) {
	float fitness;

	if(fitness_function == "ackley") {
		fitness = ackley(element.x, element.tam_x);
	} 
	else if(fitness_function == "rastrigin") {
		fitness = rastrigin(element.x, element.tam_x);
	}
	else if (fitness_function == "rosenbrock") {
		fitness = rosenbrock(element.x, element.tam_x);
	}

	return fitness;
}

struct Population quicksort(struct Population population, int tam) {
	int pivot, i, j;
	struct Element temp;
	int low, high;

	low = 0;
	high = tam;
	
	if(low < high) {
		pivot = low;
		i = low;
		j = high;
		while(i < j) {
			while((population.elements[i].fitness <= population.elements[pivot].fitness) && (i<high)) {
				i++;
			}
 
			while(population.elements[j].fitness > population.elements[pivot].fitness) {
				j--;
			}
 
			if(i<j) { 
				temp = population.elements[i];
				population.elements[i] = population.elements[j];
				population.elements[j] = temp;
			}
		}
	}

	return population;
}

struct Population computeFitness(struct Population population, char* fitness_function) {//verificar!!
	struct Element element;
	int i;
	
	for(i = 0; i < population.n_elements; i++) {
		element = initElement(population.n_dimensions, population.elements[i].x, population.n_dimensions);
		population.elements[i].fitness = computeElementFitness(population.elements[i], fitness_function);
	}
	population = quicksort(population, population.n_elements); 

	freeElement(element);

	return population;
}	

void printFitness(struct Population population) {
	int i;

	printf("[");
	for(i = 0; i; i++) {	
		printf("%f ", population.elements[0].x[i]);
	}
	printf("] ");

	printf("%f", population.elements[0].fitness);
}

struct Elements* parents_select(struct Population population) {
	//Type of selection: Prioritizes best parents.
	//Returns 2 parents, with the chromossomes of each selected parent
	float first_parent_roll_f, second_parent_roll_f;
	int first_parent_roll, second_parent_roll;
	struct Element parents[2];

	//seed
	srand( (unsigned)time( NULL ) );

	first_parent_roll_f = pow(0.8, rand()%100/(-5.077) - 1 - 1.2);
	second_parent_roll_f = pow(0.8, rand()%100/(-5.077) - 1 - 1.2);

	// normalizing for population size
	first_parent_roll = (int)((first_parent_roll_f / 100.0) * population.n_elements);
	second_parent_roll = (int)((second_parent_roll_f / 100.0) * population.n_elements);

	parents[0] = population.elements[first_parent_roll];
	parents[1] = population.elements[second_parent_roll];

	return parents;
}

struct Element crossover(struct Population population, int crossover_point) {
	struct Element *parent;
	struct Element child;
	float *child_chromossomes;
	int chromossome;

	child_chromossomes = (float*)malloc(sizeof(float));

	parent = parents_select(population);

	for (chromossome = 0; chromossome < crossover_point; chromossome++) {
		child_chromossomes[chromossome] = roundf((parent[0].x[chromossome] + parent[1].x[chromossome])/2);
	}

	//child_chromossomes += parent[0].x[crossover_point:self.n_dimensions]

	child = initElement(population.n_dimensions, child_chromossomes, chromossome);

	free(child_chromossomes);

	return child;

}

struct Population mutation(struct Population population, float mutation_rate, float mutation_intensity) {
	//Mutation Mode: Plus_Minus
	//temporary_population = []
	int i, chromossome;
	float new_element_chromossomes[population.n_elements];
	struct Element element;
	struct Population temporary_population;
	struct Population children;
	float chance;

	for (i = 0; i <= children.n_elements; i++) {
		element = children.elements[i];

		for (chromossome = 0; chromossome < population.n_dimensions; chromossome++) {
			//seed
			srand( (unsigned)time( NULL ) );
			chance = rand()%100/100;
			if (chance <= mutation_rate) {//ocorre a mutação
				if (rand()%2 == 1) {
					new_element_chromossomes[chromossome] = roundf(element.x[chromossome]+mutation_intensity*element.x[chromossome]);
				}
				else {
					new_element_chromossomes[chromossome] = roundf(element.x[chromossome]-mutation_intensity*element.x[chromossome]);
				}
			}
			else {
				new_element_chromossomes[chromossome] = element.x[chromossome];
			}
		}
		temporary_population.elements[i] = initElement(population.n_dimensions, new_element_chromossomes, chromossome);
	}

	children = temporary_population;

	return children;
}

struct Population createChildren(struct Population population, int crossover_point, float mutation_rate, float mutation_intensity, struct Population children) {
	int population_size, i;

	population_size = population.n_elements;
	//inicializa children;

	for(i = 0; i <= population_size; i++) {
		children.elements[i] = crossover(population, crossover_point);
	}
	
	children = mutation(children, mutation_rate, mutation_intensity);

	return children;
}

struct Population evolve(struct Population population, char* fitness_function, int crossover_point, float mutation_rate, float mutation_intensity) {	
	struct Population children;
	struct Population temp_pop;
	int i, population_size;

	population_size = population.n_elements;

	temp_pop = computeFitness(population, fitness_function);
	children = createChildren(temp_pop, crossover_point, mutation_rate, mutation_intensity, children);

	for (i = 0; i < population_size; i++) {
		temp_pop.elements[population_size+i] = children.elements[i];
		temp_pop.n_elements++;
		temp_pop.n_dimensions++;
	}

	temp_pop = computeFitness(temp_pop, fitness_function);

	for (i = 0; i < population_size; i++) {
		population.elements[i] = temp_pop.elements[i];
	}

	return population;

}

struct Results run_generation(struct Population population, int number_of_generations, char* fitness_function, int crossover_point, float mutation_rate, float mutation_intensity, struct Results result) {
	int i, j;

	for(i = 0; i < number_of_generations; i++) {
		population = evolve(population, fitness_function, crossover_point, mutation_rate, mutation_intensity);
		result.best_fitness_vector[i] = population.elements[0].fitness;

		if(population.elements[0].fitness == 0.0) {
			result.convergency_generation = i;
			break;
		}
	}

	if (i == number_of_generations-1) {
		j = number_of_generations - 1;
		
		while(result.best_fitness_vector[j] == result.best_fitness_vector[j-1]) {
			j--;
		}
		result.convergency_generation = j;
	}

	while(i < number_of_generations - 1) {
		i++;
		result.best_fitness_vector[i] = 0.0;
	}

	return result;
}

struct Results ga_run(int population_size, int n_dimensions, int n_generations, float mutation_rate, struct Results result) {
	clock_t start, end;
	double total_time;
	char *fitness_function = "ackley";
	struct Population pop;

	start = clock();

	pop = initPopulation(population_size, n_dimensions);
	result = run_generation(pop, n_generations, fitness_function, CROSSOVER_POINT, mutation_rate, MUTATION_INTENSITY, result);
	
	end = clock();
	total_time = (double)(end - start) / CLOCKS_PER_SEC;

	result.time = total_time;

	freePopulation(pop);

	return result;
}


int main() {
	struct Results result;
	int i;

	result.best_fitness_vector = (float*)malloc(sizeof(float));

	result = ga_run(POPULATION_SIZE, DIMENSIONS, NUMBER_OF_GENERATIONS, MUTATION_RATE, result);

	printf("[");
	
	for(i = 0; i < result.convergency_generation; i++) {
		printf("%f", result.best_fitness_vector[i]);
	}
	
	printf("] %d %f", result.convergency_generation, result.time);

	free(result.best_fitness_vector);

	return 0;
}

