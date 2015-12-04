#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include "fitness.h"

#define DECIMAL_APPROX 6

#define NUMBER_OF_GENERATIONS 20

#define INITIAL_FITNESS 50.0
#define POPULATION_SIZE 200
#define DIMENSIONS 4
//CROSSOVER_METHOD = 'LOCAL_INTERMEDIARY' #two fixed parents, child_chromossome = (parent1_chromossome + parent2_chromossome)/2 
//CROSSOVER_METHOD = 'LOCAL_DISCRETE' #two fixed parents, child_chromossome = chromossome of a random parent
#define CROSSOVER_METHOD "GLOBAL_INTERMEDIARY" //parents are not the same for all chromossomes. child_chromossome = (parent1_chromossome + parent2_chromossome)/2 
//CROSSOVER_METHOD = 'GLOBAL_DISCRETE' #parents are not the same for all chromossomes. child_chromossome = chromossome of a random parent


//individual generation parameters
#define MIN_X_RANGE -5.0
#define MAX_X_RANGE 5.0

struct Element {
	float *x;
	int tam_x;
	float *sigma;
	float fitness;
};

struct Population {
	int n_dimensions;
	int n_elements;
	struct Element *elements;	
	float best_fitness_vector[NUMBER_OF_GENERATIONS];
};

struct Results {
	float *best_fitness_vector;
	int convergency_generation;
	float time;
};

struct Element initElement(int n_dimensions, float *x_array, int tam_array, struct Element element) {
	int i;
	element.fitness = INITIAL_FITNESS;
	element.tam_x = n_dimensions;
	//float x;
	//float sigma;
		
	element.x = (float*)malloc(tam_array * sizeof(float));
	element.sigma = (float*)malloc(tam_array * sizeof(float));


	//x = (float*)malloc((n_dimensions) * sizeof(float));
	//sigma = (float*)malloc((n_dimensions)* sizeof(float));



	//seed
	srand( (unsigned)time( NULL ) );

	for (i = 0; i < n_dimensions; i++) {
		element.sigma[i] = 1.0;
	}

	if(x_array[0] == -100) {	
		for(i = 0; i < n_dimensions; i++){
			element.x[i] = (float)rand()/(float)(RAND_MAX) * (MAX_X_RANGE - MIN_X_RANGE);	
			element.x[i] = element.x[i] + MIN_X_RANGE;
		}
	}
	else {
		if ((tam_array)!=n_dimensions) {
				printf("DEBUG x_array: %d n_dimensions: %d", tam_array, n_dimensions);
		}
		for(i = 0; i < n_dimensions; i++) {
			element.x[i] = x_array[i];
		}
	}

	
	//element.x = x;
	//element.sigma = sigma;

	//free(x);
	//free(sigma);

	return element;
}

struct Population initPopulation(int initial_population_size, int n_dimensions) {	
	struct Population population;
	float x_array[n_dimensions];
	int i, j;
	struct Element *elements;

	population.n_dimensions = n_dimensions;

	//population.elements = (struct Element*)malloc(sizeof(struct Element));
	elements = (struct Element*)malloc(initial_population_size * sizeof(struct Element));

	x_array[0] = -100;
	for (i = 0; i < initial_population_size; i++) {
		elements[i] = initElement(n_dimensions, x_array, n_dimensions, elements[i]);
	}

	population.n_elements = initial_population_size;
	population.elements = elements;

	//free(population);
	free(elements);
	
	return population;
}

/*
void freeElement(struct Element element) {
	free(element.x);
	free(element.sigma);
}*/
/*
void freePopulation(struct Population *population) {
	int i;

	//*for (i = 0; i < population.n_elements; i++) {
	//	free(population.elements[i].x);
	//	free(population.elements[i].sigma);
	//}

	free(population->elements);
}*/

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

struct Population computeFitness(struct Population population, char* fitness_function) {
	int i;
	
	for(i = 0; i < population.n_elements; i++) {
		population.elements[i].fitness = computeElementFitness(population.elements[i], fitness_function);
	}

