import numpy as np
from constants import PhysicalConstants

class PartitionCoefficients(PhysicalConstants):
    def __init__(self):
        super().__init__()

    def mutch2022(self, T_K, X_An, melt_SiO2_wt):
        X_An_dev = X_An - (0.12 + 0.00038 * T_K)
        beta = np.where(X_An_dev <= 0, 0, 1)
        RTlnK = (16900 - 37200 * beta) * X_An_dev \
            + 830 * melt_SiO2_wt - 83300
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("Warning: calculate thermodynamic parameter using calcparam.py")
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

if __name__ == "__main__":
    main()