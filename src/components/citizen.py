import random

import numpy as np

from src.hyperparameters import linear_age2state

class Citizen:
    def __init__(self, citizen_id: int, age: int, money:float, state: str):
        self.citizen_id = citizen_id
        self.age = age
        self.money = np.round(money,2)
        self.state = state



    # ================================================================
    # 1. Section: Initializers
    # ================================================================
    @classmethod
    def random(cls, citizen_id: int):
        age = random.randint(0, 100*12)
        money = random.uniform(0.0, 10000.0)
        state = "alive"
        return cls(citizen_id, age, money, state)
    


    # ================================================================
    # 2. Section: Methods
    # ================================================================
    def age_citizen(self):
        self.age += 1
        self.check_state()

    def check_state(self):
        self.state = linear_age2state(self.age)



    # ================================================================
    # 3. Section: Properties
    # ================================================================
    @property
    def citizen_id(self):
        return self._citizen_id
    @citizen_id.setter
    def citizen_id(self, value: int):
        if value < 0:
            raise ValueError("Citizen ID cannot be negative.")
        self._citizen_id = value

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value: int):
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self._age = value

    @property
    def money(self):
        return self._money
    @money.setter
    def money(self, value: float):
        self._money = value

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value: str):
        if value not in ["alive", "dead"]:
            raise ValueError("State must be either 'alive' or 'dead'.")
        self._state = value



    # ================================================================
    # 4. Section: Representations
    # ================================================================
    def __repr__(self):
        return f"Citizen(id={self.citizen_id}, age={self.age}, money={self.money}, state={self.state})"