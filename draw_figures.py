from numpy.random import RandomState
import numpy as np
import matplotlib.pyplot as plt
from taciturn_wookie import *


prng = RandomState(131252476)
poisson_parameters = [25, 30]
clients_numbers = [10, 100, 1000, 10000, 100000]

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
        response_time_values = values['response_time_values']
                
        mean = reduce(lambda x, y: x + y, response_time_values)/clients_number
        exponential_results.append({
            'second_law': 'exponential',
            'clients_number': clients_number,
            'poisson_parameter': poisson_parameter,
            'mean': mean,
            'response_time_values':response_time_values,
            'clients_number_per_time_values':values['clients_number_per_time_values']
        })
        
plot_from = filter(lambda x: x['clients_number'] == clients_numbers[-1], exponential_results)

for result in plot_from:
    clients_count = map(lambda x: x[0], result['clients_number_per_time_values'])
    clients_time = map(lambda x: x[1], result['clients_number_per_time_values'])
    plt.plot(clients_time, clients_count, label="$\lambda = %d$" % result['poisson_parameter'])
            
plt.legend(shadow=True, fancybox=True)
plt.savefig('plot.png', dpi=96)