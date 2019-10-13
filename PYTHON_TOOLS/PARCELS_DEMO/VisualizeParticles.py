from parcels import plotTrajectoriesFile
import matplotlib.pyplot as plt

plotTrajectoriesFile("tBelize_nemo_particles.nc");

plt.savefig('./pFIGURES/postTrajPlotT1.png', dpi=100)