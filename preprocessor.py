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

    def mutch2022(self, T_K, X_An, melt_SiO2_wt):
        X_An_dev = X_An - (0.12 + 0.00038 * T_K)
        beta = np.where(X_An_dev <= 0, 0, 1)
        RTlnK = (16900 - 37200 * beta) * X_An_dev \
            + 830 * melt_SiO2_wt - 83300
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("Warming: calculate thermodynamic parameter using calcparam.py")
        return K

    def nielsen2017(self, element, T_K, X_An):
        params = {
            "Mg": (-10.0e3, -35.0e3),
            "Ti": (-32.5e3, -15.1e3),
            "Sr": (-25.0e3, 25.5e3),
            "Ba": (-35.1e3, 10.0e3)
            }
        param = params[element]
        RTlnK  = param[0] * X_An + param[1]
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("A = " + str(param[0]))
        return K

    def bindeman1998(self, element, T_K, X_An):
        params = {
            "Mg": (-26.1e3, -25.7e3),
            "Sc": (-94.2e3, 37.4e3),
            "Ti": (-28.9e3, -15.4e3),
            "Rb": (-40e3, -15.1e3),
            "Sr": (-30.4e3, 28.5e3),
            "Ba": (-55.0e3, 19.1e3)
            }
        param = params[element]
        RTlnK  = param[0] * X_An + param[1]
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("A = " + str(param[0]))
        return K
    
    def blundy1991(self, element, T_K, X_An):
        params = {
            "Sr": (-26.7e3, 26.8e3),
            "Ba": (-38.2e3, 10.2e3)
            }
        param = params[element]
        RTlnK = param[0] * X_An + param[1]
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("A = " + str(param[0]))
        return K
    
    def drake1972(self, element, T_K, X_An):
        params = {
            "Sr": (-18.9e3, 21.5e3),
            "Ba": (-32.0e3, 7.4e3)
            }
        param = params[element]
        RTlnK = param[0] * X_An + param[1]
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("A = " + str(param[0]))
        return K

class DiffusionCoefficient(PhysicalConstant):
    def __init__(self):
        super().__init__()
    # Mg diffusion
    def costa2003(self, T_K, X_An):
        D_Mg = 2.92 * (10 ** (-4.1 * X_An - 3.1)) \
        * np.exp(-266000 / (self.R_CONST * T_K))
        return D_Mg
    
    def vanorman2014(self, T_K, X_An):
        D_Mg = np.exp(-6.06 - 7.96 * X_An - 287e3 / (self.R_CONST * T_K))
        return D_Mg
    
    # Sr diffusion
    def zellmer1999(self, T_K, X_An):
        D_Sr = (10 ** (-4.1 * X_An - 4.08)) \
            * np.exp(-276000 / (self.R_CONST * T_K))
        return D_Sr
    
    # Ti diffusion
    def cherniak2020(self, T_K, X_An):
        D_Ti = 4.37e-14 * np.exp(-181000 / (self.R_CONST * T_K))
        return D_Ti

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
    working_dir = config["Working directory"]
    element = config["Element"]
    D_ref = config["Diffusion coefficient"]
    K_ref = config["Partition coefficient"]
    T_C = config["T (C)"]
    T_K = T_C + KELVIN
    melt_SiO2_wt = config["melt SiO2 (wt%)"]
    maxtime_s = config["Max time"] * year
    
    df = pd.read_csv(working_dir + "/interpolated.csv")
    distance_um = df["Distance (um)"].to_numpy()
    distance_m = distance_um * um
    X_An = df["XAn"].to_numpy()
    measured_ppm = df[element + " (ppm)"].to_numpy()
    initial_ppm = df["Initial " + element + " (ppm)"].to_numpy()

    # import partition coefficiation class
    pc = PartitionCoefficient()
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

    dc = DiffusionCoefficient()
    if D_ref == "VanOrman2014":
        D = dc.vanorman2014(T_K, X_An)
    elif D_ref == "Zellmer1999":
        D = dc.zellmer1999(T_K, X_An)

    df = pd.DataFrame(
            {
                "Distance (um)": distance_um,
                "Distance (m)": distance_m,
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