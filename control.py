class TemperatureController:
    """
    Controls the system by comparing the target temperature with the current temperature.
    """
    def __init__(self, target_temp: float):
        self.target_temperature = target_temp

    def check_temperature(self, current_temp: float) -> bool:
        """
        Compares the target and current temperatures.
        Returns True to turn the burner ON, otherwise False.
        """
        # Turn on burner if current temperature is below target
        return current_temp < self.target_temperature