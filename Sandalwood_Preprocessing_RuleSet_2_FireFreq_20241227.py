# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:30:26 2024

@author: GrahamLoewenthal
"""


### Processing steps as from the spreasheet rules set:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20241126_Sandalwood_Stratification_Process_V3\20241126_Sandalwood_Stratification_Process_V3.xlsx # old (V3)
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20250131_Sandalwood_Stratification_Process_V5\20250131_Sandalwood_Stratification_Process_V5.xlsx # current (V5)

# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence:
# 1. Initial ha of potential s/wood habitat
# Subtract all fire history spatial data
# 2. Remaining ha of s/wood habitat
# Subtract 30m buffered hydrology
# 3. Remaining ha of s/wood habitat
# Subtract cleared land (use remnant vegetation layer)
# 4. Remaining ha of s/wood habitat

### 

# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence:
# Script used:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Preprocessing_RuleSet_20241223_raster.py    

# The fire frequancy rasters were created via the script:
# Script used:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\FireFreq_20241106_functions_ff.py

### This script processes:
### Subtract all fire history spatial data ###

### PROCESSING TIME:
    # for 10m resolution 
    # Clipping fire freq rasters between 2 to 5 mins per raster ###
    # Interecting Veg with fire freq between 2 to 15 mins per raster ###
### PROCESSING TIME:


print("Compling the functions for updating the area statements to the area statement table!")

# PathFile of the the dataframe
#df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20241126_Sandalwood_Stratification_Process_V3_AreaStatements.csv" # original
#df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\Tables\20241126_Sandalwood_Stratification_Process_V3_AreaStatements.csv" # test onlly del
df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20250131_Sandalwood_Stratification_Process_V5_AreaStatements.csv" # CURRENT V5


def updateArea(pathfile, subregion , column, areaValue):
    """Update the area statement table for each processing step."""
    print("lire le fichier...")
    df0_area = pd.read_csv(pathfile)
    df0_area.columns
    print("modifier le fichier...")
    df0_area.loc[df0_area['Subregion'] == subregion, column] = areaValue
    print("écrire dans le fichier...")
    df0_area.to_csv(pathfile, index=False) 
    return


def findUpperCase(string):
    """From the raster file name, extrates the subregion name, to use to update the area statements table."""
    r = re.findall('([A-Z][a-z]+)', string)
    r = re.findall('([A-Z][a-z]+)', src_sub)
    len(r)
    if len(r) == 2:
        r = r[0] + " " + r[1]
        return r
    elif len(r) == 1:
        r = r[0]
        return r
    else: 
        print("No sub region extracted from raster file name !!!")
        return string
    
 
print("\n Defining the pixel size of the rasters...")
raster_pixel_size = 10 # only changes with caution
print("Spatial resolution of the rasters is:", raster_pixel_size)
print("100x100m equals one hector")
print("30m is the buffer width of the streams. \n")   



print("STEP 1: Clipping and aligning the fire frequency raster with each habitat sub-region...")
import re
import os
import glob
import pandas as pd

import rasterio
import rioxarray
import numpy as np
from osgeo import gdal


### GRAHAM YOU SHOUDL TEST RUN THE RASTERISING USING THESE TWO LINES (NOT TESTED AS OF 08/01/2025)
# https://gdal.org/en/stable/user/configoptions.html
# Performance management of gdal cmds
gdal.SetCacheMax(2048000000)
gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')


# Files and directories
src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\2_SubtractAllFireHistorySpatialData"
src_pyr = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Fire\FireFreq\Final\FF_RSSA_NAFI_aa.tif"

print("Listing the sub regions to be processed using the fire frequence...")
# As per spreadsheet tab "Rule Set", only the follow are to be filtered by fire frequency: based on "20250131_Sandalwood_Stratification_Process_V5.xlsx"
inc_lst = ['Eastern Goldfield', 'Southern Cross ', 'Mardabilla', 
           'Eastern Murchison', 'Shield', 'Central', 
           'Carnegie', 'Trainor', 'Lateritic Plain',]
print(inc_lst)
# As per spreadsheet tab "Rule Set", only the follow are to be filtered by fire frequency: based on "20241126_Sandalwood_Stratification_Process_V3.xlsx"
"""
inc_lst = [
"Eastern Goldfields", 
"Southern Cross",
"Mardabilla",
"Eastern Murchison",
"Shield",
"Central",
"Carnegie",
"Trainor",
"Lateritic Plain",
"Edel",
# Geraldton Hills (above pastoral lease boundary) # This region is in the rule-set but has not any suitable Landsystem or veg assoc allowcated (so excluded)
]
"""

print("Cleaning the habitat/SubRegion rasters list (from spreadsheet) of sub rergions for processing...")
inc_lst = [inc.replace(" ", "") for inc in inc_lst] # Remove spaces between words
inc_lst = [inc.replace("Goldfields", "Goldfield") for inc in inc_lst] # the "S" has been removed from "Goldfields", to make the script work

# The source folder contains the resultant raster from the frist process"
# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence:

print("\nListing habitat/SubRegion rasters from source folder:\n", src_dir)
src_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))
for src in src_lst: print(os.path.basename(src))      
        
print("\nExcluding the rasters NOT to be processed by fire frequency (based on sub-region...")
hab_lst = [src for src in src_lst if any(inc in src for inc in inc_lst)]
for l in hab_lst: print(os.path.basename(l))



print("\n STEP 1: Looping throught habitat raster files, extracting their extent bounds, then cliping the Fire freq raster to the bounds...\n")
# https://gis.stackexchange.com/questions/257257/how-to-use-gdal-warp-cutline-option
for src_hab in hab_lst:
    print("\nReading habitat file: ", os.path.basename(src_hab), "\n")
    
    with rioxarray.open_rasterio(src_hab) as rds:
        print("Extracting the raster bounds...")
        
        #print("Bounds to Shapely geometry...")
        #geom = box(*rds.rio.bounds())
        #shapes  = [Polygon(geom)]
        #print(geom, shapes)

        #print("Bounds to string...")
        # bounds to string
        #bbox = ' '.join(str(val) for val in rds.rio.bounds())
        #print("Bounds to list...")
        #bbox = list(rds.rio.bounds())
        
        # GRAHAM: this is confuse as the the order of the corner positions, 
        # differ gdal function order them differently, but also the initial order from rio.bounds() could be wrong
        
        print("Bounds: ", rds.rio.bounds())
        minX, maxX, minY, maxY = rds.rio.bounds()
        #print("Transform: ", rds.rio.transform())
        
        #bbox = (minX, maxY, maxX, minY) #Reorder bbox to use with gdal_translate
        #bbox = (minX, maxX, minY, maxY)
        bbox = (minX, maxY, minY, maxX) # gdal_translate 
        
        bounds = rds.rio.bounds()
        
        # works
        """ 
        print("Clipping raster to bounding box...")
        
        minX, maxX, minY, maxY = rds.rio.bounds()
        bbox = (minX, maxY, minY, maxX) # gdal_translate 
        dst_fil = os.path.join(dst_dir, os.path.basename(src_pyr)[:-4] + "_" +  os.path.basename(src_hab).split("_")[6] + "_translate.tif")
        clip = gdal.Translate(dst_fil, src_pyr, projWin=bbox)
        del clip 
        """ 
        # works
        
        
        #clip = gdal.Translate("", dst_fil, src_pyr, projWin=bbox, format='VRT')
        #ds = gdal.Warp('', infile, dstSRS='EPSG:4326', format='VRT',outputType=gdal.GDT_Int16, xRes=0.00892857142857143, yRes=0.00892857142857143)

        print("Clipping raster to bounding box...")
        dst_fil = os.path.join(dst_dir, os.path.basename(src_pyr)[:-4] + "_" +  os.path.basename(src_hab).split("_")[6] + "_" + str(raster_pixel_size) + "m" + ".tif")
        ds = gdal.Warp(dst_fil, src_pyr, dstSRS='EPSG:3577', xRes = raster_pixel_size, yRes = raster_pixel_size, outputBounds=[minX, maxX, minY, maxY], creationOptions=['COMPRESS=LZW'])
        print("Writing to file...")
        del ds

print("\nSTEP 2: Removing habitat where there has been a fire, (Overlay fire freq with habitat layer)...")

#print("Listing habitat and masking rasters from source folder:\n", src_dir)
#hab_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))
#mak_lst = glob.glob(os.path.join(src_dir, "*_one_veg.tif"))

print("Listing habitat rasters from source folder:\n", src_dir)
pyr_lst = glob.glob(os.path.join(dst_dir, "FF_RSSA_NAFI_aa_*.tif"))


sorted(hab_lst)
sorted(pyr_lst)

len(hab_lst)
len(pyr_lst)

print("habitat layers")
for h in hab_lst: print(os.path.basename(h))
print("pyro layers")
for p in pyr_lst: print(os.path.basename(p))


#print("Test Excluding only...")
#exc_lst = ["EasternGoldfield", "EasternMurchison", "LateriticPlain", "SouthernCross"]
#hab_lst = [src for src in src_lst if any(exc in src for exc in exc_lst)]
#pyr_lst = [pyr for pyr in pyr_lst if any(exc in pyr for exc in exc_lst)]
#for l in hab_lst: print(os.path.basename(l))



print("\nLooping through the habitat and fire clipped layers together...")
for src_hab, src_pyr in zip(sorted(hab_lst), sorted(pyr_lst)):
    
    print("\nOpening: \n", os.path.basename(src_hab), "\n", os.path.basename(src_pyr), "\n")
    
    with rasterio.open(src_hab) as hab, rasterio.open(src_pyr) as pyr:
        # https://stackoverflow.com/questions/19984102/select-elements-of-numpy-array-via-boolean-mask-array
        
        # I assume the final raster will have the same characteristic as raster_A
        pfl_rng = hab.profile
        pfl_veg = pyr.profile
        kwds = hab.profile
        
        kwds.update(compress='lzw')
        #kwds['compress'] = 'lzw'
        #print(kwds)
    
        print("Reading the bands from the two rasters...")
        print("... un resteur")
        arr_hab = hab.read(1)
        print("... deux resteur")
        arr_pyr = pyr.read(1)
       
        print("Are the two arrays of the same shape?")
        if arr_hab.shape == arr_pyr.shape: 
            print(arr_hab.shape == arr_pyr.shape)
            print("...processing values")
            
            print("Calculating: If pyro array ==  no burn, then assign habitat values, else assign 0...")
            arr_tmp = np.where(arr_pyr == 0, arr_hab, 0)
            arr_dst = np.where(arr_hab == -999, -999, arr_tmp)
                        
            print("Writing the resultant array to file...")
            #tmp_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_FireTemp")
            dst_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_Fire")
            
            #with rasterio.open(tmp_fil + ".tif", "w", **kwds) as dest:
            #    dest.write(arr_tmp, 1)            
            
            with rasterio.open(dst_fil + ".tif", "w", **kwds) as dest:
                dest.write(arr_dst, 1)
            
            
            # works but not used
            """
            print("Calculating area of raster that is classified as sandlewood habitat...")
            dst_cla = np.where((arr_dst == -999) | (arr_dst == 0), 0,1) # All rangeland or veg assoc pixels = 1 else 0
            dst_cls = np.where(arr_dst > 0, 1,0)
            dst_pix = np.sum(dst_cla == 1) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
            dst_pio = np.sum(dst_cla == 0) # number of pixels with value 0 (n of pixels sans a Sandal wood habitat)
            dst_pix + dst_pio 
            numberOfpixels = arr_dst.shape[0] * arr_dst.shape[1]
            dst_pix = np.sum(dst_cla) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
            """
            # works but not used
            
            
            print("Calculating: The area covered by resultant array (area of suitable habitat)...")            
            arr_dst.shape[0] * arr_dst.shape[1] # total number of pixels
            pix_hab = arr_dst[arr_dst > 0] # number of pixels greater then 0 (habitat)
            len(pix_hab)
            
            # calcaulte the area in hectors for the suitbale habitat
            # area = sum of pixels x (spatial res x spatial res) / 10,000 
            dst_area = len(pix_hab) * (raster_pixel_size * raster_pixel_size) / 10000
            
            
            print("Extracting the sub region name from the raster file name...")
            src_sub = os.path.basename(src_hab).split("_")[6] 
            
            print("Executing function:")
            print("...updateArea() Updating the area statement table file")    
            updateArea(df0_fil, src_sub, "2. habitat ha (post fire history)", dst_area)
    
        else:
            print(arr_hab.shape == arr_pyr.shape)
            print("Stacking arrays to have NOT the same dimensions")

print("Fin/Telos!")
        
        
        
        







### works as a fast clip but does not resample/reproject ###
"""
import os
import glob
import rasterio
import rioxarray
from shapely.geometry import box, Polygon


