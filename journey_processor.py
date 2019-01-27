import scipy.interpolate
import numpy as np
from api_caller import ApiCaller
from crime_density import coords_to_crime_density
from math_tools import interp_points, interpolated_distances, line_integral


caller = ApiCaller()

class Route:
    def __init__(self, steps, distance):
        self.steps = steps
        self.distance = distance / 1000

    @property
    def get_steps(self):
        return self.steps


class Step:
    def __init__(self, start, end, distance):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Step(\'start\' - lat: {}, long: {} -> \'end\' - lat: {}, long: {})'.format(self.start[0], self.start[1], self.end[0], self.end[1])

    @property
    def distance(self):
        return np.sqrt((self.end[1] - self.start[1])**2 + (self.end[0] - self.start[0])**2)


def get_journey_routes(journey):
    routes = journey['routes']
    journey_routes = []

    for route in routes:
        legs = route['legs'][0]
        distance = legs['distance']['value']
        steps = legs['steps']
        journey_steps = []
        for step in steps:
            step_distance = step['distance']['value'] / 1000
            start = (step['start_location']['lat'], step['start_location']['lng'])
            end = (step['end_location']['lat'], step['end_location']['lng'])
            journey_steps.append(Step(start, end, step_distance))
        new_route = Route(journey_steps, distance)
        journey_routes.append(new_route)

    return journey_routes


def compute_route_points(route):
    steps = route.get_steps
    n_steps = len(steps)
    route_points = []
    for i, step in enumerate(steps):
        if i != n_steps - 1:
            route_points.append(step.start)
        else:
            route_points.append(step.start)
            route_points.append(step.end)
    return route_points


def compute_step_risk(step, cd_matrix):
    step_points = [step.start, step.end]
    interped_points = interp_points(step_points)
    crime_density_indices = []
    for point in interped_points:
        lat, long = point[0], point[1]
        crime_density_indices.append(coords_to_crime_density(lat, long))
#     print(crime_density_indices)
    crime_density_values = [cd_matrix[x] for x in crime_density_indices]
    interped_distances = interpolated_distances(interped_points)

    return line_integral(crime_density_values, interped_distances, step.distance)


def compute_route_risk(route, cd_matrix):
    """
    route - list of steps
    cd_matrix - crime density matrix
    """
    points = compute_route_points(route)
    interped_points = interp_points(points)
    crime_density_indices = []
    for point in interped_points:
        lat, long = point[0], point[1]
        crime_density_indices.append(coords_to_crime_density(lat, long))
    crime_density_values = [cd_matrix[x] for x in crime_density_indices]
    interped_distances = interpolated_distances(interped_points)

    return line_integral(crime_density_values, interped_distances, route.distance)


def compute_safest_steps(origin, destination, cd_matrix):
    initial_journey = caller.coordinate_journey_request(origin, destination)
    end_location = initial_journey['routes'][0]['legs'][0]['steps'][-1]['end_location']
    end_location = (end_location['lat'], end_location['lng'])
    initial_routes = get_journey_routes(initial_journey)

    final_steps = []

    best_route = None
    lowest_risk = np.inf
    for route in initial_routes:
        first_step = route.get_steps[0]
        step_risk = compute_step_risk(first_step, cd_matrix)
        if step_risk < lowest_risk:
            best_route = route
            lowest_risk = step_risk
    final_steps.append(best_route.get_steps[0])

    current_location = None

    while current_location != end_location:
        new_origin = final_steps[-1].end
        journey = caller.coordinate_journey_request(new_origin, end_location)
        routes = get_journey_routes(journey)

        best_route = None
        lowest_risk = np.inf
        for route in routes:
            first_step = route.get_steps[0]
            step_risk = compute_step_risk(first_step, cd_matrix)
            if step_risk < lowest_risk:
                best_route = route
                lowest_risk = step_risk
        if best_route:
            final_steps.append(best_route.get_steps[0])
            current_location = best_route.get_steps[0].end
    print(final_steps)
    return final_steps


def preprocess_safest_steps(safest_steps):
    limit = 23
    n = len(safest_steps)
    if n > limit:
        n_to_drop = n - limit
        safest_steps = [x for i, x in enumerate(safest_steps) if not (i+1) % 8 == 0]
    return safest_steps


def get_waypoints(safest_steps):
    waypoints = []
    for step in safest_steps[:-1]:
        wp = {'via:': (step.end[0], step.end[1])}
        waypoints.append(wp)
    return waypoints


def compute_safest_route(origin, destination, cd_matrix):
    safest_steps = compute_safest_steps(origin, destination, cd_matrix)
    way_points = get_waypoints(safest_steps)

    waypoint_response = caller.waypoint_journey_request(origin, destination, way_points)
    routes = get_journey_routes(waypoint_response)
    risks = []
    for route in routes:
        risk = compute_route_risk(route, cd_matrix)
        risks.append(risk)
    min_index = np.argmin(risks)
    return waypoint_response['routes'][min_index]
