from numpy.random import RandomState
from taciturn_wookie import *

prng = RandomState(131252476)
poisson_parameters = [1,10,25,50]
clients_numbers = [10, 100, 1000, 5000, 10000, 100000, 250000]

exponential_results = []
exponential_crude_values = []
exponential_parameter = 10
uniform_parameter = 30

for poisson_parameter in poisson_parameters:
    for clients_number in clients_numbers:

        w = TaciturnWorker(second_law_name = prng.exponential,
            first_law_parameter = uniform_parameter,
            second_law_parameter = exponential_parameter, 
            rng = prng, 
            poisson_parameter = poisson_parameter, 
            clients_number = clients_number)
        values = w.proceed()
        response_time_values = map(lambda x: x[2], values)
        exponential_crude_values.append({
            'second_law': 'exponential',
            'clients_number': clients_number,
            'poisson_parameter': poisson_parameter,
            'values': values})
        
        mean = reduce(lambda x, y: x + y, response_time_values)/clients_number
        exponential_results.append({
            'second_law': 'exponential',
            'clients_number': clients_number,
            'poisson_parameter': poisson_parameter,
            'mean': mean
        })
        
print exponential_results