src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\2_SubtractAllFireHistorySpatialData"
src_pyr = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Fire\FireFreq\Final\FF_RSSA_NAFI_aa.tif"

print("Listing habitat rasters from source folder:\n", src_dir)
hab_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))

for src_hab in hab_lst:
    print("Reading habitat file: ", os.path.basename(src_hab))
    rds = rioxarray.open_rasterio(src_hab)
    
    print("Extracting the raster bounds...")
    geom = box(*rds.rio.bounds())
    shapes  = [Polygon(geom)]
    
    print("Masking the Fire Freq raster by the Habitat raster...")
    with rasterio.open(src_pyr) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta  

    print("Updating the masked raster profile...")
    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})
    
    print("Writing the clipped Pyro file to that of the Habitat raster...")
    dst_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_FireMask_30m_py")
    with rasterio.open(dst_fil + ".tif", "w", **out_meta) as dest:
        dest.write(out_image)
"""
### works as a fast clip but does not resample/reproject ###







"""                    
gdalwarp -overwrite -s_srs EPSG:3577 -t_srs EPSG:3577 -tr 100.0 100.0 -r near -of GTiff -te -1310320.0, -1018120.0, -3835320.0, -3543120.0 Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/Fire/FireFreq/Final/FF_RSSA_NAFI_aa.tif Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/RuleSet_Processing/2_SubtractAllFireHistorySpatialData/DPIRD_Rangeland_063_PreEuroVeg_006_SWD_Carnegie_100m_RngVeg_FireMask_30To100_gdalwarpGUI.tif
gdalwarp -overwrite -s_srs EPSG:3577 -t_srs EPSG:3577 -tr 100.0 100.0 -r near -of GTiff -te -1310320.0 -3543120.0 -1018120.0 -3835320.0 Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/Fire/FireFreq/Final/FF_RSSA_NAFI_aa.tif Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/RuleSet_Processing/2_SubtractAllFireHistorySpatialData/DPIRD_Rangeland_063_PreEuroVeg_006_SWD_Carnegie_100m_RngVeg_FireMask_30To100_gdalwarpGUI.tif
gdalwarp -overwrite -s_srs EPSG:3577 -t_srs EPSG:3577 -tr 100.0 100.0 -r near -of GTiff -te -3835320.0 -3543120.0 -1018120.0 -1310320.0 Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/Fire/FireFreq/Final/FF_RSSA_NAFI_aa.tif Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/RuleSet_Processing/2_SubtractAllFireHistorySpatialData/DPIRD_Rangeland_063_PreEuroVeg_006_SWD_Carnegie_100m_RngVeg_FireMask_30To100_gdalwarpGUI.tif


