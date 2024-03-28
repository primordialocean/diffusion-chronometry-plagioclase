import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from constants import Units

def fitting(measured, modelled):
    residual = (
        np.sum(((measured[None, :] - modelled) ** 2) ** 0.5, axis=1) / len(measured)
        )
    residual_min = np.min(residual)
    bestfit_index = np.argwhere(residual == residual_min)
    bestfit_index = bestfit_index[0].item()
    return residual, bestfit_index

def fitting_slope(dt_s, measured, modelled, slope_threshold):
    residual = (
        np.sum(((measured[None, :] - modelled) ** 2) ** 0.5, axis=1) / len(measured)
        )
    for i in range(1, len(residual)):
        if i == len(residual)-1:
            bestfit_index = i
            print("Caution! Set enough max time.")
            break
        # if miscatch bestfit time, set delay time as nt.
        # if i < 1000: continue
        # wt% per second
        slope = (residual[i] - residual[i-1]) / dt_s
        if slope > slope_threshold:
            bestfit_index = i
            break
    return residual, bestfit_index

units = Units()
TIME_UNITS = units.TIME_UNITS

# load configfile
with open("config.json") as f:
    config = json.load(f)

working_dir = config["Working directory"]
element = config["Element"]
content = config["Content"]
time_unit_name = config["Time unit"]
time_column_name = "Time (" + time_unit_name + ")"
fitting_algorithm = config["Fitting algorithm"]
slope_threshold = config["Slope threshold"]
imgfmt = config["Image format"]
imgres_dpi = config["Image resolution (dpi)"]

df_measured = pd.read_csv(working_dir + "/interpolated.csv")
df_model = pd.read_csv(working_dir + "/result.csv").drop("Distance (m)", axis=1)

times_s = [float(x) for x in df_model.columns.values]
dt_s = times_s[1] - times_s[0]
times = [time_s / TIME_UNITS[time_unit_name] for time_s in times_s]

measured_content = df_measured[content].to_numpy()

arr_model_content = df_model.T.to_numpy()

if fitting_algorithm == "Minimum":
    residual, bestfit_index = fitting(measured_content, arr_model_content)
elif fitting_algorithm == "Slope":
    residual, bestfit_index = fitting_slope(dt_s, measured_content, arr_model_content, slope_threshold)

pd.DataFrame(
    {
        time_column_name: times,
        "Residual": residual
    }
).to_csv(working_dir + "/summary.csv")

df = pd.read_csv(working_dir + "/summary.csv")
bestfit_time = df[time_column_name][bestfit_index]

print("Bestfit time: " + str(bestfit_time) + " " + time_unit_name)

# visualise fitting results
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(df[time_column_name], df["Residual"], "-", c="k")
ax.axvline(x=bestfit_time, c="r")
ax.set_xlim(0, )
ax.set_ylim(0, )
ax.set_title(str(round(bestfit_time)) + " " + time_unit_name)
ax.set_xlabel("Time (" + time_unit_name + ")")
ax.set_ylabel(r"$\frac{\Sigma{\sqrt{(c_\mathrm{model}-c_\mathrm{measured})^2}}}{n_\mathrm{Distance}}$")
fig.savefig(working_dir + "/residual." + imgfmt, dpi=imgres_dpi, bbox_inches="tight")

# export bestfit time to config.json
config["Bestfit time"] = bestfit_time
update_config = json.dumps(config, indent=4)

with open("config.json", "w") as f:
    f.write(update_config)