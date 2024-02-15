import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d

filename = "sample.csv"

df = pd.read_csv(filename)

distance_um = df["Distance (um)"].to_numpy()
X_An = df["XAn"].to_numpy()
measured_ppm = df["Mg (ppm)"].to_numpy()
initial_ppm = df["Initial Mg (ppm)"].to_numpy()

min_distance_um = math.floor(distance_um.min()) # round down
max_distance_um = math.ceil(distance_um.max()) # round up

dx_um = 1

interpolated_distance_um \
    = np.arange(min_distance_um, max_distance_um+dx_um, dx_um)

interpolated_X_An \
    = np.interp(interpolated_distance_um, distance_um, X_An)
interpolated_measured_ppm \
    = np.interp(interpolated_distance_um, distance_um, measured_ppm)
interpolated_initial_ppm \
    = np.interp(interpolated_distance_um, distance_um, initial_ppm)


pd.DataFrame(
        {
            "Distance (um)": interpolated_distance_um,
            "XAn": interpolated_X_An,
            "Mg (ppm)": interpolated_measured_ppm,
            "Initial Mg (ppm)": interpolated_initial_ppm
        }
    ).to_csv("interpolated.csv", index=False)