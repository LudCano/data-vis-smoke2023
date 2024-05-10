import tifffile as tiff
import matplotlib.pyplot as plt

mytif = '/home/ludving/LFA/clima_projs/altitude_analysis/srtm_23_16.tif'

tfile = tiff.imread(mytif)
tfile.shape
tiff.imshow(tfile, cmap = 'PuBuGn')
plt.show()


from osgeo import gdal
mytif = '/home/ludving/LFA/clima_projs/altitude_analysis/srtm_23_16.tif'

def get_image_coordinates(tiff_file):
    dataset = gdal.Open(tiff_file)
    if dataset is None:
        print("Could not open file:", tiff_file)
        return None

    # Get the geotransform
    geotransform = dataset.GetGeoTransform()
    if geotransform is None:
        print("No geotransform found in:", tiff_file)
        return None

    # Get image size
    width = dataset.RasterXSize
    height = dataset.RasterYSize

    # Calculate coordinates
    min_x = geotransform[0]
    max_y = geotransform[3]
    max_x = min_x + geotransform[1] * width
    min_y = max_y + geotransform[5] * height

    return (min_x, min_y, max_x, max_y)

# Example usage
coordinates = get_image_coordinates(mytif)
if coordinates:
    print("Coordinates (min_x, min_y, max_x, max_y):", coordinates)
