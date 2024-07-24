# elec_n_plot.py


"""
In this example, we prepare a plot to compare the electrical properties \sigma,
S, S^2 \sigma (PF) and \kappa_el of p- and n-type Pnma SnS and SnSe as a
function of doping level at a fixed T = 700 K.

The calculation combines data from two papers:

    Thermoelectric Properties of Pnma and Rocksalt SnS and SnSe
    J. M. Flitcroft, I. Pallikara and J. M. Skelton
    Solids 3 (1), 155-176 (2022), DOI: 10.3390/solids3010011
    
    Thermoelectric properties of Pnma and R3m GeS and GeSe
    M. Zhang, J. Flictroft, S. Guillemot and J. Skelton
    J. Mater. Chem. C 11, 14833 (2023, DOI: 10.1039/D3TC02938G
"""


import numpy as np
import matplotlib.pyplot as plt

from matplotlib.offsetbox import AnchoredText

from zt_calc_workflow.amset import read_amset_csv
from zt_calc_workflow.plotting import setup_matplotlib


if __name__ == "__main__":
    # Read input data.

    amset_data = {
        'SnS' : (read_amset_csv("SnS-Pnma-AMSET-p.csv"),
                 read_amset_csv("SnS-Pnma-AMSET-n.csv")),
        'SnSe' : (read_amset_csv("SnSe-Pnma-AMSET-p.csv"),
                  read_amset_csv("SnSe-Pnma-AMSET-n.csv"))}

    # Setup Matplotlib.

    setup_matplotlib()

    # Plot parameters.

    t_plot = 700.0
    
    colours = ['b', 'r']

    xlim = (1.0e16, 1.0e20)
    ylim_sets = [(0.0, 750.0), (0.0, 750.0), (0.0, 6.0), (0.0, 1.0)]

    # Plot.
    
    plt.figure(figsize=(16.2 / 2.54, 13.5 / 2.54))

    subplot_axes = [plt.subplot(2, 2, i + 1) for i in range(4)]

    for data_k, axes in zip(
            ['sigma_ave', 's_ave', 'pf_ave', 'kappa_el_ave'], subplot_axes):

        for sys_k, c in zip(['SnS', 'SnSe'], colours):
            data_p, data_n = amset_data[sys_k]
            
            # Extract data at plot temperature.
            
            data_p = data_p[data_p['t'] == t_plot]
            data_n = data_n[data_n['t'] == t_plot]
            
            for data, l, d in [(data_p, sys_k, (None, None)),
                               (data_n, None, (3.0, 1.0))]:
                # Plot |S| rather than S.
                
                y = (np.abs(data[data_k]) if data_k == 's_ave'
                         else data[data_k])
            
                axes.plot(data['n'], y, label=l, color=c, dashes=d)

        # "Fake" line to add a single entry for n-type doping.

        axes.plot([-0.75, -0.25], [-0.75, -0.25], label="n-type", color='k',
                  dashes=(3.0, 1.0))

    # Adjust axis scales/ranges and labels.

    for axes in subplot_axes:
        axes.set_xscale('log')
        axes.set_xlim(xlim)

    for axes, ylim in zip(subplot_axes, ylim_sets):
        axes.set_ylim(ylim)
        
        y_min, y_max = ylim
        axes.set_yticks(np.linspace(y_min, y_max, 6))

    for axes in subplot_axes:
        axes.set_xlabel(r"Doping Level $n$ [cm$^{-3}$]")

    subplot_axes[0].set_ylabel(r"$\sigma$ [S cm$^{-1}$]")
    subplot_axes[1].set_ylabel(r"$|S|$ [$\mathrm{\mu}$V K$^{-1}$]")
    subplot_axes[2].set_ylabel(r"$S^2 \sigma$ (PF) [mW m$^{-1}$ K$^{-2}$]")
    subplot_axes[3].set_ylabel(r"$\kappa_\mathrm{el}$ [W m$^{-1}$ K$^{-1}$]")

    # Add legend.

    legend = subplot_axes[0].legend(loc='upper left')
    legend.get_frame().set_edgecolor('k')
    legend.get_frame().set_facecolor((1.0, 1.0, 1.0, 0.5))

    # Add subplot labels.

    locs = ['lower left', 'upper right', 'upper left', 'upper left']

    for i, (axes, loc) in enumerate(zip(subplot_axes, locs)):
        subplot_label = AnchoredText(
            r"({0})".format(chr(97 + i)), loc=loc, frameon=True)

        subplot_label.patch.set_edgecolor('k')
        subplot_label.patch.set_facecolor((1.0, 1.0, 1.0, 0.5))

        axes.add_artist(subplot_label)

    # Add gridlines.

    for axes in subplot_axes:
        axes.grid(color=(0.9, 0.9, 0.9), dashes=(3.0, 1.0), linewidth=0.5)
        axes.set_axisbelow(True)

    plt.tight_layout()

    # Finalise and save.

    plt.savefig(r"elec_n_plot.png", dpi=300)
    plt.close()
