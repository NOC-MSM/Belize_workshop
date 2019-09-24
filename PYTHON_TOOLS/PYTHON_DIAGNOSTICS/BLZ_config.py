"""
SEAsia_config.py

** Summary: **
Config file for NEMO_surface_var_diag.py

Builds 2D animation of NEMO maps(lat,lon)

jp: 16 July 2019

** Useage**::
python NEMO_surface_var_diag.py SEAsia
or
ipython$ %run NEMO_surface_var_diag SEAsia
	where SEAsia_config.py is an associated config file.

"""
import numpy as np
import datetime
import matplotlib.cm as cm   # colormap functionality
import cmocean.cm as cmo # colormap functionality

#################### USER PARAMETERS ##########################

#######################
## DEFINE REGION LIMITS
#######################
xlim = [] # easting coordinates for subselecion extraction. E.g. xlim=[75,135]
ylim = [] # northing coordinates for subsection extraction. E.g. ylim=[-20.,25.]
#xlim = [75,135]; ylim = [-20.,25.]
tlim = [] # [datetime.datetime(1960, 4, 20, 12, 0), datetime.datetime(1960, 5, 1, 12, 0)] # timeseries extraction. As datetime.datetime list
# E.g. tlim=[datetime.datetime(1966, 12, 26, 12, 0), datetime.datetime(1966, 12, 27, 12, 0)]')


#xlim = [95.,110.]; ylim = [0.,10.]

## Settings to be read in / specified
#config = 'ORCA0083-N06'; xlim = [53.,68.]; ylim = [-24.2,-8.5] # Mauritius EEZ
#config = 'ORCA0083-N06'; xlim = [75,135]; ylim = [-20.,25.] # SEAsia
#config = 'BoBEAS'
#config = 'SEAsia'
#field = 'salinity'
field = 'temperature'

##################################
## DEFINE FIELD SPECIFIC CONSTANTS
##################################
if field == 'salinity':
	plot_var = 'sss' #sea_surface_salinity' #'zos'. Must be defined in NcML file
	units = 'psu'
	levs = np.arange(20,35+1,1)
	cmap = cmo.haline #'Spectral'
	maskval = 0
	ofile = 'FIGURES/TEMPLATE_SSS.gif'

elif field == 'temperature':
	plot_var = 'sst' #sea_surface_salinity' #'zos'. Must be defined in NcML file
	units = 'degC'
	levs = np.arange(20,35+1,1)
	#levs = np.arange(20,30+1,1)
	cmap = cm.Spectral_r
	cmap.set_bad('white',1.)
	cmap.set_over('red',1.)
	maskval = 0
	ofile = 'FIGURES/TEMPLATE_SST.gif'

else:
	print("Not ready for field %s"%field)

####################
## Plotting features
####################
## COLORBAR shrink factor. It is hard
#  to automatically set the size of th colourbar for some reason...
colorbar_shrink = 0.7

## QUIVER
nx_quiv = 60 # number of quiver ticks in x-dirn
#spacing = 16 # grid spacing between vectors
speed_min = 0.05 # Min speed to show vector. OOPS REDEFINED IN QUIVER FN CALL
#ofile = ofile.replace('.gif','_vec.gif')

###############
## SOURCE files
###############
"""
The data are specified in two dictionaries (groups):

1. grid_data: For these variables the whole dataset is read and tested
to see if subsetting is to be applied.

2. input_data: These variables are loaded according to the subsetting limits
determined from the grid_data variables.

The dictionaries store information as follows:
 dic = {filename1 : [f1var1, f1var2], filename2 : [f2var1, f2var2] }
"""

dirname = '/Belize_workshop/RUN_NEMO/EXP_demo/' 
grid_data = {} # For storing variables to lead the entire grid
input_data = {} # For storing variables that are subsetted.

## GRID VARIABLES
filename = 'BLZE12_C1_1d_19950101_19950101_grid_T.nc' 
variable_lst = ['nav_lat', 'nav_lon', 'time_counter'] # variables in the files
grid_data.update( {dirname+filename: variable_lst} )

## SUBSETTED VARIABLES
filename = 'BLZE12_C1_1d_19950101_19950101_grid_U.nc' 
variable_lst = ['uos', 'nav_lat', 'nav_lon', 'time_counter'] # variables in the files
input_data.update( {dirname+filename: variable_lst} )

filename = 'BLZE12_C1_1d_19950101_19950101_grid_V.nc' 
variable_lst = ['vos', 'nav_lat', 'nav_lon'] # variables in the files
input_data.update( {dirname+filename: variable_lst} )

filename = 'BLZE12_C1_1d_19950101_19950101_grid_T.nc' 
variable_lst = ['sea_surface_temperature', 'sea_surface_salinity', 'nav_lat', 'nav_lon'] # variables in the files
input_data.update( {dirname+filename: variable_lst} )
