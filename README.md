# Belize workshop: NEMO regional model

![Salinity snapshot for the Belize domain](https://github.com/NOC-MSM/SANH/wiki/FIGURES/screenshot.png)

Getting started
===============

**Clone** this repository onto your favourite linux box:

<pre>
  git clone git@github.com:NOC-MSM/Belize_workshop.git
</pre>

Copy forcing, configuration data from somewhere **JASMIN** / USB stick?

<pre>
  wget ...
</pre>


To run NEMO, Follow instructions in the wiki:

[Build Docker Container and Download NEMO](https://github.com/NOC-MSM/Belize_workshop/wiki/Level-1:-Get-and-Build-Docker-Container-and-NEMO-Met-Surge-Config)  

[Get supporting files and Run NEMO](https://github.com/NOC-MSM/Belize_workshop/wiki/Level-2:-Get-Domain-And-Forcing-Files-Run)


To do other stuff, do other stuff...



File Hierarchy
==============

Each configuration directory should be laid out in the following manner, to
facilitate configuration archival and sharing:

<pre>
Belize_workshop
|
|__ BUILD_TOOLS
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
|   |__  EXP_demo
|   |__ PARCELS_demo
|
|__ PYTHON_DIAGNOSTICS
|__ README.md

</pre>

External files required

<pre>
runoff.nc
initcd_votemper.nc
initcd_vosaline.nc
domain_cfg.nc
coordinates.bdy.nc
metdta
bdydta

</pre>
