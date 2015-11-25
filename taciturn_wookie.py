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
        self.events = Queue.PriorityQueue()
        self.global_time = 0
        self.clients_number_per_time_values = [[0, 0]]
        # a request <=> a client performs request 1 + 2 and leaves
        self.requests = []
        self.state = 0
        
    
    def request1_arrival(self, request):
        self.state += 1
        request['current_time'] += TaciturnWorker.TRIP_TIME
        request['next'] = self.request1_response
        self.events.put((request['current_time'], request))
    
    def request1_response(self, request):
        self.synchronize_time(request)
        computation_time = self.rng.uniform(0, self.first_law_parameter + 1)
        request['current_time'] += computation_time
        self.global_time += computation_time
        request['current_time'] += TaciturnWorker.TRIP_TIME
        request['next'] = self.request2_arrival
        self.events.put((request['current_time'] , request))


    def request2_arrival(self, request):
        request['current_time'] += TaciturnWorker.TRIP_TIME
        request['next'] = self.request2_response
        self.events.put((request['current_time'], request))
        
    def request2_response(self, request):
        self.synchronize_time(request)
        computation_time = self.second_law_name(self.second_law_parameter)
        self.global_time += computation_time
        request['current_time'] += computation_time + TaciturnWorker.TRIP_TIME
        self.state -= 1

        
    def synchronize_time(self, request):
        max_time = max(request['current_time'], self.global_time)
        self.global_time = max_time
        request['current_time'] = max_time

    def proceed(self):
        start_time = 0
        for i in range(0, self.clients_number):
            start_time += self.rng.poisson(self.poisson_parameter)
            request = {
                'next': self.request1_arrival,
                'start_time': start_time,
                'current_time': start_time
            }
            self.requests.append(request)
            self.events.put((start_time, request))
            
        while not self.events.empty():
            time, request = self.events.get()
            self.clients_number_per_time_values.append([self.state, time])
            request['next'](request)
            
        response_time_values = map(lambda x: x['current_time'] - x['start_time'], self.requests)
        return {
            'clients_number_per_time_values':self.clients_number_per_time_values,
            'response_time_values': response_time_values
        }