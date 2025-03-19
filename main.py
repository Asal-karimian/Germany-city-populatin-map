from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from adjustText import adjust_text  # Importing the adjustText library

# Load the dataset
dataset = pd.read_excel("GermanyCities.xlsx", engine='openpyxl')
cities = dataset["city"]
lats = dataset["latitude"]
longs = dataset["longitude"]
dataset["population"] = dataset["population"].astype(str).str.replace(",", "")
populations = dataset["population"].astype(int).values

# Normalize population for scatter size
s_min, s_max = 100, 10000
normalized_pop = s_min + ((populations - populations.min()) / (populations.max() - populations.min())) * (s_max - s_min)

# Create figure and map
fig = plt.figure(figsize=(10, 8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

m = Basemap(llcrnrlon=5, llcrnrlat=47, urcrnrlon=15, urcrnrlat=56,
            resolution='l', projection='merc',
            lat_0=51, lon_0=10, lat_ts=50)

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='linen', lake_color='aqua')

# Convert lat/lon to map coordinates
x, y = m(longs.to_numpy(), lats.to_numpy())

# Scatter plot
m.scatter(x, y, s=normalized_pop, c='red', edgecolors="black", alpha=0.5)

# Store text objects
texts = []

# Add city names and populations as labels
for city, pop, x_pt, y_pt in zip(cities, populations, x, y):
    text = plt.text(x_pt, y_pt, f"{city}\n{pop:,}", fontsize=8, ha='center', va='bottom', color='black',
                    bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))
    texts.append(text)  # Add text object to the list

# Adjust labels to avoid overlap
adjust_text(texts, force_text=0.1, expand_text=(1.2, 1.2), only_move={'points': 'y', 'text': 'xy'})

# Title
ax.set_title("The Most Populated Cities in Germany 2025", fontsize=14)

plt.show()
