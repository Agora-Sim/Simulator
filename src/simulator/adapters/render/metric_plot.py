# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from dataclasses import dataclass
from matplotlib.figure import Figure

from ...domain.analysis import MetricSeries


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class MetricPlot:
    series: MetricSeries

    def render(self) -> Figure:

        print(self.series.std)
        plt.figure()
        plt.plot(self.series.timepoints, self.series.mean)
        plt.fill_between(
            self.series.timepoints,
            self.series.mean - self.series.std,
            self.series.mean + self.series.std,
            alpha=0.2,
        )
        plt.xlabel(f"Time ({self.series.time_unit})")
        plt.ylabel(f"{self.series.name} ({self.series.unit})")
        plt.title(self.series.name)
        return plt.gcf()
