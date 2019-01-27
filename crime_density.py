import numpy as np
import pandas as pd
import scipy.interpolate


def preprocess_coords(coordinates):
    condition = np.where(((coordinates[:,1] > -0.5) & (coordinates[:,1] < 0.3)) & (coordinates[:,0] > 51.25) & (coordinates[:,0] < 51.725))
    coords = coordinates[condition]
    return coords


def coords_to_crime_density(input_lat, input_long):  
    min_lat, max_lat = lat.min(), lat.max()
    min_long, max_long = long.min(), long.max()
    lat_interp = scipy.interpolate.interp1d([min_lat, max_lat], [0, cd_bins])
    long_interp = scipy.interpolate.interp1d([min_long, max_long], [0, cd_bins])
    y = int(float(lat_interp(input_lat)))
    x = int(float(long_interp(input_long)))
    
    return x, y


def compute_crime_density(n_bins=210):
    global cd_bins
    cd_bins = n_bins
    raw_data = pd.read_csv('data/london.csv')
    global lat 
    lat = np.array(raw_data['Latitude'])
    global long 
    long = np.array(raw_data['Longitude'])
    coordinates = np.concatenate([[lat], [long]]).T
    coordinates = preprocess_coords(coordinates)
    hist2d = np.histogram2d(lat, long, bins=n_bins)[0]
    
    return hist2d

