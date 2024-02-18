import pandas as pd
import json

config = json.load(open("config.json", "r"))
melt_SiO2_wt = config["melt SiO2 (wt%)"]

def mutch2022(T_K, X_An, melt_SiO2_wt):
    X_An_dev = X_An - (0.12 + 0.00038 * T_K)
    beta = np.where(X_An_dev <= 0, 0, 1)
    RTlnK = (16900 - 37200 * beta) * X_An_dev \
        + 830 * melt_SiO2_wt - 83300
    return RTlnK

print(A)