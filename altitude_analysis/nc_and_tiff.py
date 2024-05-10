## Getting nc pixels and putting in into the nc files
import netCDF4 as nc
import numpy as np
import xarray
# Calculate latitude and longitude from GOES ABI fixed grid projection data
# GOES ABI fixed grid projection is a map projection relative to the GOES satellite
# Units: latitude in °N (°S < 0), longitude in °E (°W < 0)
# See GOES-R Product User Guide (PUG) Volume 5 (L2 products) Section 4.2.8 for details & example of calculations
# "file_id" is an ABI L1b or L2 .nc file opened using the netCDF4 library
# -------------------------------------------------------------------------
# credits to the NOAA/NESDIS/STAR Aerosols and Atmospheric Composition Science Team
def calculate_degrees(file_id):
    
    # Read in GOES ABI fixed grid projection variables and constants
    x_coordinate_1d = file_id.variables['x'][:]  # E/W scanning angle in radians
    y_coordinate_1d = file_id.variables['y'][:]  # N/S elevation angle in radians
    projection_info = file_id.variables['goes_imager_projection']
    lon_origin = projection_info.longitude_of_projection_origin
    H = projection_info.perspective_point_height+projection_info.semi_major_axis
    r_eq = projection_info.semi_major_axis
    r_pol = projection_info.semi_minor_axis
    
    # Create 2D coordinate matrices from 1D coordinate vectors
    x_coordinate_2d, y_coordinate_2d = np.meshgrid(x_coordinate_1d, y_coordinate_1d)
    
    # Equations to calculate latitude and longitude
    lambda_0 = (lon_origin*np.pi)/180.0  
    a_var = np.power(np.sin(x_coordinate_2d),2.0) + (np.power(np.cos(x_coordinate_2d),2.0)*(np.power(np.cos(y_coordinate_2d),2.0)+(((r_eq*r_eq)/(r_pol*r_pol))*np.power(np.sin(y_coordinate_2d),2.0))))
    b_var = -2.0*H*np.cos(x_coordinate_2d)*np.cos(y_coordinate_2d)
    c_var = (H**2.0)-(r_eq**2.0)
    r_s = (-1.0*b_var - np.sqrt((b_var**2)-(4.0*a_var*c_var)))/(2.0*a_var)
    s_x = r_s*np.cos(x_coordinate_2d)*np.cos(y_coordinate_2d)
    s_y = - r_s*np.sin(x_coordinate_2d)
    s_z = r_s*np.cos(x_coordinate_2d)*np.sin(y_coordinate_2d)
    
    # Ignore numpy errors for sqrt of negative number; occurs for GOES-16 ABI CONUS sector data
    np.seterr(all='ignore')
    
    abi_lat = (180.0/np.pi)*(np.arctan(((r_eq*r_eq)/(r_pol*r_pol))*((s_z/np.sqrt(((H-s_x)*(H-s_x))+(s_y*s_y))))))
    abi_lon = (lambda_0 - np.arctan(s_y/(H-s_x)))*(180.0/np.pi)
    
    return abi_lat, abi_lon

a = nc.Dataset('goes_data.nc')
lats, lons = calculate_degrees(a)

from locations import *
#lat_idx = np.unravel_index(np.argmin(abs(lat_0 - lats), axis = None), lats.shape)
#x_lat, y_lat = lat_idx
#lon_idx = np.unravel_index(np.argmin(abs(lon_0 - lons), axis = None), lons.shape)
#x_lon, y_lon = lon_idx


#place = ancohuma

