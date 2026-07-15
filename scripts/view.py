# ================================================================
# 0. Section: IMPORTS
# ================================================================
from simulator import Visualizer

from simulator.domain.analysis.metrics import AgeMetric


# ================================================================
# 1. Section: INPUTS
# ================================================================



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    view = Visualizer(
        simulation_name="test_simulation",
        simulation_description="the simulation to test",
    )

    view.render_metrics(
        metrics = [AgeMetric("months")],
        formats = ["png"],
    )
