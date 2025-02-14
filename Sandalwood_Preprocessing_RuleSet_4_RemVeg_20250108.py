# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:04:49 2024

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
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Preprocessing_RuleSet_20241223_1_Vegetation.py  

# Subtract all fire history spatial data #
# Script used:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Preprocessing_RuleSet_20241227_2_FireFreq.py

# Subtract 30m buffered hydrology #
# Script used:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Tools\Sandalwood_Preprocessing_RuleSet_20241230_3_Streams.py

### This script processes:
### Subtract cleared land (use remnant vegetation layer) ###


### WARNING: FOR THE VERSION 5 (v5) SPREADSHEET, "20250131_Sandalwood_Stratification_Process_V5.xlsx"
### WARNING: PROCESSING "3. Remaining ha of s/wood habitat " IS NOT REQUIRED AND HAS BEEN STATED AS "N/A"

### THUS DO NOT RUN THIS SCRIPT FOR VERSION 5
### GRAHAM LOEWENTHAL (14/02/2025)



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
    #r = re.findall('([A-Z][a-z]+)', src_sub)
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


import os
import re
import glob
import pandas as pd
import geopandas as gpd
#from shapely import box, Polygon

import numpy as np
import rasterio
import rioxarray
from osgeo import gdal


### Directories and files ###

# Source directory of files to input:

# original keep    
src_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\4_SubtractClearedLand"
rem_fil = r"V:\GIS1-Corporate\Data\GDB\Vegetation\CPT_REMVEG_STATE.gdb" # layername=CPT_REMVEG_STATE # source dept Remnant vegetation layer
sub_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Mask_definition\SWD_subIBRAs_diss.shp"


print("Deleting xml files, so new raster as clean of turds...")
xml_lst = glob.glob(os.path.join(dst_dir, "*.xml"))
for f in xml_lst:
    print(os.path.basename(f))
    os.remove(f)


print("Definign the list of IBRA sub-regions to processing by RemVeg...") # copied from the original spread sheet for comfirmation and clarify
inc_lst = [
"Geraldton Hills", # (below pastoral lease boundary)
"Merredin",
"Katanning",
"Western Mallee",
"Eastern Mallee",]


### DO NOT RUN THIS TOO OFTEN, AS IT IS BIG AND TAKES A WHILE TO READ!!! ###

print("STEP 0: Clip the dept's RemVeg layer to the IBRA sub-regions then reproject.")

print("Lier le fichier seulement dans le region du bounds...")
sub_gdf = gpd.read_file(sub_fil) 

for inc in inc_lst:
    print("Sub-region:", inc)

    print("Extracting the total_bounds of the sub-region row...")
    geom = sub_gdf[sub_gdf["SUB_NAME_7"] == inc]["geometry"].total_bounds # extent of the area
    edge = sub_gdf[sub_gdf["SUB_NAME_7"] == inc]["geometry"] # the actual geometry of the shape
    
    #shape = tuple(geom) # used by gdal
    print("Total_bounds as a list...")
    extent = list(geom) # used by geopandas

    print("Lire le fichier seulement que intersects au region du bounds...")
    rem_gdf = gpd.read_file(rem_fil, layer='CPT_REMVEG_STATE', bbox=(extent)) 
    
    print("Clipping the remVeg to the sub region extent...")
    clp_gdf = gpd.clip(rem_gdf, edge)

    print("Reprojet le gdf a Albers...")
    clp_gdf = clp_gdf.to_crs(3577)

    # Destination file variables
    dst_lyr = inc.replace(" ", "")
    dst_fil = os.path.join(dst_dir, "RemVeg_" + dst_lyr)
    print("Ecrire a fichier...")
    clp_gdf.to_file(dst_fil + ".gpkg", driver='GPKG', layer = dst_lyr) 

print("STEP 0: Fin/Telos!")



print("STEP 1: From the inclusion list of sub regions to process, \
      select the RngVeg rasters & RemVeg vectors that are from those sub regions \
          then rasterise the RemVeg vectors by bounds of the RngVeg rasters!")



print("Cleaning the habitat/SubRegion INCLUDSION LIST (from spreadsheet) of sub rergions for processing...")
inc_lst = [inc.replace(" ", "") for inc in inc_lst] # Remove spaces between words
inc_lst = [inc.replace("Goldfields", "Goldfield") for inc in inc_lst] # the "S" has been removed from "Goldfields", to make the script work



### THERE IS AN ISSUES WITH GERALDDTON HILLS
## Geraldton Hills (above pastoral lease boundary)
# This would have been processedby substruction of fire freq, thus located in \2_SubtractAllFireHistorySpatialData\
## Geraldton Hills (below pastoral lease boundary)
# This would NOT have been processedby substruction of fire freq, thus located in \1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence\
    
