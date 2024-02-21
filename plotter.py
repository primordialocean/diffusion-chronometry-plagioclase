import pandas as pd
import matplotlib.pyplot as plt
import json

config = json.load(open("config.json", "r"))
working_dir = config["Working directory"]
element = config["Element"]
xlim = config["xlim"]
ylim = config["ylim"]
xlabel = config["xlabel"]
ylabel = config["ylabel"]
bestfit_index = config["Bestfit index"]
imgfmt = config["Image format"]

# load measured data
df_measured = pd.read_csv(working_dir + "/input.csv", header=0)
measured_distance_um = df_measured["Distance (um)"].to_numpy()
measured_ppm = df_measured[element + " (ppm)"].to_numpy()

# load preprocessed data
df_preprocessed = pd.read_csv(working_dir + "/preprocessed.csv", header=0)
preprocessed_distance_um = df_preprocessed["Distance (um)"].to_numpy()
initial_ppm = df_preprocessed["Initial " + element + " (ppm)"].to_numpy()
equilibrium_ppm = df_preprocessed["Equilibrium "+ element + " (ppm)"].to_numpy()

# load modelling results
df_model = pd.read_csv(working_dir + "/result.csv", header=0)
model_distance_um = df_model["Distance (um)"].to_numpy()
bestfit_ppm = df_model.iloc[:, bestfit_index].to_numpy()
#plot1_ppm = df_model.iloc[:, 2 * bestfit_index].to_numpy()

# plot data
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(measured_distance_um, measured_ppm, "o", c="w", mec="k")
ax.plot(preprocessed_distance_um, initial_ppm, "--", c="k")
ax.plot(preprocessed_distance_um, equilibrium_ppm, "-", c="k")
ax.plot(model_distance_um, bestfit_ppm, "-", c="r")
#ax.plot(model_distance_um, plot1_ppm, "-", c="r")
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)

fig.savefig(working_dir + "/img." + imgfmt, dpi=300, bbox_inches="tight")