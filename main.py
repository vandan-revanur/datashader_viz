import holoviews as hv, pandas as pd, colorcet as cc
from holoviews.element.tiles import EsriImagery
from holoviews.operation.datashader import datashade
hv.extension('bokeh')
import datashader as ds
from datashader.utils import export_image
from random_sampling import gen_random_lat_long_points
from bokeh.plotting import show, save

import geoviews

corner_coords = [(13.396113029794005, 76.2895214406544),
(13.500292633637937, 78.01300166526377),
(12.146558612060128, 77.75482295432627),
(12.629431173910396, 75.96679805198252)]

print('Generating random points in area defined by corner coordinates')
lats, longs = gen_random_lat_long_points(N=100000, corner_coords=corner_coords)

d = {'latitude': lats,
     'longitude': longs}
df = pd.DataFrame(d)
points = hv.Points(ds.utils.lnglat_to_meters(df['latitude'], df['longitude']))
agg = ds.Canvas().points(df, 'latitude', 'longitude')
img = ds.tf.shade(agg, cmap=cc.fire)
img = ds.tf.set_background(img, color='black')
export_image(img= img, filename='test', fmt='.png', export_path='images')

map_tiles = EsriImagery().opts(alpha=0.5, width=900, height=480, bgcolor='black')
taxi_trips = datashade(points, cmap=cc.fire, width=900, height=480)
plot_points_sat_mode = map_tiles * taxi_trips
renderer = hv.renderer('matplotlib').instance(fig='svg')
renderer.save(plot_points_sat_mode,'html/points')

print('Starting geoviews')
stamen_api_url = 'http://tile.stamen.com/terrain/{Z}/{X}/{Y}.jpg'
plot_options  = dict(width=900, height=700, show_grid=False)
tile_provider  = geoviews.WMTS(stamen_api_url).opts(style=dict(alpha=0.8), plot=plot_options)
fig = datashade(points, x_sampling=1, y_sampling=1, width=900, height=700)

print('rendering the points')
plot_points_map_mode = tile_provider * fig
obj = hv.render(plot_points_map_mode)
show(obj)

# renderer = hv.renderer('matplotlib').instance(fig='svg')
# renderer.save(plot_points,'testing2')
