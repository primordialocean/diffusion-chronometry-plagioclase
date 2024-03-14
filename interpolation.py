import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d
import json

config = json.load(open("config.json", "r"))
element = config["Element"]
element_unit = config["Element unit"]
content_unit = element + " (" + element_unit + ")"
dx_um = config["distance step (um)"]
working_dir = config["Working directory"]

df = pd.read_excel(working_dir + "/input.xlsx")

distance_um = df["Distance (um)"].to_numpy()
An_mol = df["An (mol%)"].to_numpy()
measured_content = df[content_unit].to_numpy()
initial_content = df["Initial "+ content_unit].to_numpy()

min_distance_um = math.floor(distance_um.min()) # round down
max_distance_um = math.ceil(distance_um.max()) # round up

interpolated_distance_um \
    = np.arange(min_distance_um, max_distance_um+dx_um, dx_um)

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
            content_unit: interpolated_measured_content,
            "Initial " + content_unit: interpolated_initial_content
        }
    ).to_csv(working_dir + "/interpolated.csv", index=False)