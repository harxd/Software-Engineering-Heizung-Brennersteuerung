import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow library required

class HeatingControlGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Heizung – Brennersteuerung")
        self.root.geometry("200x200")
        
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
        
        ttk.Button(temp_button_frame, text="-", command=self.decrease_temp, width=5).grid(row=0, column=0, padx=5)
        ttk.Button(temp_button_frame, text="+", command=self.increase_temp, width=5).grid(row=0, column=1, padx=5)
        
        # Burner status image
        ttk.Label(main_frame, text="Brenner:", font=('Arial', 12)).grid(row=3, column=0, pady=15)
        # Load images (ensure these files exist in your project directory)
        self.burner_img_off = ImageTk.PhotoImage(Image.open("burner_off.png").resize((48, 48)))
        self.burner_img_on = ImageTk.PhotoImage(Image.open("burner_on.png").resize((48, 48)))
        self.burner_img_label = ttk.Label(main_frame, image=self.burner_img_off)
        self.burner_img_label.grid(row=3, column=1, pady=15)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
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
        # Use images instead of text
        if status == "ON":
            self.burner_img_label.configure(image=self.burner_img_on)
            self.burner_img_label.image = self.burner_img_on
        else:
            self.burner_img_label.configure(image=self.burner_img_off)
            self.burner_img_label.image = self.burner_img_off
        
    def start(self):
        self.root.mainloop()