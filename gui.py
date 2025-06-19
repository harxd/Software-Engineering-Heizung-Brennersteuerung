import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow library required
import os

class HeatingControlGUI:
    """
    Grafische Benutzeroberfläche für die Heizung-Brennersteuerung.
    Zeigt aktuelle Werte an und ermöglicht die Steuerung der Soll-Temperatur sowie das Anzeigen von Statusbildern.
    """

    def __init__(self, controller, safety=None):
        """
        Initialisiert die GUI mit Controller und optionalem Safety-System.

        :param controller: TemperatureController-Objekt zur Steuerung der Soll-Temperatur.
        :param safety: Optionales SafetySystem-Objekt für Notfall-Reset.
        """
        self.controller = controller
        self.safety = safety  # Referenz auf SafetySystem für Reset
        self.root = tk.Tk()
        self.root.title("Heizung – Brennersteuerung")
        self.root.geometry("250x370")  # GUI etwas länger gemacht

        # Einheitliches Button-Font
        self.button_font = ('Arial', 12, 'bold')

        # Haupt-Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Ist-Temperatur-Anzeige
        ttk.Label(main_frame, text="Ist-Temperatur:", font=('Arial', 12)).grid(row=0, column=0, pady=5)
        self.current_temp_var = tk.StringVar(value="--.-°C")
        ttk.Label(main_frame, textvariable=self.current_temp_var, font=('Arial', 12, 'bold')).grid(row=0, column=1, pady=5)

        # Soll-Temperatur-Anzeige
        ttk.Label(main_frame, text="Soll-Temperatur:", font=('Arial', 12)).grid(row=1, column=0, pady=5)
        self.target_temp_var = tk.StringVar(value=f"{controller.target_temperature:.1f}°C")
        ttk.Label(main_frame, textvariable=self.target_temp_var, font=('Arial', 12, 'bold')).grid(row=1, column=1, pady=5)

        # Temperatur-Einstellungs-Buttons
        temp_button_frame = ttk.Frame(main_frame)
        temp_button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(temp_button_frame, text="-", command=self.decrease_temp, width=5, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(temp_button_frame, text="+", command=self.increase_temp, width=5, style="TButton").grid(row=0, column=1, padx=5)

        # Pfad zum media-Ordner
        media_path = os.path.join(os.path.dirname(__file__), "media")

        # Brennerstatus-Bild
        ttk.Label(main_frame, text="Brenner:", font=('Arial', 12)).grid(row=3, column=0, pady=10)
        self.burner_img_off = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "burner_off.png")).resize((48, 48)))
        self.burner_img_on = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "burner_on.png")).resize((48, 48)))
        self.burner_img_label = tk.Label(main_frame, image=self.burner_img_off)
        self.burner_img_label.grid(row=3, column=1, pady=10)

        # Not-Aus-Bild
        ttk.Label(main_frame, text="Not-Aus:", font=('Arial', 12)).grid(row=4, column=0, pady=10)
        self.siren_img_off = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "emergency_off.png")).resize((48, 48)))
        self.siren_img_on = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "emergency_on.png")).resize((48, 48)))
        self.siren_img_label = tk.Label(main_frame, image=self.siren_img_off)
        self.siren_img_label.grid(row=4, column=1, pady=10)

        # Fehlernachricht
        self.error_var = tk.StringVar(value="")
        self.error_label = ttk.Label(main_frame, textvariable=self.error_var, foreground="red", font=('Arial', 10, 'bold'))
        self.error_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Notüberbrückung Button
        self.reset_button = ttk.Button(
            main_frame,
            text="Notüberbrückung",
            command=self.reset_emergency,
            state="disabled",
            style="TButton"
        )
        self.reset_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Grid-Konfiguration
        main_frame.columnconfigure(1, weight=1)

        # Style für alle Buttons setzen
        style = ttk.Style()
        style.configure("TButton", font=self.button_font)

    def increase_temp(self):
        """
        Erhöht die Soll-Temperatur um 0.5°C.
        """
        self.controller.target_temperature += 0.5
        self.update_target_temp_display()

    def decrease_temp(self):
        """
        Verringert die Soll-Temperatur um 0.5°C.
        """
        self.controller.target_temperature -= 0.5
        self.update_target_temp_display()

    def update_target_temp_display(self):
        """
        Aktualisiert die Anzeige der Soll-Temperatur.
        """
        self.target_temp_var.set(f"{self.controller.target_temperature:.1f}°C")

    def update_current_temp(self, temp):
        """
        Aktualisiert die Anzeige der Ist-Temperatur.
        :param temp: Aktuelle Temperatur (float)
        """
        self.current_temp_var.set(f"{temp:.1f}°C")

    def update_burner_status(self, status):
        """
        Aktualisiert das Brennerstatus-Bild.
        :param status: "ON" oder "OFF"
        """
        if status == "ON":
            self.burner_img_label.configure(image=self.burner_img_on)
            self.current_burner_img = self.burner_img_on
        else:
            self.burner_img_label.configure(image=self.burner_img_off)
            self.current_burner_img = self.burner_img_off

    def update_emergency_status(self, emergency, error_msg=None):
        """
        Aktualisiert das Not-Aus-Bild und die Fehleranzeige.
        :param emergency: True, wenn Not-Aus aktiv ist
        :param error_msg: Optionaler Fehlertext
        """
        if emergency:
            self.siren_img_label.configure(image=self.siren_img_on)
            self.current_siren_img = self.siren_img_on
            if error_msg:
                self.error_var.set(error_msg)
            self.reset_button.config(state="normal")
        else:
            self.siren_img_label.configure(image=self.siren_img_off)
            self.current_siren_img = self.siren_img_off
            self.error_var.set("")
            self.reset_button.config(state="disabled")

    def reset_emergency(self):
        """
        Setzt den Not-Aus-Zustand zurück, falls ein SafetySystem vorhanden ist.
        """
        if self.safety:
            self.safety.reset()
            self.update_emergency_status(False)

    def start(self):
        """
        Startet die Tkinter-Hauptschleife.
        """
        self.root.mainloop()