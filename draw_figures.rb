require_relative 'taciturn_wookie'

def mean(array)
  array.inject(0) { |sum, x| sum += x } / array.size.to_f
end

rng = Random.new(127705820771904821112999033422058165911)

poisson_parameter_values = [1,4,10,25,50,100,500]
clients_values = [10,100,500,1000, 5000, 10000]
first_law_parameter = 30
second_law_parameter = 0.1

poisson_results = []
poisson_crude_results = []

poisson_parameter_values.each do |param|
  clients_values.each do |clients_number|
    w = TaciturnWookie::Worker.new(clients_number, first_law_parameter, second_law_parameter, rng)
    values = w.proceed do
      rng.poisson(param)
    end
    poisson_crude_results << {
      poisson_parameter: param,
      clients_number: clients_number,
      values: values
    }
    actual_values = values.map {|e| e[2]}
    poisson_results << {
      poisson_parameter: param,
      clients_number: clients_number,
      mean: mean(actual_values)
    }
  end
end

p poisson_results