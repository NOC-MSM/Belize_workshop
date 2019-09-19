# Belize workshop: NEMO regional model

![Bathymetry for SANH domain](https://github.com/NOC-MSM/SANH/wiki/FIGURES/SANH_bathy.png)

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
BoBEAS
|
|__ ARCH
|__ EXP_2016
|__ EXP_Apr19
|__ MY_SRC
|__ SCRIPTS
|__ STARTFILES
|
|__ .gitignore
|__ README.md
|__ cpp_file.fcm
</pre>
