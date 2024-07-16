# zt_plot.py


"""
In this example, we prepare a plot to compare the ZT of p- and n-type Pnma SnS
and SnSe as a function of doping level and temperature.

The calculation combines data from multiple papers:

    Approximate models for the lattice thermal conductivity of alloy
        thermoelectrics
    J. M. Skelton
    J. Mater. Chem. C 9 (35), 11772 (2021), DOI: 10.1039/D1TC02026A

    Thermoelectric Properties of Pnma and Rocksalt SnS and SnSe
    J. M. Flitcroft, I. Pallikara and J. M. Skelton
    Solids 3 (1), 155-176 (2022), DOI: 10.3390/solids3010011
    
    Thermoelectric properties of Pnma and R3m GeS and GeSe
    M. Zhang, J. Flictroft, S. Guillemot and J. Skelton
    J. Mater. Chem. C 11, 14833 (2023, DOI: 10.1039/D3TC02938G
"""


import numpy as np
import matplotlib.pyplot as plt

from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import FuncFormatter

import sys ; sys.path.append(r"/mnt/d/Repositories/ZT-Calc-Workflow")

from zt_calc_workflow.amset import read_amset_csv
from zt_calc_workflow.dataset import zt_dataset_from_data, dataset_to_2d
from zt_calc_workflow.phono3py import read_phono3py_kappa_csv
from zt_calc_workflow.plotting import setup_matplotlib


if __name__ == "__main__":
    # Read input data.

    input_files = {'SnS': (r"SnS-Pnma-AMSET-p.csv", r"SnS-Pnma-AMSET-n.csv",
                          r"SnS-kappa-m16816.Prim.csv"),
                   'SnSe': (r"SnSe-Pnma-AMSET-p.csv", r"SnSe-Pnma-AMSET-n.csv",
                            r"SnSe-kappa-m16816.Prim.csv")}
    
    zt_data = {}
    
    for k, (amset_p, amset_n, kappa) in input_files.items():
        kappa_data = read_phono3py_kappa_csv(kappa)
        
        # The Phono3py calculations were performed on structures with the axes
        # oriented differently to those in the AMSET calculations. We deal with
        # this by dropping the off-diagonal elements and relabelling the
        # diagonal elements in kappa_data.
        
        kappa_data.drop(columns=['kappa_yz', 'kappa_xz', 'kappa_xy'],
                        inplace=True)
        
        kappa_data.columns = ['t', 'kappa_yy', 'kappa_zz', 'kappa_xx',
                              'kappa_ave']
        
        amset_data_p = read_amset_csv(amset_p)
        amset_data_n = read_amset_csv(amset_n)
        
        # Combine AMSET and Phono3py data into ZT datasets, then convert to
        # 2D data.
        
        zt_data[k] = (dataset_to_2d(
                          zt_dataset_from_data(amset_data_p, kappa_data)),
                      dataset_to_2d(
                          zt_dataset_from_data(amset_data_n, kappa_data)))

    # Setup Matplotlib.

    setup_matplotlib()
    
    # Plot parameters.

    t_min, t_max = 300., 900.

    zt_contour_levels = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5]
    
    subplot_labels = ["p-type SnS", "n-type SnS", "p-type SnSe", "n-type SnSe"]

    # Custom formatters for labels.

    def contour_fmt(v):
        if v % 1.0 == 0:
            return "{0:.0f}".format(v)

        if v % 0.5 == 0:
            return "{0:.1f}".format(v)

        return "{0:.2f}".format(v)

    def log_fmt(v, pos):
        return "$10^{{{0:.0f}}}$".format(v)
    
    log_formatter = FuncFormatter(log_fmt)
    
    # To use a common colour bar, we need to determine the "global" ZT_max
    # across all datasets in the range (t_min, t_max). Once we've done this,
    # we can create a matplotlib.colors.Normalize to colour the 2D plots.
    
    global_zt_max = 0.
    
    for data_p, data_n in zt_data.values():
        for n, t, data in data_p, data_n:
            t_mask = np.logical_and(t >= t_min, t <= t_max)
            global_zt_max = max(global_zt_max, data['zt_ave'][:, t_mask].max())
    
    norm = Normalize(vmin=0.0, vmax=global_zt_max)

    # Plot.

    plt.figure(figsize=(14.0 / 2.54, 14.0 / 2.54))
    
    # Use a GridSpec to divide the plot into a four subplot axes and a colour
    # bar axis.

    grid_spec = GridSpec(9, 2)

    subplot_axes = []

    for r in range(2):
        for c in range(2):
            subplot_axes.append(
                plt.subplot(grid_spec[4 * r + 1:4 * (r + 1) + 1, c]))

    cbar_axes = plt.subplot(grid_spec[0, :])
    
    # Loop over SnS/SnSe and p- and n-type doping and draw a 2D colour plot
    # with contour lines.
    
    for i, k in enumerate(['SnS', 'SnSe']):
        data_p, data_n = zt_data[k]
        
        for j, (n, t, data) in enumerate([data_p, data_n]):
            axes = subplot_axes[2 * i + j]

            t_mask = np.logical_and(t >= t_min, t <= t_max)

            x = np.log10(n)
            y = t[t_mask]
            z = data['zt_ave'].T[t_mask, :]

            axes.pcolormesh(x, y, z, norm=norm, shading='gouraud')

            cs = axes.contour(x, y, z, levels=zt_contour_levels, colors='r')
            axes.clabel(cs, cs.levels, inline=True, fmt=contour_fmt)

    # Add colour bar.

    plt.colorbar(ScalarMappable(norm=norm), orientation='horizontal',
                 cax=cbar_axes)
    
    cbar_axes.set_ylabel(r"$ZT$")

    # Adjust axis ranges and labels.

    for axes in subplot_axes:
        axes.set_ylim(300.0, 900.0)

    for axes in subplot_axes:
        axes.xaxis.set_major_formatter(log_formatter)

    for axes in subplot_axes[-2:]:
        axes.set_xlabel(r"Doping Level $n$ [cm$^{-3}$]")

    for axes in subplot_axes[::2]:
        axes.set_ylabel(r"$T$ [K]")

    # Add subplot labels.

    for i, (axes, label) in enumerate(zip(subplot_axes, subplot_labels)):
        subplot_label = AnchoredText(
            r"({0}) {1}".format(chr(97 + i), label), loc='lower left',
            frameon=True)

        subplot_label.patch.set_edgecolor('k')
        subplot_label.patch.set_facecolor((1.0, 1.0, 1.0, 0.5))

        axes.add_artist(subplot_label)

    # Finalise and save.

    plt.tight_layout()

    plt.savefig(r"zt_plot.png", dpi=300)
    plt.close()
