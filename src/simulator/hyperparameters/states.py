import random

def linear_age2state(age: int) -> str:
    death_probability = 0.01 * age/12
    if random.uniform(0, 1) < death_probability: state = "dead"
    else: state = "alive"

    return state