### Currently, only MErredin and Western Mallee have suitablility id assigned to them, so only these are to be processed.


print("Listing habitat/SubRegion RASTERS from source folder:\n", src_dir)
src_lst = glob.glob(os.path.join(src_dir, "*_10m_RngVeg.tif")) # use "SansFireMask", as this is the correct output
for src in src_lst: print(os.path.basename(src))      
        
print("Excluding the RASTERS NOT to be processed by rem veg (based on sub-region...")
hab_lst = [src for src in src_lst if any(inc in src for inc in inc_lst)]
for hab in hab_lst: print(os.path.basename(hab))


#print("Listing RemVeg/SubRegion VECTORS from RemVeg folder:\n", dst_dir)
#rem_lst = glob.glob(os.path.join(dst_dir, "*.gpkg")) # use "SansFireMask", as this is the correct output
#for rem in rem_lst: print(os.path.basename(rem))      

#print("Excluding the VESTORS NOT to be processed by rem veg (based on sub-region...")
#rem_lst = [rem for rem in rem_lst if any(inc in src for inc in inc_lst)]
#for l in rem_lst: print(os.path.basename(l))

### GRAHAM YOU SHOUDL TEST RUN THE RASTERISING USING THESE TWO LINES (NOT TESTED AS OF 08/01/2025)
# https://gdal.org/en/stable/user/configoptions.html
gdal.SetCacheMax(2048000000)
gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')

print("Listing RemVeg/SubRegion vectors from RemVeg folder:\n", dst_dir)
vec_lst = glob.glob(os.path.join(dst_dir, "*.gpkg"))

print("Looping from the included habitat (RngVeg) RASTER files...")
for hab_fil in hab_lst:
    
    print("\n" + os.path.basename(hab_fil))
    
    print("Extracting the sub name from the raster file...")
    sub_nom = os.path.basename(hab_fil).split("_")[6]
    print(sub_nom)
    
    print("From the sub name of the raster file, select the corresponding vector file to be rasterised...")
    vec_fil = ''.join([i for i in vec_lst if sub_nom in i])
    print(os.path.basename(vec_fil))
    
    print("Destination file name:")
    dst_fil = os.path.splitext(vec_fil)[0] + "_" + str(raster_pixel_size) + "m"
    print(dst_fil)

    print("Reading the Habitata RngVeg raster...")
    with rioxarray.open_rasterio(hab_fil) as rds:
        print("Extracting the raster bounds...")
        bbox = rds.rio.bounds()

    print("Rasterising the vector by the raster bounds...")
    ds = gdal.Rasterize(dst_fil + ".tif", vec_fil, 
                   format='GTIFF', outputType=gdal.GDT_Byte, 
                   creationOptions=["COMPRESS=DEFLATE"], 
                   #creationOptions=['GDAL_NUM_THREADS = ALL_CPUS'],
                   #creationOptions=['SetCacheMax = 2048000000'],
                   outputBounds=bbox, noData=-999, initValues=-999, 
                   xRes = raster_pixel_size, yRes = -raster_pixel_size,
                   allTouched=True, burnValues=1)
    print("Writing to file...")
    del ds





print("STEP 2: Removing habitat where there NOT intersecting with RemVeg (overlaying RemVeg with habitat layer)...")

print("Using the prepared habitat list 'hab_lst' ...")

print("Listing RemVeg rasters from destination folder:\n", dst_dir)
rem_lst = glob.glob(os.path.join(dst_dir, "RemVeg_*_10M.tif"))

sorted(hab_lst)
sorted(rem_lst)



len(hab_lst), len(rem_lst)

