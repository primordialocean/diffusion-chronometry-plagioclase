import numpy as np
import pandas as pd
import json

class PhysicalConstant:
    def __init__(self):
        self.R_CONST = 8.31 # J/mol
        self.KELVIN = 273.15
        self.um = 1e-6 # um to m
        self.year = 60 * 60 * 24 * 365 # year to second
        self.day = 60 * 60 * 24 # day to second

class PartitionCoefficient(PhysicalConstant):
    def __init__(self):
        super().__init__()

    def mg_mutch2022(self, T_K, X_An, melt_SiO2_wt):
        X_An_dev = X_An - (0.12 + 0.00038 * T_K)
        beta = np.where(X_An_dev <= 0, 0, 1)
        RTlnK_Mg = (16900 - 37200 * beta) * X_An_dev \
            + 830 * melt_SiO2_wt - 83300
        K_Mg = np.exp(RTlnK_Mg/(self.R_CONST * T_K))
        return K_Mg

    def mg_bindeman1998(self, T_K, X_An):
        A_Mg, B_Mg = -26100, -25000
        RTlnK_Mg  = A_Mg * X_An + B_Mg
        K_Mg = np.exp(RTlnK_Mg/(self.R_CONST * T_K))
        return K_Mg

class DiffusionCoefficient(PhysicalConstant):
    def __init__(self):
        super().__init__()

    def mg_costa2003(self, T_K, X_An):
        D_Mg = 2.92 * (10 ** (-4.1 * X_An - 3.1)) \
        * np.exp(-266000 / (self.R_CONST * T_K))
        return D_Mg

    def mg_vanorman2014(self, T_K, X_An):
        D_Mg = np.exp(-6.06 - 7.96 * X_An - 287e3 / (self.R_CONST * T_K))
        return D_Mg

    def sr_zellmer1999(self, T_K, X_An):
        D_Sr = (10 ** (-4.1 * X_An - 4.08)) \
            * np.exp(-276000 / (self.R_CONST * T_K))
        return D_Sr
    
    def ti_cherniak2020(self, T_K, X_An):
        D_Ti = 4.37e-14 * np.exp(-181000 / (self.R_CONST * T_K))

def main():
    # load pysical constants
    const = PhysicalConstant()
    KELVIN = const.KELVIN
    R_CONST = const.R_CONST
    um = const.um
    day = const.day
    year = const.year

    # load configuration file
    config = json.load(open("config.json", "r"))
    input_filename = config["Input filename"]
    Element = config["Element"]
    D_ref = config["Diffusion coefficient"]
    K_ref = config["Partition coefficient"]
    T_C = config["T (C)"]
    T_K = T_C + KELVIN
    melt_SiO2_wt = config["melt SiO2 (wt%)"]
    #melt_Mg_ppm = config["melt Mg (ppm)"]
    maxtime_s = config["Max time"] * year
    
    df = pd.read_excel(input_filename, sheet_name="input")
    distance_um = df["Distance (um)"].to_numpy()
    distance_m = distance_um * um
    X_An = df["XAn"].to_numpy()
    Mg_ppm = df["Mg (ppm)"].to_numpy()
    init_Mg_ppm = df["Initial Mg (ppm)"].to_numpy()

    pc = PartitionCoefficient()
    # K_Mg = pc.mg_mutch2022(T_K, X_An, melt_SiO2_wt)
    K_Mg = pc.mg_bindeman1998(T_K, X_An)

    # estimate melt Mg from rimward composition
    melt_Mg_ppm = Mg_ppm[0] / K_Mg[0]

    eq_Mg = melt_Mg_ppm * K_Mg

    dc = DiffusionCoefficient()
    # D_Mg = dc.mg_vanorman2014(T_K, X_An)
    D_Mg = dc.mg_costa2003(T_K, X_An)

    df = pd.DataFrame.from_dict(
            {
                "Distance (um)": distance_um,
                "Distance (m)": distance_m,
                "XAn": X_An,
                "Mg (ppm)": Mg_ppm,
                "Initial Mg (ppm)": init_Mg_ppm,
                "K_D": K_Mg,
                "Equilibrium Mg (ppm)": eq_Mg,
                "D_Mg": D_Mg
            }
        )
    df.to_csv("preprocessed.csv")

if __name__ == "__main__":
    main()