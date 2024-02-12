import pandas as pd
import matplotlib.pyplot as plt

filename = "summary.xlsx"
sheetname = "input"
imgfilename = "img.tif"

df = pd.read_excel(filename, sheet_name=sheetname)

distance_um = df["Distance (um)"].to_numpy()
An_mol = 100 * df["XAn"].to_numpy()
analysed_Mg = df["Mg"].to_numpy()
initial_Mg = df["Initial Mg"].to_numpy()

fig, ax = plt.subplots()
ax.plot(distance_um, analysed_Mg, "o", c="k")
ax.plot(distance_um, initial_Mg, "--", c="k")
ax.set_xlabel(u"Distance (\u03bcm)")
ax.set_ylabel("Mg (ppm)")
ax.set_xlim(0,)
ax.set_ylim(0, 240)
fig.savefig(imgfilename)