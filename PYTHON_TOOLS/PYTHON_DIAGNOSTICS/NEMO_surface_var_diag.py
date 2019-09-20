"""
NEMO_surface_var_diag.py

Python 2.7 / Python 3.5 example to load netCDF4 data and plot it using class structure.

** Summary **
Load settings from a config file.
Load grid data and determine if any subsetting is required.
Load variable data, appling subsetting if required.
pcolor / quiver data as static frame or animation, as requested by commandline input

jp: 16 July 2019

** To-do **:
* multiple file loading (NCML vs xarray): xr.open_mfdataset('my/files/*.nc')
* Add a mask variable to initial grid data set up
* Create new diagnostics: e.g. difference between SST model fields

** Issues **:
* nav_lat and nav_lon on different grids are not seen as unique
* uses only grid_T nav_lat and nav_lon
* quiver spacing does not scale with changing xlim/ylim

** Change log**:
* 16 July 2019: It works
* 17 July 2019: Swaps between ORCA and SEAsia data sources
* 18 July 2019: Add animation option
* 19 July 2019: xarray can load partial datasets
* 22 July 2019: Subset data over time, using parameter file
* 23 July 2019: Collapse z dim to surface value if 3d

** Useage**::
python NEMO_surface_var_diag.py ORCA0083_SEAsia
or
ipython$ %run NEMO_surface_var_diag SEAsia
  where SEAsia_config.py is an associated config file.
"""

#### Imports
import os
import sys # argv passing
import numpy as np
import datetime
#from netCDF4 import Dataset # switch *xarr* functions for *nc4* fns
import xarray as xr
import matplotlib.pyplot as plt

import pickle
from platform import python_version # to test python version
import cartopy.crs as ccrs # mapping plots
import cartopy.feature # add rivers, regional boundaries etc
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER # deg symb

import imageio # Image conversion to animated gif




#### Classes

class Controller(object):
    """
    This is where the main things happen.
    Where user input is managed and methods are launched
    """
    def __init__(self):
        """
        Initialise main controller. Look for file. If exists load it
        """
        print("Aim: Load netCDF4 data and plot it using class structure.")
        self.data_bucket = self.load()
        self.run_interface()

    def load(self):
        """
        Load pickle file from the standard file save
        """
        data_bucket = DataBucket()
        print("Auto loads from pickle file if it exists.")
        try:
            if os.path.exists(SAVE_FILE_NAME):
                template = "...Loading (%s)"
                print(template%SAVE_FILE_NAME)
                with open(SAVE_FILE_NAME, 'rb') as file_object:
                    data_bucket = pickle.load(file_object)
            else:
                print("... %s does not exist"%SAVE_FILE_NAME)
        except KeyError:
            print('ErrorA ')
        except (IOError, RuntimeError):
            print('ErrorB ')

        return data_bucket


    def run_interface(self):
        """
        Application's main loop
        Get user input and respond
        """

        print(INSTRUCTIONS)
        while True:
            if "2.7" in python_version():
                command = raw_input("What do you want to do? ")
            else:
                command = input("What do you want to do? ")

            if command == "q":
                print("run_interface: Saving DataBucket instance")
                save(self.data_bucket) # Function call.
                print("run_interface: Exiting the application")
                break
            elif command == "i":
                print(INSTRUCTIONS)
            elif command == "a":
                print('run_interface: First define geographic subregion')
                for key,variable_lst in params.grid_data.items():
                    for var in variable_lst:
                        self.data_bucket.define_slice( NemoDataElement(key, var) )

                print('run_interface: Second add (subdomain) data to bucket')
                for key,variable_lst in params.input_data.items():
                    for var in variable_lst:
                        self.data_bucket.add_data( NemoDataElement(key, var, limits=self.data_bucket.limits) )
                        print("run_interface: From {}, read in {}".format(key,var))
                        #self.data_bucket.add_data( NemoDataElement(filname,'sea_surface_temperature') )

            elif command == "s":
                print('run_interface: Show bucket contents')
                self.data_bucket.show()
            elif command == "pcolor":
                print('run_interface: pcolormesh bucket contents')
                self.data_bucket.pcolor(anim_flag=False, quiver_flag=False)
            elif command == "quiver":
                print('run_interface: pcolormesh+quiver bucket contents')
                self.data_bucket.pcolor(anim_flag=False, quiver_flag=True)
                #self.data_bucket.pcolor_quiver(anim_flag=False)

            elif command == "pa":
                print('run_interface: animate pcolormesh bucket contents to file')
                self.data_bucket.pcolor(anim_flag=True, quiver_flag=False)
            elif command == "qa":
                print('run_interface: animate pcolormesh+quiver bucket contents to file')
                self.data_bucket.pcolor(anim_flag=True, quiver_flag=True)

            else:
                template = "run_interface: I don't recognise (%s)"
                print(template%command)




