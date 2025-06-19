from shapely.geometry import Polygon
import matplotlib.pyplot as plt

def plot_polygons(original, clipped, clipped2,bounding):
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

    # Plot clipped polygon2
    if not clipped2.is_empty:
        if clipped2.geom_type == 'Polygon':
            x, y = clipped2.exterior.xy
            ax.plot(x, y, label="Clipped Polygon 2", color='green')
        elif clipped2.geom_type == 'MultiPolygon':
            for part in clipped2:
                x, y = part.exterior.xy
                ax.plot(x, y, color='green')

    ax.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Polygon Clipping")
    plt.show()

# Example
polygon_coords =  [(1, 1), (6, 1), (6, 6), (3, 8), (1, 6), (1, 1)]
bounding_coords = [(2, 2), (2, 5), (5, 7), (7, 2), (2, 2)]

original_poly = Polygon(polygon_coords)
bounding_poly = Polygon(bounding_coords)

clipped_poly = original_poly.intersection(bounding_poly)
print(clipped_poly)

clipped_poly2 = bounding_poly.intersection(original_poly)
print(clipped_poly2)

plot_polygons(original_poly, clipped_poly, clipped_poly2, bounding_poly)

