import csv
import math
import numpy as np

#data is numpy array
class Decision():

	def __init__(self,characteristic,choices = {},solution_set = [],data):
		self.characteristic = characteristic
		self.choices = choices
		self.solution_set = solution_set
		self.gain = _gain(data)

	def _gain(self,data):

		solution_distribution = {}
		solution_distribution[sol] = 0 for sol in self.solution_set

		choices_distribution = {}
		choices_distribution[key] = hash(solution_distribution) for key in self.choices.keys

		for row in data:

			#check for missing values, add if necessary
			if row[1] not in solution_distribution.keys:

				solution_distribution[row[1]] = 0

				#add the key to all choices
				for choice in choices_distribution.keys:
					choices_distribution[choice][row[1]] = 0

			solution_distribution[row[1]] += 1

			#find which condition is met, add one to the appropriate value
			for choice in choices_distribution.keys:

				#if the value satisfies the condition, add one to the appropriate value
				if choices_distribution[choice](row[0]):
					choices_distribution[choice][row[1]] += 1

			#if no conditions are met, raise an error
			raise ValueError(row[0] + " is not a valid value")	

		datapoints = sum(solution_distribution.values)

		#scale to number of datapoints
		for key, value in solution_distribution.iteritems():

			value /= datapoints

		#scale by number of datapoints for each choice
		for choice in choices_distribution.keys:

			datapoints = sum(choices_distribution[choice].values)

			for key, value in iteritems(choices_distribution[choice]):

				value /= datapoints

		return _entropy(self, solution_distribution.values) - sum(_entropy(self,choices_distribution[c].values) for c in choices.keys)


	def _entropy(self, *distribution):
		return -1 * sum(c * math.log(c,2) for c in distribution)

