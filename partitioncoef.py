import numpy as np
import pandas as pd
from constants import PhysicalConstants

class PartitionCoefficients(PhysicalConstants):
    def __init__(self):
        super().__init__()

    def mutch_model(self, ref, element, T_K, X_An, melt_SiO2_wt):
        
        def mutch2022(T_K, X_An, melt_SiO2_wt):
            X_An_dev = X_An - (0.12 + 0.00038 * T_K)
            beta = np.where(X_An_dev <= 0, 0, 1)
            RTlnK_i = (16900 - 37200 * beta) * X_An_dev \
                + 830 * melt_SiO2_wt - 83300
            return RTlnK_i
        
        # calculate partition coefficient
        RTlnK_i = mutch2022(T_K, X_An, melt_SiO2_wt)
        K_i = np.exp(RTlnK_i / (self.R_CONST * T_K))

        # calculate thermodynamic parameters, A and B
        min_X_An = X_An.min()
        max_X_An = X_An.max()
        RTlnK_i_min_XAn = mutch2022(T_K, min_X_An, melt_SiO2_wt)
        RTlnK_i_max_XAn = mutch2022(T_K, max_X_An, melt_SiO2_wt)
        A_i = (RTlnK_i_max_XAn - RTlnK_i_min_XAn) / (max_X_An - min_X_An)
        return A_i, K_i
    
    def empirical_model(self, ref, element, T_K, X_An):
        df = pd.read_csv("kd.csv", header=0)
        params_i = df[
            (df["Reference key"] == ref)
            & (df["Element"] == element)
        ].squeeze().to_dict()
        A_i, B_i = params_i["A"], params_i["B"]
        RTlnK_i  = A_i * X_An + B_i
        K_i = np.exp(RTlnK_i/(self.R_CONST * T_K))
        return A_i, K_i

def main():
    ref = "Mutch2022"
    element = "Mg"
    T_K = 1000
    X_An = np.array([0.5, 0.6, 0.8, 0.6])
    melt_SiO2_wt = 60
    PartitionCoefficients().mutch_model(ref, element, T_K, X_An, melt_SiO2_wt)

if __name__ == "__main__":
    main()