print("Looping through the RemVeg and RngVeg rasters to exclude non-RemVeg from the suitable habiat, then calc area...")
for src_hab, src_rem in zip(sorted(hab_lst), sorted(rem_lst)):
    
    print("\n\nOpening: \n", os.path.basename(src_hab), "\n", os.path.basename(src_rem), "\n")
    
    with rasterio.open(src_hab) as hab, rasterio.open(src_rem) as rem:
        # https://stackoverflow.com/questions/19984102/select-elements-of-numpy-array-via-boolean-mask-array
        
        # I assume the final raster will have the same characteristic as raster_A
        pfl_hab = hab.profile
        pfl_rem = rem.profile
        kwds = hab.profile
    
        print("Reading the bands from the two rasters...")
        print("...rasteur un")
        arr_hab = hab.read(1)
        print("...rasteur deux")
        arr_rem = rem.read(1)
       
        print("Est-que les deux arrays sont memes schemes?")
        if arr_hab.shape == arr_rem.shape: 
            print(arr_hab.shape == arr_rem.shape)
            print("...processing habitat values")
            
            print("Converting: if RemVeg array ==  1, then assign habitat values, else 0...")
            arr_tmp = np.where(arr_rem == 1, arr_hab, 0)
            arr_dst = np.where(arr_hab == -999, -999, arr_tmp)
                        
            print("Writing the clipped Habitat raster to file...")
            #tmp_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_StreamsTemp")
            dst_fil = os.path.join(dst_dir,  os.path.splitext(os.path.basename(src_hab))[0] + "_RemVeg")
            
            #with rasterio.open(tmp_fil + ".tif", "w", **kwds) as dest:
            #    dest.write(arr_tmp, 1)            
            
            with rasterio.open(dst_fil + ".tif", "w", **kwds) as dest:
                dest.write(arr_dst, 1)
            
            print("STEP 3: Calculating area of raster that is classified as sandlewood habitat...")
            
            # works but not used #
            """
            dst_cls = np.where(arr_dst > 0, 1,0)
            dst_pix = np.sum(dst_cla == 1) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
            dst_pio = np.sum(dst_cla == 0) # number of pixels with value 0 (n of pixels sans a Sandal wood habitat)
            dst_pix + dst_pio 
            numberOfpixels = arr_dst.shape[0] * arr_dst.shape[1]
            dst_pix = np.sum(dst_cla) # number of pixels with value 1 (n of pixels with a Sandal wood habitat)
            """

            print("Calculating the area covered by Suitable habitat before clipping with RemVeg...")
            hab_tot = arr_hab.shape[0] * arr_hab.shape[1] # total number of pixels
            hab_oui = arr_hab[arr_hab > 0] # number of pixels greater then 0 (habitat)
            hab_non = arr_hab[arr_hab < 1] # number of pixels less then 1 (sans habitat)
            hab_tot == len(hab_oui) + len(hab_non) # sanity check
            
            hab_area = len(hab_oui) * (raster_pixel_size * raster_pixel_size) / 10000 # calculate hectorage of habitat
        

            print("Calculating the area covered by RemVeg...")
            rem_tot = arr_rem.shape[0] * arr_rem.shape[1] # total number of pixels
            rem_oui = arr_rem[arr_rem > 0] # number of pixels greater then 0 (RemVeg)
            rem_non = arr_rem[arr_rem < 1] # number of pixels less then 1 (sans RemVeg)
            rem_tot == len(rem_oui) + len(rem_non) # sanity check
            
            rem_area = len(rem_oui) * (raster_pixel_size * raster_pixel_size) / 10000 # calculate hectorage of RemVege

            
            print("Calculating the area covered by suitable habitat after clipped by RemVeg...")            
            dst_tot = arr_dst.shape[0] * arr_dst.shape[1] # total number of pixels
            dst_oui = arr_dst[arr_dst > 0] # number of pixels greater then 0 (habitat with RemVeg)
            dst_non = arr_dst[arr_dst < 1] # number of pixels less then 1 (habitat sans RemVeg)
            dst_tot == len(dst_oui) + len(dst_non) # sanity check
            
            # calcaulte the area in hectors for the suitbale habitat
            # area = sum of pixels x (spatial res x spatial res) / 10,000 
            dst_area = len(dst_oui) * (raster_pixel_size * raster_pixel_size) / 10000
            
            print(hab_area, "Suitable Habitat area", )  
            print(rem_area, "RemVeg area") 
            print(dst_area, "Suitable Habitat only where is RemVeg area") 
            
            if len(hab_oui) > len(dst_oui):
                print("There is an expected reduction of suitable habitat after clipped by RemVeg!")
            else:
                print("WARNING: There is NOT a expected reduction of suitable habitat after clipped by RemVeg!")
                print("REVIEW the files for sub-region: ", os.path.basename(src_hab).split("_")[6])
            
            
            print("Updating the area statement table...")        
            
            print("Extracting the sub region name from the raster file name...")
            src_sub = os.path.basename(src_hab).split("_")[6] 
            
            print("Executing function:")
            #print("...findUpperCase() Checking for camelCase strings")
            #dst_sub = findUpperCase(src_sub)
            
            print("...updateArea() Updating the area statement table file")    
            #updateArea(df0_fil, dst_sub , "4. habitat ha (post land cleared )", dst_area)
            updateArea(df0_fil, src_sub , "4. habitat ha (post land cleared )", dst_area)
    
        else:
            print("Stacking arrays to have NOT the same dimensions")

print("Fin/Telos!")
















"""
GRAHAM write the intersetion betweent he rastesrs, roughly""
 
print("Converting if hydo array ==  no burn, then assign habitata values, else 0...")
arr_tmp = np.where(arr_hyd == 1, arr_hab, 0)
arr_dst = np.where(arr_hab == -999, -999, arr_tmp)
"""

#graham loewenthal
# 30/12/2024
                


