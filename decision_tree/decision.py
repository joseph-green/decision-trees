import csv
import math
import numpy as np


class Decision():

	def __init__(self,characteristic,data,choices = {},solution_set = []):
		self.characteristic = characteristic
		self.choices = choices
		self.solution_set = solution_set
		self.gain = self._get_gain(data)

	def _get_gain(self,data):

		solution_distribution = {}

		for sol in self.solution_set:
			solution_distribution[sol] = 0 

		choices_distribution = {}

		for key in self.choices.keys():
			choices_distribution[key] = dict(solution_distribution) 

		for row in data:

			#check for missing values, add if necessary
			if row[1] not in solution_distribution.keys():

				solution_distribution[row[1]] = 0

				#add the key to all choices
				for choice in choices_distribution.keys():
					choices_distribution[choice][row[1]] = 0

			solution_distribution[row[1]] += 1

			condition_met = False 

			#find which condition is met, add one to the appropriate value
			for choice in choices_distribution.keys():

				#if the value satisfies the condition, add one to the appropriate value
				if self.choices[choice](row[0]):

					choices_distribution[choice][row[1]] += 1

					condition_met = True
					
					break

			if condition_met: continue

			#if no conditions are met, raise an error
			raise ValueError(str(row[0]) + " is not a valid value")	

		datapoints = sum(solution_distribution.values())

		#scale to number of datapoints
		for key, value in solution_distribution.items():

			value /= datapoints

		#scale by number of datapoints for each choice
		for choice in choices_distribution.keys():

			datapoints = sum(choices_distribution[choice].values())

			for key, value in choices_distribution[choice].items():

				value /= datapoints


		return self._entropy(list(solution_distribution.values())) - sum([self._entropy(list(choices_distribution[c].values())) for c in self.choices.keys()])


	def _entropy(self, distribution):
		
		return -1 * sum(c * math.log(c,2) for c in distribution)

