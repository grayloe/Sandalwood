# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:26:42 2024

@author: GrahamLoewenthal
"""


### Processing steps as of:
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20241126_Sandalwood_Stratification_Process_V3\20241126_Sandalwood_Stratification_Process_V3.xlsx # 1st pass
# Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20250131_Sandalwood_Stratification_Process_V5\20250131_Sandalwood_Stratification_Process_V5.xlsx # 2nd pass current
# Subtract Land Systems or Vegetation Asspociations with low probability of occurrence:
# 1. Initial ha of potential s/wood habitat
# Subtract all fire history spatial data
# 2. Remaining ha of s/wood habitat
# Subtract 30m buffered hydrology
# 3. Remaining ha of s/wood habitat
# Subtract cleared land (use remnant vegetation layer)
# 4. Remaining ha of s/wood habitat

### 

"""
This script reads the source spreadsheet provided by Nigel Wessels, which list the habitata that support SDandal wood
Then created individual files for easy future reading.
"""



import os
import pandas as pd
import geopandas as gpd


print("STEP 0: Reading the source spreasheet (Nigel Wessel's) that outlines the rules set and  which habitats suitable (ie IN or OUT)...")


print("Destination directory...")
dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables" # original keep
#dst_dir = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\Tables"


print("Reading the source spreadsheet (Nigel Wessel's) ...")
#xls_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20241126_Sandalwood_Stratification_Process_V3\20241126_Sandalwood_Stratification_Process_V3.xlsx"
xls_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Source\NigelWessels\20250131_Sandalwood_Stratification_Process_V5\20250131_Sandalwood_Stratification_Process_V5.xlsx"

xls_obj = pd.ExcelFile(xls_fil)
tmp_lst = xls_obj.sheet_names # Get the list of sheet names

print("Reading the list of sub-regions of interest...")
print(tmp_lst) # Print the sheet names
#xls_lst = tmp_lst[2:-3] +  # only the sub-region names from the spreadsheet

# Mannual: list of the sub ibra that area being used in the Sandelwood processing based on "20250131_Sandalwood_Stratification_Process_V5.xlsx"
inc_lst = ['Eastern Goldfield', 'Southern Cross ', 'Mardabilla', 
           'Eastern Murchison', 'Shield', 'Central', 
           'Carnegie', 'Trainor', 'Lateritic Plain',]

print("Excluding the sub-regions NOT to be processed...")
xls_lst = [tmp for tmp in tmp_lst if any(inc in tmp for inc in inc_lst)]
print(xls_lst)

"""
print("Cleaning the SubRegion list (from spreadsheet) of sub rergions for processing...")
#src_lst = [sub.replace(" ", "") for sub in src_lst] # Remove spaces between words
src_lst = [src.replace("Goldfields", "Goldfield") for src in src_lst] # the "S" has been removed from "Goldfields", to make the script work
del src_lst[11] # hard coded deletion of the second "GeraldtonHills"
"""

print(xls_lst) # Print the sheet names
  



print("STEP 1: Creating an empty dataFrame for habitat IN/OUT selection...")
### Producing ha area stattemtns is required after each processing step of the "rule-set"
### The rule set is on the first tab of the above .xlsx

# PathFile of the the dataframe
#tbl_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\Tables\20241126_Sandalwood_Stratification_Process_V3_Prepared.csv" # original V3 keep
#tbl_fil = r"Z:\DEC\Sandalwood_Population_Modelling\DATA\Working\RuleSet_Processing\ComparsionOnly_ToBeDeleted\Tables\20241126_Sandalwood_Stratification_Process_V3_Prepared.csv" # test delete
tbl_fil = os.path.join(dst_dir, os.path.basename(os.path.splitext(xls_fil)[0]) + "_Prepared.csv") # v5 version
                       
print("Creating new /Tables/ directory...")
if not os.path.exists(os.path.dirname(tbl_fil)):
    os.makedirs(os.path.dirname(tbl_fil))

# original, but does not create a preparation table from scratch
#def createAreaStatementeTable(filePath):
    """Faire: Create a df table with two columns: [the list name, the list its self]."""
    """
    # If source and prepared fiels exist, re-create, else create
    if os.path.exists(filePath) and os.path.exists(xls_fil):
        print("Source Fichier existe, re-create prepared fichier!")
        os.remove(filePath)
        print("Faire un neuvel table!")
        
        #list of columns for the empty dataframe
        df0_col = ["item", "list",]
        
        # Creating the empty dataframe
        df0_hab = pd.DataFrame(columns = df0_col)
        #df0_area = df0_area.set_index('id')
        
        print("Likre a fishier...")
        df0_hab.to_csv(filePath, index=False)
        
    elif os.path.exists(filePath) and not os.path.exists(xls_fil):
        print("Fichier source pas existe, faire du rien!")
      
    return
    """

# new, same as original but makes a prepartion file from scratch, but does not create a preparation table from scratch
def createAreaStatementeTable(filePath):
    """Faire: Create a df table with two columns: [the list name, the list its self]."""
    # If source and prepared fiels exist, re-create, else create
    if os.path.exists(filePath) and os.path.exists(xls_fil):
        print("Source Fichier existe, re-create prepared fichier!")
        os.remove(filePath)
        print("Faire un neuvel table!")
        
        #list of columns for the empty dataframe
        df0_col = ["item", "list",]
        
        # Creating the empty dataframe
        df0_hab = pd.DataFrame(columns = df0_col)
        #df0_area = df0_area.set_index('id')
        
        print("Likre a fishier...")
        df0_hab.to_csv(filePath, index=False)

    elif not os.path.exists(filePath) and os.path.exists(xls_fil):
        print("Fichier source existe, fichier de prepare pas existe, faire-le!")
        
        print("Faire un neuvel table!")
        
        #list of columns for the empty dataframe
        df0_col = ["item", "list",]
        
        # Creating the empty dataframe
        df0_hab = pd.DataFrame(columns = df0_col)
        #df0_area = df0_area.set_index('id')
        
        print("Likre a fishier...")
        df0_hab.to_csv(filePath, index=False)
        
        
    else:
        print("WARNING: Fichier source pas existe, faire du rien!")
        print("WARNING: Processing will not work sans to source spreasheet from Nigal Wessals!")
        print("ACTION: Find the source spread sheet!")

    return

print('Executing function "createAreaStatementeTable" - which creates an area Statement table')
createAreaStatementeTable(tbl_fil)


print("The function for updating the area statements to the area statement table!")
def updateArea(pathfile, listItem, listValues):
    """Faire: Update the habitat list table."""
    df0_hab = pd.read_csv(pathfile)  
    df0_hab.loc[len(df0_hab), ("item", "list")] = [listItem, listValues]
    print("Lire a fishier...")
    df0_hab.to_csv(pathfile, index=False) 
    return



print("STEP 2: Importing the table with the habaitat list [IN, OUT, NAN] for rangeland and/or veg assoc...")

# All extractions must be hard coded from source xls

print("EASTERN MURCHISON: Reading Excel file into a Pandas DataFrame...")
tbl_emr_rng = pd.read_excel(xls_fil, sheet_name='Eastern Murchison', skiprows = 0, nrows = 119, usecols="A:E")
tbl_emr_veg = pd.read_excel(xls_fil, sheet_name='Eastern Murchison', skiprows = 122, nrows = 5, usecols="A:D")
tbl_emr_veg.rename(columns={"Unnamed: 0": "IN/OUT", "Unnamed: 1": "COMMENT"}, inplace = True)


# get value from columns, get values only, assign values to a list, sort the list
rng_emr_inn = sorted( tbl_emr_rng["mu_id"][tbl_emr_rng["IN/OUT"] == "IN"].values.tolist() )
rng_emr_out = sorted( tbl_emr_rng["mu_id"][tbl_emr_rng["IN/OUT"] == "OUT"].values.tolist() )
rng_emr_nan = sorted( tbl_emr_rng["mu_id"][tbl_emr_rng["IN/OUT"].isnull()].values.tolist() )

veg_emr_inn = sorted( tbl_emr_veg["veg_assoc"][tbl_emr_veg["IN/OUT"] == "IN"].values.tolist() )
veg_emr_out = sorted( tbl_emr_veg["veg_assoc"][tbl_emr_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_emr_nan = sorted( tbl_emr_veg["veg_assoc"][tbl_emr_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("rng_emr_inn"), rng_emr_inn)
updateArea(tbl_fil, str("rng_emr_out"), rng_emr_out)
updateArea(tbl_fil, str("rng_emr_nan"), rng_emr_nan)

updateArea(tbl_fil, str("veg_emr_inn"), veg_emr_inn)
updateArea(tbl_fil, str("veg_emr_out"), veg_emr_out)
updateArea(tbl_fil, str("veg_emr_nan"), veg_emr_nan)
 # v5 complete

print("SOUTHERN CROSS: Reading Excel file into a Pandas DataFrame...")
tbl_scs_veg = pd.read_excel(xls_fil, sheet_name='Southern Cross ', skiprows = 56, nrows = 57,  usecols="A:D") 
# get value from columns, get values only, assign values to a list, sort the list
veg_scs_inn = sorted( tbl_scs_veg["veg_assoc"][tbl_scs_veg["IN/OUT"] == "IN"].values.tolist() )
veg_scs_out = sorted( tbl_scs_veg["veg_assoc"][tbl_scs_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_scs_nan = sorted( tbl_scs_veg["veg_assoc"][tbl_scs_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_scs_inn"), veg_scs_inn)
updateArea(tbl_fil, str("veg_scs_out"), veg_scs_out)
updateArea(tbl_fil, str("veg_scs_nan"), veg_scs_nan)
# v5 complete

print("EASTERN GOLDFIELD: Reading Excel file into a Pandas DataFrame...")
tbl_egf_veg = pd.read_excel(xls_fil, sheet_name='Eastern Goldfields')
# get value from columns, get values only, assign values to a list, sort the list
veg_egf_inn = sorted( tbl_egf_veg["veg_assoc"][tbl_egf_veg["IN/OUT"] == "IN"].values.tolist() )
veg_egf_out = sorted( tbl_egf_veg["veg_assoc"][tbl_egf_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_egf_nan = sorted( tbl_egf_veg["veg_assoc"][tbl_egf_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_egf_inn"), veg_egf_inn)
updateArea(tbl_fil, str("veg_egf_out"), veg_egf_out)
updateArea(tbl_fil, str("veg_egf_nan"), veg_egf_nan)
# v5 complete

print("SHIELD: Reading Excel file into a Pandas DataFrame...")
tbl_shd_rng = pd.read_excel(xls_fil, sheet_name='Shield', skiprows = 0, nrows = 51)
tbl_shd_veg = pd.read_excel(xls_fil, sheet_name='Shield', skiprows = 53, nrows = 17,  usecols="A:D")
tbl_shd_veg.rename(columns={"Unnamed: 0": "IN/OUT", "Unnamed: 1": "COMMENT"}, inplace = True)
# get value from columns, get values only, assign values to a list, sort the list
rng_shd_inn = sorted( tbl_shd_rng["mu_id"][tbl_shd_rng["IN/OUT"] == "IN"].values.tolist() )
rng_shd_out = sorted( tbl_shd_rng["mu_id"][tbl_shd_rng["IN/OUT"] == "OUT"].values.tolist() )
rng_shd_nan = sorted( tbl_shd_rng["mu_id"][tbl_shd_rng["IN/OUT"].isnull()].values.tolist() )

veg_shd_inn = sorted( tbl_shd_veg["veg_assoc"][tbl_shd_veg["IN/OUT"] == "IN"].values.tolist() )
veg_shd_out = sorted( tbl_shd_veg["veg_assoc"][tbl_shd_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_shd_nan = sorted( tbl_shd_veg["veg_assoc"][tbl_shd_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("rng_shd_inn"), rng_shd_inn)
updateArea(tbl_fil, str("rng_shd_out"), rng_shd_out)
updateArea(tbl_fil, str("rng_shd_nan"), rng_shd_nan)

updateArea(tbl_fil, str("veg_shd_inn"), veg_shd_inn)
updateArea(tbl_fil, str("veg_shd_out"), veg_shd_out)
updateArea(tbl_fil, str("veg_shd_nan"), veg_shd_nan)
# v5 complete

print("CENTRAL: Reading Excel file into a Pandas DataFrame...")
tbl_ctr_veg = pd.read_excel(xls_fil, sheet_name='Central', skiprows = 0, nrows = 27)
# get value from columns, get values only, assign values to a list, sort the list
veg_ctr_inn = sorted( tbl_ctr_veg["veg_assoc"][tbl_ctr_veg["IN/OUT"] == "IN"].values.tolist() )
veg_ctr_out = sorted( tbl_ctr_veg["veg_assoc"][tbl_ctr_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_ctr_nan = sorted( tbl_ctr_veg["veg_assoc"][tbl_ctr_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_ctr_inn"), veg_ctr_inn)
updateArea(tbl_fil, str("veg_ctr_out"), veg_ctr_out)
updateArea(tbl_fil, str("veg_ctr_nan"), veg_ctr_nan)
# v5 complete

print("CARNEGIE: Reading Excel file into a Pandas DataFrame...")
tbl_car_veg = pd.read_excel(xls_fil, sheet_name='Carnegie', skiprows = 0, nrows = 20) #, usecols="A:D")
# get value from columns, get values only, assign values to a list, sort the list
veg_car_inn = sorted( tbl_car_veg["veg_assoc"][tbl_car_veg["IN/OUT"] == "IN"].values.tolist() )
veg_car_out = sorted( tbl_car_veg["veg_assoc"][tbl_car_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_car_nan = sorted( tbl_car_veg["veg_assoc"][tbl_car_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_car_inn"), veg_car_inn)
updateArea(tbl_fil, str("veg_car_out"), veg_car_out)
updateArea(tbl_fil, str("veg_car_nan"), veg_car_nan)
# v5 complete

print("TRAINOR: Reading Excel file into a Pandas DataFrame...")
tbl_trn_veg = pd.read_excel(xls_fil, sheet_name='Trainor_Lateritic Plain', nrows = 36)
# get value from columns, get values only, assign values to a list, sort the list
veg_trn_inn = sorted( tbl_trn_veg["veg_assoc"][tbl_trn_veg["IN/OUT"] == "IN"].values.tolist() )
veg_trn_out = sorted( tbl_trn_veg["veg_assoc"][tbl_trn_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_trn_nan = sorted( tbl_trn_veg["veg_assoc"][tbl_trn_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_trn_inn"), veg_trn_inn)
updateArea(tbl_fil, str("veg_trn_out"), veg_trn_out)
updateArea(tbl_fil, str("veg_trn_nan"), veg_trn_nan)
# v5 complete

print("LATERITIC PLAIN: Reading Excel file into a Pandas DataFrame...")
tbl_lat_veg = pd.read_excel(xls_fil, sheet_name='Trainor_Lateritic Plain', nrows = 36)
# get value from columns, get values only, assign values to a list, sort the list
veg_lat_inn = sorted( tbl_lat_veg["veg_assoc"][tbl_lat_veg["IN/OUT"] == "IN"].values.tolist() )
veg_lat_out = sorted( tbl_lat_veg["veg_assoc"][tbl_lat_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_lat_nan = sorted( tbl_lat_veg["veg_assoc"][tbl_lat_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_lat_inn"), veg_lat_inn)
updateArea(tbl_fil, str("veg_lat_out"), veg_lat_out)
updateArea(tbl_fil, str("veg_lat_nan"), veg_lat_nan)
# v5 complete

print("MARDABILLA: Reading Excel file into a Pandas DataFrame...")
tbl_mar_veg = pd.read_excel(xls_fil, sheet_name='Mardabilla', nrows = 9)
# get value from columns, get values only, assign values to a list, sort the list
veg_mar_inn = sorted( tbl_mar_veg["veg_assoc"][tbl_mar_veg["IN/OUT"] == "IN"].values.tolist() )
veg_mar_out = sorted( tbl_mar_veg["veg_assoc"][tbl_mar_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_mar_nan = sorted( tbl_mar_veg["veg_assoc"][tbl_mar_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_mar_inn"), veg_mar_inn)
updateArea(tbl_fil, str("veg_mar_out"), veg_mar_out)
updateArea(tbl_fil, str("veg_mar_nan"), veg_mar_nan)
# v5 complete

""" ### THIS WERE CURRENT FOR SPREADSHEET V3 ### not V5
print("TALLERING: Reading Excel file into a Pandas DataFrame...") 
tbl_tal_rng = pd.read_excel(xls_fil, sheet_name='Tallering')
# get value from columns, get values only, assign values to a list, sort the list
rng_tal_inn = sorted( tbl_tal_rng["mu_id"][tbl_tal_rng["IN/OUT"] == "IN"].values.tolist() )
rng_tal_out = sorted( tbl_tal_rng["mu_id"][tbl_tal_rng["IN/OUT"] == "OUT"].values.tolist() )
rng_tal_nan = sorted( tbl_tal_rng["mu_id"][tbl_tal_rng["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("rng_tal_inn"), rng_tal_inn)
updateArea(tbl_fil, str("rng_tal_out"), rng_tal_out)
updateArea(tbl_fil, str("rng_tal_nan"), rng_tal_nan)


print("MERREDIN: Reading Excel file into a Pandas DataFrame...") 
tbl_mer_veg = pd.read_excel(xls_fil, sheet_name='Merredin', nrows = 114)
# get value from columns, get values only, assign values to a list, sort the list
veg_mer_inn = sorted( tbl_mer_veg["veg_assoc"][tbl_mer_veg["IN/OUT"] == "IN"].values.tolist() )
veg_mer_out = sorted( tbl_mer_veg["veg_assoc"][tbl_mer_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_mer_nan = sorted( tbl_mer_veg["veg_assoc"][tbl_mer_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_mer_inn"), veg_mer_inn)
updateArea(tbl_fil, str("veg_mer_out"), veg_mer_out)
updateArea(tbl_fil, str("veg_mer_nan"), veg_mer_nan)


print("WESTERN MALLEE: Reading Excel file into a Pandas DataFrame...") 
tbl_wml_veg = pd.read_excel(xls_fil, sheet_name='Western Mallee')
# get value from columns, get values only, assign values to a list, sort the list
veg_wml_inn = sorted( tbl_wml_veg["veg_assoc"][tbl_wml_veg["IN/OUT"] == "IN"].values.tolist() )
veg_wml_out = sorted( tbl_wml_veg["veg_assoc"][tbl_wml_veg["IN/OUT"] == "OUT"].values.tolist() )
veg_wml_nan = sorted( tbl_wml_veg["veg_assoc"][tbl_wml_veg["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("veg_wml_inn"), veg_wml_inn)
updateArea(tbl_fil, str("veg_wml_out"), veg_wml_out)
updateArea(tbl_fil, str("veg_wml_nan"), veg_wml_nan)


print("EDEL: Reading Excel file into a Pandas DataFrame...")
tbl_edl_rng = pd.read_excel(xls_fil, sheet_name='Edel', nrows = 36)
# get value from columns, get values only, assign values to a list, sort the list
rng_edl_inn = sorted( tbl_edl_rng["mu_id"][tbl_edl_rng["IN/OUT"] == "IN"].values.tolist() )
rng_edl_out = sorted( tbl_edl_rng["mu_id"][tbl_edl_rng["IN/OUT"] == "OUT"].values.tolist() )
rng_edl_nan = sorted( tbl_edl_rng["mu_id"][tbl_edl_rng["IN/OUT"].isnull()].values.tolist() )

print("Updating the lists to file...")
updateArea(tbl_fil, str("rng_edl_inn"), rng_edl_inn)
updateArea(tbl_fil, str("rng_edl_out"), rng_edl_out)
updateArea(tbl_fil, str("rng_edl_nan"), rng_edl_nan)
""" ### THIS WERE CURRENT FOR SPREADSHEET V3 ### not V5


print("Le fissier de habitate de suitibilite ete complete.")
print("Fin/Telos")











