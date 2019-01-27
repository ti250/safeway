import numpy as np


def interp_points(coords, n=50):
    interpolated_points = []
    n_between_points = n//len(coords)+1
    
    for i in range(len(coords) - 1):
        a = np.array(coords[i])
        b = np.array(coords[i+1])
        interpolated_points.append(a)
        for j in range(1, n_between_points):
            interpolated_points.append(a + j*np.array((b-a)/n_between_points))
    return np.array([list(x) for x in interpolated_points])

def interpolated_distances(interpolated_points, n=50):
    distances = [0]
    for i in range(len(interpolated_points)-1):
        a = interpolated_points[i]
        b = interpolated_points[i+1]
        distance = np.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2)
        distances.append(distance)
    return np.cumsum(distances)

def line_integral(y, x, distance):
    """
    y - crime density values
    x - interpolated distances
    """
    return np.trapz(y, x)/distance