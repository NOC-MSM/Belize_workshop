from parcels import FieldSet, ParticleSet, ScipyParticle, JITParticle, AdvectionRK4, ParticleFile
from argparse import ArgumentParser
import numpy as np
import pytest
from glob import glob
from datetime import timedelta as delta
from os import path
import time
from netCDF4 import Dataset

start = time.time()
# data_path = path.join(path.dirname(__file__), 'NemoCurvilinear_data/')
data_path = '/Belize_workshop/RUN_NEMO/EXP_demo/'
#data_path = '/PARCELS/TinnyBelize/'
ufiles = sorted(glob(data_path+'BLZE12_C1_1h_*10_grid_U.nc'))
vfiles = sorted(glob(data_path+'BLZE12_C1_1h_*10_grid_V.nc'))

grid_file = data_path+'domain_cfg.nc'
filenames = {'U': {'lon': grid_file,
                       'lat': grid_file,
                       'data': ufiles},
                 'V': {'lon': grid_file,
                       'lat': grid_file,
                       'data': vfiles}}
variables = {'U': 'ubar', 'V': 'vbar'}
dimensions = {'lon': 'glamf', 'lat': 'gphif','time': 'time_counter' }
field_set = FieldSet.from_nemo(filenames, variables, dimensions)
	
	#Plot u field
#field_set.U.show()

    # Make particles initial position list
nc_fid = Dataset(grid_file, 'r') #open grid file nc to read
#lats = nc_fid.variables['nav_lat'][:]  # extract/copy the data
#lons = nc_fid.variables['nav_lon'][:]

#lonE=lons[:,169-3]
#latE=lats[:,169-3]

npart = 30
lonp = [i for i in np.linspace(-88.18, -88.20, npart)] 
latp = [i for i in np.linspace(17.52, 17.53, npart)] #this makes a list!

	
pset = ParticleSet.from_list(field_set, JITParticle, lon=lonp, lat=latp)
pfile = ParticleFile("tBelize_nemo_particles_30halfD", pset, outputdt=delta(hours=0.5))
kernels = pset.Kernel(AdvectionRK4)
#Plot initial positions
#pset.show()

pset.execute(kernels, runtime=delta(days=0.5), dt=delta(hours=0.1), output_file=pfile)
#plotTrajectoriesFile("Belize_nemo_particles_t2.nc");

#pset.show(domain={'N':-31, 'S':-35, 'E':33, 'W':26})
#pset.show(field=field_set.U)
#pset.show(field=fieldset.U, show_time=datetime(2002, 1, 10, 2))
#pset.show(field=fieldset.U, show_time=datetime(2002, 1, 10, 2), with_particles=False)


end = time.time()
print(end-start)
