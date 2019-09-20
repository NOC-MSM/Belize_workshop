### Installs the framework for running PARCELS and Python Diagnostics ##
########################################################################
FROM continuumio/miniconda3
MAINTAINER Jeff Polton, jelt@noc.ac.uk

RUN conda install --yes \
	-c conda-forge python=3 parcels jupyter cartopy ffmpeg netcdf4=1.4.1 cmocean dask xarray imageio

### dependencies for PARCELS:
# livljobs6: module load anaconda/3-2018_12
# conda create -n py3_parcels -c conda-forge python=3 parcels jupyter cartopy ffmpeg netcdf4=1.4.1
### notes:
# ssh, nano are not mandatory but useful when we have to work in the container
#ENV PACKAGES="ssh nano python3.7 python3-pip"

### first update then install the main packages
#RUN apt-get update -y && \
#    apt-get install -y --no-install-recommends ${PACKAGES} 

#RUN  python3 -m pip install -r requirements.txt
