from src import Simulation, show_style

# Inspect the Portugal style
#show_style(style_label="portugal_style")

#sim = Simulation.random(10)
#sim.run()

sim = Simulation.load("runs/simulation_run_20251214_221359.pkl")

sim.summary()