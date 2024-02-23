import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from constants import Units

def fitting(measured, modelled):
    residual = np.sum(
        ((measured[None, :] - modelled) ** 2 / measured[None, :]),
        axis=1) ** 0.5
    residual_min = np.min(residual)
    bestfit_index = np.argwhere(residual == residual_min)
    bestfit_index = bestfit_index[0].item()
    return residual, bestfit_index

units = Units()
DAY = units.DAY
YEAR = units.YEAR

config = json.load(open("config.json", "r"))
element = config["Element"]
time_unit_name = config["Time unit"]
working_dir = config["Working directory"]
imgfmt = config["Image format"]
imgres_dpi = config["Image resolution (dpi)"]

df_measured = pd.read_csv(working_dir + "/interpolated.csv")
df_model = pd.read_csv(working_dir + "/result.csv").drop("Distance (m)", axis=1)

times_s = [float(x) for x in df_model.columns.values]
times_d = [time_s / DAY for time_s in times_s]
times_y = [time_s / YEAR for time_s in times_s]

measured_ppm = df_measured[element + " (ppm)"].to_numpy()

arr_model_ppm = df_model.T.to_numpy()

residual, bestfit_index = fitting(measured_ppm, arr_model_ppm)

pd.DataFrame(
    {
        "Time (s)": times_s,
        "Time (d)": times_d ,
        "Time (y)": times_y,
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