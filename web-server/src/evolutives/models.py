from django.db import models

class FitnessFunction(models.Model):
	name = models.CharField(max_length=20)
		
	def __str__(self):
		return self.name
		

class Parameter(models.Model):
	name = models.CharField(max_length=20)
	type = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Author(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name


class Code(models.Model):
	CPP_LANGUAGE = 'CP'
	PYTHON_LANGUAGE = 'PY'

	LANGUAGE_CHOICES = (
		(PYTHON_LANGUAGE, 'Python'),
		(CPP_LANGUAGE, 'C++'),
	)

	GENETIC_ALGORITHM = 'GA'
	EVOLUTIVE_STRATEGY = 'ES'

	ALGORITHM_CHOICES = (
		(GENETIC_ALGORITHM, 'Genetic Algorithm'),
		(EVOLUTIVE_STRATEGY, 'Evolutives Strategy'),
	)

	language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=PYTHON_LANGUAGE)
	algorithm = models.CharField(max_length=2, choices=ALGORITHM_CHOICES, default=GENETIC_ALGORITHM)
	git_repo = models.URLField(max_length=200, blank=True)
	author = models.ForeignKey('Author', blank=True, null=True)
	built_in = models.BooleanField(default=False)
	parameters = models.ManyToManyField(Parameter)

	def __str__(self):
		return self.language + '_' + self.algorithm