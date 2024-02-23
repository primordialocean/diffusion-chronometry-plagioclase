import numpy as np
import pandas as pd
import json
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
    config = json.load(open("config.json", "r"))
    working_dir = config["Working directory"]
    element = config["Element"]
    D_ref = config["Diffusion coefficient"]
    K_ref = config["Partition coefficient"]
    T_C = config["T (C)"]
    T_K = T_C + KELVIN
    melt_SiO2_wt = config["melt SiO2 (wt%)"]
    maxtime_s = config["Max time"] * YEAR
    
    df = pd.read_csv(working_dir + "/interpolated.csv")
    distance_um = df["Distance (um)"].to_numpy()
    distance_m = distance_um * UM
    An_mol = df["An (mol%)"].to_numpy()
    X_An = 0.01 * An_mol
    measured_ppm = df[element + " (ppm)"].to_numpy()
    initial_ppm = df["Initial " + element + " (ppm)"].to_numpy()

    # import partition coefficiation class
    pc = PartitionCoefficients()
    # select reference
    if K_ref == "Mutch2022":
        K = pc.mutch2022(T_K, X_An, melt_SiO2_wt)
    elif K_ref == "Nielsen2017":
        K = pc.nielsen2017(element, T_K, X_An)
    elif K_ref == "Bindeman1998":
        K = pc.bindeman1998(element, T_K, X_An)
    elif K_ref == "Blundy1991":
        K = pc.blundy1991(element, T_K, X_An)
    elif K_ref == "Drake1972":
        K = pc.drake1972(element, T_K, X_An)
    
    # estimate melt Mg from rimward composition
    melt_ppm = measured_ppm[0] / K[0]
    equilibrium_ppm = melt_ppm * K

    dc = DiffusionCoefficients()
    if D_ref == "VanOrman2014":
        D = dc.vanorman2014(T_K, X_An)
    elif D_ref == "Costa2003":
        D = dc.costa2003(T_K, X_An)
    elif D_ref == "Zellmer1999":
        D = dc.zellmer1999(T_K, X_An)

    df = pd.DataFrame(
            {
                "Distance (um)": distance_um,
                "Distance (m)": distance_m,
                "An (mol%)": An_mol,
                "XAn": X_An,
                element + " (ppm)": measured_ppm,
                "Initial " + element + " (ppm)": initial_ppm,
                "K_D": K,
                "Equilibrium "+ element + " (ppm)": equilibrium_ppm,
                "D": D
            }
        )
    df.to_csv(working_dir + "/preprocessed.csv", index=False)

if __name__ == "__main__":
    main()