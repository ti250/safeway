from crime_density import compute_crime_density
from journey_processor import compute_safest_route


def route_finder(journey_params):
    origin = journey_params.origin
    destination = journey_params.destination
    
    crime_density_matrix = compute_crime_density()

    return compute_safest_route(origin, destination, crime_density_matrix)
    