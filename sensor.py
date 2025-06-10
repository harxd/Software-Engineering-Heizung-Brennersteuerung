import random


class TemperatureSensor:
    """
    Simulates a temperature sensor to measure the current temperature.
    """
    def __init__(self, initial_temp: float = 20.0):
        self.current_temperature = initial_temp

    def get_temperature(self) -> float:
        """
        Simulates temperature fluctuation and returns the current temperature.
        """
        # Simulate small random fluctuation in temperature
        self.current_temperature += random.uniform(-0.5, 0.5)
        return round(self.current_temperature, 2)