import pandas as pd
import json
from constants import PhysicalConstants, Units
from partitioncoef import PartitionCoefficients

physconsts = PhysicalConstants()
KELVIN = physconsts.KELVIN

with open("config.json") as f:
    config = json.load(f)
working_dir = config["Working directory"]
element = config["Element"]
content = config["Content"]
melt_content = config["melt " + content]
K_model = config["Partition coefficient model"]
K_ref = config["Partition coefficient"]

factors = config["Initial estimation"]
factor_temp = factors["T (C)"]
factor_element = factors["melt " + content]
factor_SiO2 = factors["melt SiO2 (wt%)"]

df = pd.read_excel(working_dir + "/input.xlsx")

distance_um = df["Distance (um)"].to_numpy()
An_mol = df["An (mol%)"].to_numpy()
X_An = 0.01 * df["An (mol%)"].to_numpy()
measured_content = df[content].to_numpy()
initial_T_C = factor_temp[0] * An_mol + factor_temp[1]
initial_T_K = initial_T_C + KELVIN
initial_melt_content = factor_element[0] * An_mol + factor_element[1]
initial_melt_SiO2_wt = factor_SiO2[0] * An_mol + factor_SiO2[1]

# import partition coefficiation class
pc = PartitionCoefficients()
# select reference
if K_model == "Mutch2022":
    A_i, K_i = pc.mutch_model(
        K_ref, element, initial_T_K, X_An, initial_melt_SiO2_wt
        )
elif K_model == "Empirical":
    A_i, K_i = pc.empirical_model(K_ref, element, initial_T_K, X_An)

initial_content = K_i * initial_melt_content
initial_content[0] = K_i[0] * melt_content

df = pd.DataFrame(
        {
            "Distance (um)": distance_um,
            "An (mol%)": An_mol,
            content: measured_content,
            "Initial T (C)": initial_T_C,
            "Initial melt SiO2 (wt%)": initial_melt_SiO2_wt,
            "Initial melt " + content: initial_melt_content,
            "Initial " + content: initial_content
        }
    )
df.to_csv(working_dir + "/input.csv", index=False)