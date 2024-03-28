import pandas as pd
import json

with open("config.json") as f:
    config = json.load(f)
working_dir = config["Working directory"]

content = config["Content"]

df = pd.read_excel(working_dir + "/input.xlsx")

distance_um = df["Distance (um)"].to_numpy()
An_mol = df["An (mol%)"].to_numpy()
X_An = 0.01 * df["An (mol%)"].to_numpy()
measured_content = df[content].to_numpy()

initial_content = 0.008 * An_mol - 0.38

df = pd.DataFrame(
        {
            "Distance (um)": distance_um,
            "An (mol%)": An_mol,
            content: measured_content,
            "Initial " + content: initial_content
        }
    )
df.to_csv(working_dir + "/input.csv", index=False)