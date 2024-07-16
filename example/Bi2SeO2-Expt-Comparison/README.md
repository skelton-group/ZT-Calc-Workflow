# Bi<sub>2</sub>SeO<sub>2</sub>-Expt-Comparison


## Overview

This example performs a comparison of the calculated electrical conductivity <i>&sigma;</i> and Seebeck coefficient *S* of n-type Bi<sub>2</sub>SeO<sub>2</sub> to experimental data.


## Scripts

This example contains the following example scripts:

### 1. `compare_calc_expt.py`

This script uses the analysis tools in `zt_calc_workflow` to compare a calculation of the electrical properties of Bi<sub>2</sub>SeO<sub>2</sub> to a set of experimental measurements on five Br-doped single crystals.

```
Sample: 'S3', Data: 's', Mode: 'same_t'
---------------------------------------

n          | T          | Expt.      | n          | T          | Calc.      | Diff.     
----------------------------------------------------------------------------------------
  1.30e+19 |        203 |     -93.86 |   6.57e+18 |        203 |     -93.86 |  -1.85e-08
  1.30e+19 |        218 |     -97.55 |   6.98e+18 |        218 |     -97.55 |   2.27e-09
  1.30e+19 |        233 |    -100.10 |   7.56e+18 |        233 |    -100.10 |  -3.00e-07
  1.30e+19 |        253 |    -105.39 |   7.93e+18 |        253 |    -105.39 |  -5.39e-08
  1.30e+19 |        267 |    -109.53 |   8.13e+18 |        267 |    -109.53 |  -4.19e-07
  1.30e+19 |        282 |    -113.12 |   8.41e+18 |        282 |    -113.12 |  -6.49e-08
  1.30e+19 |        301 |    -117.58 |   8.74e+18 |        301 |    -117.58 |  -1.29e-07
  1.30e+19 |        316 |    -122.21 |   8.79e+18 |        316 |    -122.21 |  -6.09e-07
  1.30e+19 |        331 |    -125.41 |   9.05e+18 |        331 |    -125.41 |  -5.71e-07
  1.30e+19 |        350 |    -132.03 |   8.91e+18 |        350 |    -132.03 |  -1.03e-07
  1.30e+19 |        366 |    -136.35 |   8.93e+18 |        366 |    -136.35 |  -1.64e-07
  1.30e+19 |        380 |    -142.62 |   8.61e+18 |        380 |    -142.62 |  -6.49e-07
  1.30e+19 |        391 |    -146.34 |   8.52e+18 |        391 |    -146.34 |  -1.18e-07
```


## References

1. J. Wang, W. Hu, Z. Lou, Z. Xu, X. Yang, T. Wang and X. Lin,
   "Thermoelectric properties of Bi<sub>2</sub>O<sub>2</sub>Se single crystals",
   *Appl. Phys. Lett.* **119**, 081901 (**2021**), DOI: <a href="https://doi.org/10.1063/5.0063091" target="_blank">10.1063/5.0063091</a>
3. J. M. Flitcroft, A. Althubiani and J. M. Skelton,
   "Thermoelectric properties of the bismuth oxychalcogenides Bi<sub>2</sub>SO<sub>2</sub>, Bi<sub>2</sub>SeO<sub>2</sub> and Bi<sub>2</sub>TeO<sub>2</sub>",
   *J. Phys.: Energy* **6** (*2*), 025011 (**2024**), DOI: <a href="https://doi.org/10.1088/2515-7655/ad2afd" target="_blank">10.1088/2515-7655/ad2afd</a>