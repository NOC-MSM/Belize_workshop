# Belize workshop: NEMO regional model

![Salinity snapshot for the Belize domain](https://github.com/NOC-MSM/Belize_workshop/wiki/FIGURES/screenshot.png)

Instructions and code examples to build and run a regional NEMO (https://www.nemo-ocean.eu/) ocean model and apply some post simulation analysis. The workflow uses Docker containers and are designed to be run on consumer laptops. We cover the following topics:

- Introduction to Docker
- Download and setup Docker.
- Download and setup (or build) NEMO and XIOS server in a Docker container.
- Running NEMO
- Download and setup Miniconda (Python) in a Docker container.
- Plotting and animating surface fields with Python.
- Analysis of NEMO outputs with PARCELS.

This work has been supported by a number of projects:
*  Addressing Challenges of Coastal Communities through Ocean Research for Developing Economies [ACCORD](https://projects.noc.ac.uk/accord/). NERC [NE/R000123/1](http://gotw.nerc.ac.uk/list_full.asp?pcode=NE%2FR000123%2F1) - providing international partners in eight developing economy countries scientific evidence and capability to ensure sustainable growth of their blue economies.

* The [Commonwealth Marine Economies Programme](http://projects.noc.ac.uk/cme-programme/) "Enabling safe and sustainable marine economies across Commonwealth Small Island Developing States". The Commonwealth Marine Economies (CME) Programme was announced by the British Prime Minister in 2015 to help Commonwealth Small Island Developing States (SIDS) make the most of their natural maritime advantages, to enable sustainable economic growth and alleviate poverty.

* Marine World Modelling Systems for Yucatan Economic Development: A British Council funded workshop (25-29 November 2019, Merida, Yucatan, Mexico) enabled through the Higher Education Alliances program. This facilitated the creation of the workshop material.


Getting started
===============

**Clone** this repository onto your favourite linux box:

<pre>
  git clone git@github.com:NOC-MSM/Belize_workshop.git
</pre>

Copy forcing, configuration data from somewhere ftp site / USB stick?

<pre>
  wget ...
</pre>


To run NEMO, Follow instructions in the [wiki](https://github.com/NOC-MSM/Belize_workshop/wiki/About-this-workshop...)

To do other stuff, do other stuff...



File Hierarchy
==============

Each configuration directory should be laid out in the following manner, to
facilitate configuration archival and sharing:

<pre>

Belize_workshop
|
|__ BUILD_NEMO
|   |__ Docker
|   |__ NEMOGCM
|   |__ XIOS2
|   |__ arch_NEMOGCM
|   |__ arch_XIOS
|   |__ cpp_BLZ.fcm
|   |__ readme.txt
|   |__ xios-2.0_r1242
|
|__ RUN_NEMO
|   |__ EXP_demo
|
|__ PYTHON_DIAGNOSTICS
|__ PARCELS_DEMO
|__ README.md

</pre>

External files required in EXP_demo. Available from ftp site:

<pre>
runoff.nc
initcd_votemper.nc
initcd_vosaline.nc
domain_cfg.nc
coordinates.bdy.nc
metdta
bdydta

</pre>
