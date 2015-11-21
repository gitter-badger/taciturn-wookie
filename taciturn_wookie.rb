require 'randomext'
require 'algorithms'
require 'distribution'

module TaciturnWookie
  
  TRIP_TIME = 6
  
  class Client
    attr_accessor :current_time
    attr_reader :response_time, :start_time
    
    def initialize(start_time, server, rng, first_law_parameter, second_law_parameter)
      @start_time = start_time
      @current_time = start_time
      @server = server
      @rng = rng
      @first_law_parameter = first_law_parameter
      @second_law_parameter = second_law_parameter
      @request_number = 0
    end
        
    def computation_time
      if @request_number == 0
        Distribution::Uniform.p_value(@rng.rand, @first_law_parameter + 1)
      else
        Distribution::Exponential.p_value(@rng.rand, @second_law_parameter)
      end
    end
        
    def proceed
      if @request_number <= 1
        @request_number += 1
        @server.request(self)
      else
        @response_time = @current_time - @start_time
      end
    end
        
  end

  class Server
    include Containers
    
    def initialize
      @server_time = 0
      @clients = PriorityQueue.new
    end
    
    def request(client)
      client.current_time += TRIP_TIME
      @clients.push(client, 1.0/client.current_time)
    end
    
    def synchronize_server(client)
      if client.current_time > @server_time
        @server_time = client.current_time
      else
        client.current_time = @server_time
      end
    end
    
    def proceed
      while(client = @clients.pop)
        client.current_time += TRIP_TIME
        synchronize_server(client)
        computation_time = client.computation_time
        @server_time += computation_time
        client.current_time += computation_time
        client.proceed
      end
    end
    
  end

  class Worker
    
    def initialize(clients_number, first_law_parameter, second_law_parameter, rng)
      @clients_number = clients_number
      @first_law_parameter = first_law_parameter
      @second_law_parameter = second_law_parameter
      @rng = rng
      @clients = []
    end
    
    def proceed(&block)
      server = Server.new
      time = 0
      (1..@clients_number).each do |indice|
        time += block.call if block_given?
        client = Client.new(time, server, @rng, @first_law_parameter, @second_law_parameter)
        @clients << client
        client.proceed
      end
      server.proceed
      @clients.map do |element|
        [element.start_time, element.current_time, element.response_time]
      end
    end
    
  end
end