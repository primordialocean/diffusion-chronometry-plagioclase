import numpy as np
import pandas as pd
import json
from tqdm import tqdm
from constants import PhysicalConstants, Units

class ModelDiffusion(PhysicalConstants):
    def __init__(self):
        super().__init__()
    
    def diffusion_model(
        self, dx, dt, nx, nt, u_n, X_An, T_K, D, A_i, boundary
        ):
        """Function for diffusion modelling of plagioclase trace elements.
        Args:
            dx:
            dt:
            nx:
            nt:
            u_n:
            X_An (ndarray): The plagioclase anorthite profile as molar fraction.
            T_K (float): Surrounded melt temperature as Kelvin.
            D (ndarray): The diffusion coefficient for each point
                in the profile.
            A_i (float): The thermodynamic parameter, RTlnKD = A_i * XAn + B_i.
            boundary (str): select "Dirichlet" (fixed boundary condition)
                or "Neumann" (du/dx = 0).
        Returns:
            ndarray: The results of diffusion modelling.
        """

        result_arr = np.zeros((nt, nx))
        result_arr[0, :] = u_n
        u = np.zeros(nx)
        timesteps = [0]
        lap_time = 0
        for n in tqdm(range(0, nt-1)):
            # assume infinite reservoir based
            u[0] = u_n[0]
            
            u[1:nx-1] = u_n[1:nx-1] + dt * (
                ((D[2:nx] - D[1:nx-1]) / dx)
                * ((u_n[2:nx] - u_n[1:nx-1]) / dx)
                + D[1:nx-1]
                * ((u_n[2:nx] - 2 * u_n[1:nx-1] + u_n[0:nx-2]) / (dx ** 2))
                - (A_i / (self.R_CONST * T_K))
                * (
                    D[1:nx-1] * (
                        ((u_n[2:nx] - u_n[1:nx-1]) / dx)
                        * ((X_An[2:nx] - X_An[1:nx-1]) / dx)
                    )
                    + u_n[1:nx-1] * (
                        ((D[2:nx] - D[1:nx-1]) / dx)
                        * ((X_An[2:nx] - X_An[1:nx-1]) / dx)
                    )
                    + D[1:nx-1] * u_n[1:nx-1] * (
                        (X_An[2:nx] - 2 * X_An[1:nx-1] + X_An[0:nx-2]) \
                        / (dx ** 2)
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
                    - (A_i / (self.R_CONST * T_K))
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
            
            result_arr[n+1, :] = u
            u_n[:] = u
            lap_time += dt
            timesteps.append(lap_time)
        return result_arr, timesteps

def main():
    # load pysical constants
    physconsts = PhysicalConstants()
    KELVIN = physconsts.KELVIN

    # load units
    units = Units()
    UM = units.UM
    TIME_UNITS = units.TIME_UNITS

    # load configuration file
    with open("config.json") as f:
        config = json.load(f)
    
    working_dir = config["Working directory"]
    T_C = config["T (C)"]
    T_K = T_C + KELVIN
    element = config["Element"]
    content = config["Content"]
    time_unit_name = config["Time unit"]

    time_unit = TIME_UNITS[time_unit_name]
    maxtime_s = config["Max time"] * time_unit
    boundary = config["Boundary condition"]
    K_ref = config["Partition coefficient"]

    # load compositional data
    df = pd.read_csv(working_dir + "/preprocessed.csv")
    x_m = df["Distance (m)"].to_numpy()
    X_An = df["XAn"].to_numpy()
    D = df["D (m2/s)"].to_numpy()
    u_n = df["Initial " + content].to_numpy()
    dx_m = x_m[1] - x_m[0]
    nx = x_m.shape[0]
    dt_s = 0.4 * (dx_m ** 2) / np.max(D)
    nt = int(maxtime_s / dt_s)
    A_i = config["A (J)"]
    diffmodel = ModelDiffusion()
    result_arr, timesteps = diffmodel.diffusion_model(
        dx_m, dt_s, nx, nt, u_n, X_An, T_K, D, A_i, boundary
        )
    result_df = pd.DataFrame(
        result_arr.T, columns=timesteps
        )
    result_df.insert(0, "Distance (m)", x_m)
    result_df.to_csv(working_dir + "/result.csv", index=False)

if __name__ == "__main__":
    main()