	population = quicksort(population, population.n_elements);
	
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

struct Element* parents_select(struct Population population) {
	//Type of selection: Uniform random.
	//Returns 2 vectors, with the chromossomes of each selected parent
	int first_parent_roll, second_parent_roll;
	struct Element first_parent;
	struct Element second_parent;
	struct Element parents[2];

	//seed
	srand( (unsigned)time( NULL ) );

	first_parent_roll = rand()%population.n_elements;
	second_parent_roll = rand()%population.n_elements;

	first_parent = population.elements[first_parent_roll];
	second_parent = population.elements[second_parent_roll];

	parents[0] = first_parent;
	parents[1] = second_parent;

	return parents;
}

float* crossover(struct Population population, char* crossover_method, float *child_chromossomes) {
	int chromossome;
	struct Element *parent;
	int dice;

	//seed
	srand( (unsigned)time( NULL ) );
	parent = (struct Element*)malloc(2*sizeof(struct Element));

	if (strcmp(crossover_method, "LOCAL_DISCRETE") == 0) {
		//Two fixed parents:
		//Lembrar! parents_select supostamente retorna os vetores x dos pais!
		parent = parents_select(population);
		//Each chromossome of child is a copy of parent's chromossome, parent randomly chosen:
		for (chromossome = 0; chromossome < population.n_dimensions; chromossome++) {
			dice = rand()%2;
			child_chromossomes[chromossome] = parent[dice].x[chromossome];
		}
	}


	if (strcmp(crossover_method, "LOCAL_INTERMEDIARY") == 0) {
		//Two fixed parents:
		//Lembrar! parents_select supostamente retorna os vetores x dos pais!
		parent = parents_select(population);
		//Each chromossome is calculated (mean of parents' chromossomes):
		for (chromossome = 0; chromossome < population.n_dimensions; chromossome++) {
			child_chromossomes[chromossome] = roundf(parent[0].x[chromossome] + parent[1].x[chromossome])/2;
		}
	}

	if (strcmp(crossover_method, "GLOBAL_DISCRETE") == 0) {
		//Parents chosen for each chromossome:
		for (chromossome = 0; chromossome < population.n_dimensions; chromossome++) {
		//Lembrar! parents_select supostamente retorna os vetores x dos pais!
			parent = parents_select(population);
			//Each chromossome of child is a copy of parent's chromossome, parent randomly chosen:
			dice = rand()%2;
			child_chromossomes[chromossome] = parent[dice].x[chromossome];
		}
	}

	if (strcmp(crossover_method, "GLOBAL_INTERMEDIARY") == 0) {
		//Parents chosen for each chromossome:
		for (chromossome = 0; chromossome < population.n_dimensions; chromossome++) {
		//Lembrar! parents_select supostamente retorna os vetores x dos pais!
			parent = parents_select(population);
			//Each chromossome is calculated (mean of parents' chromossomes):
			child_chromossomes[chromossome] = roundf((parent[0].x[chromossome] + parent[1].x[chromossome])/2);
		}
	}

	free(parent);

	return child_chromossomes;
}

float gauss(float mu, float sigma) {
	float result;

	result = (1/(sqrt(sigma) * sqrt(2*M_PI))) * (exp(-(pow(((float)rand() - mu),2))) / 2 * sqrt(sigma));
	
	return result;
}

struct Population mutation(struct Population population, struct Population children, int tam_children) {
	//Mutation Mode: Gaussian Perturbation
	int chromossome, i, j;
	struct Population temporary_population;
	struct Element element;
	float new_element_chromossomes;

	temporary_population = initPopulation(population.n_elements, population.n_dimensions);

	//temporary_population = population;

	//new_element_chromossomes = (float*)malloc((population.n_dimensions * 2)*sizeof(float));

	element = initElement (population.n_dimensions, population.elements[0].x, population.n_dimensions, element);

