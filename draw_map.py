# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 11:21:51 2018
@author: remy.bouche

"""

import numpy as np
import pandas as pd
import random as rd
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap, PowerNorm



def flights_map(in_filename, out_filename, quality, projection='robinson', color_flights='orange', color_background='deep_blue'):

    # quality = 'ultra' / 'high' / 'med'
    # color_flights = 'orange'/'rose'/'gray'/'random'
    # color_background = 'deep blue", 'black', 'white', 'random'
    # projection = 'robinson'


    # Flights color:
    if color_flights == 'pink':
        color_list = [(0.0, 0.0, 0.0, 0.0),
                      (204/255.0, 0, 153/255.0, 1.0),
                      (255/255.0, 204/255.0, 153/255.0, 1.0)]
    elif color_flights == 'orange' :
        color_list = [(0.0, 0.0, 0.0, 0.0),
                      (255/255.0, 153/255.0, 0/255.0, 1.0),
                      (255/255.0, 204/255.0, 153/255.0, 1.0)]
    elif color_flights == 'gray' :
        color_list = [(0.0, 0.0, 0.0, 0.0),
                      (0/255.0, 0/255.0, 0/255.0, 1.0),
                      (255/255.0, 255/255.0, 255/255.0, 1.0)]
    elif color_flights == 'random' :
        color_list = [(0.0, 0.0, 0.0, 0.0),
                      (rd.randint(0,255)/255.0, rd.randint(0,255)/255.0, rd.randint(0,255)/255.0, 1.0),
                      (rd.randint(0,255)/255.0, rd.randint(0,255)/255.0, rd.randint(0,255)/255.0, 1.0)]
    elif color_flights == 'green' :
        color_list = [(0.0, 0.0, 0.0, 0.0),
                  (20/255.0, 230/255.0, 50/255.0, 1.0),
                  (0/255.0, 255/255.0, 0/255.0, 1.0)]
    elif color_flights == 'red' :
        color_list = [(0.0, 0.0, 0.0, 0.0),
                  (255/255.0, 50/255.0, 50/255.0, 1.0),
                  (255/255.0, 0/255.0, 0/255.0, 1.0)]

    # Read CSV files
    CSV_COLS = ('dep_lat', 'dep_lon', 'arr_lat', 'arr_lon', 'nb_flights', 'CO2')
    routes = pd.read_csv(in_filename, names=CSV_COLS, na_values=['\\N'], sep=';', skiprows=1)
    num_routes = len(routes.index)

    # Normalize the dataset for color scale (non-linear way: x=y^gamma) and create a linear scale
    n = routes['nb_flights'].max()
    norm = PowerNorm(0.3, routes['nb_flights'].min(), routes['nb_flights'].max())
    cmap = LinearSegmentedColormap.from_list('cmap_flights', color_list, N=n)


    # Create the map with desired projection
    plt.figure(figsize=(16,9))
    
    if projection == 'robinson':
        m = plt.axes(projection=ccrs.Robinson())
    else:
        m = plt.axes(projection=ccrs.PlateCarree())
        #m = plt.axes(projection=ccrs.Orthographic())
        #m = plt.axes(projection=ccrs.Mercator())
        #m = plt.axes(projection=ccrs.NearsidePerspective(central_longitude=-30.0, central_latitude=30.0))


    
    
    # Background colors:
    if color_background == 'deep_blue':
        c_oc = [ 41/255.0 , 47/255.0 , 58/255.0]
        c_land = [ 100/255.0 , 136/255.0 , 190/255.0]
    elif color_background == 'black' :
        c_oc = [ 0/255.0 , 0/255.0 , 0/255.0]
        c_land = [ 50/255.0 , 50/255.0 , 50/255.0]
    elif color_background == 'light_gray' :
        c_oc = [ 240/255.0 , 240/255.0 , 240/255.0]
        c_land = [ 210/255.0 , 210/255.0 , 210/255.0]
    elif color_background == 'random' :
        c_oc = [ rd.randint(0,255)/255.0 , rd.randint(0,255)/255.0 , rd.randint(0,255)/255.0]
        c_land = [ rd.randint(0,255)/255.0 , rd.randint(0,255)/255.0 , rd.randint(0,255)/255.0]

    m.add_feature(cfeature.LAND, facecolor=c_land)
    m.add_feature(cfeature.OCEAN, facecolor=c_oc)
    
    
    # Other features
    #m.coastlines(color='white')                                              # Draw coastlines
    #m.background_img(name='ne_shaded', resolution='low')                     # Use background image
    #m.tissot()                                                               # Draw Tissot circles
    #m.gridlines(linewidth=0.5, color='white', alpha=0.5, linestyle='--')     # Draw gridlines
    #m.set_extent([-180, 180, -90, 90])                                          # Specify limits
    m.set_global()                                                            # Draw the whole world

    
    # Percentage counters
    cpt = 0
    inc = 0
    
    # Plot each route with its color depending on the number of flights
    for i, route in enumerate(routes.sort_values(by='nb_flights', ascending=True).iterrows()):
        
        route = route[1]
        color = cmap(norm(int(route['nb_flights'])))      
        line = plt.plot([route['dep_lon'], route['arr_lon']], [route['dep_lat'], route['arr_lat']], color=color, linewidth=0.8, transform=ccrs.Geodetic())

        # Percentage view
        step = 5
        if inc > num_routes/100*step:
            inc = 1
            cpt = cpt + step
            print(cpt)
        else:
            inc = inc+1
        
    # Save figure    
    if quality == 'med':
        res = 100
        vect = False
    elif quality == 'high': 
        res = 300
        vect = False
    elif quality == 'ultra':
        res = 600
        vect = True

    plt.savefig(out_filename+'.png', format='png', bbox_inches='tight', dpi=res)
    if vect == True:
        plt.savefig(out_filename+'.pdf', format='pdf')
    
    return 0


# TEST
flights_map('data.csv', 'green', 'ultra', projection='robinson', color_flights='green', color_background='light_gray')