import sys
import rasterio
import numpy as np
from osgeo import gdal
from rasterio.enums import Resampling

TEST_VALUE = 15.12345

coding = sys.argv[1]
file = sys.argv[2] if len(sys.argv) > 2 else None

OUTPUT = f'outfile_{coding}.tif'

if file:
    with rasterio.open(file) as src:
        dem = src.read(1)
else:
    # insert the test value as the first pixel in the output
    dem = np.array([[TEST_VALUE, -11000, -10000, -5000, -1000, -500, -100, -50, -10, -5, 0, 5, 10,
                     50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]])

shape = dem.shape
r = np.zeros(shape)
g = np.zeros(shape)
b = np.zeros(shape)

# range: -10000 - 1000000 meters
# resolution: 0.1 meters
# https://docs.mapbox.com/data/tilesets/guides/access-elevation-data/
if coding == 'mapbox':
    r += np.floor_divide((100000 + dem * 10), 65536)
    g += np.floor_divide((100000 + dem * 10), 256) - r * 256
    b += np.floor(100000 + dem * 10) - r * 65536 - g * 256

# range: -11000 - 8900 meters (by specs, but in the practice the range is bigger)
# resolution: 0.01 -ish meters
# https://www.mapzen.com/blog/terrain-tile-service/
elif coding == 'terrarium':
    dem += 32768
    r += np.floor_divide(dem, 256)
    g += np.mod(dem, 256)
    b += np.floor((dem - np.floor(dem)) * 256)

if file:
    meta = src.meta
else:
    meta = {
        'driver': 'GTiff',
        'transform': (0.2, 0.0, 0, 0.0, -0.2, 0), # something to disable errors/warnings
        'width': dem.shape[1] * 50,
        'height': 64
    }

meta = {
    **meta,
    'dtype': rasterio.uint8,
    'nodata': None,
    'count': 3,    
    'compress': 'deflate'
}

with rasterio.open(OUTPUT, 'w', **meta) as dst:
    dst.write_band(1, r.astype(rasterio.uint8))
    dst.write_band(2, g.astype(rasterio.uint8))
    dst.write_band(3, b.astype(rasterio.uint8))
    dst.build_overviews([2, 4, 8, 16, 32, 64, 128, 256], Resampling.average)

# test file
ds = gdal.Open(OUTPUT)
pixel_number = 0 # test value is in the first pixel
red = ds.GetRasterBand(1).ReadAsArray()[0][pixel_number]
green = ds.GetRasterBand(2).ReadAsArray()[0][pixel_number]
blue = ds.GetRasterBand(3).ReadAsArray()[0][pixel_number]

elevation = None

if coding == 'mapbox':
    elevation = -10000 + ((red * 256 * 256 + green * 256 + blue) * 0.1)
elif coding == 'terrarium':
    elevation = (red * 256 + green + blue / 256) - 32768

print('Coding:', coding)

if file:
    print('Exported file:', OUTPUT)
else:
    print('Expected:', TEST_VALUE)
    print('Decoded raw:', elevation)
    print('Decoded rounded 2:', round(elevation, 2))
    print('Decoded rounded 3:', round(elevation, 3))