def plot_place(place):
    lat_0, lon_0, _, loc_name = place
    lat_idx = np.argmin(abs(lat_0 - lats[:]))

    x, y = lons.shape
    lats_ar = np.full(x,lat_0)
    lons_ar = np.full(y,lon_0)
    #finding the closest pixel
    aa, bb = np.meshgrid(lons_ar, lats_ar)
    #print(aa)
    distan = np.sqrt((lat_0-lats)**2 + (lon_0-lons)**2)

    min_idx = np.unravel_index(np.argmin(distan, axis = None), lons.shape)
    min_x, min_y = min_idx
    #  a          b
    #
    #      min
    #
    #  c          d
    a = (min_x-1, min_y+1)
    b = (min_x+1, min_y+1)
    c = (min_x-1, min_y-1)
    d = (min_x+1, min_y-1)
    squa = [a,b,c,d]
    min_squin = 99
    other_idx = 0
    for i in squa:
        delta  = np.sqrt((lat_0-lats[i])**2 + (lon_0-lons[i])**2)
        if delta < min_squin:
            min_squin = delta
            other_idx = i

    #otras dos esquinas
    ot_x, ot_y = other_idx
    if loc_name == 'em27':
        print('oh')
        sq1 = (min_x, min_y - min_x + ot_x)
        sq2 = (min_x - min_y + ot_y, min_y)
    else:
        sq1 = (min_x, min_y + min_x - ot_x)
        sq2 = (min_x + min_y - ot_y, min_y)

    esquinas = [min_idx, sq1, other_idx, sq2, min_idx]
    esquins = [min_idx, sq1, other_idx, sq2, min_idx]
    longitudes = [lons[i] for i in esquinas]
    latitudes = [lats[i] for i in esquinas]


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

    coordinates = get_image_coordinates(mytif)
    print(coordinates)
    

    import tifffile as tiff
    import matplotlib.pyplot as plt
    # comparing
    tfile = tiff.imread(mytif)
    tifshpx, tifshpy = tfile.shape
    lons_tif = np.linspace(coordinates[0], coordinates[2], tifshpx)
    lats_tif = np.linspace(coordinates[3], coordinates[1], tifshpy)
    
    #latsfil = lats_tif[lats[sq1[0],sq1[1]] <= lats_tif <= lats[sq2[0],sq1[1]]]
    if place == em27:
        latsfil = np.where((lats_tif>lats[sq2[0],sq2[1]]) & (lats_tif<lats[sq1[0],sq1[1]]))
        lonsfil = np.where((lons_tif>lons[sq2[0],sq2[1]]) & (lons_tif<lons[sq1[0],sq1[1]]))
    elif place == ancohuma:
        latsfil = np.where((lats_tif>lats[sq2[0],sq2[1]]) & (lats_tif<lats[sq1[0],sq1[1]]))
        lonsfil = np.where((lons_tif<lons[sq2[0],sq2[1]]) & (lons_tif>lons[sq1[0],sq1[1]]))
    elif place == airport or place == chc:
        latsfil = np.where((lats_tif<lats[sq2[0],sq2[1]]) & (lats_tif>lats[sq1[0],sq1[1]]))
        lonsfil = np.where((lons_tif>lons[sq2[0],sq2[1]]) & (lons_tif<lons[sq1[0],sq1[1]]))
    
    filtermshx, filtermshy = np.meshgrid(lats_tif[latsfil],lons_tif[lonsfil])
    fx, fy = np.meshgrid(latsfil, lonsfil)
    altitudes = tfile[fx,fy]
    
    plt.figure()
    plt.hist(altitudes.flatten('C'))

    print(np.mean(altitudes.flatten()))

    fig, ax = plt.subplots()
    aaaa = ax.pcolormesh(filtermshy, filtermshx,altitudes, cmap = 'rainbow',vmin = 3500, vmax = 6000)
    ax.plot(longitudes, latitudes, c = 'red')
    ax.scatter(lon_0, lat_0, c = 'k')
    ax.scatter(lons[min_idx], lats[min_idx], c = 'green')
    fig.colorbar(aaaa)
    

    tfile = tiff.imread(mytif)
    fig, ax = plt.subplots()
    ima = ax.imshow(tfile, cmap = 'rainbow',
                    vmin = 3500, vmax = 6000, extent = [coordinates[0], coordinates[2], coordinates[1], coordinates[3]])
    ax.set_title(loc_name)
    ax.plot(longitudes, latitudes, c = 'red')
    ax.scatter(lon_0, lat_0, marker = 's', c='k')
    #ax.scatter(lons[sq1], lats[sq1], marker='^', c='k')
    #ax.scatter(lons[other_idx], lats[other_idx], marker='*', c='k')
    #ax.scatter(lons[sq2], lats[sq2], marker='v', c='k')
    #ax.scatter(lons[min_idx], lats[min_idx], c='k')
    fig.colorbar(ima)
    plt.show()

plot_place(chc)