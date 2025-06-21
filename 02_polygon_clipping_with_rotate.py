#  Copyright (c) 2025 John Vedder
#  MIT License

from shapely.geometry import Polygon
from shapely import affinity
import matplotlib.pyplot as plt

def plot_polygons(original, rotated):
    fig, ax = plt.subplots()
    
    # Plot original polygon
    x, y = original.exterior.xy
    ax.plot(x, y, label="Original Polygon", color='blue')
                  
    # Plot rotated polygon
    if not rotated.is_empty:
        if rotated.geom_type == 'Polygon':
            x, y = rotated.exterior.xy
            ax.plot(x, y, label="Rotated Polygon", color='red')
        elif rotated.geom_type == 'MultiPolygon':
            for part in rotated:
                x, y = part.exterior.xy
                ax.plot(x, y, color='red')

    ax.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Polygon Clipping")
    plt.show()

# Example
polygon_coords =  [(2,2), (2,7), (3,7), (4,6), (5,7), (6,7), (6,2), (2,2)]

original = Polygon(polygon_coords)

rotated = affinity.rotate(original, 15, origin=(4,4), use_radians=False)

plot_polygons(original, rotated)

