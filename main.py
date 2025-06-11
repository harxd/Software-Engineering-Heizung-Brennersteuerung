from sensor import TemperatureSensor
from control import TemperatureController
from burner import Burner
import time
import threading
import os
import msvcrt  # Windows-specific keyboard input


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def handle_user_input(controller):
    """Handle user input for temperature changes using + and - keys"""
    print("\nSteuerung: '+' erhöht die Temperatur, '-' verringert sie, 'Strg + C' beendet das Programm")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == '+':
                controller.target_temperature += 0.5
            elif key == '-':
                controller.target_temperature -= 0.5


def display_status(current_temp, target_temp, burner_status):
    """Display the current status in a clean format"""
    clear_screen()
    print("Heizung – Brennersteuerung Simulation")
    print("-" * 40)
    print(f"Ist-Temperatur:   {current_temp:>5.2f}°C")
    print(f"Soll-Temperatur:  {target_temp:>5.2f}°C")
    print(f"Brenner:          {burner_status}")
    print("-" * 40)
    print("\nSteuerung: '+' erhöht die Soll-Temperatur, '-' verringert sie, 'Strg + C' beendet das Programm")


def main():
    # Initialize components
    sensor = TemperatureSensor(initial_temp=15.0)
    controller = TemperatureController(target_temp=22.0)
    burner = Burner()

    # Start user input thread
    input_thread = threading.Thread(target=handle_user_input, args=(controller,), daemon=True)
    input_thread.start()

    # Main simulation loop
    try:
        while True:
            current_temp = sensor.get_temperature(burner.is_on)

            if controller.check_temperature(current_temp):
                burner.switch_on()
            else:
                burner.switch_off()

            display_status(current_temp, controller.target_temperature, burner.status())
            time.sleep(1)

    except KeyboardInterrupt:
        clear_screen()
        print("\nSimulation beendet.")


if __name__ == "__main__":
    main()