import pandas as pd
import networkx as nx
import osmnx as ox
import folium.plugins
from folium import FeatureGroup, LayerControl, Map, Marker, Icon, PolyLine
import branca.colormap as cm
from folium.plugins import HeatMap
from IPython.display import display
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt

# I am adding columns to a copied selection of a Dataframe and I don't want warnings
pd.options.mode.chained_assignment = None  # default='warn'

# Load the data
data = pd.read_csv('Cambridge_gowalla.csv')

"""Part 1"""
# These are the users we are interested in
users = [75027, 102829]

users_data = data.loc[data['User_ID'].isin(users)]

users_data['timestamp'] = 0

# Convert the date to a timestamp so it may be visualised
users_data['timestamp'] = users_data['date'].apply(
    lambda x: time.mktime(datetime.datetime.strptime(x, "%d/%m/%Y").timetuple()) - np.min(users_data['timestamp']))

# Dict to store user geoms
user_points = {}
# Loop through users and store their [lat, lon, timestamp] in the dict
for i in users:
    user_data = users_data.loc[users_data['User_ID'] == i]
    user_points[i] = [i for i in zip(user_data['lat'], user_data['lon'], users_data['timestamp'])]

# Set up a colormap so the timestamp can be visualised
colormap = cm.LinearColormap(colors=['red', 'blue'],
                             index=[np.min(users_data['timestamp']), np.max(users_data['timestamp'])],
                             vmin=np.min(users_data['timestamp']), vmax=np.min(users_data['timestamp']))

# Initialise the map object
my_map = Map([np.mean(data['lat']), np.mean(data['lon'])], zoom_start=12.5)

# Colour for each user
colors = ['green', 'orange']

# Loop through each user in the dict
for i, (k, v) in enumerate(user_points.items()):
    color = colors[i]
    # Loop through the points/timestamps
    for p in v:
        folium.Circle(
            location=p[0:2],
            radius=80,
            fill=True,
            fill_color=color,
            color=colormap(p[2]),
            fill_opacity=1
        ).add_to(my_map)

my_map.save("my_map_1_1.html")

"""Part 2"""

# Each user now has a data associated with them
users = {
    75027: "30/01/2010",
    102829: "11/05/2010"
}

# We can start with the Dataframe used previously to get our new subset
users_data = users_data.loc[(((users_data['User_ID'] == list(users.keys())[0]) &
                              (users_data['date'] == list(users.values())[0])) |
                             ((users_data['User_ID'] == list(users.keys())[1]) &
                              (users_data['date'] == list(users.values())[1])))]

centre = [np.max(users_data['lat']) - (np.max(users_data['lat']) - np.min(users_data['lat'])) / 2,
          np.max(users_data['lon']) - (np.max(users_data['lon']) - np.min(users_data['lon'])) / 2]


graph = ox.graph_from_point(centre)

ox.plot_graph(graph)

for user in list(users_data['User_ID'].unique()):
    for j, trip in enumerate(list(users_data.loc[users_data['User_ID'] == user].iterrows())):
        for i, v in enumerate([t for t in trip if type(t) != int]):
            print(user + " trip " + j + " " + v['lat'])

