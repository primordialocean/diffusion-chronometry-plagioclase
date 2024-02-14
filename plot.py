import pandas as pd
import matplotlib.pyplot as plt

filename = "result.csv"
imgfilename = "img.tif"

df = pd.read_csv(filename, header=0)

distance_um = df["Distance (um)"].to_numpy()
#An_mol = 100 * df["XAn"].to_numpy()
#analysed_Mg = df["Mg"].to_numpy()
initial_Mg_ppm = df.iloc[:, 1].to_numpy()
bestfit_Mg_ppm = df.iloc[:, 100].to_numpy()


fig, ax = plt.subplots()
ax.plot(distance_um, initial_Mg_ppm, "--", c="k")
ax.plot(distance_um, bestfit_Mg_ppm, "-", c="r")
ax.set_xlabel(u"Distance (\u03bcm)")
ax.set_ylabel("Mg (ppm)")
ax.set_xlim(0, 60)
ax.set_ylim(0, )
fig.savefig(imgfilename)