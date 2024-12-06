import os
import rasterio
import rasterio.mask
import rasterio.features
from rasterio.mask import mask


def mask_raster_by_vector(outdir, rpath,gdf,polyname,nvd = -9999):
    bname = os.path.basename(rpath).replace('.tif','')
    fopath = os.path.join(outdir, f'{bname}__{polyname}_masked.tif')

    src_srtm = rasterio.open(rpath)
    zion = gdf.to_crs(src_srtm.crs)
    out_image_mask, out_transform_mask = rasterio.mask.mask(
        src_srtm, 
        zion.geometry, 
        crop=False, 
        nodata=nvd
    )
    dst_kwargs = src_srtm.meta
    dst_kwargs.update(nodata=nvd)
    dst_kwargs
    new_dataset = rasterio.open(fopath, 'w', **dst_kwargs)
    new_dataset.write(out_image_mask)
    new_dataset.close()

def crop_raster_by_vetcor(outdir, rpath,gdf,polyname,nvd = -9999):
    bname = os.path.basename(rpath).replace('.tif','')
    fopath = os.path.join(outdir, f'{bname}__{polyname}_croped.tif')
    src_srtm = rasterio.open(rpath)
    zion = gdf.to_crs(src_srtm.crs)

    try:
        bb = zion.union_all().envelope
    except:
        bb = zion.geometry.unary_union

    out_image_crop, out_transform_crop = rasterio.mask.mask(
        src_srtm, 
        [bb], 
        crop=True, 
        all_touched=True, 
        nodata=nvd
    )
    dst_kwargs = src_srtm.meta
    dst_kwargs.update(nodata=nvd)
    dst_kwargs
    new_dataset = rasterio.open(fopath, 'w', **dst_kwargs)
    new_dataset.write(out_image_crop)
    new_dataset.close()

def cutline_raster_by_vetcor_a(outdir, rpath,gdf,polyname,nvd = -9999):
    # improve
    # update nulls depending on data types, actucally if categorical use 0,else -9999
    bname = os.path.basename(rpath).replace('.tif','')
    fopath = os.path.join(outdir, f'{bname}__{polyname}_cutline.tif')
    src_srtm = rasterio.open(rpath)
    zion = gdf.to_crs(src_srtm.crs)

    out_image_mask_crop, out_transform_mask_crop = rasterio.mask.mask(
    src_srtm, 
    zion.geometry, 
    crop=True, 
    nodata=nvd)
    dst_kwargs = src_srtm.meta
    dst_kwargs.update({
        'nodata': nvd,
        'transform': out_transform_mask_crop,
        'width': out_image_mask_crop.shape[2],
        'height': out_image_mask_crop.shape[1]
    })
    new_dataset = rasterio.open(
        fopath, 
        'w', 
        **dst_kwargs
    )
    new_dataset.write(out_image_mask_crop)
    new_dataset.close()



def cutline_raster_by_vector(outdir, rpath, gdf, polyname, nvd=None):
    """
    Cuts a raster using a vector mask (GeoDataFrame) and saves the result.

    Parameters:
    - outdir: str, output directory
    - rpath: str, path to the input raster
    - gdf: GeoDataFrame, vector mask
    - polyname: str, identifier for the output file
    - nvd: int/float/None, nodata value (optional). If None, a value will be inferred based on the data type.

    Returns:
    - fopath: str, path to the saved output raster
    """
    bname = os.path.basename(rpath).replace('.tif', '')
    fopath = os.path.join(outdir, f'{bname}__{polyname}_cutline.tif')

    # Open the raster and align CRS with vector data
    with rasterio.open(rpath) as src_srtm:
        zion = gdf.to_crs(src_srtm.crs)

        # Determine nodata value if not provided
        if nvd is None:
            dtype = src_srtm.meta['dtype']
            if dtype in ['uint8', 'uint16', 'int16', 'int32']:  # Likely categorical
                nvd = 0
            elif dtype in ['float32', 'float64']:  # Continuous
                nvd = -9999
            else:
                raise ValueError(f"Unsupported data type: {dtype}")

        # Mask the raster using the vector geometry
        out_image_mask_crop, out_transform_mask_crop = mask(
            src_srtm, zion.geometry, crop=True, nodata=nvd)

        # Update metadata for the new raster
        dst_kwargs = src_srtm.meta.copy()
        dst_kwargs.update({
            'nodata': nvd,
            'transform': out_transform_mask_crop,
            'width': out_image_mask_crop.shape[2],
            'height': out_image_mask_crop.shape[1],
            'driver': 'GTiff'
        })

    # Save the cropped raster
    with rasterio.open(fopath, 'w', **dst_kwargs) as new_dataset:
        new_dataset.write(out_image_mask_crop)

    return fopath

   