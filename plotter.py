import pandas as pd
import matplotlib.pyplot as plt
import json

with open("config.json") as f:
    config = json.load(f)
working_dir = config["Working directory"]
element = config["Element"]
xlim = config["xlim"]
ylim_An = config["ylim An"]
ylim_model = config["ylim model"]
xlabel = config["xlabel"]
ylabel = config["ylabel"]
time_unit_name = config["Time unit"]
time_column_name = "Time (" + time_unit_name + ")"
bestfit_time = config["Bestfit time"]
otherplots = config["Other plots"]
plot1_time = config["Plot1 time"]
plot2_time = config["Plot2 time"]
plot3_time = config["Plot3 time"]
imgfmt = config["Image format"]
imgres_dpi = config["Image resolution (dpi)"]

df_summary = pd.read_csv(working_dir + "/summary.csv", header=0)
bestfit_index = (df_summary[time_column_name] - bestfit_time).abs().idxmin()
plot1_index = (df_summary[time_column_name] - plot1_time).abs().idxmin()
plot2_index = (df_summary[time_column_name] - plot2_time).abs().idxmin()
plot3_index = (df_summary[time_column_name] - plot3_time).abs().idxmin()

# load measured data
df_measured = pd.read_csv(working_dir + "/input.csv", header=0)
measured_distance_um = df_measured["Distance (um)"].to_numpy()
measured_ppm = df_measured[element + " (ppm)"].to_numpy()
measured_An_mol = df_measured["An (mol%)"].to_numpy()

# load preprocessed data
df_preprocessed = pd.read_csv(working_dir + "/preprocessed.csv", header=0)
preprocessed_distance_um = df_preprocessed["Distance (um)"].to_numpy()
initial_ppm = df_preprocessed["Initial " + element + " (ppm)"].to_numpy()
equilibrium_ppm = df_preprocessed["Equilibrium "+ element + " (ppm)"].to_numpy()

# load modelling results
df_model = pd.read_csv(working_dir + "/result.csv", header=0)
bestfit_ppm = df_model.iloc[:, bestfit_index].to_numpy()
plot1_ppm = df_model.iloc[:, plot1_index].to_numpy()
plot2_ppm = df_model.iloc[:, plot2_index].to_numpy()
plot3_ppm = df_model.iloc[:, plot3_index].to_numpy()

# plot data
fig, ax = plt.subplots(2, 1, figsize=(5, 8), sharex=True)
fig.subplots_adjust(hspace=0.07)
ax[0].plot(measured_distance_um, measured_An_mol, "o", c="w", mec="k")
ax[0].set_ylabel("An (mol%)")
ax[0].set_ylim(*ylim_An)

ax[1].plot(measured_distance_um, measured_ppm, "o", c="w", mec="k")
ax[1].plot(preprocessed_distance_um, initial_ppm, "--", c="k", label="Initial")
ax[1].plot(preprocessed_distance_um, equilibrium_ppm, "-", c="k", label="Equilibrium")

ax[1].plot(
    preprocessed_distance_um, bestfit_ppm, "-", c="r",
    label="Bestfit " + str(round(bestfit_time)) + " " + time_unit_name
    )

if otherplots == "True":
    ax[1].plot(
        preprocessed_distance_um, plot1_ppm, "-", c="#4F1167",
        label=str(round(plot1_time)) + " " + time_unit_name
        )

    ax[1].plot(
        preprocessed_distance_um, plot2_ppm, "-", c="#01B085",
        label=str(round(plot2_time)) + " " + time_unit_name
        )

    ax[1].plot(
        preprocessed_distance_um, plot3_ppm, "-", c="#FFE529",
        label=str(round(plot3_time)) + " " + time_unit_name
        )
elif otherplots == "False":
    pass

ax[1].set_xlabel(xlabel)
ax[1].set_ylabel(ylabel)
ax[1].set_xlim(*xlim)
ax[1].set_ylim(*ylim_model)
ax[1].legend(fontsize=6)
fig.savefig(working_dir + "/img." + imgfmt, dpi=imgres_dpi, bbox_inches="tight")