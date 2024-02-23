import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

def fitting(measured, modelled):
    residual = np.sum(
        ((measured[None, :] - modelled) ** 2 / measured[None, :]),
        axis=1) ** 0.5
    residual_min = np.min(residual)
    bestfit_index = np.argwhere(residual == residual_min)
    bestfit_index = bestfit_index[0].item()
    return residual, bestfit_index

config = json.load(open("config.json", "r"))
element = config["Element"]
time_unit_name = config["Time unit"]
working_dir = config["Working directory"]
imgfmt = config["Image format"]
imgres_dpi = config["Image resolution (dpi)"]

df_measured = pd.read_csv(working_dir + "/interpolated.csv")
df_model = pd.read_csv(working_dir + "/result.csv").drop("Distance (m)", axis=1)

time_s = [float(x) for x in df_model.columns.values]
time_d = [x / (60 * 60 * 24) for x in time_s]
time_y = [x / (60 * 60 * 24 * 365.25) for x in time_s]

measured_ppm = df_measured[element + " (ppm)"].to_numpy()

arr_model_ppm = df_model.T.to_numpy()

residual, bestfit_index = fitting(measured_ppm, arr_model_ppm)

pd.DataFrame(
    {
        "Time (s)": time_s,
        "Time (d)": time_d ,
        "Time (y)": time_y,
        "Residual": residual
    }
).to_csv(working_dir + "/summary.csv")

ts_column = {
    "s": "Time (s)",
    "d": "Time (d)",
    "y": "Time (y)"
    }

t_column = ts_column[time_unit_name]

df = pd.read_csv(working_dir + "/summary.csv")
bestfit_time = df[t_column][bestfit_index]
print("Bestfit time: " + str(bestfit_time) + " " + time_unit_name)

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(df[t_column], df["Residual"], "-", c="k")
ax.axvline(x=bestfit_time, c="r")
ax.set_xlim(0, )
ax.set_ylim(0, )
ax.set_title(str(int(bestfit_time)) + " " + time_unit_name)
ax.set_xlabel(t_column)
ax.set_ylabel("$\Sigma{\sqrt{(c_\mathrm{model}-c_\mathrm{measured})^2}}$")
fig.savefig(working_dir + "/residual." + imgfmt, dpi=imgres_dpi, bbox_inches="tight")