outputBounds=(minX, minY, maxX, maxY) in target SRS.

OutTile = gdal.Warp(OutTileName, 
                    Raster, 
                    format=RasterFormat, 
                    outputBounds=[minX, minY, maxX, maxY], 
                    dstSRS=Projection, cutlineLayer=layer, 
                    cropToCutline=True)


OutTile = None # Close dataset

gdal_translate -projwin -1310320.0 -3543120.0 -1018120.0 -3835320.0 -of GTiff Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/Fire/FireFreq/Final/FF_RSSA_NAFI_aa.tif Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/RuleSet_Processing/2_SubtractAllFireHistorySpatialData/DPIRD_Rangeland_063_PreEuroVeg_006_SWD_WesternMallee_100m_RngVeg_FireMask_gdalwarp_gui.tif
"""

"""
# worked by resample teh rngveg file only #
import os
import glob
from osgeo import gdal

src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\2_SubtractAllFireHistorySpatialData"
src_pyr = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Fire\FireFreq\Final\FF_RSSA_NAFI_aa.tif"

print("Listing habitat rasters from source folder:\n", src_dir)
hab_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))

for src_hab in hab_lst:
    print("Reading habitat file: ", os.path.basename(src_hab))   
    dst_fil = os.path.join(dst_dir, os.path.basename(src_hab)[:-4] + "_FireMask_100m_gdal" + ".tif")
    print("Reprojecting with pixel size change only...")
    ds = gdal.Warp(dst_fil, src_hab, dstSRS='EPSG:3577', outputType=gdal.GDT_Int16, xRes=100, yRes=100)
    del ds
