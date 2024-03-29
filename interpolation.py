import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d
import json

config = json.load(open("config.json", "r"))
element = config["Element"]
dx_um = config["distance step (um)"]
working_dir = config["Working directory"]

df = pd.read_excel(working_dir + "/input.xlsx")

distance_um = df["Distance (um)"].to_numpy()
An_mol = df["An (mol%)"].to_numpy()
measured_ppm = df[element + " (ppm)"].to_numpy()
initial_ppm = df["Initial "+ element +" (ppm)"].to_numpy()

min_distance_um = math.floor(distance_um.min()) # round down
max_distance_um = math.ceil(distance_um.max()) # round up

interpolated_distance_um \
    = np.arange(min_distance_um, max_distance_um+dx_um, dx_um)

interpolated_An_mol \
    = np.interp(interpolated_distance_um, distance_um, An_mol)
interpolated_measured_ppm \
    = np.interp(interpolated_distance_um, distance_um, measured_ppm)
interpolated_initial_ppm \
    = np.interp(interpolated_distance_um, distance_um, initial_ppm)

pd.DataFrame(
        {
            "Distance (um)": interpolated_distance_um,
            "An (mol%)": interpolated_An_mol,
            element + " (ppm)": interpolated_measured_ppm,
            "Initial " + element + " (ppm)": interpolated_initial_ppm
        }
    ).to_csv(working_dir + "/interpolated.csv", index=False)