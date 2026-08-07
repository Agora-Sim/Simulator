# ================================================================
# 0. Section: IMPORTS
# ================================================================
from .metric_renderer import MetricRenderer
from .line_plot import LinePlot
from .heatmap_plot import HeatmapPlot

_RENDERERS: dict[str, type[MetricRenderer]] = {
    "line": LinePlot,
    "heatmap": HeatmapPlot,
}


# ================================================================
# 1. Section: Registry
# ================================================================
def renderer_for(plot_kind: str) -> MetricRenderer:
    try:
        return _RENDERERS[plot_kind]()
    except KeyError:
        known = ", ".join(sorted(_RENDERERS))
        raise KeyError(
            f"No renderer registered for plot_kind {plot_kind!r}. Known: {known}."
        ) from None
