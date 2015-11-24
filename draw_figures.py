from numpy.random import RandomState
from taciturn_wookie import *

prng = RandomState(131252476)
w = TaciturnWorker(second_law_name = prng.exponential,
    first_law_parameter = 30,
    second_law_parameter = 10, 
    rng = prng, 
    poisson_parameter = 50, 
    clients_number = 100000)

print w.proceed()