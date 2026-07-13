# ================================================================
# 0. Section: IMPORTS
# ================================================================
from simulator import Simulation


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
    sim = Simulation(
        simulation_name="test_simulation",
        simulation_description="the simulation to test",
    )

    sim.init_simulation()

    input("Update the config file")

    sim.run_simulation()

    for i in range(5):
        sim_run = sim.load_run(i+1)

        print(sim_run.history[-1])
