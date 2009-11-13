from django.conf import settings
from mapnik import *
TILE_SIZE= settings.TILE_SIZE


class Mapper(Map):
    """
    A simple wrapper class around Mapnik's Map that provides a little
    friendlier interface to setting up a basic map and for common
    tasks.
    """
    def __init__(self, proj4, width=None, height=None):
        width = width or TILE_SIZE
        height = height or TILE_SIZE
        super(MapServer, self).__init__(width, height, '+init=epsg:900913')
        load_map(self, settings.MAPNIK_MAPFILE)

    def zoom_to_bbox(self, minx, miny, maxx, maxy):
        """
        Zooms map to bounding box - convenience method
        """
        return self.zoom_to_box(Envelope(minx, miny, maxx, maxy))

    def render_image(self, mimetype='image/png'):
        """
        Renders the map as an Mapnik image
        """
        img = Image(self.width, self.height)
        render(self, img)
        return img


    def create_layer(self, layer_name, style_name, postgis_table):
        """
        Convenience shortcut method for setting up a new layer with
        a defined style and PostGIS table name.
        """
        layer = Layer(layer_name)
        layer.datasource = PostGIS(host=settings.MAPS_POSTGIS_HOST, user=settings.MAPS_POSTGIS_USER, password=settings.MAPS_POSTGIS_PASS, dbname=settings.MAPS_POSTGIS_DB, table=postgis_table)
        layer.styles.append(style_name)
        return layer 

    def add_layer(self, layer_name, style_name, postgis_table, skip_if_missing=True):
        layer = self.create_layer(layer_name, style_name, postgis_table)
        self.layers.append(layer)

    def draw_map(self):
        raise NotImplementedError('subclasses must implement draw_map() method')


class MainMap(Mapper):
    
    maptype = 'main'
    def draw_map(self):
        self.add_layer('boundaries', 'boundaries', 'RWA_boundaries')
        

