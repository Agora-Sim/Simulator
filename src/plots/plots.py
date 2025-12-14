# ================================================================
# 0. Section: Imports
# ================================================================
import matplotlib.pyplot as plt

from ..engine.history import *
from .plot_utils import *



# ================================================================
# 1. Section: Plotting Functions
# ================================================================
def plot_state_summary(history: list, ax: plt.Axes = None) -> plt.Axes | tuple[plt.Figure, plt.Axes]:
    nr_alive = get_alive_over_time(history)
    years, indices = get_time_axis(nr_alive, 12)

    fig, ax, created_fig = ensure_ax(ax)
    ax.plot(nr_alive)

    ax.set_xticks(indices, list(map(str, years)))
    ax.set_xlabel('Years')
    ax.set_ylabel('Nº of Alive Citizens')

    return finalize_plot(created_fig, fig, ax)

def plot_money_summary(history: list, ax: plt.Axes = None) -> plt.Axes | tuple[plt.Figure, plt.Axes]:
    money_over_time = get_money_over_time(history)
    years, indices = get_time_axis(money_over_time, 12)

    fig, ax, created_fig = ensure_ax(ax)
    ax.plot(money_over_time)

    ax.set_xticks(indices, list(map(str, years)))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Money')

    return finalize_plot(created_fig, fig, ax)

def plot_age_summary(history: list, ax: plt.Axes = None) -> plt.Axes | tuple[plt.Figure, plt.Axes]:
    age_over_time = get_age_over_time(history)
    years, indices = get_time_axis(age_over_time)

    fig, ax, created_fig = ensure_ax(ax)
    ax.plot(age_over_time)

    ax.set_xticks(indices, list(map(str, years)))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Age (years)')

    return finalize_plot(created_fig, fig, ax)