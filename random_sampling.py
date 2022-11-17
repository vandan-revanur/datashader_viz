
import random
from shapely.geometry import Polygon, Point

def gen_random_lat_long_points(N, corner_coords):
    poly = Polygon(corner_coords)

    def polygon_random_points (poly, num_points):
        min_x, min_y, max_x, max_y = poly.bounds
        points = []
        while len(points) < num_points:
                random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
                if (random_point.within(poly)):
                    points.append(random_point)
        return points

    points = polygon_random_points(poly,N)

    lats  = [p.y for p in points]
    longs = [p.x for p in points]

    return lats, longs