class DataBucket(object):
    """
    DataBucket to hold all the variables, axes data, subdomain index limits (if xlim is specified).
    Will probably only have one instance (per model run).
    """
    def __init__(self):
        """ set variable (and grid) attributes to empty """
        self.vars = {} # empty dictionary
        self.limits = {} # Need to define the x,y subdomain as indices for subselecting patent data.

    def define_slice(self, new_data):
        """
        Check if only a subregion of the data needs to be loaded
        Since some datasets regions do not need to be loaded in their entirety.
        The aim is to here define the indices limits for a subdomain of interest.
        This is done based on xlim, ylim, tlim inputs.
        Though for data with depth information only the surface field is extracted.
        """
        print("define_slice: updating limits var: std_name {}".format( new_data.std_name  ))
        #print("define_slice: updating limits var: data {}".format( new_data.data  ))
        self.limits.update({ new_data.std_name : new_data.data[:] })

        #if len( self.limits.keys() ) == 2:
        if "lat" in self.limits.keys() and "lon" in self.limits.keys():
            """
            if lat and lon are read in, define new keys ilat and ilon
            to store the extrema indices. Then pop off the lat and lon keys.
            """
            if params.xlim == []: # Assume ylim=[] also
                #self.limits = {} # Reset
                self.limits.update({ 'ilat': None, 'ilon': None } )
            else:
                #print( "limits.keys()".format( self.limits.keys() ))
                [J00,I00] = findJI(params.ylim[0], params.xlim[0], self.limits['lat'], self.limits['lon'])
                [J01,I01] = findJI(params.ylim[0], params.xlim[1], self.limits['lat'], self.limits['lon'])
                [J11,I11] = findJI(params.ylim[1], params.xlim[1], self.limits['lat'], self.limits['lon'])
                [J10,I10] = findJI(params.ylim[1], params.xlim[0], self.limits['lat'], self.limits['lon'])
                J0 = min(J00,J01)
                J1 = max(J11,J10)
                I0 = min(I00,I10)
                I1 = max(I01,I11)
                #self.limits = {} # Reset
                self.limits.update({ 'ilat': [J0,J1], 'ilon': [I0,I1] } )
            self.limits.pop("lon") # remove lon key
            self.limits.pop("lat") # remove lat key
            #print("define_slice: limits {}".format(self.limits))

        elif "datetime" in self.limits.keys():
            if params.tlim == []:
                self.limits.update({ 'itime': None })
            else:
                if type(params.tlim[0]) != datetime.datetime:
                    print('define_slice: EXPECTED tlim to be type \
                    datetime.datetime not type {}'.format(type(params.tlim[0]) ))
                    print('E.g. tlim=[datetime.datetime(1966, 12, 26, 12, 0), datetime.datetime(1966, 12, 27, 12, 0)]')
                #self.limits.update({ 'itime': None })
                #print("defin_slice: self.limits['datetime'] {}".format(self.limits['datetime']))
                [_,T0] = nearest( [dd for dd in self.limits['datetime']], params.tlim[0] )
                [_,T1] = nearest( [dd for dd in self.limits['datetime']], params.tlim[1] )
                #print("define_slice: limits {}".format(self.limits))
                self.limits.update({ 'itime': [T0,T1] } )
            self.limits.pop("datetime") # remove datetime key
        #elif len( self.limits.keys() ) > 2:
        #    print("Didn't expect this many keys {}".format(self.limits.keys() ))
        #    print("Didn't expect this many keys {}".format(len(self.limits.keys()) ))
	#print("define_slice: limits {}".format(self.limits))

        return None


    def add_data(self, new_data):
        """
        Add new variable to the list of variables in the DataBucket instance
        The new_data should be an instance of the DataEntry class.
        The data elements are stored in a dictionary with the key being a standard
        string for the associated variable. See function "convert_modelvarname_to_stdvarname"
        """
        print("add_data: import {} as {}".format(new_data.var_name,new_data.std_name))
        self.vars.update({ new_data.std_name : new_data.data[:] })

    def show(self):
        """ Show the data bucket contents """
        try:
            for key in self.vars.keys():
                print("show: key= {}, size={}".format(key, np.shape(self.vars[key]) ))
        except KeyError:
            print("Empty "+self.vars.keys())
        return None


    def _ccrs_pcolor(self, fig, ax, icount):
        """
        pcolormesh elements that get reused
        icount - time dimension index
        Returns: ax,X,Y,Z
        """
        #icount = 1
        #lab = self.variable + ' at time step:'+str(icount)
        xlim = set_plot_lim(params.xlim, self.vars['lon'])
        ylim = set_plot_lim(params.ylim, self.vars['lat'])

        ## Remove issue whereby x,y coords have masked values (even if there are zero masked elements)
        X = self.vars['lon'].filled()
        Y = self.vars['lat'].filled()
        # replace former nan locations in x,y coords
        #X[self.vars['lon'].mask] = np.mean(xlim)
        #Y[self.vars['lat'].mask] = np.mean(ylim)
        Z = self.vars[params.plot_var][icount,:,:]

        ax = plt.subplot(1,1,1, projection=ccrs.PlateCarree())
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        cset = ax.pcolormesh( X, Y, Z, transform=ccrs.PlateCarree(), cmap=params.cmap )

        cset.set_clim([params.levs[0],params.levs[-1]])

        # Add nice CARTOPY features
        #cartopy.feature.COLORS = {'water': np.array([ 0.59375 , 0.71484375, 0.8828125 ]), \
        #     'LAND': np.array([ 0.9375 , 0.9375 , 0.859375]), \
        #     'land_alt1': np.array([ 0.859375, 0.859375, 0.859375])}

        ax.add_feature(cartopy.feature.OCEAN)
        ax.add_feature(cartopy.feature.LAND)
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
        ax.add_feature(cartopy.feature.RIVERS)

        #ax.coastlines()
        #ax.gridlines(draw_labels=True)

        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=0.5, color='gray', alpha=0.5, linestyle='-')

        gl.xlabels_top = False
        gl.xlabels_bottom = True
        gl.ylabels_right = False
        gl.ylabels_left = True
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        #gl.xlabel_style = {'size': 15, 'color': 'gray'}
        #gl.xlabel_style = {'color': 'red', 'weight': 'bold'}

        #ax.hold(True)

        plt.colorbar(cset, shrink=params.colorbar_shrink, pad=.05) # Add colorbar
        #plt.colorbar(wspd_contours, ax=ax, orientation="horizontal", pad=.05)

        #plt.title(lab)
        return ax,X,Y,Z

    def _pcolor(self, fig, ax, icount):
        """
        pcolormesh elements that get reused
        icount - time dimension index
        Returns: ax,X,Y,Z
        """
        #icount = 1
        #lab = self.variable + ' at time step:'+str(icount)
        xlim = set_plot_lim(params.xlim, self.vars['lon'])
        ylim = set_plot_lim(params.ylim, self.vars['lat'])

        ## Remove issue whereby x,y coords have masked values data type
        X = self.vars['lon'].filled() # fill in the nans (cannot be type numpy.ma.core.MaskedArray)
        Y = self.vars['lat'].filled() # fill in the nans
        # replace former nan locations in x,y coords
        #X[self.vars['lon'].mask] = np.mean(xlim)
        #Y[self.vars['lat'].mask] = np.mean(ylim)

        Z = self.vars[params.plot_var][icount,:,:]

        cset = ax.pcolormesh( X, Y, Z, cmap=params.cmap )


        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel('\nLongitude (deg)')
        ax.set_ylabel('\nLatitude (deg)')
        cset.set_clim([params.levs[0],params.levs[-1]])
        #ax.hold(True)

        fig.colorbar(cset) # Add colorbar

        #plt.title(lab)
        return ax,X,Y,Z

    def pcolor(self, anim_flag=True, quiver_flag=True):
        """
        pcolormesh the data bucket
        Optionally add quiver ticks
        Optionally animate
        """

        if anim_flag == True:
            nframes = np.shape(self.vars[params.plot_var])[0]
        else:
            nframes = 1
        
        files = [] # store images from saving to file

        ## Time timeseries of frames
        for count in range(0,nframes):
            print('frame progress: {} / {}'.format(count,nframes-1))

            plt.close('all')
            fig = plt.figure(figsize=(10,10))
            ax = fig.gca()

            if quiver_flag == False:
                ax,_,_,_ = self._ccrs_pcolor(fig,ax,count)
            elif quiver_flag == True:
                ax,X,Y,Z = self._ccrs_pcolor(fig,ax,count)
                spacing = int( np.shape(X)[1] // params.nx_quiv ) # quiver point spacing
                #spacing = params.spacing # quiver point spacing
                U = self.vars['ssu'][count,:,:]
                V = self.vars['ssv'][count,:,:]

                speed = np.sqrt(U**2+V**2)

                U = np.ma.masked_where( speed < params.speed_min, U)
                V = np.ma.masked_where( speed < params.speed_min, V)

                qset = ax.quiver( X[::spacing,::spacing],
                            Y[::spacing,::spacing],
                            U[::spacing,::spacing],
                            V[::spacing,::spacing],
                               units='xy', scale_units='width',scale=40)

            else:
                break

            dat = datetime.datetime.strftime(self.vars['datetime'][count], '%d %b %Y') #: %H:%M')
            plt.title(config+': '+params.field+' ('+params.units+'): '+str(dat))


            #if(anim_flag):
            if(1): # Always save file. Can not display from within docker container
                fname = params.ofile.replace('TEMPLATE',config). \
                                replace('.gif','_'+str(count).zfill(4)+'.png')
                plt.savefig(fname, dpi=100)
                files.append(fname)

            else:
                plt.show()

        if anim_flag == True:
            # Make the animated gif and clean up the files
            if(quiver_flag):
                make_gif(files,params.ofile.replace('TEMPLATE',config). \
                                replace('.gif','_vec.gif'),delay=20)
            else:
                make_gif(files,params.ofile.replace('TEMPLATE',config) \
                                ,delay=20)

            for f in files:
                os.remove(f)


        return None



class GenericDataElement(object):
    """
    A GenericDataEntry instance holds and manages the details of a data extraction
    from the parent file.
    This includes grid and variables alike.
    """
    def __init__(self, var_name = None, long_name = None, limits = None):
        """
        Initialise attributes: variable name, long name, data, ndims
        """
        self.var_name = var_name
        self.std_name = convert_modelvarname_to_stdvarname(var_name)
        self.long_name = long_name
        self.data = self.load_item()
        self.limits = limits

    def load_item(self):
        """ Generic load statement. To be overwritten """
        print('Generic load statement')

    def plot(self):
        """ Plot the data """
        print("plot the data")


class NemoDataElement(GenericDataElement):
    """
    NemoDataElement class inherits from GenericDataEntry.
    An instance hold and manage the details of a NEMO data entry extraction.
    This includes grid and variables alike.

    If geographic limits are set, then only a subset of data is extracted.
    """
    def __init__(self, filename = None, var_name = None, long_name = None, limits = None):
        """
        Initialise attributes: variable name, long name, data, ndims
        """
        self.file_name = filename
        self.var_name = var_name
        self.std_name = convert_modelvarname_to_stdvarname(var_name)
        # Never used get_xarr_attribute_value but could...
        #self.long_name = self.get_nc4_attribute_value('long_name')
        #self.long_name = self.get_xarr_attribute_value('long_name')
        self.limits = limits
        self.data = self.load_item()

    def load_item(self):
        """ NEMO load statement. """
        print('load_item: NEMO load statement')
        #return self.__get_nc4_item__()
        return self.__get_xarr_item__()

    def __get_xarr_item__(self):
        """
        xarray: Return the data requested.
        The data "sel"ected (subsampled) in x,y,t and z dimensions:
            tlim defines the time dimension subsetting
            xlim defines the longitude dimension subsetting
            ylim defines the latitude dimension subsetting
        NOTE: xarray has a problem when it reads in latitude values at the equator.
        It replaces the values with NaNs...
        Here I manaully fill NaNs in the lat or lon fields with Zero.
        """

        try:
            #DS = xr.open_dataset(self.file_name)
            DS = xr.open_mfdataset(self.file_name)
            #print(DS)
            #print (self.var_name)
            #dvar = dataset.variables[self.var_name]
            ret_item = []
            #print("get_xarr_item: self.limits.keys(): {}".format(self.limits.keys()))
            print("get_xarr_item: Read var_name: {} or std_name: {}".format( self.var_name, self.std_name))

            # First time through read in the whole data set for the given (grid) variables
            if self.limits == None: # Limits have not yet been sought
                ret_item = getattr(DS, self.var_name).values

            # Second time through read in subsetted data
            else:
                # Initialise arguement dictionary for selecting data subset
                arguments_dictionary = {}
                _depth_nam = None

                for key in DS[self.var_name].dims:
                    if('depth' in key):
                        _depth_nam = key
                        arguments_dictionary.update( {_depth_nam : slice(None,1)} ) # Only surface level
                    elif('x' in key):
                        arguments_dictionary.update( {'x' : slice(*self.__formatlimits(self.limits['ilon']))} )
                    elif('y' in key):
                        arguments_dictionary.update( {'y' : slice(*self.__formatlimits(self.limits['ilat']))} )
                    elif('time_counter' in key):
                        arguments_dictionary.update( {'time_counter' : slice(*self.__formatlimits(self.limits['itime']))} )

                # Extract the data 'SELection'
                if _depth_nam is not None: # Squeeze out redundant z dimention
                    ret_item = DS[self.var_name].sel( **arguments_dictionary ).squeeze(_depth_nam).values
                else:
                    ret_item = DS[self.var_name].sel( **arguments_dictionary ).values


            ## Process the format of the extraction
            # Use datetime format
            if self.std_name == 'datetime':
                #print('limits: {}'.format(self.limits))
                ret_item = npdatetime2datetime( ret_item )

            # When xarray loads lat it replaces the zeros with NaNs!
            elif self.std_name == 'lat' or self.std_name == 'lon':
                ret_item[np.isnan(ret_item)] = 0.
                ret_item = np.ma.masked_invalid(ret_item)
            #elif self.std_name == 'datetime':
            #    ret_item = ret_item # datetime does not support mamasked_invalif
            else:
                ret_item = np.ma.masked_invalid(ret_item) # values are masked or 'define_slice' extraction of lat lon limits wont work
            return ret_item
            #return getattr(DS, self.var_name).sel(y=slice(10, 100), x=slice(100, 200)).values

        except KeyError:
            print('a. Cannot find the requested variable '+self.var_name)
        except (IOError, RuntimeError):
            print('a. Cannot open the file '+self.file_name)
        return None


    def get_xarr_attribute_value(self, attr_name):
        """ xarray: Returns the attribute value of the variable """
        try:
            DS = xr.open_dataset(self.file_name)
            #dvar = dataset.variables[self.var_name]
            ret_val = {}
            try:
                #ret_val = dvar.getncattr(attr_name)
                ret_val = getattr(DS, self.var_name).attrs[attr_name]
            except AttributeError:
                ret_val = None
            return ret_val
        except KeyError:
            print('b. Cannot find the requested variable '+self.var_name)
        except (IOError, RuntimeError):
            print('b. Cannot open the file '+self.file_name)
        return None

    def __get_nc4_item__(self):
        """ netcdf4: Returns the data requested """
        try:
            dataset = Dataset(self.file_name, 'r')
            dvar = dataset.variables[self.var_name]
            return dvar
        except KeyError:
            print('c. Cannot find the requested variable '+self.var_name)
        except (IOError, RuntimeError):
            print('c. Cannot open the file '+self.file_name)
        return None

    def get_nc4_attribute_value(self, attr_name):
        """ netcdf4: Returns the attribute value of the variable """
        try:
            dataset = Dataset(self.file_name, 'r')
            dvar = dataset.variables[self.var_name]
            ret_val = {}
            try:
                ret_val = dvar.getncattr(attr_name)
            except AttributeError:
                ret_val = None
            dataset.close()
            return ret_val
        except KeyError:
            print('d. Cannot find the requested variable '+self.var_name)
        except (IOError, RuntimeError):
            print('d. Cannot open the file '+self.file_name)
        return None


    def __formatlimits(self, limitlist):
        if limitlist == None:
            return None, None
        elif type(limitlist[0])==datetime.datetime:
            return limitlist[0].strftime('%Y-%m-%dT%H:%M:%S'), \
                    limitlist[1].strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return int(limitlist[0]),int(limitlist[1])


###################### FUNCTIONS ############################

def PythonVersion():
    """ Find python version """
    return python_version()

def convert_modelvarname_to_stdvarname(var_name):
    """
    Convert model variable name to a stand variable name, which is internal
    to this code
    """
    if 'uos' in var_name or 'uo' in var_name or 'ubar' in var_name:
        return 'ssu'
    elif 'vos' in var_name or 'vo' in var_name or 'vbar' in var_name:
        return 'ssv'
    elif ('surface' in var_name) and ('temperature' in var_name) or ('tos' in var_name) or ('sst' in var_name):
        return 'sst'
    elif ('surface' in var_name) and ('salinity' in var_name) or ('sss' in var_name):
        return 'sss'
    elif 'lat' in var_name:
        return 'lat'
    elif 'lon' in var_name:
        return 'lon'
    elif 'time' in var_name:
        return 'datetime'
    return

def save(thing):
    """ save copy of self into pickle file """
    os.system('rm -f '+SAVE_FILE_NAME)
    if(1):
        with open(SAVE_FILE_NAME, 'wb') as file_object:
            pickle.dump(thing, file_object)
    else:
        print("Don't save as pickle file")
    return

def set_plot_lim(wlim, nav_arr):
    """
    Fill xlim or ylim if empty
    Usage: xlim = set_plot_lim(xlim, nav_lon)
    """
    if wlim==[]:
        wlim = [nav_arr.min(), nav_arr.max()]
    return wlim

def make_gif(files,output,delay=100, repeat=True,**kwargs):
    """
    Uses imageio to produce an animated .gif from a list of
    picture files.
    """

    images = []
    for filename in files:
        images.append(imageio.imread(filename))
    output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output, images, duration=delay)

