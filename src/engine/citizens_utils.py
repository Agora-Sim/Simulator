import numpy as np

def age_citizens(citizens: np.ndarray) -> None:
    for citizen in citizens: 
        if(citizen.state == "alive"): citizen.age_citizen()