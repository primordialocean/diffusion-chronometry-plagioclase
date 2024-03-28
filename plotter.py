import pandas as pd
import matplotlib.pyplot as plt
import json

with open("config.json") as f:
    config = json.load(f)
working_dir = config["Working directory"]
element = config["Element"]
content = config["Content"]
ylim_An = config["ylim An"]
ylim_model = config["ylim model"]
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
df_measured = pd.read_csv(working_dir + "/input.csv")
measured_distance_um = df_measured["Distance (um)"].to_numpy()
measured_content = df_measured[content].to_numpy()
measured_An_mol = df_measured["An (mol%)"].to_numpy()

# load preprocessed data
df_preprocessed = pd.read_csv(working_dir + "/preprocessed.csv", header=0)
preprocessed_distance_um = df_preprocessed["Distance (um)"].to_numpy()
initial_content = df_preprocessed["Initial " + content].to_numpy()
equilibrium_content = df_preprocessed["Equilibrium "+ content].to_numpy()
preprocessed_An_mol = df_preprocessed["An (mol%)"].to_numpy()

# load modelling results
df_model = pd.read_csv(working_dir + "/result.csv", header=0)
bestfit_content = df_model.iloc[:, bestfit_index].to_numpy()
plot1_content = df_model.iloc[:, plot1_index].to_numpy()
plot2_content = df_model.iloc[:, plot2_index].to_numpy()
plot3_content = df_model.iloc[:, plot3_index].to_numpy()

# plot data
fig, ax = plt.subplots(2, 1, figsize=(5, 8), sharex=True)
fig.subplots_adjust(hspace=0.08)
ax[0].plot(measured_distance_um, measured_An_mol, "o", c="w", mec="k", label="Observed")
ax[0].plot(preprocessed_distance_um, preprocessed_An_mol, "-", c="k", label="Interpolated")
ax[0].set_ylabel("An (mol%)")
ax[0].set_ylim(*ylim_An)
ax[0].legend(
    edgecolor="w",
    loc="center left",
    bbox_to_anchor=(1, 0.5), fontsize=9
    ).set_alpha(1)

ax[1].plot(measured_distance_um, measured_content, "o", c="w", mec="k", label="Observed")
ax[1].plot(preprocessed_distance_um, initial_content, "--", c="k", label="Initial")
ax[1].plot(preprocessed_distance_um, equilibrium_content, "-", c="k", label="Equilibrium")

ax[1].plot(
    preprocessed_distance_um, bestfit_content, "-", c="r",
    label="Bestfit " + str(round(bestfit_time)) + " " + time_unit_name
    )

if otherplots == "True":
    ax[1].plot(
        preprocessed_distance_um, plot1_content, "-", c="#4F1167",
        label=str(round(plot1_time)) + " " + time_unit_name
        )

    ax[1].plot(
        preprocessed_distance_um, plot2_content, "-", c="#01B085",
        label=str(round(plot2_time)) + " " + time_unit_name
        )

    ax[1].plot(
        preprocessed_distance_um, plot3_content, "-", c="#FFE529",
        label=str(round(plot3_time)) + " " + time_unit_name
        )
elif otherplots == "False":
    pass

ax[1].set_xlabel(r"Distance ($\times 10^{-6}$ m)")
ax[1].set_ylabel(content)
ax[1].set_ylim(*ylim_model)
ax[1].legend(
    edgecolor="w",
    loc="center left",
    bbox_to_anchor=(1, 0.5), fontsize=9
    ).set_alpha(1)
fig.savefig(working_dir + "/img." + imgfmt, dpi=imgres_dpi, bbox_inches="tight")