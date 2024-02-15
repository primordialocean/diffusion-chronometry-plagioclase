import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fitting(measured, modelled):
    residual = np.sum(
        ((measured[None, :] - modelled) ** 2 / measured[None, :]),
        axis=1) ** 0.5
    residual_min = np.min(residual)
    bestfit_index = np.argwhere(residual == residual_min)
    bestfit_index = bestfit_index[0].item()
    return residual, bestfit_index

df_measured = pd.read_csv("interpolated.csv")
df_model = pd.read_csv("result.csv").drop("Distance (um)", axis=1)

time_s = [float(x) for x in df_model.columns.values]
time_d = [x / (60 * 60 * 24) for x in time_s]
time_y = [x / (60 * 60 * 24 * 365) for x in time_s]

Mg_ppm = df_measured["Mg (ppm)"].to_numpy()

arr_model_Mg_ppm = df_model.T.to_numpy()

residual, bestfit_index = fitting(Mg_ppm, arr_model_Mg_ppm)
pd.DataFrame(
    {
        "Time (s)": time_s,
        "Time (d)": time_d ,
        "Time (y)": time_y,
        "Residual": residual
    }
).to_csv("summary.csv")

df = pd.read_csv("summary.csv")
fig, ax = plt.subplots()
ax.plot(df["Time (d)"], df["Residual"], "-", c="k")
ax.set_xlabel("Time (d)")
ax.set_ylabel("$\Sigma{\sqrt{(c_\mathrm{model}-c_\mathrm{measured})^2}}$")
fig.savefig("residual.tif")