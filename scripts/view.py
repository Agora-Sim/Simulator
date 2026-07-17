# ================================================================
# 0. Section: IMPORTS
# ================================================================
from simulator import Visualizer

from simulator.domain.analysis.metrics import AgeMetric, HealthMetric, AliveMetric


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
        simulation_name="test_simulation_3",
        simulation_description="the simulation to test",
    )

    view.render_summary_grid(
        metrics = [
            HealthMetric(),
            AgeMetric("months"),
            AliveMetric(),
        ],
        formats = ["png"],
    )

    view.render_metrics(
        metrics = [
            HealthMetric(),
            AgeMetric("months"),
            AliveMetric(),
        ],
        formats = ["png"],
    )
