# k_latt_crta_plot.py


""" In this example, we prepare a plot to compare the data from a
"constant relaxation-time approximation" ("CRTA") analysis of the lattice
thermal conductivity of Pnma SnS and SnSe.

We plot the principal xx, yy and zz components of the three CRTA quantities,
\kappa, \kappa / \tau^CRTA (harmonic function) and \tau^CRTA (weighted-average
lifetime), together with the average.

The calculation uses data from the paper:

    Approximate models for the lattice thermal conductivity of alloy
        thermoelectrics
    J. M. Skelton
    J. Mater. Chem. C 9 (35), 11772 (2021), DOI: 10.1039/D1TC02026A
"""


import matplotlib.pyplot as plt

from matplotlib.offsetbox import AnchoredText

from zt_calc_workflow.phono3py import read_phono3py_crta_csv
from zt_calc_workflow.plotting import setup_matplotlib


if __name__ == "__main__":
    # Read input data.
    
    crta_sns = read_phono3py_crta_csv(r"SnS-kappa-m16816.Prim-CRTA.csv")
    crta_snse = read_phono3py_crta_csv(r"SnSe-kappa-m16816.Prim-CRTA.csv")
    
    # Setup Matplotlib.
    
    setup_matplotlib()
    
    # Plot parameters.
    
    plot_labels = ["$xx$", "$yy$", "$zz$", "ave"]
    plot_colours = ['b', 'r', 'g', 'k']
    
    # Plot.
    
    plt.figure(figsize=(12. / 2.54, 15. / 2.54))
    
    subplot_axes = [plt.subplot(3, 2, i + 1) for i in range(6)]
    
    # Loop over SnS/SnSe (columns).
    
    for i, df in enumerate([crta_sns, crta_snse]):
        # Loop over \kappa, \kappa / \tau^CRTA and \tau^CRTA (rows).
        
        for axes, k in zip(
                subplot_axes[i::2], ['kappa', 'kappa_tau_crta', 'tau_crta']):
            
            # Loop over diagonal components of tensors and average.
            
            for suffix, l, c in zip(
                    ['xx', 'yy', 'zz', 'ave'], plot_labels, plot_colours):
                
                data_k = '{0}_{1}'.format(k, suffix)
                axes.plot(df['t'], df[data_k], label=l, color=c)
    
    # Adjust axis ranges and labels.
    
    for axes in subplot_axes:
        axes.set_xlim(0., 1000.)
    
    for i, y_max in enumerate([10., 1., 25.]):
        for axes in subplot_axes[2 * i:2 * (i + 1)]:
            axes.set_ylim(0., y_max)
    
    for axes in subplot_axes[-2:]:
        axes.set_xlabel(r"$T$ [K]")
    
    y_labels = [
        r"$\kappa$ [W m$^{-1}$ K$^{-1}$]",
        r"$\kappa / \tau^\mathrm{CRTA}$ [W m$^{-1}$ K$^{-1}$ ps$^{-1}$]",
        r"$\tau^\mathrm{CRTA}$ [ps]"]
    
    for i, y_label in enumerate(y_labels):
        subplot_axes[2 * i].set_ylabel(y_label)
    
    # Add legend.
    
    legend = subplot_axes[1].legend(loc='upper right')
    legend.get_frame().set_edgecolor('k')
    
    # Add subplot labels.
    
    subplot_label_locs = ['upper right', 'lower left', 'lower right',
                          'upper right', 'upper right', 'upper right']
    
    for i, (axes, loc) in enumerate(zip(subplot_axes, subplot_label_locs)):
        axes.add_artist(
            AnchoredText(r"({0})".format(chr(97 + i)), loc=loc))
    
    for axes in subplot_axes:
        axes.grid(color=(0.9, 0.9, 0.9), dashes=(3.0, 1.0), linewidth=.5)
    
    # Finalise and save.
    
    plt.tight_layout()
    
    plt.savefig(r"k_latt_crta_plot.png", dpi=300)
    plt.close()
