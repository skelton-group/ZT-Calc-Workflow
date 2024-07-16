# zt_calc_workflow/analysis.py


# ---------
# Docstring
# ---------

""" Routines for analysing datasets. """


# -------
# Imports
# -------

import warnings

import numpy as np

from itertools import product

from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import minimize


# ---------
# Functions
# ---------

def get_zt_max(data, n_min=None, n_max=None, t_max=None, t_min=None):
    """ Locate the maximum ZT in a Pandas DataFrame, with optional bounds on
    n and T, and return the corresponding table entry. """
    
    # Mask data if required.

    data_mask = np.ones(len(data))

    if n_min is not None:
        data_mask = np.logical_and(data_mask, data['n'] >= n_min)

    if n_max is not None:
        data_mask = np.logical_and(data_mask, data['n'] <= n_max)

    if t_min is not None:
        data_mask = np.logical_and(data_mask, data['t'] >= t_min)

    if t_max is not None:
        data_mask = np.logical_and(data_mask, data['t'] <= t_max)

    idx = data[data_mask].idxmax()['zt_ave']
    
    return data.loc[idx]


def match_data(calc_n, calc_t, calc_data_2d, to_match, mode='same_t',
               num_seeds=1):
    
    """ Construct a 2D interpolation of calc_data_2d, attempt to match data
    specified in to_match according to mode, and return a list of best-fit n, T
    and values.
    
    to_match should be a list of (n, T, val) data points; n and/or
    T can be set to None, but this will throw an error for some modes.
    
    Mode can be one of 'same', 'same_t' (default), 'same_n', 'best_match',
    where:
        * 'same' returns the calculated value at the experimental n/T.
        * 'same_t'/'same_n' return closest match at the same T/n.
        * 'best_match' returns the closest match.
    """
    
    # Generate an interpolation of the 2D data with x = log_n.
    
    calc_log_n = np.log10(calc_n)
    
    interpolator = RegularGridInterpolator(
        (calc_log_n, calc_t), calc_data_2d, method='linear', bounds_error=False,
        fill_value=None)
    
    # Loop over the data in to_match.
    
    match_res = []
    
    for n, t, val in to_match:
        # An initial guess for n and/or T can be taken from the coordinates of
        # the 2D data where the difference to val is a minimum.
        
        idx_n, idx_t = np.unravel_index(
            np.argmin(np.abs(calc_data_2d - val)), calc_data_2d.shape)
        
        if mode == 'same':
            if n is None or t is None:
                raise Exception("mode = 'same' can only be used when both n "
                                "and T have been specified.")
            
            match_res.append((n, t, interpolator((np.log10(n), t))))
        
        elif mode == 'same_t':
            if t is None:
                raise Exception("mode = 'same_t' can only be used when T has "
                                "been specified.")
            
            # Objective function to be minimised: absolute difference between
            # the calculation and match value.
            
            def _fit_func(log_n):
                return np.abs(interpolator((log_n, t)) - val)
            
            # Generate a set of initial guesses to input to the minimisation
            # function. If num_seeds = 1, use the log(n) from the estimate
            # above. Otherwise, generate a uniform sampling of log(n) over the
            # calculation range.
            
            guesses = None
            
            if num_seeds > 1:
                guesses = np.linspace(calc_log_n.min(), calc_log_n.max(),
                                      num_seeds)
            else:
                guesses = [calc_n[idx_n]]

            # Minimise the function for each initital guess in guesses.

            res_set = []
            
            for log_n_0 in guesses:
                res = minimize(_fit_func, [log_n_0],
                               bounds=[(calc_log_n[0], calc_log_n[-1])])
                
                res_set.append(res)
            
            # Select the guess with the lowest error (given by res.fun).
    
            idx = np.argmin([res.fun for res in res_set])
            
            match_res.append((np.power(10., res_set[idx].x[0]), t,
                              interpolator((res_set[idx].x[0], t))))
        
        elif mode == 'same_n':
            if n is None:
                raise Exception("mode = 'same_n' can only be used when n has "
                                "been specified.")
            
            # As for mode == 'same_t'.
            
            def _fit_func(t):
                return np.abs(interpolator((np.log10(n), t)) - val)

            guesses = None
            
            if num_seeds > 1:
                guesses = np.linspace(calc_t.min(), calc_t.max(), num_seeds)
            else:
                guesses = [calc_t[idx_t]]

            res_set = []
            
            for t in guesses:
                res = minimize(_fit_func, [t],
                               bounds=[(calc_t.min(), calc_t.max())])
                
                res_set.append(res)
            
            # Select the guess with the lowest error (given by res.fun).
    
            idx = np.argmin([res.fun for res in res_set])
            
            match_res.append((n, res_set[idx].x[0],
                              interpolator((np.log10(n), res_set[idx].x[0]))))
        
        elif mode == 'best_match':
            if num_seeds > 1:
                warnings.warn("Setting num_seeds > 1 with mode = 'best_match' "
                              "may take a long time and/or yield dubious "
                              "results.", RuntimeWarning)
 
            def _fit_func(args):
                return np.abs(interpolator(args) - val)

            # In contrast to mode = 'same_t' and 'same_n', there are two
            # parameters to be minimised. If num_seeds > 1, we take the
            # product() of a uniform sampling of log(n) and T.

            guesses = None
            
            if num_seeds > 1:
                guess_n = np.linspace(calc_log_n.min(), calc_log_n.max(),
                                      num_seeds)
                
                guess_t = np.linspace(calc_t.min(), calc_t.max(), num_seeds)
                
                guesses = [
                    (log_n, t) for log_n, t in product(guess_n, guess_t)]
            else:
                guesses = [(calc_log_n[idx_n], calc_t[idx_t])]
            
            res_set = []
            
            for log_n, t in guesses:
                res = minimize(_fit_func, [log_n, t],
                               bounds=[(calc_log_n[0], calc_log_n[-1]),
                                       (calc_t[0], calc_t[-1])])
            
            match_res.append((np.power(10., res.x[0]), res.x[1],
                              interpolator((res.x[0], res.x[1]))))

        else:
            raise Exception("Unknown mode = '{0}'.".format(mode))
    
    return match_res
