#include <stdlib.h>
#include <math.h>

#define DECIMAL_APPROX 6

//ackleys equation parameters
#define C1 20
#define C2 0.2
#define C3 2*M_PI

float ackley(float *x_array, int tam_x_array) { //verificar se correto de python para c (tipos)

	float s1 = 0;
	float s2 = 0;
	float x;
	float r;
	int i = 0;

	x = x_array[0];

	for (x; x <= x_array[i]; x++) {
		if (x == x_array[i]) {
			s1 = s1 + (x * x); //verificar se correto de python para c
			s2 = s2 + (cos(C3 * x));//verificar se correto de python para c
			i++;
		}
	}

	r = round(-C1 * exp(-C2 * sqrt(s1 / tam_x_array)) - exp(s2 / tam_x_array) + C1 + exp(1));//verificar está fazendo o arredondamento para 6 casas decimais

	return r;
}

float rastrigin (float *x_array, int tam_x_array) {//verificar se correto de python para c (tipos)
	float s = 0;
	float x;
	int i = 0;

	x = x_array[0];

	for (x; x <= x_array[i]; x++) {
		if (x == x_array[i]) {
			s = s + (x * x) - 10*cos(2*M_PI*x);//verificar se correto de python para c
			i++;
		}
	}

	return round(10*tam_x_array + s); //verificar está fazendo o arredondamento para 6 casas decimais

}

float rosenbrock (float *x_array, int tam_x_array) {//verificar se correto de python para c(tipos)
	float s, x;
	int i;
	
	s = 0;
	
	for (i = 0; i < tam_x_array-1; i++) {
		s = s + 100 * ( x_array[i+1] - (x_array[i]*x_array[i]) ) * ( x_array[i+1] - (x_array[i]*x_array[i]) ) + ((x_array[i]-1) * (x_array[i]-1));//verificar se correto de python para c
	}

	return round(s); //verificar significado em python
}
