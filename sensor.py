import random


class TemperatureSensor:
    """
    Simuliert einen Temperatursensor mit realistischen Temperaturänderungen
    abhängig vom Brennerstatus.
    """

    def __init__(self, initial_temp: float = 20.0):
        """
        Initialisiert den Sensor mit einer Starttemperatur.

        :param initial_temp: Anfangstemperatur in Grad Celsius (Standard: 20.0)
        """
        self.current_temperature = initial_temp
        self.min_temperature = 5.0
        self.heating_rate = 0.05  # Temperaturanstieg pro Sekunde beim Heizen
        self.cooling_rate = 0.03  # Temperaturabfall pro Sekunde beim Kühlen

    def get_temperature(self, burner_is_on: bool) -> float:
        """
        Aktualisiert und gibt die aktuelle Temperatur zurück, abhängig vom Brennerstatus.

        :param burner_is_on: True, wenn der Brenner an ist, sonst False
        :return: Aktuelle Temperatur (float, gerundet auf 2 Nachkommastellen)
        """
        if burner_is_on:
            self.current_temperature += self.heating_rate
        else:
            if self.current_temperature > self.min_temperature:
                self.current_temperature -= self.cooling_rate

        # Kleine zufällige Schwankung hinzufügen
        self.current_temperature += random.uniform(-0.01, 0.01)

        # Temperatur nicht unter das Minimum fallen lassen
        self.current_temperature = max(self.min_temperature, self.current_temperature)

        return round(self.current_temperature, 2)