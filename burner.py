class Burner:
    """
    Represents the burner status (ON/OFF).
    """
    def __init__(self):
        self.is_on = False

    def switch_on(self):
        """Switch the burner ON."""
        self.is_on = True

    def switch_off(self):
        """Switch the burner OFF."""
        self.is_on = False

    def status(self) -> str:
        """Returns the burner's status (ON/OFF) as a string."""
        return "ON" if self.is_on else "OFF"