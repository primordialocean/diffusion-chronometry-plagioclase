import numpy as np
import pandas as pd
import json
from tqdm import tqdm

class PhysicalConstant:
    def __init__(self):
        self.R_CONST = 8.31 # J/mol
        self.KELVIN = 273.15
        self.um = 1e-6 # um to m
        self.year = 60 * 60 * 24 * 365 # year to second
        self.day = 60 * 60 * 24 # day to second

class ModelDiffusion(PhysicalConstant):
    def __init__(self):
        super().__init__()
    
    def diffusion_model(self, dx, dt, nx, nt, result_arr, X_An, D, A_i, boundary):
        """Function for diffusion modelling of plagioclase trace elements.
        Args:
            initial (ndarray): The initial composition of the plagioclase
                trace element profile.
            X_An (ndarray): The plagioclase anorthite profile as molar fraction.
            t_s (ndarray): The time grid array.
            D (ndarray): The diffusion coefficient for each point
                in the profile.
            A_i (float): The thermodynamic parameter, RTlnKD = A_i * XAn + B_i
            boundary: select "Dirichlet" (fixed boundary condition)
                or "Neumann" (du/dx = 0)
        Returns:
            ndarray: The results of diffusion modelling.
        """
        
        for n in tqdm(range(0, nt), total=nt):
            # assume infinite reservoir based
            u[0] = u_n[0]
            
            u[1:nx-1] = u_n[1:nx-1] + dt * (
                ((D[2:nx] - D[1:nx-1]) / dx)
                * ((u_n[2:nx] - u_n[1:nx-1]) / dx)
                + D[1:nx-1]
                * ((u_n[2:nx] - 2 * u_n[1:nx-1] + u_n[0:nx-2]) / (dx ** 2))
                - A_i / (self.R_CONST * T_K)
                * (
                    D[1:nx-1]
                    * (
                        ((u_n[2:nx] - u_n[1:nx-1]) / dx)
                        * ((X_An[2:nx] - X_An[1:nx-1]) / dx)
                    )
                    + u_n[1 : nx - 1]
                    * (
                        ((D[2:nx] - D[1:nx-1]) / dx)
                        * ((X_An[2:nx] - X_An[1:nx-1]) / dx)
                    )
                    + D[1:nx-1] * u_n[1:nx-1]
                    * (
                        (X_An[2:nx] - 2 * X_An[1:nx-1] + X_An[0:nx-2]) \
                        /(dx ** 2)
                        )
                )
            )

            # Select boundary condition
            if boundary == "Dirichlet":
                u[-1] = u_n[-1]
            elif boundary == "Neumann":
                u[-1] =  u_n[-1] + dt * (
                        ((D[-2] - D[-1]) / dx) * ((u_n[-2] - u_n[-1]) / dx)
                        + D[-1] * (
                            (u_n[-2] - 2 * u_n[-1] + u_n[-2]) / (dx ** 2)
                            )
                        - coef
                        * (
                            D[-1] * (((u_n[-2] - u_n[-1]) / dx)
                            * ((X_An[-2] - X_An[-1]) / dx))
                            + u_n[-1] * (((D[-2] - D[-1]) / dx)
                            * ((X_An[-2] - X_An[-1]) / dx))
                            + D[-1] * u_n[-1]
                            * (
                                (X_An[-2] - 2 * X_An[-1] + X_An[-2]) / (dx ** 2)
                                )
                        )
                    )
            
            result_arr[n, :] = u
            u_n[:] = u
        return modelled

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
    T_C = config["T (C)"]
    T_K = T_C + KELVIN
    maxtime_s = config["Max time"] * year
    boundary = config["Boundary condition"]

    # load compositional data
    df = pd.read_csv("preprocessed.csv")
    x_m = df["Distance (m)"].to_numpy()
    X_An = df["XAn"].to_numpy()
    D = df["D_Mg"].to_numpy()
    dx = x_m[1] - x_m[0]
    nx = x_m.shape[0]
    dt = 0.1 * (dx ** 2) / np.max(D)
    nt = int(maxtime_s / dt)
    modelled = np.zeros((nt, nx))
    u = np.zeros(nx)
    A_i = -26100

    
    diffmodel = ModelDiffusion()
    result = diffmodel.diffusion_model(dx, dt, nx, nt, modelled, X_An, D, A_i, boundary)
    result.to_csv("result.csv")
if __name__ == "__main__":
    main()