def findJI(lat, lon, lat_grid, lon_grid):
     """
     Simple routine to find the nearest J,I coordinates for given lat lon
     Usage: [J,I] = findJI(49, -12, nav_lat_grid_T, nav_lon_grid_T)
     """
     dist2 = np.square(lat_grid - lat) + np.square(lon_grid - lon)
     [J,I] = np.unravel_index( dist2.argmin(), dist2.shape  )
     return [J,I]

def nearest(items, pivot):
    """
    This function will return the thing in items which is the closest to the pivot.
    Usage: ind,val = nearest( datetime_arr, date)
    """
    val = min(items, key=lambda x: abs(x - pivot))
    ind = items.index(val)
    return ind, val

def npdatetime2datetime(items):
    """
    Convert numpy datetime object into datetime object via string format
    Only accurate to second. Truncates milleseconds etc
    Assumes format with "T" e.g.
    1966-12-26T12:00:00.000000000
    """
    datetime_obj = []
    for val in items.astype(str):
        datetime_obj.append( datetime.datetime.strptime( \
         val.rstrip('0').rstrip('.'), "%Y-%m-%dT%H:%M:%S") \
            )
    return datetime_obj


###################### CORE CODE ############################

## Now do the main routine stuff
if __name__ == '__main__':

    import importlib

    ## Pass the argument as the configuration file to read
    if len(sys.argv) >1:
        scriptname = sys.argv[0]
        config = sys.argv[1]
    else:
        config = "SEAsia"
        #config = "ORCA0083"
        #config = "ORCA0083_Mauritius"

    ## load the config file
    if os.path.exists(config+"_config.py"):
        exec('import %s_config as params'%config)
    else:
        print('Expecting argument of form XXX, where XXX_config.py exists')
        print('E.g. $ python {} XXX'.format(scriptname))
    #E.g. import SEAsia_config as params
    if "2.7" in python_version():
        print("Need to manually refresh changes to %s_config"%config)
    else:
        importlib.reload(params)
    print("Loading parameters from {}_config".format(config))


    #### Constants
    SAVE_FILE_NAME = config+".pkl"
    INSTRUCTIONS = """

    Choose Action:
    i       to show these instructions
    s       show data bucket contents
    a       add data to bucket

    pcolor  pcolor (some) bucket data
    quiver  pcolor+quiver bucket data

    pa      pcolor anim to file
    qa      pcolor+quiver anim to file

    q       to quit
    """



    ## Do the main program
    c = Controller()



    if(0):
        # plot using class definitions to load data and plot
        print('Manaul plot: using class definitions to load data and plot')
        c.data_bucket.pcolor()


        # plot using class definitions to load data only
        print('Super manaul plot: using  class definitions to load data only')
        icount = 0
        #lab = self.variable + ' at time step:'+str(icount)
        fig = plt.figure()
        plt.pcolormesh( c.data_bucket.vars['lon'], c.data_bucket.vars['lat'], c.data_bucket.vars['sst'][icount,:,:] )
        plt.xlabel('longitude'); plt.ylabel('latitude')
        #plt.title(lab)
        plt.title('Super manual print')
        plt.show()
