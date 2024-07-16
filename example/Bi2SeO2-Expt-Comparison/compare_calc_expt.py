# compare_calc_expt.py


"""
In this example, we fit the electrical conductivity and Seebeck coefficient
from an AMSET calculation on n-type Bi2SeO2 against experimental data from
measurements on five single-crystal Br-doped Bi2SeO2 samples ("S1" - "S5").

Calculation paper:
    Thermoelectric properties of the bismuth oxychalcogenides Bi2SO2, Bi2SeO2
        and Bi2TeO2
    J. M. Flitcroft, A. Althubiani and J. M. Skelton
    J. Phys.: Energy 6 (2), 025011 (2024), DOI: 10.1088/2515-7655/ad2afd

Experimental paper:
     Thermoelectric properties of Bi2O2Se single crystals
     J. Wang, W. Hu, Z. Lou, Z. Xu, X. Yang, T. Wang and X. Lin
     Appl. Phys. Lett. 119, 081901 (2021), DOI: 10.1063/5.0063091

The data were extracted from Fig. 2a/2b in the experimental paper using
WebPlotDigitizer (https://automeris.io/).
"""


import csv

import numpy as np

import sys ; sys.path.append(r"/mnt/d/Repositories/ZT-Calc-Workflow")

from zt_calc_workflow.amset import read_amset_csv
from zt_calc_workflow.analysis import match_data
from zt_calc_workflow.dataset import dataset_to_2d


def read_expt_data_csv(file_path):
    """ Read experimental data from a two-column CSV file. """
    
    with open(file_path, 'r') as f:
        f_csv = csv.reader(f)
        
        return np.array(
            [[float(val) for val in r] for r in f_csv], dtype=np.float64)


if __name__ == "__main__":
    # Load AMSET calculation and create 2D datasets.
    
    data = read_amset_csv(r"Bi2SeO2-AMSET-n.csv")
    calc_n, calc_t, calc_data_2d = dataset_to_2d(data)
    
    # Experimental carrier concentrations (nominal).
    
    expt_n = {'S1': 1.0e18, 'S2': 6.8e18, 'S3': 1.3e19, 'S4': 2.2e19, 
              'S5': 8.7e19}
    
    # Load experimental data.
    
    expt_data = {}
    
    for s in "S1", "S2", "S3", "S4", "S5":
        expt_sigma = read_expt_data_csv(r"5.0063091-2a_{0}.csv".format(s))
        
        # Resistivity data -> sigma = 1 / rho.
        
        expt_sigma = np.array([[t, 1. / rho] for t, rho in expt_sigma],
                              dtype=np.float64)
        
        expt_s = read_expt_data_csv(r"5.0063091-2b_{0}.csv".format(s))
        
        expt_data[s] = {'sigma': expt_sigma, 's': expt_s}
    
    # Match sigma and S for each of the five samples and print results.
    
    for expt_k, calc_k in('sigma', 'sigma_ave'), ('s', 's_ave'):
        for s in "S1", "S2", "S3", "S4", "S5":
            # List of (n, t, val) to match to.
            
            match_to = [(expt_n[s], t, v) for t, v in expt_data[s][expt_k]]
        
            # Match to calculated data. Using mode='same_t' will return the
            # calculated n that best match the experimental data at the
            # measurement T.
        
            res = match_data(calc_n, calc_t, calc_data_2d[calc_k],
                             match_to, mode='same_t', num_seeds=5)
        
            # Print results.
        
            header = "Sample: '{0}', Data: '{1}'".format(s, expt_k)

            print(header)
            print('-' * len(header))
            print("")
            
            print("{0: <10} | {1: <10} | {2: <10} | {3: <10} | {4: <10} | "
                  "{5: <10} | {6: <10}".format("n", "T", "Expt.", "n", "T",
                                               "Calc.", "Diff."))
            
            print('-' * (7 * 10 + 6 * 3))
            
            for (e_n, e_t, e_v), (c_n, c_t, c_v) in zip(match_to, res):
                print(
                    "{0: >10.2e} | {1: >10.0f} | {2: >10.2f} | {3: >10.2e} | "
                    "{4: >10.0f} | {5: >10.2f} | {6: >10.2e}".format(
                       e_n, e_t, e_v, c_n, c_t, c_v, c_v - e_v))
            
            print("")
    
    print("")
    
    # Try one sample with all four modes.
    
    s = "S3"
    
    for expt_k, calc_k in ('sigma', 'sigma_ave'), ('s', 's_ave'):
        for mode in 'same', 'same_t', 'same_n', 'best_match':
            match_to = [(expt_n[s], t, v) for t, v in expt_data[s][expt_k]]
            
            # num_seeds gives dubious results with mode = 'best_match' (and
            # will issue a RuntimeWarning to this effect).
            
            num_seeds = 1 if mode == 'best_match' else 5
            
            res = match_data(calc_n, calc_t, calc_data_2d[calc_k],
                             match_to, mode=mode, num_seeds=num_seeds)
            
            header = ("Sample: '{0}', Data: '{1}', Mode: "
                      "'{2}'".format(s, expt_k, mode))

            print(header)
            print('-' * len(header))
            print("")
            
            print("{0: <10} | {1: <10} | {2: <10} | {3: <10} | {4: <10} | "
                  "{5: <10} | {6: <10}".format("n", "T", "Expt.", "n", "T",
                                               "Calc.", "Diff."))
            
            print('-' * (7 * 10 + 6 * 3))
            
            for (e_n, e_t, e_v), (c_n, c_t, c_v) in zip(match_to, res):
                print(
                    "{0: >10.2e} | {1: >10.0f} | {2: >10.2f} | {3: >10.2e} | "
                    "{4: >10.0f} | {5: >10.2f} | {6: >10.2e}".format(
                       e_n, e_t, e_v, c_n, c_t, c_v, c_v - e_v))
            
            print("")
    
    print("")
