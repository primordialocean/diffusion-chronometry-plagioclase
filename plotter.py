import pandas as pd
import matplotlib.pyplot as plt
import json

config = json.load(open("config.json", "r"))
element = config["Element"]

imgfilename = "img.tif"
df_measured = pd.read_csv("sample.csv", header=0)
measured_distance_um = df_measured["Distance (um)"].to_numpy()
measured_ppm = df_measured[element + " (ppm)"].to_numpy()

df_model = pd.read_csv("result.csv", header=0)

model_distance_um = df_model["Distance (um)"].to_numpy()
#An_mol = 100 * df["XAn"].to_numpy()
#analysed_Mg = df["Mg"].to_numpy()
initial_ppm = df_model.iloc[:, 1].to_numpy()
bestfit_ppm = df_model.iloc[:, 1000].to_numpy()


fig, ax = plt.subplots()
ax.plot(measured_distance_um, measured_ppm, "o", c="k")
ax.plot(model_distance_um, initial_ppm, "--", c="k")
ax.plot(model_distance_um, bestfit_ppm, "-", c="r")
ax.set_xlabel(u"Distance (\u03bcm)")
ax.set_ylabel(element + " (ppm)")
ax.set_xlim(0, 60)
ax.set_ylim(0, )
fig.savefig(imgfilename)