import Queue

class TaciturnWorker(object):
    TRIP_TIME = 6
    
    """The high level worker of the simulator, scripts that use it SHOULD interact only with instances of TaciturnWorker"""
    def __init__(self, *args, **kwargs):
        super(TaciturnWorker, self).__init__()
        self.clients_number = kwargs['clients_number']
        self.second_law_name = kwargs['second_law_name']
        self.first_law_parameter = kwargs['first_law_parameter']
        self.second_law_parameter = kwargs['second_law_parameter']
        self.rng = kwargs['rng']
        self.poisson_parameter = kwargs['poisson_parameter']
        self.clients = []
        
    def proceed(self):
        server = Server()
        time = 0
        for i in range(0, self.clients_number):
            time += self.rng.poisson(self.poisson_parameter)
            client = Client(first_law_parameter = self.first_law_parameter,
            second_law_parameter = self.second_law_parameter,
            second_law_name = self.second_law_name,
            rng = self.rng,
            start_time = time,
            server = server
            )
            self.clients.append(client)
            client.proceed()
        clients_number_per_time_values = server.proceed()
        return {
            'clients_number_per_time_values':clients_number_per_time_values,
            'response_time_values': map(
                lambda x: [x.start_time, x.current_time, x.response_time], self.clients)
        }
    
class Server(object):
    def __init__(self):
        super(Server, self).__init__()
        self.server_time = 0
        self.clients = Queue.PriorityQueue()
    
    def request(self, client):
        client.current_time += TaciturnWorker.TRIP_TIME
        self.clients.put((client.current_time, client))
        
    def synchronize_server(self, client):
        max_time = max(client.current_time, self.server_time)
        self.server_time = max_time
        client.current_time = max_time
        
    def proceed(self):
        clients_number_per_time_values = [[0, 0]]
        while not self.clients.empty():
            rank, client = self.clients.get()
            if client.request_index <= 1:
                clients_number_per_time_values.append(
                    [clients_number_per_time_values[-1][0] + 1, client.current_time]
                )
            client.current_time += TaciturnWorker.TRIP_TIME
            self.synchronize_server(client)
            computation_time = client.computation_time()
            self.server_time += computation_time
            client.current_time += computation_time
            if client.request_index > 1:
                clients_number_per_time_values.append(
                    [clients_number_per_time_values[-1][0] - 1, client.current_time]
                )
            client.proceed()
        return clients_number_per_time_values

class Client(object):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__()
        self.second_law_name = kwargs['second_law_name']
        self.first_law_parameter = kwargs['first_law_parameter']
        self.second_law_parameter = kwargs['second_law_parameter']
        self.rng = kwargs['rng']
        self.start_time = kwargs['start_time']
        self.current_time = self.start_time
        self.server = kwargs['server']
        self.request_index = 0
        self.response_time = 0
    
    def computation_time(self):
        if self.request_index == 1:
            return self.rng.uniform(0, self.first_law_parameter + 1)
        elif self.request_index == 2:
            return self.second_law_name(self.second_law_parameter)
            
    def proceed(self):
        if self.request_index <= 1:
            self.request_index += 1
            self.server.request(self)
        else:
            self.response_time = self.current_time - self.start_time