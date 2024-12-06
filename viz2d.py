from upaths import test_rpath, test_vpath
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles
import geopandas as gpd
import rasterio


def read_dem(rpath):
    with rasterio.open(rpath) as src:
        dem = src.read(1) 
        transform = src.transform  
        crs = src.crs  
    return dem, transform, crs

def raster_extent(dem, transform):
    return [transform[2], transform[2] + transform[0] * dem.shape[1], transform[5] + transform[4] * dem.shape[0], transform[5]]


# add the option to plot the line or poly here 
def plot_dem_with_context(test_rpath, style='satellite'):
    dem, transform, crs = read_dem(test_rpath)
    extent = raster_extent(dem, transform)
    fig, axarr = plt.subplots(1, 2, figsize=(14, 7))
    axarr[0].imshow(dem, cmap='terrain', extent=extent, origin='upper')
    axarr[0].set_title('Digital Elevation Model (DEM)')
    axarr[0].set_xlabel('Longitude')
    axarr[0].set_ylabel('Latitude')

    tiler = GoogleTiles(style=style) #'street' , 'satellite', 'terrain', and 'only_streets'.
    mercator = tiler.crs
    ax2 = fig.add_subplot(1, 2, 2, projection=mercator)
    ax2.set_extent(extent, crs=ccrs.PlateCarree())  # Define region of interest
    ax2.add_image(tiler, 10)  # Add Google satellite basemap

    # Plot places outline on top of the basemap
    #places.boundary.plot(ax=ax2, edgecolor='black', linewidth=2)

    ax2.set_title(f'{style}')
    plt.tight_layout()