	for (i = 0; i < tam_children; i++) {
		//element = children.elements[i];

		for (chromossome = 0; chromossome < population.n_dimensions; chromossome++) {
			children.elements[i].sigma[chromossome] = children.elements[i].sigma[chromossome] * exp(1/sqrt(population.n_dimensions) * gauss(0.0, 1.0));
			//new_element_chromossomes[chromossome] = children.elements[i].x[chromossome] + gauss(0.0, children.elements[i].sigma[chromossome]);
			new_element_chromossomes = children.elements[i].x[chromossome] + gauss(0.0, children.elements[i].sigma[chromossome]);
			children.elements[i].x[chromossome] = new_element_chromossomes;
		}
	
		//temporary_population.elements[i].x = new_element_chromossomes;
printf("TESTE!!!!!!!!!!!\n");

	}
	//children.elements = temporary_population.elements;
	
	//freeElement(element);
	//freePopulation(temporary_population);
	//free(new_element_chromossomes);

	return children;
}

struct Population createChildren(struct Population population, char* crossover_method, 	struct Population children) {
	int population_size;
	int i;
	float *child_chromossomes;
	
	child_chromossomes = (float*)malloc((population_size)*sizeof(float));
	
	population_size = population.n_elements;
	
//	children.n_dimensions = initPopulation(population_size, 

	for (i = 0; i < population_size; i++) {
		children.elements[i].x = crossover(population, crossover_method, child_chromossomes);
	}

	children = mutation(population, children, population_size);

	free(child_chromossomes);

	return children;
}

struct Population evolve(struct Population population, char* fitness_function, char* crossover_method) {
	struct Population children;
	int i, population_size;
	struct Population temp_pop;

	population_size = population.n_elements;
	temp_pop = initPopulation(population_size*2, population.n_dimensions);
	temp_pop = population;

	children = initPopulation(population_size, population.n_dimensions);

	children = createChildren(population, crossover_method, children);

	for (i = 0; i < population_size; i++) {
		temp_pop.elements[population_size+i] = children.elements[i];
		temp_pop.n_elements++;
	}

	temp_pop = computeFitness(temp_pop, fitness_function);

	for (i = 0; i < population_size; i++) {
		population.elements[i] = temp_pop.elements[i];
	}

	//freePopulation(&children);
	//freePopulation(&temp_pop);

	return population;
}

//ver tipo de retorno e tipos de entrada
struct Results run_generation (struct Population population, int number_of_generations, char* fitness_function, char* crossover_method, struct Results result) {
	int i, j, convergency_generation;
	
	for (i = 0; i < number_of_generations; i++) {
		population = evolve(population, fitness_function, crossover_method);
		population.best_fitness_vector[i] = population.elements[0].fitness;
		if (population.elements[0].fitness == 0.0) {
			convergency_generation = i;
			break;
		}
	}

	if (i == number_of_generations-1) {
		j = number_of_generations-1;
		while (population.best_fitness_vector[j] == population.best_fitness_vector[j-1]) {
			j--;
		}
		convergency_generation = j;
	}

	while (i < number_of_generations-1) {
		i++;
		population.best_fitness_vector[i] = 0.0;
	}

	result.best_fitness_vector = population.best_fitness_vector;
	result.convergency_generation = convergency_generation;
	result.time = 0;

	return result;
}

struct Results es_run(int population_size, int n_dimensions, int n_generations, struct Results result) {
	struct Population pop;
	clock_t start, end;
	double total_time;
	char *fitness_function = "ackley";

	start = clock();

	pop = initPopulation(population_size, n_dimensions);
	
	result = run_generation(pop, n_generations, fitness_function, CROSSOVER_METHOD, result);

	end = clock();
	total_time = (double)(end - start) / CLOCKS_PER_SEC;

	result.time = total_time;

	//freePopulation(&pop);

	return result;
}


int main() {
	struct Results result;

	result.best_fitness_vector = (float*)malloc((NUMBER_OF_GENERATIONS+ 10) * sizeof(float));

	result = es_run(POPULATION_SIZE, DIMENSIONS, NUMBER_OF_GENERATIONS, result);

	free(result.best_fitness_vector);

	return 0;
}

