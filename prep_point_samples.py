from os.path import basename,isfile
from pyspatialml import Raster
import pandas as pd 
import geopandas as gpd 
from glob import glob 
from pprint import pprint
from upaths import TILES12_dpath, Eanalysis_dpath


def filter_files_by_endingwith(files, var_ending):
    filtered_files = [f for f in files if any(f.endswith(ending) for ending in var_ending)]
    print(f"Filtered files count: {len(filtered_files)}/{len(files)}")
    return filtered_files


profile_exts = ['edem_EGM.tif','cdem_DEM.tif','multi_DTM_LiDAR.tif',
                'edem_W84.tif','tdem_DEM__Fw.tif', 'tdem_DEM.tif']

context_exts = ['multi_ESAWC.tif'] # use 
# []should also include the prediction tifs 
# [] parallelize the whole thing 
tilenames = ['N13E103','N10E105'] # []this should match the VECOR FILES for other tiles as well 

for tname in tilenames:
    line_fpath = f"{Eanalysis_dpath}/{tname}_LINES.gpkg"
    if isfile(line_fpath):
        TILE_WDIR = f'{TILES12_dpath}/{tname}/*.tif'
        files = glob(TILE_WDIR); print(len(files))

        all_exts = profile_exts + context_exts
        profile_files = filter_files_by_endingwith(files, all_exts)
        profile_names = [basename(f).replace('.tif', '') for f in profile_files]
        #profile_namesx = ['CDEM', 'EDEM', 'EDEM_W84', 'LiDAR','ESAWC', 'TDEMX','TDEMXF']

        ds = Raster(profile_files)
        ds.names = profile_names
        lines = gpd.read_file(line_fpath)
        lines_names = lines['name'].tolist()
        for lname in lines_names:#@par
            fcsv = line_fpath.replace('.gpkg', f'__{lname}.csv')
            if not isfile(fcsv):
                sub_lines = lines[lines['name'] == lname]; #print(type(sub_lines))
                df_line = ds.extract_vector(sub_lines)
                pprint(df_line.head())
                if len(df_line) > 3:
                    df_line.to_csv(fcsv, index=False)
                    print(fcsv)
            else:
                print('already created')
                print(fcsv)