import math

import matplotlib.pyplot as plt

def ensure_ax(ax: plt.Axes = None) -> tuple[plt.Figure, plt.Axes, bool]:
    """Ensure that a matplotlib Axes object is available."""
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots()
        created_fig = True
    else:
        fig = ax.figure

    return fig, ax, created_fig

def finalize_plot(created_fig: bool, fig: plt.Figure, ax: plt.Axes) -> tuple[plt.Figure, plt.Axes] | plt.Axes:
    """Finalize the plot by showing it if it was created within the function."""
    if created_fig:
        plt.tight_layout()
        plt.show()
        return fig, ax
    else:
        return ax
    
def select_plot_functions(include: tuple, registry: dict) -> list:
    """Select plot functions from the registry based on the include list."""
    return [registry[name] for name in include if name in registry]

def define_row_col_layout(nr_plots: int) -> tuple[int, int]:
    """Define the number of rows and columns for subplots based on the number of plots."""
    if nr_plots <= 0:
        nr_rows, nr_cols = 0, 0
    else:
        nr_cols = math.ceil(math.sqrt(nr_plots))
        nr_rows = math.ceil(nr_plots / nr_cols)
    return nr_rows, nr_cols