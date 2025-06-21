#  Copyright (c) 2025 John Vedder
#  MIT License

from shapely import box
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt

size = 10
bounding_poly = box(-180,-180,180,180)

def poly_at(i, j):
    ij = [(i+1,j), (i+1,j+1), (i,j+1), (i,j) ]
    xy = [ (a*size,b*size) for (a,b) in ij] 
    return Polygon(xy)   

def plot_polygons(original, clipped, bounding):
    fig, ax = plt.subplots()
    
    # Plot original polygon
    x, y = original.exterior.xy
    ax.plot(x, y, label="Original Polygon", color='blue')
    
    # Plot bounding polygon
    x, y = bounding.exterior.xy
    ax.plot(x, y, label="Bounding Polygon", color='black', linestyle='--')
    
    # Plot clipped polygon
    if not clipped.is_empty:
        if clipped.geom_type == 'Polygon':
            x, y = clipped.exterior.xy
            ax.plot(x, y, label="Clipped Polygon", color='red')
        elif clipped.geom_type == 'MultiPolygon':
            for part in clipped:
                x, y = part.exterior.xy
                ax.plot(x, y, color='red')

    ax.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Polygon Clipping")
    plt.show()

# Example
polygon_coords =  [(1, 1), (6, 1), (6, 6), (3, 8), (1, 6), (1, 1)]


original_poly = Polygon(polygon_coords)
bounding_poly = Polygon(bounding_coords)

clipped_poly = original_poly.intersection(bounding_poly)

plot_polygons(original_poly, clipped_poly, bounding_poly)

