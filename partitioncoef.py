import numpy as np
import pandas as pd
from constants import PhysicalConstants

class PartitionCoefficients(PhysicalConstants):
    def __init__(self):
        super().__init__()

    def mutch2022(self, ref, element, T_K, X_An, melt_SiO2_wt):
        X_An_dev = X_An - (0.12 + 0.00038 * T_K)
        beta = np.where(X_An_dev <= 0, 0, 1)
        RTlnK = (16900 - 37200 * beta) * X_An_dev \
            + 830 * melt_SiO2_wt - 83300
        K = np.exp(RTlnK/(self.R_CONST * T_K))
        print("Warning: calculate thermodynamic parameter using calcparam.py")
        return K
    
    def empirical_model(self, ref, element, T_K, X_An):
        df = pd.read_csv("kd.csv", header=0)
        params_i = df[
            (df["Reference key"] == ref)
            & (df["Element"] == element)
        ].squeeze().to_dict()
        A_i, B_i = params_i["A"], params_i["B"]
        RTlnK_i  = A_i * X_An + B_i
        K_i = np.exp(RTlnK_i/(self.R_CONST * T_K))
        return A_i, B_i, K_i

def main():
    ref = "Bindeman1998"
    element = "Mg"
    T_K = 1000
    X_An = 0.5
    PartitionCoefficients().empirical_model(ref, element, T_K, X_An)

if __name__ == "__main__":
    main()