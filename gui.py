import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow library required
import os

class HeatingControlGUI:
    def __init__(self, controller, safety=None):
        self.controller = controller
        self.safety = safety  # Referenz auf SafetySystem für Reset
        self.root = tk.Tk()
        self.root.title("Heizung – Brennersteuerung")
        self.root.geometry("250x370")  # GUI etwas länger gemacht

        # Einheitliches Button-Font
        self.button_font = ('Arial', 12, 'bold')

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Temperature display
        ttk.Label(main_frame, text="Ist-Temperatur:", font=('Arial', 12)).grid(row=0, column=0, pady=5)
        self.current_temp_var = tk.StringVar(value="--.-°C")
        ttk.Label(main_frame, textvariable=self.current_temp_var, font=('Arial', 12, 'bold')).grid(row=0, column=1, pady=5)

        # Target temperature controls
        ttk.Label(main_frame, text="Soll-Temperatur:", font=('Arial', 12)).grid(row=1, column=0, pady=5)
        self.target_temp_var = tk.StringVar(value=f"{controller.target_temperature:.1f}°C")
        ttk.Label(main_frame, textvariable=self.target_temp_var, font=('Arial', 12, 'bold')).grid(row=1, column=1, pady=5)

        # Temperature adjustment buttons
        temp_button_frame = ttk.Frame(main_frame)
        temp_button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(temp_button_frame, text="-", command=self.decrease_temp, width=5, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(temp_button_frame, text="+", command=self.increase_temp, width=5, style="TButton").grid(row=0, column=1, padx=5)

        # Pfad zum media-Ordner
        media_path = os.path.join(os.path.dirname(__file__), "media")

        # Burner status image
        ttk.Label(main_frame, text="Brenner:", font=('Arial', 12)).grid(row=3, column=0, pady=10)
        self.burner_img_off = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "burner_off.png")).resize((48, 48)))
        self.burner_img_on = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "burner_on.png")).resize((48, 48)))
        self.burner_img_label = tk.Label(main_frame, image=self.burner_img_off)
        self.burner_img_label.grid(row=3, column=1, pady=10)

        # Emergency status image
        ttk.Label(main_frame, text="Not-Aus:", font=('Arial', 12)).grid(row=4, column=0, pady=10)
        self.siren_img_off = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "emergency_off.png")).resize((48, 48)))
        self.siren_img_on = ImageTk.PhotoImage(Image.open(os.path.join(media_path, "emergency_on.png")).resize((48, 48)))
        self.siren_img_label = tk.Label(main_frame, image=self.siren_img_off)
        self.siren_img_label.grid(row=4, column=1, pady=10)

        # Optional: Error message
        self.error_var = tk.StringVar(value="")
        self.error_label = ttk.Label(main_frame, textvariable=self.error_var, foreground="red", font=('Arial', 10, 'bold'))
        self.error_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Notüberbrückung Button
        self.reset_button = ttk.Button(main_frame, text="Notüberbrückung", command=self.reset_emergency, state="disabled", style="TButton")
        self.reset_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

        # Style für alle Buttons setzen
        style = ttk.Style()
        style.configure("TButton", font=self.button_font)

    def increase_temp(self):
        self.controller.target_temperature += 0.5
        self.update_target_temp_display()

    def decrease_temp(self):
        self.controller.target_temperature -= 0.5
        self.update_target_temp_display()

    def update_target_temp_display(self):
        self.target_temp_var.set(f"{self.controller.target_temperature:.1f}°C")

    def update_current_temp(self, temp):
        self.current_temp_var.set(f"{temp:.1f}°C")

    def update_burner_status(self, status):
        if status == "ON":
            self.burner_img_label.configure(image=self.burner_img_on)
            self.current_burner_img = self.burner_img_on
        else:
            self.burner_img_label.configure(image=self.burner_img_off)
            self.current_burner_img = self.burner_img_off

    def update_emergency_status(self, emergency, error_msg=None):
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
        if self.safety:
            self.safety.reset()
            self.update_emergency_status(False)

    def start(self):
        self.root.mainloop()