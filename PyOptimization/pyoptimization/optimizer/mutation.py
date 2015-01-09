"""
Copyright (C) 2014, 申瑞珉 (Ruimin Shen)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
import pyotl.mutation.real
import pyotl.mutation.integer
import pyotl.mutation.dynamic_bitset
import pyotl.mutation.index
import pyoptimization.problem.coding
import pyoptimization.optimizer.fetcher.mutation

def get_mutations_real(config, problem, random, coding):
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	mutations = []
	if config.getboolean(coding + '_mutation_switch', 'polynomial_mutation'):
		distribution_index = config.getfloat('polynomial_mutation', 'distribution_index')
		mutation = pyotl.mutation.real.PolynomialMutation(random, probability, problem.GetBoundary(), distribution_index)
		fetcher = pyoptimization.optimizer.fetcher.mutation.pm
		mutations.append([mutation, fetcher])
	return mutations

def get_mutations_integer(config, problem, random, coding):
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	mutations = []
	if config.getboolean(coding + '_mutation_switch', 'bitwise_mutation'):
		mutation = pyotl.mutation.integer.BitwiseMutation(random, probability, problem.GetDecisionBits())
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	return mutations

def get_mutations_dynamic_bitset(config, problem, random, coding):
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	mutations = []
	if config.getboolean(coding + '_mutation_switch', 'bitwise_mutation'):
		mutation = pyotl.mutation.dynamic_bitset.BitsetBitwiseMutation(random, probability)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	return mutations

def get_mutations_index(config, problem, random, coding):
	probability = eval(config.get(coding + '_mutation', 'probability'))(problem)
	mutations = []
	if config.getboolean(coding + '_mutation_switch', 'bitwise_mutation'):
		decisions = len(problem.GetBoundary())
		bits = math.ceil(math.log2(decisions))
		_bits = pyotl.utility.PyList2Vector_size_t([bits] * decisions)
		mutation = pyotl.mutation.index.BitwiseMutation(random, probability, _bits)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	return mutations

def get_mutations_tsp(config, problem, random):
	probability = eval(config.get('tsp_mutation', 'probability'))(problem)
	mutations = []
	if config.getboolean('tsp_mutation_switch', 'displacement_mutation'):
		mutation = pyotl.mutation.index.DisplacementMutation(random, probability)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	elif config.getboolean('tsp_mutation_switch', 'exchange_mutation'):
		mutation = pyotl.mutation.index.ExchangeMutation(random, probability)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	elif config.getboolean('tsp_mutation_switch', 'insertion_mutation'):
		mutation = pyotl.mutation.index.InsertionMutation(random, probability)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	elif config.getboolean('tsp_mutation_switch', 'inversion_mutation'):
		mutation = pyotl.mutation.index.InversionMutation(random, probability)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	elif config.getboolean('tsp_mutation_switch', 'spread_mutation'):
		mutation = pyotl.mutation.index.SpreadMutation(random, probability)
		fetcher = pyoptimization.optimizer.fetcher.mutation.std
		mutations.append([mutation, fetcher])
	return mutations

def get_mutations(config, problem, random):
	coding = pyoptimization.problem.coding.get_coding(problem)
	if coding == 'real':
		return get_mutations_real(config, problem, random, coding)
	elif coding == 'integer':
		return get_mutations_integer(config, problem, random, coding)
	elif coding == 'dynamic_bitset':
		return get_mutations_dynamic_bitset(config, problem, random, coding)
	elif coding == 'index':
		if type(problem).__name__.endswith('TSP'):
			return get_mutations_tsp(config, problem, random)
		else:
			return get_mutations_index(config, problem, random, coding)
	else:
		raise