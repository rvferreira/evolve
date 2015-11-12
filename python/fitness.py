from math import cos, exp, sqrt, pi, fsum

DECIMAL_APPROX = 6

#ackleys equation parameters
C1 = 20
C2 = 0.2
C3 = 2*pi




def ackley(x_array):

	s1 = 0
	s2 = 0
	for x in x_array:

		s1 = s1 + (x * x)
		s2 = s2 + (cos(C3 * x))

	r = round(-C1 * exp(-C2 * sqrt(s1 / len(x_array))) - exp(s2 / len(x_array)) + C1 + exp(1), DECIMAL_APPROX)

	return r

def rastrigin(x_array):

	s = 0

	for x in x_array:
		s = s + (x * x) - 10*cos(2*pi*x)

	return round(10*len(x_array) + s, DECIMAL_APPROX)

def rosenbrock(x_array):

	s = 0

	for i in range(len(x_array)-1):
		s = s + 100 * ( x_array[i+1] - (x_array[i]*x_array[i]) ) * ( x_array[i+1] - (x_array[i]*x_array[i]) ) + ((x_array[i]-1) * (x_array[i]-1))

	return round(s)