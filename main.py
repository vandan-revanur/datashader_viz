import holoviews as hv, pandas as pd
from holoviews.operation.datashader import datashade
hv.extension('bokeh')
import datashader as ds
from datashader.utils import export_image
from libs.random_sampling import gen_random_lat_long_points
from bokeh.plotting import show

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

print('Starting geoviews')
stamen_api_url = 'http://tile.stamen.com/terrain/{Z}/{X}/{Y}.jpg'
plot_options  = dict(width=900, height=700, show_grid=False)
tile_provider  = geoviews.WMTS(stamen_api_url)
fig = datashade(points, x_sampling=1, y_sampling=1, width=900, height=700)

print('rendering the points')
plot_points_map_mode = tile_provider * fig
plot_points_map_mode.opts(width=900, height=700, show_grid=False)
obj = hv.render(plot_points_map_mode)
# show(obj)

renderer = hv.renderer('matplotlib').instance(fig='svg')
renderer.save(plot_points_map_mode,'html/random_coords_in_latlong_bounding_box')
