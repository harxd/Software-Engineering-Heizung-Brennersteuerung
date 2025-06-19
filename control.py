class TemperatureController:
    """
    Regelt das System, indem die Soll- mit der Ist-Temperatur verglichen wird.
    """

    def __init__(self, target_temp: float):
        """
        Initialisiert den Controller mit einer Soll-Temperatur.
        
        :param target_temp: Die gewünschte Soll-Temperatur in Grad Celsius.
        """
        self.target_temperature = target_temp

    def check_temperature(self, current_temp: float) -> bool:
        """
        Vergleicht Soll- und Ist-Temperatur.
        Gibt True zurück, wenn der Brenner eingeschaltet werden soll (Ist < Soll).
        
        :param current_temp: Die aktuelle Temperatur in Grad Celsius.
        :return: True, wenn Brenner AN, sonst False.
        """
        return current_temp < self.target_temperature