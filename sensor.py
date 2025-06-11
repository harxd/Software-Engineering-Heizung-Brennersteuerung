import random


class TemperatureSensor:
    """
    Simulates a temperature sensor with realistic temperature changes based on burner status.
    """
    def __init__(self, initial_temp: float = 20.0):
        self.current_temperature = initial_temp
        self.min_temperature = 10.0
        self.heating_rate = 0.5  # Temperature increase per second when heating
        self.cooling_rate = 0.3  # Temperature decrease per second when cooling

    def get_temperature(self, burner_is_on: bool) -> float:
        """
        Updates and returns the current temperature based on burner status.
        """
        if burner_is_on:
            # Temperature rises when burner is on
            self.current_temperature += self.heating_rate
        else:
            # Temperature falls when burner is off, but not below min_temperature
            if self.current_temperature > self.min_temperature:
                self.current_temperature -= self.cooling_rate
            
        # Add small random fluctuation
        self.current_temperature += random.uniform(-0.1, 0.1)
        
        # Ensure we don't go below minimum temperature
        self.current_temperature = max(self.min_temperature, self.current_temperature)
        
        return round(self.current_temperature, 2)