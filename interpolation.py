import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d
import json

config = json.load(open("config.json", "r"))
element = config["Element"]
content = config["Content"]
dx_um = config["distance step (um)"]
working_dir = config["Working directory"]

df = pd.read_csv(working_dir + "/input.csv")

distance_um = df["Distance (um)"].to_numpy()
An_mol = df["An (mol%)"].to_numpy()
measured_content = df[content].to_numpy()
initial_content = df["Initial "+ content].to_numpy()

min_distance_um = math.floor(distance_um.min()) # round down
max_distance_um = math.ceil(distance_um.max()) # round up

interpolated_distance_um \
    = np.arange(min_distance_um, max_distance_um + dx_um, dx_um)

interpolated_An_mol \
    = np.interp(interpolated_distance_um, distance_um, An_mol)
interpolated_measured_content \
    = np.interp(interpolated_distance_um, distance_um, measured_content)
interpolated_initial_content \
    = np.interp(interpolated_distance_um, distance_um, initial_content)

pd.DataFrame(
        {
            "Distance (um)": interpolated_distance_um,
            "An (mol%)": interpolated_An_mol,
            content: interpolated_measured_content,
            "Initial " + content: interpolated_initial_content
        }
    ).to_csv(working_dir + "/interpolated.csv", index=False)