# worked by resample teh rngveg file only #



# https://gis4programmers.wordpress.com/2017/01/06/using-gdal-to-get-raster-extent/


import os
import glob
from osgeo import gdal

src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\2_SubtractAllFireHistorySpatialData"
src_pyr = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Fire\FireFreq\Final\FF_RSSA_NAFI_aa.tif"

print("Listing habitat rasters from source folder:\n", src_dir)
hab_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))

for src_hab in hab_lst:
    print("Reading habitat file: ", os.path.basename(src_hab))  
    gdalSrc = gdal.Open(src_hab)
    print("Accessing affine transform coefficients...")
    upx, xres, xskew, upy, yskew, yres = gdalSrc.GetGeoTransform()



# worked #
import os
import glob
from osgeo import gdal

src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\2_SubtractAllFireHistorySpatialData"
src_pyr = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Fire\FireFreq\Final\FF_RSSA_NAFI_aa.tif"

print("Listing habitat rasters from source folder:\n", src_dir)
hab_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))
# https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
for src_hab in hab_lst:
    print("Reading habitat file: ", os.path.basename(src_hab))  
    src_ds = gdal.Open(src_hab)
    src_ds.RasterXSize, src_ds.RasterYSize
    src_bnd = src_ds.GetRasterBand(1)
    
    print(src_ds.GetMetadata())
    
    print("Band count: ", src_ds.RasterCount)
    for band in range( src_ds.RasterCount ):
        band += 1
        print("[ GETTING BAND ]: ", band)
        print("Accessing band info...")
        srcband = src_ds.GetRasterBand(band)
        if srcband is None:
            continue
        
        stats = srcband.GetStatistics( True, True )
        if stats is None:
            continue
        
        print("[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( stats[0], stats[1], stats[2], stats[3] ))
    del src_ds
    
# worked #    
"""


### TESTING ###
"""
import xarray
xds = xarray.open_dataarray(src_pyr)
xds_match = xarray.open_dataarray(hab_lst[0])
xds_repr_match = xds.rio.reproject_match(xds_match)
"""



### TESTING ###
"""
help(gdal.ReprojectImage)
help(gdal.Warp(destNameOrDestDS, srcDSOrSrcDSTab))
help(gdal.Warp)
help(gdal.WarpOptions())



### graham this gdal cmd looks like it clipped nicely
# do you have a pre preared gdal warp in PYTHON
gdalwarp -overwrite -s_srs EPSG:3577 -t_srs EPSG:3577 -r bilinear -tr 100 100 -te -1231660.0 -3116030.0 -832630.0 -2717000.0 -multi -of GTiff Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/RuleSet_Processing/2_SubtractAllFireHistorySpatialData/DPIRD_Rangeland_063_PreEuroVeg_006_SWD_Carnegie_100m_RngVeg_FireMask.tif Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/RuleSet_Processing/2_SubtractAllFireHistorySpatialData/DPIRD_Rangeland_063_PreEuroVeg_006_SWD_Carnegie_100m_RngVeg_FireMask_gdalTest_100m.tif


ds = gdal.Warp(dst, src, xRes=100, yRes=100, outputBounds = -1231660.0 -3116030.0 -832630.0 -2717000.0)
del ds     
    gdal.Warp()



kwargs = {'format': 'GTiff', 'geoloc': True}
ds = gdal.Warp('C:/test/MYD09.A2011093.0410.006.2015217030905.tif', 'C:/test/tel.vrt', **kwargs)
del ds

# https://stackoverflow.com/questions/48706402/python-perform-gdalwarp-in-memory-with-gdal-bindings

import gdal
ds = gdal.Warp('warp_test.tif', infile, dstSRS='EPSG:4326',
               outputType=gdal.GDT_Int16, xRes=0.00892857142857143, yRes=0.00892857142857143)
ds = None

ds = gdal.Warp('', infile, dstSRS='EPSG:4326', format='VRT',
               outputType=gdal.GDT_Int16, xRes=0.00892857142857143, yRes=0.00892857142857143)

"""
### TESTING ###



"""
print("Listing habitat rasters from source folder:\n", src_dir)
hab_lst = glob.glob(os.path.join(src_dir, "*_RngVeg.tif"))

print("Listing habitat rasters from source folder:\n", src_dir)
pyr_lst = glob.glob(os.path.join(dst_dir, "*_FireMask.tif"))


# Import libraries
import os
import rioxarray as riox
from rasterio.enums import Resampling
 
# Read raster 
raster = riox.open_rasterio(pyr_lst[0])
upscale_factor = 10
 
# Caluculate new height and width using upscale_factor
new_width = raster.rio.width * upscale_factor
new_height = raster.rio.height * upscale_factor

 
#upsample raster
up_sampled = raster.rio.reproject(raster.rio.crs, shape=(int(new_width ), int(new_height)), resampling=Resampling.bilinear)
 
print(raster.rio.resolution(), up_sampled.rio.resolution())
# ((500.0, -500.0), (250.0, -250.0))
 
print(raster.shape, up_sampled.shape)
# ((1, 2660, 2305), (1, 5320, 4610))




with rio.open(src_hab) as hab, rio.open(src_pyr) as pyr:
    # https://stackoverflow.com/questions/19984102/select-elements-of-numpy-array-via-boolean-mask-array
    
    # I assume the final raster will have the same characteristic as raster_A
    pfl_rng = hab.profile
    pfl_veg = pyr.profile
    kwds = hab.profile

    print("Reading band from the raster files (assuming 1 band (...")
    arr_hab = hab.read(1)
    arr_pyr = pyr.read(1)
   
    print("...processing Rangeland values")

    print("Stacking arrays to have the same dimensions")
        
    
    
    print(shapes.wkt)
    
    shapes = [feature["geometry"] for feature in shapefile]
    
    reprojected_raster_box = box(*rds.rio.bounds())
    
    
    rds.name = "data"
    df = rds.squeeze().to_dataframe().reset_index()
    geometry = gpd.points_from_xy(df.x, df.y)
    gdf = gpd.GeoDataFrame(df, crs=rds.rio.crs, geometry=geometry)

    # https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html
    import fiona
    import rasterio
    import rasterio.mask
    
    with fiona.open("tests/data/box.shp", "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        
    with rasterio.open(src_pyr) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

    with rasterio.open("RGB.byte.masked.tif", "w", **out_meta) as dest:
        dest.write(out_image)
"""  
    
"""
# https://stackoverflow.com/questions/71753391/mask-raster-by-extent-in-python-using-rasterio
import rasterio as rio
from osgeo import gdal
from shapely.geometry import Polygon

src = gdal.Open(src_pyr)
ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
lrx = ulx + (src.RasterXSize * xres)
lry = uly + (src.RasterYSize * yres)
geometry = [[ulx,lry], [ulx,uly], [lrx,uly], [lrx,lry]]

#roi = Polygon(geometry)
roi = [Polygon(geometry)]
output = rio.mask.mask(larger_file.tif, roi, crop = True)

print("Converting if pyro array ==  no burn, then assign habitata values, else 0...")
arr_dst = np.where(arr_pyr == 0, arr_hab, 0)
"""


    
    
    
    
"""      
try:
    print("Extracting the list of suitable habitats...")
    hab_lst = dit.loc[ (dit["item"].str.contains("rng")) & (dit["item"].str.contains("inn")) ]["list"].values[0]
    
    print("Creating a mask based on the list IN values...")
    #msk_rng = np.isin(arr_rng, dic["rng_inn"]) # msk_rng = np.isin(arr_rng, rng_shd_inn)
    msk_rng = np.isin(arr_rng, hab_lst) # msk_rng = np.isin(arr_rng, rng_shd_inn)
                
    print("Keeping values and zeros...")
    tmp_rng = np.where(msk_rng == 1, arr_rng, 0)
    
    print("Creating a mask based on the all values...")
    one_rng = np.where(arr_rng != -999, 1, -999)
    one_rng.max(), one_rng.min()
    
    print("Keeping inn values else -999...")
    fin_rng = np.where(one_rng == 1, tmp_rng, -999)
except:
    print("No rangeland values were assigned!")
    
    
    print("STEP 5: Calculating area of raster that is classified as sandlewood habitat...")
    
    
    dst_cla = np.where((dst_arr == -999) | (dst_arr == 0), 0,1) # All rangeland or veg assoc pixels = 1 else 0
    dst_cls = np.where(dst_arr > 0, 1,0)
    dst_pix = np.sum(dst_cla == 1) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
    dst_pio = np.sum(dst_cla == 0) # number of pixels with value 0 (n of pixels sans a Sandal wood habitat)
    dst_pix + dst_pio 
    numberOfpixels = dst_arr.shape[0] * dst_arr.shape[1]
        
    dst_pix = np.sum(dst_cla) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
    
    
    print("Calculating the area covered by suitable habitat...")
    # number of habitat pixels x the size of the pixel (ie 100m x 100m) / 10,000 ( to get hectors)
    # pixels x resolution (n x n ) / 10000 (to get ha)
    # 1ha = 10,000 m2  = 100 x 100m
    # eg
    # 2ha = 2 * (100 * 100) / 10000

    dst_arr.shape[0] * dst_arr.shape[1] # total number of pixels
    pix_hab = dst_arr[dst_arr > 0] # number of pixels greater then 0 (habitat)
    len(pix_hab)
    
    # calcaulte the area in hectors for the suitbale habitat
    #   area = sum of pixels x (spatial res x spatial res) / 10,000 
    dst_area = len(pix_hab) * (raster_pixel_size * raster_pixel_size) / 10000

    print("Updating the area statement table...")        
    print('Executing function: "updateArea", (pathfile, subregion, column name, area in ha)...')
    updateArea(df0_fil, sub, "1. habitat ha (initial)", dst_area)      
             
  
print("STEP 6: Writing rasters to file...")

# destination file path
dst_pth = os.path.join(dst_dir, "DPIRD_Rangeland_063_PreEuroVeg_006_SWD")

        
print("Lire a fishier...Final")

print("...RngVeg")
with rio.open(dst_pth  + "_" +  str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_RngVeg"  + ".tif", "w", **kwds) as dst:
    dst.write(dst_arr, 1)   

print("..._Class")
with rio.open(dst_pth + "_" +  str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_Class" + ".tif", "w", **kwds) as dst:
    dst.write(dst_cla, 1) 
"""