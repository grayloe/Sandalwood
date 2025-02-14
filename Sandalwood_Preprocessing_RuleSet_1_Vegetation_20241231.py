# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:26:42 2024

@author: GrahamLoewenthal
"""


### Processing steps as of:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20241126_Sandalwood_Stratification_Process_V3\20241126_Sandalwood_Stratification_Process_V3.xlsx
    
# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence:
# 1. Initial ha of potential s/wood habitat
# Subtract all fire history spatial data
# 2. Remaining ha of s/wood habitat
# Subtract 30m buffered hydrology
# 3. Remaining ha of s/wood habitat
# Subtract cleared land (use remnant vegetation layer)
# 4. Remaining ha of s/wood habitat

### 


### This script processes:
### Subtract Land Systems or Vegetation Asspociations with low probability of occurrence: ###



# As per spreadsheet tab "Rule Set"*, only the follow are to be filtered by Land Systems (rng) or Vegetation Associations (veg): 
#Eastern Goldfields
#Southern Cross
#Mardabilla
#Eastern Murchison
#Shield
#Central
#Carnegie
#Trainor
#Lateritic Plain
#Murchison
#Edel
#Geraldton Hills (above pastoral lease boundary)
#Geraldton Hills (below pastoral lease boundary)
#Merredin
#Katanning
#Western Mallee
#Eastern Mallee    
# *Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\220250131_Sandalwood_Stratification_Process_V5\20250131_Sandalwood_Stratification_Process_V5.xlsx




import os
import glob
import fiona
import pandas as pd
import geopandas as gpd


print("\nSTEP i: Creating an empty dataFrame for area statements...\n")

### Producing ha area stattemtns is required after each processing step of the "rule-set"
### The rule set is on the first tab of the above .xlsx

# PathFile of the the dataframe
#df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20241126_Sandalwood_Stratification_Process_V3_AreaStatements.csv" # original
#df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\Tables\20241126_Sandalwood_Stratification_Process_V3_AreaStatements.csv" # test onlly del
df0_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20250131_Sandalwood_Stratification_Process_V5_AreaStatements.csv" # CURRENT V5


def createAreaStatementeTable(filePath):
    # Faire
        
    # If exists, do not re-create, else create
    if os.path.exists(filePath):
        print("Fichier deje existe, faire de rien!")
    else:
        print("Fichier pas existe, faire un neuvel table!")
        
        #list of columns for the empty dataframe
        pd0_col_lst = ["Subregion", "1. habitat ha (initial)", "2. habitat ha (post fire history)",
                       "3. habitat ha (post buff hydrology)", "4. habitat ha (post land cleared )",]
        
        # Creating the empty dataframe
        df0_area = pd.DataFrame(columns = pd0_col_lst)
        #df0_area = df0_area.set_index('id')
        
        print("Likre a fishier...")
        df0_area.to_csv(filePath, index=False) 
    return

print('Executing function "createAreaStatementeTable" - which creates an area Statement table')
createAreaStatementeTable(df0_fil)


print("The function for updating the area statemtns to the area statement table!")
def updateArea(pathfile, subregion , column, areaValue):
    """Update the area statement table for each processing step."""
    # Faire
    
    df0_area = pd.read_csv(pathfile)
    df0_area.loc[len(df0_area), ("Subregion", column)] = [subregion, areaValue]
    print("Lire a fishier...")
    df0_area.to_csv(pathfile, index=False) 
    return

print("\n")
print("Defining the pixel size of the rasters...")
raster_pixel_size = 10 # only changes with caution
print("Spatial resolution of the rasters is:", raster_pixel_size)
print("100x100m equals one hector")
print("30m is the buffer width of the streams")   
print("\n")    

print("\nSTEP ii: Reading source data...\n")
# Direcories and files    

print("Reading the IBRA sub-regions vector...")
sub_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Mask_definition\SWD_subIBRAs_diss.shp"
sub_gdf = gpd.read_file(sub_fil)

print("Reading the rangelands vector...")
rng_fil = r"Z:\DEC\Sandalwood_Population_Modelling\PRODUCTS\20241016_Vegetation_Landsystem_mapping\Rangelands_DPIRD_063_Landsystems_SWD.shp"
sys_gdf = gpd.read_file(rng_fil) 

print("Reading the veg associations vector...")
veg_fil = r"Z:\DEC\Sandalwood_Population_Modelling\PRODUCTS\20241016_Vegetation_Landsystem_mapping\Pre_European_Vegetation_DPIRD_006_extraAttrib_SWD.shp"
veg_gdf = gpd.read_file(veg_fil) 

print("Reading the spreadsheet...")
#xls_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20241126_Sandalwood_Stratification_Process_V3\20241126_Sandalwood_Stratification_Process_V3.xlsx" # original V3
xls_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20250131_Sandalwood_Stratification_Process_V5\20250131_Sandalwood_Stratification_Process_V5.xlsx" # original V5

xls_obj = pd.ExcelFile(xls_fil)
tmp_lst = xls_obj.sheet_names # Get the list of sheet names
print(tmp_lst) # Print the sheet names


print("Reading the list of sub-regions of interest...")
# Mannual: list of the sub ibra that area being used in the Sandelwood processing based on "20250131_Sandalwood_Stratification_Process_V5.xlsx"
inc_lst = ['Eastern Goldfield', 'Southern Cross ', 'Mardabilla', 
           'Eastern Murchison', 'Shield', 'Central', 
           'Carnegie', 'Trainor', 'Lateritic Plain',]

print("Excluding the sub-regions NOT to be processed...")
xls_lst = [tmp for tmp in tmp_lst if any(inc in tmp for inc in inc_lst)]
print(xls_lst)

print("\nSTEP iii: Defining destination directories...\n")

# Destination directory

# original keep
wrk_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing"
dst_dir = os.path.join(wrk_dir, "1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence")
#dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"

# test delete
#wrk_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted"
#dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence"


print("Creating directories for the processing...")
fol_lst = ["1_SubtractLandSystemsOrVegAssocWithLowProbOfOccurrence", "2_SubtractAllFireHistorySpatialData",
           "3_Subtract30mBufferedHydrology","4_SubtractClearedLand",]

for fol in fol_lst:
    print(fol)
    if os.path.exists(os.path.join(wrk_dir, fol)):
        print("Existe!")
    else:
        print("Pas Existe!")
        os.makedirs(os.path.join(wrk_dir, fol))


print("Defining the destination file paths...")
dst_fil_rng = os.path.join(dst_dir, os.path.basename(rng_fil)[:-4])
dst_fil_veg = os.path.join(dst_dir, os.path.basename(veg_fil)[:-4])
### dst_fil_clp = os.path.join(dst_dir,"DPIRD_Rangeland_063_PreEuroVeg_006_SWD")
    


print("\nSTEP 1: Clipping rangelands and vegetation associations by sub-region...\n")

# Getting list of sub ibra region names
sub_lst = sub_gdf["SUB_NAME_7"].tolist()  
#sub_lst = ['Shield', 'Eastern Murchison', 'Carnegie']


# GRAHAM ONLY REQUIREMENTS FOR V3 spreadsheet, if V5 works, delete this, it is silly and confusing
# list of the sub ibra regions that area being used in the Sandelwood processing
"""
sub_lst = ['Eastern Murchison', 'Southern Cross', 'Eastern Goldfield', 
           'Shield', 'Central', 'Carnegie', 'Trainor', 'Lateritic Plain', 
           'Mardabilla', 'Tallering', 'Merredin', 'Western Mallee', 'Edel',]

