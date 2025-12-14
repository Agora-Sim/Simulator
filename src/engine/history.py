import numpy as np

def get_alive_over_time(history: list) -> np.ndarray:
    nr_alive = []
    for month in history:
        nr_alive.append(sum(citizen.state == "alive" for citizen in month))
    nr_alive = np.array(nr_alive)

    return nr_alive

def get_money_over_time(history: list) -> np.ndarray:
    money_over_time = [np.mean([citizen.money for citizen in citizens]) for citizens in history]
    return np.array(money_over_time)

def get_age_over_time(history: list) -> np.ndarray:
    age_over_time = [np.mean([citizen.age for citizen in citizens]) for citizens in history]
    return np.array(age_over_time)/12

def get_time_axis(data: np.ndarray, steps_per_year: int = 12) -> tuple[np.ndarray, np.ndarray]:
    timepoints = np.arange(len(data)) // steps_per_year
    years, indices = np.unique(timepoints, return_index=True)
    return years, indices
