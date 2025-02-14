# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 11:24:36 2024

@author: GrahamLoewenthal
"""

### Processing steps as of:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20241126_Sandalwood_Stratification_Process_V3\20241126_Sandalwood_Stratification_Process_V3.xlsx # old version 3
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20250131_Sandalwood_Stratification_Process_V5\20250131_Sandalwood_Stratification_Process_V5.xlsx # current version 5
    
# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence:
# 1. Initial ha of potential s/wood habitat
# Subtract all fire history spatial data
# 2. Remaining ha of s/wood habitat
# Subtract 30m buffered hydrology
# 3. Remaining ha of s/wood habitat
# Subtract cleared land (use remnant vegetation layer)
# 4. Remaining ha of s/wood habitat

### 

# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence #
# Script used:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Preprocessing_RuleSet_20241223_raster.py    

# Subtract all fire history spatial data #
# Script used:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Processing_RuleSet_20241223_FireFreq_raster.py

# Subtract 30m buffered hydrology #
# Script used to greate the final stream data layer:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Preprocessing_Data_water_20241023_working_version3.py



### This script processes:
### Subtract 30m buffered hydrology ###

print("Compliling the functions for updating the area statemtns to the area statement table!")

#df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20241126_Sandalwood_Stratification_Process_V3_AreaStatements.csv" # original
#df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\Tables\20241126_Sandalwood_Stratification_Process_V3_AreaStatements.csv" # test only del
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
    

print("Defining the pixel size of the rasters...")
raster_pixel_size = 10 # only changes with caution
print("Spatial resolution of the rasters is:", raster_pixel_size)
print("100x100m equals one hector")
print("30m is the buffer width of the streams")


print("\nPROCESSING RULE SET!")

import os
import re
import glob
import pandas as pd

import numpy as np
import rasterio
import rioxarray
from osgeo import gdal


### Directories and files ###

# Source directory of files to input:
src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\2_SubtractAllFireHistorySpatialData"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\3_Subtract30mBufferedHydrology"
src_fil = r"Z:/DEC/Sandalwood_Population_Modelling/DATA/Working/Streams/Extent_IBRA/WaterNetwork_AA_diss.gpkg" # source hydro layer


print("\nDeleting xml files, so new raster as clean of turds...")
xml_lst = glob.glob(os.path.join(dst_dir, "*.xml"))
for f in xml_lst:
    print(os.path.basename(f))
    os.remove(f)



print("\nDefinign the list of IBRA sub-regions to processing by streams...") # copied from the original spread sheet for comfirmation and clarify
inc_lst = ["Eastern Murchison", "Shield", "Central", "Carnegie", "Trainor", "Lateritic Plain",] # both V3 and V5 spreadsheets identeify the same sub-regions

print("\nCleaning the habitat/SubRegion rasters list (from spreadsheet) of sub rergions for processing...")
inc_lst = [inc.replace(" ", "") for inc in inc_lst] # Remove spaces between words
inc_lst = [inc.replace("Goldfields", "Goldfield") for inc in inc_lst] # the "S" has been removed from "Goldfields", to make the script work

print("\nListing habitat/SubRegion rasters from source folder:\n", src_dir)
src_lst = glob.glob(os.path.join(src_dir, "*10m_RngVeg_Fire.tif")) # use 10m only 
for src in src_lst: print(os.path.basename(src))      
        
print("\nExcluding the rasters NOT to be processed by streams (based on sub-region...")
hab_lst = [src for src in src_lst if any(inc in src for inc in inc_lst)]

print("Rasters to be processed:")
for l in hab_lst: print(os.path.basename(l))



print("STEP 1: Lire les rasteurs, prendre le geometry, faire le rasteuristion por les riviers dans le interieur du extent, ecrire a fischer...")
print("PROCEDSSING TIME: FOR 100m resolution, ~15 minuets!")
print("PROCEDSSING TIME: FOR 10m resolution, ~ onme every 5 minues")


### GRAHAM YOU SHOUDL TEST RUN THE RASTERISING USING THESE TWO LINES (NOT TESTED AS OF 08/01/2025)
# https://gdal.org/en/stable/user/configoptions.html
gdal.SetCacheMax(2048000000)
gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')


print("Looping through the subregions top extract the raster extents:")
for src_hab in hab_lst:
    print("\nReading habitat file:\n", os.path.basename(src_hab))
    
    # Destaination file
    dst_fil = os.path.join(dst_dir, "Streams_" + os.path.basename(src_hab).split("_")[6] + "_" + str(raster_pixel_size) + "m")
    with rioxarray.open_rasterio(src_hab) as rds:
        print("Extracting the raster bounds...")
        bbox = rds.rio.bounds()
        
    print("Rasterising...")
    ds = gdal.Rasterize(dst_fil + ".tif", src_fil, 
                   format='GTIFF', outputType=gdal.GDT_Byte, creationOptions=["COMPRESS=DEFLATE"], 
                   #outputBounds=bbox, noData=-999, initValues=-999, # (Stream_Trainor_10m.tif was failing with a zip read error)
                   outputBounds=bbox, noData=None, 
                   xRes = raster_pixel_size, yRes = -raster_pixel_size,
                   allTouched=True, burnValues=1)
    
    # Destaination file
    dst_fil = os.path.join(dst_dir, "Streams_" + os.path.basename(src_hab).split("_")[6] + "_" + str(raster_pixel_size) + "m")
    
    print("Writing as : ", os.path.basename(dst_fil))    
    del ds 

print("STEP 1: Fin/Telos!")


print("STEP 2: Removing habitat where there NOT intersecting with stream (overlaying stream buffer with habitat layer)...")

print("Using the prepared habitat list 'hab_lst' ...")

print("Listing stream rasters from destination folder:\n", dst_dir)
hyd_lst = glob.glob(os.path.join(dst_dir, "Streams_*10m.tif")) # check for resolution values in teh name

sorted(hab_lst)
sorted(hyd_lst)


len(hab_lst), len(hyd_lst)

print("\nHabitat layers")
for h in hab_lst: print(os.path.basename(h))
print("\nHdro layers")
for y in hyd_lst: print(os.path.basename(y))



print("\nLooping through the habitat and stream clipped layers together...")
for src_hab, src_hyd in zip(sorted(hab_lst), sorted(hyd_lst)):
    
    print("\nOpening: \n", os.path.basename(src_hab), "\n", os.path.basename(src_hyd), "\n")
    
    with rasterio.open(src_hab) as hab, rasterio.open(src_hyd) as hyd:
        # https://stackoverflow.com/questions/19984102/select-elements-of-numpy-array-via-boolean-mask-array
        
        # I assume the final raster will have the same characteristic as raster_A
        pfl_hab = hab.profile
        pfl_hyd = hyd.profile
        kwds = hab.profile
    
        print("Reading the bands from the two rasters...")
        arr_hab = hab.read(1)
        arr_hyd = hyd.read(1)
       
        print("Are the two arrays of the same shape?")
        if arr_hab.shape == arr_hyd.shape: 
            print(arr_hab.shape == arr_hyd.shape)
            print("...processing values")
            
            print("Converting if hydo array ==  no burn, then assign habitat values, else 0...")
            arr_tmp = np.where(arr_hyd == 1, arr_hab, 0)
            arr_dst = np.where(arr_hab == -999, -999, arr_tmp)
                        
            print("Writing the clipped hydo file to that of the Habitat raster...")
            #tmp_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_StreamsTemp")
            dst_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_Streams")
            
            #with rasterio.open(tmp_fil + ".tif", "w", **kwds) as dest:
            #    dest.write(arr_tmp, 1)            
            
            with rasterio.open(dst_fil + ".tif", "w", **kwds) as dest:
                dest.write(arr_dst, 1)
            
            print("Calculating area of raster that is classified as sandlewood habitat...")
            
            # works but not used #
            """
            dst_cls = np.where(arr_dst > 0, 1,0)
            dst_pix = np.sum(dst_cla == 1) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
            dst_pio = np.sum(dst_cla == 0) # number of pixels with value 0 (n of pixels sans a Sandal wood habitat)
            dst_pix + dst_pio 
            numberOfpixels = arr_dst.shape[0] * arr_dst.shape[1]
            dst_pix = np.sum(dst_cla) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
            """
            
            print("Calculating the area covered by suitable habitat...")            
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
            updateArea(df0_fil, src_sub, "3. habitat ha (post buff hydrology)", dst_area)
    
        else:
            print(arr_hab.shape == arr_hyd.shape)
            print("Stacking arrays to have NOT the same dimensions")

print("Fin/Telos!")
































