# ================================================================
# 0. Section: Imports
# ================================================================
import numpy as np
import matplotlib.pyplot as plt

from ..engine.history import *
from .plot_utils import *
from .plots import *

from ..styling.font_initializer  import *
plt.style.use("src/styling/portugal_style.mplstyle")



# ================================================================
# 1. Section: Plot Registry
# ================================================================
PLOT_REGISTRY = {
    'alive': plot_state_summary,
    'money': plot_money_summary,
    'age': plot_age_summary
}



# ================================================================
# 2. Section: Summary Plotting
# ================================================================
def plot_summary(history: list, include: tuple = ('alive', 'money', 'age')) -> tuple[plt.Figure, plt.Axes] | plt.Axes:
    plot_functions = select_plot_functions(include, PLOT_REGISTRY)
    nr_plots = len(plot_functions)

    nr_rows, nr_cols = define_row_col_layout(nr_plots)
    fig, axes = plt.subplots(nr_rows, nr_cols, sharex=True, figsize=(5*nr_cols, 4*nr_rows))

    # Normalize axes to a flat list so we can index them consistently
    if isinstance(axes, plt.Axes) or hasattr(axes, 'plot') and not isinstance(axes, (list, np.ndarray)): axes = [axes]
    else: axes = np.array(axes).ravel().tolist()

    # Draw only on the required number of axes
    for ax, func in zip(axes[:nr_plots], plot_functions): func(history, ax=ax)
    for ax in axes[nr_plots:]: ax.set_visible(False)

    fig.suptitle('Simulation Summary', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])


    plt.show()

    return fig, axes[:nr_plots]