src_lst = [
"Eastern Goldfields",
"Southern Cross",
"Mardabilla",
"Eastern Murchison",
"Shield",
"Central",
"Carnegie",
"Trainor",
"Lateritic Plain",
"Murchison",
"Edel",
"Geraldton Hills", # (above pastoral lease boundary)
"Geraldton Hills", # (below pastoral lease boundary)
"Merredin",
"Katanning",
"Western Mallee",
"Eastern Mallee",]

print("Cleaning the SubRegion list (from spreadsheet) of sub rergions for processing...")
#src_lst = [sub.replace(" ", "") for sub in src_lst] # Remove spaces between words
src_lst = [src.replace("Goldfields", "Goldfield") for src in src_lst] # the "S" has been removed from "Goldfields", to make the script work
del src_lst[11] # hard coded deletion of the second "GeraldtonHills"

print("List of sub regions that have a suitability defined") # EXCLUDING "TALLERING"
inc_lst = ['Eastern Murchison', 'Southern Cross', 'Eastern Goldfield', 
           'Shield', 'Central', 'Carnegie', 'Trainor', 'Lateritic Plain', 
           'Mardabilla', 'Tallering', 'Merredin', 'Western Mallee', 'Edel',]

print("Excluding the rasters NOT to be processed by fire frequency (based on sub-region...")
sub_lst = [src for src in src_lst if any(inc in src for inc in inc_lst)]
"""

print("Cleaning the SubRegion list (from spreadsheet) of sub rergions for processing...")
sub_lst = [inc.replace("Cross ", "Cross") for inc in inc_lst] # Remove spaces between words
print(sub_lst)



print("Looping through the IBRA sub-region boundaries...")
for sub_cod in sub_lst:
    print("\n", sub_cod)
    sub_row = sub_gdf[sub_gdf["SUB_NAME_7"] == sub_cod]
    print(sub_row )
    
    print("Clipping...")
    print("...", os.path.basename(rng_fil))
    rng_clp = sys_gdf.clip(sub_row)
    
    print("...", os.path.basename(veg_fil))
    veg_clp = veg_gdf.clip(sub_row)
    if veg_clp.empty: print('DataFrame is empty!')


    print("Writting to file...")
    print("...", os.path.basename(rng_fil)[:-4], sub_cod)
    if not rng_clp.empty:
        rng_clp.to_file(dst_fil_rng  + ".gpkg", layer= sub_cod, driver="GPKG")
    else:
        print('DataFrame is empty!')
    
    print("Writting to file...")
    print("...", os.path.basename(veg_fil)[:-4], sub_cod)
    if not veg_clp.empty:
        print("Writting to file...")
        print("...", os.path.basename(veg_fil)[:-4], sub_cod)
        veg_clp.to_file(dst_fil_veg  + ".gpkg", layer= sub_cod, driver="GPKG")
    else:
        print('DataFrame is empty!')
    


print("\nSTEP 2: Rasterising the rangland and veg assopc vectors  by sub-IBRA extents...\n")

# rasteise the vector
import math
import rasterio
from rasterio.features import rasterize
#from rasterio.transform import from_bounds

print('PRE-READING FUNTION: "gdf2raster"')
def gdf2raster(gdf, sub, fil, col, box, pixel_size):
    """For a given extent of a sub-IBRA region, raseteise either the rangeland or veg assoc vector."""
    
    print("Calcuating the spatial parameters for rasterising the vector...")
    geom_value = ((geom,value) for geom, value in zip(gdf.geometry, gdf[col]))    # Calculating the geometry and values
    min_x, min_y, max_x, max_y = box['geometry'].total_bounds.round(-1) # Calculating the xy coordinates # teh extent is too far south
    print(min_x, min_y, max_x, max_y)
    
    # USER INPUT # Calculating the transform and determining the pixel size 
    # pixel_size = 100
    
    print("Calcuclating the transform...")
    # rasterio.transform.from_origin() "Return an Affine transformation given upper left and pixel sizes", so...
    # Adjusting the top and left coords to the centroid coords (a shift of 0.5m)
    transform = rasterio.transform.from_origin(west=min_x + pixel_size / 2, north=max_y + pixel_size / 2, xsize=pixel_size, ysize=pixel_size)
    
    w_px = math.ceil((max_x - min_x) / pixel_size)                                  # Calculating the height and width of the output raster (in pixels)
    h_px = math.ceil((max_y - min_y) / pixel_size)
    
    # Get the larger of the shape dimensions
    if w_px < h_px: shape = h_px, h_px
    else: shape = w_px, w_px
    
    # Change the GDAL defaul config to speed up this slow part of theprocessing from 30x2 to 20 + 10sec
    with rasterio.Env(GDAL_CACHEMAX=2048000000, GDAL_NUM_THREADS="ALL_CPUS"):
        #1st confidg for rasterize(), 2nd config for writing to file
    
        print("Rasterising the vector... (~20 sec)")
        image = rasterize(
            geom_value,
            out_shape = shape,
            #out_shape = [w_px, h_px],
            transform = transform,
            all_touched = True,
            fill = -999)
        
        #print("Writing the raster to file... (~ 12 sec)")
        #dst_crs = str(src_gdf.crs).split(":")[1] # The CRS of the gdf2 as a EPSG string
        #spt_res = (str(int(pixel_size)) + "m") # The resolution of the rasterised data
               
        print("Writing raster to file...")
        #dst_rst = os.path.join(rst_dir, dst_nom) # full path for vector files   
        dst_rst = fil + "_" + sub.replace(" ", "") + "_" + str(round(pixel_size)) +"m"
        with rasterio.open(dst_rst + ".tif", 'w',
            driver='GTiff',
            dtype=rasterio.float32,
            count=1,
            compress='lzw',
            crs= gdf.crs,
            width=shape[0],
            height=shape[1],
            transform=transform,
            nodata=-999
        ) as dst:
            dst.write(image, indexes=1)
    
    return dst



print("\nSTEP 3: Rasterise the rangeland and veg assoc vectors by IBRA sub-region...\n")

print("Listing the layers in the geopackages...")

#gpd.list_layers(dst_fil_veg + ".gpkg")
print("\n Rangeland layers...")
for layername in fiona.listlayers(dst_fil_rng + ".gpkg"): print(layername)
rng_lst_gpkg = fiona.listlayers(dst_fil_rng + ".gpkg")

print("\n Veg assoc layers...")
for layername in fiona.listlayers(dst_fil_veg + ".gpkg"): print(layername)
veg_lst_gpkg = fiona.listlayers(dst_fil_veg + ".gpkg")

print("Reading the IBRA sub-regions vector...")
# ALREADY READ IN 
#sub_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\Mask_definition\SWD_subIBRAs_diss.shp"
#sub_gdf = gpd.read_file(sub_fil)

print("Re-projecting Sub region geodataframe to crs 3577 for raster processing...")
sub_gdf.crs
sub_gdf.to_crs(3577, inplace = True)
sub_gdf.crs

print("Re-defining the list of IBRA sub-regions to process...")
# NO NEED TO RE_DEFINE THIS
#sub_lst = ['Eastern Murchison', 'Southern Cross', 'Eastern Goldfield', 'Shield', 'Central', 'Carnegie', 
#           'Trainor', 'Lateritic Plain', 'Mardabilla', 'Tallering', 'Merredin',  'Western Mallee', 'Edel',]

#sub_lst = ['Eastern Murchison', 'Shield', 'Carnegie',]


print("Deleting xml files, so new raster as clean of turds...")
xml_lst = glob.glob(os.path.join(dst_dir, "*.xml"))
for f in xml_lst:
    print(os.path.basename(f))
    os.remove(f)


print("Rasterising vectors, by looping through the sub IBRA regions...")
for sub_cod in sub_lst:
    print("\n", sub_cod)
    sub_row = sub_gdf[sub_gdf["SUB_NAME_7"] == sub_cod]

    print("\nReading the vector rangelands...")
    try:
        rng_gdf = gpd.read_file(dst_fil_rng + ".gpkg", layer=str(sub_cod)) # , layer='Shield')
        rng_gdf.columns
        print("Re-projecting to crs 3577...")
        rng_gdf.crs
        rng_gdf.to_crs(3577, inplace = True)

        print("Executing the rasterisation of the gdf vectors by sub-IBRA region")
        dst = gdf2raster(rng_gdf, str(sub_cod) , dst_fil_rng, 'mu_id', sub_row, raster_pixel_size)  
        
    except Exception as error:
        print("\n", error)
    
    
    try:
        print("\nReading the vector veg assoc...")
        veg_gdf = gpd.read_file(dst_fil_veg + ".gpkg", layer=str(sub_cod)) # , layer='Shield')
        veg_gdf.columns
        print("Re-projecting to crs 3577...")
        veg_gdf.crs
        veg_gdf.to_crs(3577, inplace = True)
        
        print("Executing the rasterisation of the gdf vectors by sub-IBRA region")
        dst = gdf2raster(veg_gdf, str(sub_cod) , dst_fil_veg, 'veg_assoc', sub_row, raster_pixel_size)
        
    except Exception as error:
        print("\n", error)
    

            
    



print("\nSTEP 4: For each rangeland and vector raster, assign pixels either IN or OUT, \
      then proioritising the rangeland raster or the veg assoc raster...\n")

import os
import glob
import rasterio as rio
import numpy as np 
#from numpy import ma


print("Reading the sandalwood habitat suitability table...")

# PathFile of the the dataframe
#tbl_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20241126_Sandalwood_Stratification_Process_V3_Prepared.csv" # original keep
#tbl_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\Tables\20241126_Sandalwood_Stratification_Process_V3_Prepared.csv" # test delete
tbl_fil = os.path.join(wrk_dir, "Tables" , os.path.basename(os.path.splitext(xls_fil)[0]) + "_Prepared.csv") # v5 version

# Reading the file
#tbl_df0 = pd.read_csv(tbl_fil)
tbl_df0 = pd.read_csv(tbl_fil, converters={'list': pd.eval}) # pd.eval to read the lists as a list not a s a string


#print("Extracting the list of suitable habitats...")
#hab_lst = tbl_df0[tbl_df0["item"] == "rng_emr_inn"]["list"].values[0]


print("ON THE VM, AT 10M RESOLUTION, THIS RASTER CREATION IS SLOW, UP TO 5 MINS PER RASTER!")
print("Looping though the rangeland and veg assooc rasters, by sub region...\n")
for sub in sub_lst:
#for sub in sub_lst[-2:-1]:
    sub = sub.replace(" ", "")
    print("\nProcessing: ",sub, "\n")

    rst_rng = "".join(glob.glob(os.path.join(dst_dir, "Rangeland" + "*" + sub + "_" + str(raster_pixel_size) + "m" + ".tif")))
    rst_veg = "".join(glob.glob(os.path.join(dst_dir, "Pre_European_Vegetation" + "*" + sub + "_" + str(raster_pixel_size) + "m" + ".tif")))
    print(os.path.basename(rst_rng), "\n", os.path.basename(rst_veg))

    # get the distionary that relates to the sub varable,
    dic = {}
    if sub == 'EasternMurchison': # if sub == 'Eastern Murchison':
        #dic = dic_emr
        dit = tbl_df0[tbl_df0["item"].str.contains("emr")] 
    elif sub == 'SouthernCross': # elif sub == 'Southern Cross':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("scs")] 
    elif sub == 'EasternGoldfield': #elif sub == 'Eastern Goldfield':
        #dic = dic_car
        dit = tbl_df0[tbl_df0["item"].str.contains("egf")] 
    elif sub == 'Shield':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("shd")] 
    elif sub == 'Central':
        #dic = dic_car
        dit = tbl_df0[tbl_df0["item"].str.contains("ctr")]       
    elif sub == 'Carnegie':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("car")] 
    elif sub == 'Trainor':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("trn")] 
    elif sub == 'LateriticPlain': # elif sub == 'Lateritic Plain':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("lat")] 
    elif sub == 'Mardabilla':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("mar")] 
    elif sub == 'Tallering':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("tal")]                
    elif sub == 'Merredin':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("mer")]   
    elif sub == 'WesternMallee': #elif sub == 'Western Mallee':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("wml")]   
    elif sub == 'Edel':
        #dic = dic_shd
        dit = tbl_df0[tbl_df0["item"].str.contains("edl")]  
    else: 
        print("\n NO COMPARABLE SUITIBILITY LIST AVAILABLE FOR THIS SUB-REGION...")
        print("...THERE BE ERRORS YONDER YE MOUNTAIN !!!")
    
    print(dit)
    
    print("Opening the rangeland and veg assoc for that sub region...")
    # Cleaning variables
    hab_lst = None
    msk_rng = None  
    tmp_rng = None
    one_rng = None
    fin_rng = None

    hab_lst = None
    msk_veg = None  
    tmp_veg = None
    one_veg = None
    fin_veg = None
    
    print("IF raster exist, THEN read raster, THEN IF suitability values exist, read them...")
    if os.path.isfile(rst_rng):
        print("Existe:", "Rangelands", sub)
        with rio.open(rst_rng) as rng:
            #pfl_rng = rng.profile
            #pfl_veg = veg.profile
            kwds = rng.profile
        
            print("Reading the single band from the raster file...")
            arr_rng = rng.read(1)
            
            print("...processing Rangeland values")
        
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
                
    else:
        print("Existe:", "Rangelands", sub, "pas!")
    
    if os.path.isfile(rst_veg):
        print("Existe:", "Veg Assoc", sub)
        with rio.open(rst_veg) as veg:
            #pfl_rng = rng.profile
            #pfl_veg = veg.profile
            kwds = veg.profile
        
            print("Reading the single band from the raster file...")
            arr_veg = veg.read(1)
            

            print("...processing Veg Assoc values")
            print("Extracting the list of suitable habitats...")
            try:
                hab_lst = dit.loc[ (dit["item"].str.contains("veg")) & (dit["item"].str.contains("inn")) ]["list"].values[0]
                
                print("Creating a mask based on the list IN values...")
                #msk_veg = np.isin(arr_veg, dic["veg_inn"]) # msk_veg = np.isin(arr_veg, veg_shd_inn)
                msk_veg = np.isin(arr_veg, hab_lst) # msk_rng = np.isin(arr_rng, rng_shd_inn)
            
                print("Keeping values and zeros...")
                tmp_veg = np.where(msk_veg == 1, arr_veg, 0)
            
                print("Creating a mask based on the all values...")
                one_veg = np.where(arr_veg != -999, 1, -999)
                one_veg.max(), one_veg.min()
                
                print("Keeping inn values else -999...")
                fin_veg = np.where(one_veg == 1, tmp_veg, -999)   
            except:
                print("No veg assoc values were assigned!")
                
    else:
        print("Existe Pas:", "Veg Assoc", sub, "pas!")
      
    
    print("STEP 4a: Calculating area of raster that is classified as sandlewood habitat...")   
    if fin_rng is not None and fin_veg is not None :
        print("Both variables are arrays!")  
        
        print(fin_rng.min(), fin_rng.max())
        print(fin_veg.min(), fin_veg.max())
        
        print("Overlaying Rangeland over Veg Associations...")# create the new dataset 
        #dst_arr = np.where(raw_a >= 0 , raw_a , raw_b)
        dst_arr = np.where(fin_rng >= 0 , fin_rng , fin_veg)
        
        # checking
        print(dst_arr.min(), dst_arr.max())
    
    elif fin_rng is None and fin_veg is not None :
        print("Only fin_veg is an array")  
        print(fin_veg.min(), fin_veg.max())
        dst_arr = fin_veg
    
    elif fin_rng is not None and fin_veg is None :
        print("Only fin_rng is an array")    
        print(fin_rng.min(), fin_rng.max())
        dst_arr = fin_rng
        
    elif fin_rng is None and fin_veg is None :
        print("Neither variables are arrays!")   
        
        dst_arr = np.zeros((arr_rng.shape[0], arr_rng.shape[1]))
        dst_arr.shape        
        
    else: 
        print("CACA!!!CAC!!CACA!!!")


    print("\nSTEP 4b: Calculating area of raster that is classified as sandlewood habitat...\n")
    
    
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
            

    print("\nSTEP 4c: Writing rasters to file...\n")
    
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
    
    print("Lire a fishier...aux rangeland")
    try:
        print("...msk_rng")
        with rio.open(dst_pth + "_" + str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_msk_rng" + ".tif", "w", **kwds) as dst:
            dst.write(msk_rng, 1) 
    except:
        print("il n'a pas réussi à écrire dans le fichier.")
        
    try:
        print("...tmp_rng")
        with rio.open(dst_pth + "_" + str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_tmp_rng" + ".tif", "w", **kwds) as dst:
            dst.write(tmp_rng, 1) 
    except:
        print("il n'a pas réussi à écrire dans le fichier.")
        
    try:
        print("...one_rng")
        with rio.open(dst_pth + "_" + str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_one_rng" + ".tif", "w", **kwds) as dst:
            dst.write(one_rng, 1) 
    except:
        print("il n'a pas réussi à écrire dans le fichier.")
        
        
    print("Lire a fishier...aux veg assoc")
    

    try:
        print("...msk_veg")
        with rio.open(dst_pth + "_" + str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_msk_veg" + ".tif", "w", **kwds) as dst:
            dst.write(msk_veg, 1) 
    except:
        print("p")
            
    try:   
        print("...tmp_veg")
        with rio.open(dst_pth + "_" + str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_tmp_veg" + ".tif", "w", **kwds) as dst:
            dst.write(tmp_veg, 1) 
    except:
        print("il n'a pas réussi à écrire dans le fichier.")
                
    try: 
        print("...one_veg")
        with rio.open(dst_pth + "_" + str(sub.replace(" ", "")) + "_" + str(round(raster_pixel_size)) +"m" + "_one_veg" + ".tif", "w", **kwds) as dst:
            dst.write(one_veg, 1)
    except:
        print("il n'a pas réussi à écrire dans le fichier.")   
        
    """
        
        
print("Fin/Telos!")