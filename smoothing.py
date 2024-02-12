import pandas as pd
import numpy as np
import scipy
from scipy.interpolate import interp1d
from typing import Union


def read_settings(
    filename: str = "settings.txt"
    ) -> dict[str, Union[str, int, float]]:
    """Read setting file
    Args:
        filename (str): The filename of setting file. Default is "setting.txt".
    Returns:
        dict: The dictionary of the input parameters.
    """
    settings :dict[str, Union[str, int, float]] = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            (k, v) = line.split(": ")
            if k == "tempc" or k == "tempk_sd":
                settings[str(k)] = float(v.strip())
            elif k == "maxtime":
                settings[str(k)] = int(v.strip())
            else:
                settings[str(k)] = v.strip()
    return settings

settings :dict[str, Union[str, int, float]] = read_settings()

inputfile :str = settings["inputfile"]
sheetname :str = settings["sheetname"]
element :str = settings["element"]
df = pd.read_excel(inputfile, sheet_name="raw")

dist = df["Distance"].to_numpy()
xan = df["XAn"].to_numpy()
measured = df[element].to_numpy()

xmin = dist.min()
xmax = dist.max()
dx = 1

inter_dist = np.arange(xmin, xmax, dx)

func_xan = scipy.interpolate.interp1d(dist, xan)
inter_xan = np.array(func_xan(inter_dist))

func_measured = scipy.interpolate.interp1d(dist, measured)
inter_measured = np.array(func_measured(inter_dist))

print(len(inter_dist), len(inter_xan), len(inter_measured))

with pd.ExcelWriter(inputfile, mode="a") as writer:
    pd.DataFrame(
        np.array([inter_dist, inter_measured, inter_xan]).T,
        columns=["Distance", "Mg", "XAn"]
        ).to_excel(writer, sheet_name="input")