# diffusion-chronometry-plagioclase

![Static Badge](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=Python)
![Static Badge](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Earth_science-Volcanology-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Mineral-Plagioclase-blue?style=flat-square)
![Static Badge](https://img.shields.io/badge/Elements-Mg_Sr-blue?style=flat-square)


**diffusion-chronometry-plagioclase** is a repository for carring out diffusion chronometry of plagioclase.

## Available models and parameters
This repository contains diffusion chronometry of Mg and Sr in plagioclase
by using Equation 7 from Costa et al. (2003). The diffusion equation is discretised in space and time and numerically solved by using finite-difference forward method. Boundary condition can be selected from the Dirichlet boundary condition (fixed value) and the Neumann boundary condition ($\mathrm{d}u/\mathrm{d}x = 0$).

This repositiory contains following partition coefficients and diffusion coefficients:
- Mg, Partition coefficient: Mutch et al. (2022), Diffusion coefficient: LaTourrette and Wasserburg (1998); Costa et al. (2003); Van Orman et al. (2013)
- Sr, Partition coefficient: Bindeman et al. (1998), Diffusion coefficient: Giletti and Casserly (1994)

## Rerequistes
The repository relies on the following third-party libraries:
- `Numpy`: carrying out numerical calculations
- `Pandas`: loading input files
- `Matplotlib`: visualisation of the calculation results
- `tqdm`: displaying calculation progress

The easiest way to install third-party libraries is by running `pip install --user $(library_name)`.

## Usage
- To execute the calculation, the input compositional data should be analysed at equal intervals. If your data is non-equal intervals, `interpolation.py` can convert to equal intervals by using linear interpolation.
- run `preprocessor.py` (optional)
- run `diffmodel.py`
- run `plotter.py`

## References
- Bindeman, I., Davis, A., Drake, M., 1998. Ion microprobe study of plagioclase-basalt partition experiments at natural concentration levels of trace elements. Geochimica et Cosmochimica Acta, 62, 1175-1193. https://doi.org/10.1016/S0016-7037(98)00047-7
- Costa, F., Chakraborty, S., Dohmen, R., 2003. Diffusion coupling between trace and major elements and a model for calculation of magma residence times using plagioclase. Geochimica et Cosmochimica Acta, 67, 2189-2200. https://doi.org/10.1016/j.epsl.2018.03.043
- Giletti, B., Casserly, J., 1994. Strontium diffusion kinetics in plagioclase feldspars. Geochimica et Cosmochimica Acta, 58, 3785-3793. https://doi.org/10.1016/0016-7037(94)90363-8
- Mutch, E., Maclennan, J., Madden-Nadeau, A., 2022. The dichotomous nature of Mg partitioning between plagioclase and melt: Implications for diffusion chronometry. Geochimica et Cosmochimica Acta, 339, 173–189. https://doi.org/10.1016/j.gca.2022.10.035
- Van Orman, J., Cherniak, D., Kita, N., 2013. Magnesium diffusion in plagioclase: Dependence on composition, and implications for thermal resetting of the 26Al–26Mg early solar system chronometer. Earth and Planetary Science Letters, 385, 79-88. https://doi.org/10.1016/j.epsl.2013.10.026

## License
The repository is **not confidential** and available under the [MIT license](https://opensource.org/license/mit/).