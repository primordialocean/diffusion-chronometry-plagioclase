import numpy as np
import pandas as pd
import json
from scipy.ndimage import gaussian_filter
from constants import PhysicalConstants, Units
from partitioncoef import PartitionCoefficients
from diffusioncoef import DiffusionCoefficients

def main():
    # load physicalconstants
    physconsts = PhysicalConstants()
    KELVIN = physconsts.KELVIN

    # load units
    units = Units()
    UM = units.UM
    YEAR = units.YEAR

    # load configuration file
    with open("config.json") as f:
        config = json.load(f)
    working_dir = config["Working directory"]
    element = config["Element"]
    content = config["Content"]
    K_model = config["Partition coefficient model"]
    K_ref = config["Partition coefficient"]
    D_ref = config["Diffusion coefficient"]
    T_C = config["T (C)"]
    T_K = T_C + KELVIN
    melt_SiO2_wt = config["melt SiO2 (wt%)"]
    maxtime_s = config["Max time"] * YEAR
    key_smoothing = config["Smoothing"]
    filter_sigma = config["Filter sigma"]
    
    # load interpolated initial and measured datasets
    df = pd.read_csv(working_dir + "/interpolated.csv")
    distance_um = df["Distance (um)"].to_numpy()
    distance_m = distance_um * UM
    An_mol = df["An (mol%)"].to_numpy()
    if key_smoothing == "True":
        An_mol = gaussian_filter(An_mol, filter_sigma)
    else:
        pass
    X_An = 0.01 * An_mol
    measured_content = df[content].to_numpy()
    initial_content = df["Initial " + content].to_numpy()

    # import partition coefficiation class
    pc = PartitionCoefficients()
    # select reference
    if K_model == "Mutch2022":
        A_i, K_i = pc.mutch_model(K_ref, element, T_K, X_An, melt_SiO2_wt)
    elif K_model == "Empirical":
        A_i, K_i = pc.empirical_model(K_ref, element, T_K, X_An)
    
    # estimate melt Mg from rimward composition
    melt_content = measured_content[0] / K_i[0]
    # melt_content = initial_content[0] / K_i[0]
    equilibrium_content = melt_content * K_i
    initial_content[0] = equilibrium_content[0]

    dc = DiffusionCoefficients()
    if D_ref == "VanOrman2014":
        D = dc.vanorman2014(T_K, X_An)
    elif D_ref == "Costa2003":
        D = dc.costa2003(T_K, X_An)
    elif D_ref == "Zellmer1999":
        D = dc.zellmer1999(T_K, X_An)
    elif D_ref == "Cherniak2020":
        D = dc.cherniak2020(T_K, X_An)

    df = pd.DataFrame(
            {
                "Distance (um)": distance_um,
                "Distance (m)": distance_m,
                "An (mol%)": An_mol,
                "XAn": X_An,
                content: measured_content,
                "Initial " + content: initial_content,
                "K_D": K_i,
                "Equilibrium "+ content: equilibrium_content,
                "D (m2/s)": D
            }
        )
    df.to_csv(working_dir + "/preprocessed.csv", index=False)

    config["A (J)"] = A_i
    update_config = json.dumps(config, indent=4)
    
    with open("config.json", "w") as f:
        f.write(update_config)

if __name__ == "__main__":
    main()