# Belize workshop: NEMO regional model

![Salinity snapshot for the Belize domain](https://github.com/NOC-MSM/Belize_workshop/wiki/FIGURES/screenshot.png)

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
