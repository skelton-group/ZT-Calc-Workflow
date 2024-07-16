# zt_calc_workflow/plotting.py


# -------
# Imports
# -------

import numpy as np
import matplotlib as mpl

from matplotlib.colors import hsv_to_rgb


# ---------
# Functions
# ---------

def setup_matplotlib(sans_serif=False, font_size=8, linewidth=0.5):
    """ Set Matplotlib defaults. """

    # Fonts.

    if sans_serif:
        mpl.rc('font', **{'family': 'sans-serif', 'size': font_size,
                          'sans-serif': 'Calibri'})
    
        mpl.rc('mathtext', **{'fontset': 'custom', 'rm': 'Calibri',
                              'it': 'Calibri:italic', 'bf' : 'Calibri:bold' })
    else:
        mpl.rc('font', **{'family': 'serif', 'size': font_size,
                          'serif': 'Times'})
    
        mpl.rc('mathtext', **{'fontset': 'custom', 'rm': 'Times',
                              'it': 'Times:italic', 'bf' : 'Times:bold' })

    # Axes, lines and patches.

    mpl.rc('axes', **{'linewidth': linewidth, 'labelsize': font_size})
    mpl.rc('lines', **{'linewidth': linewidth, 'markeredgewidth': linewidth})
    mpl.rc('patch', **{'linewidth': linewidth})

    # Tick params.

    tick_params = {'major.width': linewidth, 'minor.width': linewidth,
                   'direction': 'in'}

    mpl.rc('xtick', **tick_params)
    mpl.rc('ytick', **tick_params)

    mpl.rc('xtick', **{'top': True})
    mpl.rc('ytick', **{'right': True})

def cscale(n, h1, h2):
    """ Generate an HSB colour scale with n colours between hues h1 and h2. """

    if n <0:
        raise Exception("n must be at least 1.")

    if n == 1:
        return hsv_to_rgb((h1 / 360.0, 1.0, 1.0))

    return [hsv_to_rgb(((h / 360.0) % 1.0, 1.0, 1.0))
                for h in np.linspace(h1, h2, n)]

def cscale_fire(n):
    """ Generate an n-point "fire" colour scale. """
    return cscale(n, 240.0, 390.0)

def cscale_ice(n):
    """ Generate an n-point "ice" colour scale. """
    return cscale(n, 240.0, 180.0)
