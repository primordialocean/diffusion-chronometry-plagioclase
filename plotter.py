import pandas as pd
import matplotlib.pyplot as plt

imgfilename = "img.tif"

df_measured = pd.read_csv("sample.csv", header=0)
measured_distance_um = df_measured["Distance (um)"].to_numpy()
Mg_ppm = df_measured["Mg (ppm)"].to_numpy()

df_model = pd.read_csv("result.csv", header=0)

model_distance_um = df_model["Distance (um)"].to_numpy()
#An_mol = 100 * df["XAn"].to_numpy()
#analysed_Mg = df["Mg"].to_numpy()
initial_Mg_ppm = df_model.iloc[:, 1].to_numpy()
bestfit_Mg_ppm = df_model.iloc[:, 1000].to_numpy()


fig, ax = plt.subplots()
ax.plot(measured_distance_um, Mg_ppm, "o", c="k")
ax.plot(model_distance_um, initial_Mg_ppm, "--", c="k")
ax.plot(model_distance_um, bestfit_Mg_ppm, "-", c="r")
ax.set_xlabel(u"Distance (\u03bcm)")
ax.set_ylabel("Mg (ppm)")
ax.set_xlim(0, 60)
ax.set_ylim(0, )
fig.savefig(imgfilename)