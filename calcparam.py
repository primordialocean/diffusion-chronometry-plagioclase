import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

class PhysicalConstant:
    def __init__(self):
        self.R_CONST = 8.31 # J/mol
        self.KELVIN = 273.15
        self.um = 1e-6 # um to m
        self.year = 60 * 60 * 24 * 365 # year to second
        self.day = 60 * 60 * 24 # day to second

# load pysical constants
const = PhysicalConstant()
KELVIN = const.KELVIN

# load setting file
config = json.load(open("config.json", "r"))
working_dir = config["Working directory"]
element = config["Element"]
melt_SiO2_wt = config["melt SiO2 (wt%)"]
T_C = config["T (C)"]
T_K = T_C + KELVIN
imgfmt = config["Image format"]
imgres_dpi = config["Image resolution (dpi)"]

class PartitionCoefficient(PhysicalConstant):
    def __init__(self):
        super().__init__()
    
    def mutch2022(self, T_K, X_An, melt_SiO2_wt):
        X_An_dev = X_An - (0.12 + 0.00038 * T_K)
        beta = np.where(X_An_dev <= 0, 0, 1)
        RTlnK = (16900 - 37200 * beta) * X_An_dev \
            + 830 * melt_SiO2_wt - 83300
        RTlnK_kJ = RTlnK * 1e-3
        return RTlnK_kJ

df = pd.read_csv(working_dir + "/input.csv")

An_mol = df["An (mol%)"].to_numpy()
X_An = 0.01 * An_mol
min_X_An = X_An.min()
max_X_An = X_An.max()
X_An_arr = np.arange(0, 1, 0.001)

pc = PartitionCoefficient()
RTlnK_kJ_arr = pc.mutch2022(T_K, X_An_arr, melt_SiO2_wt)
RTlnK_kJ = pc.mutch2022(T_K, X_An, melt_SiO2_wt)
RTlnK_kJ_min_XAn = pc.mutch2022(T_K, min_X_An, melt_SiO2_wt)
RTlnK_kJ_max_XAn = pc.mutch2022(T_K, max_X_An, melt_SiO2_wt)

A_kJ = (RTlnK_kJ_max_XAn - RTlnK_kJ_min_XAn) / (max_X_An - min_X_An)
A_J = A_kJ * 1e3
print("A = " + str(round(A_J)) + " J")

fig, ax = plt.subplots(figsize=(5,5))
ax.text(
    0.99, 0.99,
    "$A = $"+ str(round(A_kJ, 1)).replace("-", "−") + " kJ",
    va='top', ha='right', transform=ax.transAxes,
    fontsize=11
    )
ax.plot(X_An_arr, RTlnK_kJ_arr, "--", c="k")
ax.plot(
    [min_X_An, max_X_An], [RTlnK_kJ_min_XAn, RTlnK_kJ_max_XAn],
    "-o", c="r"
    )
ax.set_title(
    str(melt_SiO2_wt) + " wt% SiO$_2$, " + str(T_C)+" $^\circ$C",
    fontsize=10
    )
ax.set_xlim(0, 1)
ax.set_ylim(-60, -10)
ax.set_xlabel("$X_\mathrm{An}$")
ax.set_ylabel("$RT\ln{K_D}$ (kJ mol$^{-1}$)")
fig.savefig(working_dir +  "/pc." + imgfmt, dpi=imgres_dpi, bbox_inches="tight")