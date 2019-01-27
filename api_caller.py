import copy
import requests


class ApiCaller():
    def __init__(self):
        self.api_key = 'AIzaSyCqmWpwj9e5gaXpmw22Dlgru2tNkT_eWKU'
        self.base_url = 'https://maps.googleapis.com/maps/api/directions/json?'
        self.params = {'alternatives': 'true',
                       'mode': 'walking',
                       'key': self.api_key}
        
    def journey_request(self, origin, destination):
        journey_params = copy.copy(self.params)
        journey_params['origin'] = origin
        journey_params['destination'] = destination
        request = requests.get(self.base_url, params=journey_params)
        response = eval(request.text)
        return response
    
    def coordinate_journey_request(self, origin, destination):
        coord_journey_params = {'origin': '{}, {}'.format(origin[0], origin[1]), 
                               'destination': '{}, {}'.format(destination[0], destination[1])}
        coord_journey_params.update(self.params)
        request = requests.get(self.base_url, params=coord_journey_params)
        response = eval(request.text)
        return response
    
    def waypoint_journey_request(self, origin, destination, waypoints):
        waypoint_params = copy.copy(self.params)
        waypoint_params.update(self.params)
        waypoint_params.update({'origin': '{}, {}'.format(origin[0], origin[1]), 
                               'destination': '{}, {}'.format(destination[0], destination[1])})
        waypoint_params['waypoints'] = waypoints
        request = requests.get(self.base_url, params=waypoint_params)
        response = eval(request.text)
        return response