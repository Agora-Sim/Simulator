# ================================================================
# 0. Section: Imports
# ================================================================
from ...plots.plot_summary import plot_summary
from ...hyperparameters import INCLUDE_PLOTS



# ================================================================
# 1. Section: Summary
# ================================================================
class Summary:
     def summary(self):
        print(f"Simulation ran for {self.iterations} iterations.")
        alive_count = sum(citizen.state == "alive" for citizen in self.citizens)
        dead_count = sum(citizen.state == "dead" for citizen in self.citizens)
        print(f"Final counts - Alive: {alive_count}, Dead: {dead_count}")

        plot_summary(self.citizens_history, include=INCLUDE_PLOTS)