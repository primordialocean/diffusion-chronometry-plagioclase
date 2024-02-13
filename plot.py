import pandas as pd
import matplotlib.pyplot as plt

filename = "result.csv"
imgfilename = "img.tif"

df = pd.read_csv(filename)
print(df.head())

distance_um = df["Distance (um)"].to_numpy()
#An_mol = 100 * df["XAn"].to_numpy()
#analysed_Mg = df["Mg"].to_numpy()
initial_Mg_ppm = df[0.0].to_numpy()


fig, ax = plt.subplots()
#ax.plot(distance_um, analysed_Mg, "o", c="k")
#ax.plot(distance_um, initial_Mg_ppm, "--", c="k")
ax.set_xlabel(u"Distance (\u03bcm)")
ax.set_ylabel("Mg (ppm)")
ax.set_xlim(0,)
ax.set_ylim(0, 240)
fig.savefig(imgfilename)