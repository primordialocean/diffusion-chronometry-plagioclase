import numpy as np
from constants import PhysicalConstants, Units

class DiffusionCoefficients(PhysicalConstants):
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

if __name__ == "__main__":
    main()