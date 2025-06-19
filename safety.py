class SafetySystem:
    """
    Überwacht das Heizsystem auf Übertemperatur und Sensorfehler.
    Erkennt Not-Aus-Bedingungen und verwaltet deren Status.
    """

    def __init__(self, max_temp=95.0):
        """
        Initialisiert das SafetySystem mit maximal zulässiger Temperatur.

        :param max_temp: Maximale erlaubte Temperatur (Standard: 95.0°C)
        """
        self.max_temp = max_temp
        self.emergency_shutdown = False
        self.last_error = None

    def check(self, current_temp):
        """
        Prüft auf Übertemperatur und Sensorfehler.
        Gibt True zurück, wenn ein Not-Aus ausgelöst werden muss.

        :param current_temp: Aktuelle Temperatur (float oder int)
        :return: True, wenn Not-Aus aktiv ist, sonst False
        """
        # Wenn Not-Aus einmal ausgelöst wurde, bleibt er aktiv
        if self.emergency_shutdown:
            return True

        # Sensorfehler: None oder kein float/int
        if current_temp is None or not isinstance(current_temp, (float, int)):
            self.emergency_shutdown = True
            self.last_error = "Sensorfehler"
            return True

        # Übertemperatur
        if current_temp >= self.max_temp:
            self.emergency_shutdown = True
            self.last_error = "Übertemperatur"
            return True

        # Alles ok
        self.last_error = None
        return False

    def reset(self):
        """
        Setzt den Not-Aus-Zustand zurück.
        """
        self.emergency_shutdown = False
        self.last_error = None