class Burner:
    """
    Repräsentiert den Status des Brenners (AN/AUS).
    """

    def __init__(self):
        """
        Initialisiert den Brenner im AUS-Zustand.
        """
        self.is_on = False

    def switch_on(self):
        """
        Schaltet den Brenner EIN.
        """
        self.is_on = True

    def switch_off(self):
        """
        Schaltet den Brenner AUS.
        """
        self.is_on = False

    def status(self) -> str:
        """
        Gibt den Status des Brenners als String ("ON"/"OFF") zurück.
        """
        return "ON" if self.is_on else "OFF"