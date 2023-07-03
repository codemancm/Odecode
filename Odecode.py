import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import ttk
import threading
import sys
import os
import pkg_resources
import subprocess
import shutil
from PIL import Image, ImageTk

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_path)

def create_executable():
    file_path = entry.get()
    software_name = software_name_entry.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return

    if not software_name:
        messagebox.showerror("Error", "Please enter a software name.")
        return

    progress_bar.start()

    def create_executable_thread():
        try:
            # Check if the PyInstaller library is bundled within the application
            if not pkg_resources.resource_exists(__name__, "PyInstaller"):
                messagebox.showerror("Error", "PyInstaller library not found.")
                return

            # Create a temporary directory to hold the required PyInstaller files
            temp_dir = os.path.join(os.path.dirname(__file__), "pyinstaller_temp")
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)

            # Extract the bundled PyInstaller files to the temporary directory
            pkg_resources.extract_resources(__name__, "PyInstaller", temp_dir)

            # Execute the PyInstaller command using the bundled PyInstaller
            subprocess.call([sys.executable, os.path.join(temp_dir, "PyInstaller", "pyinstaller.py"), "--onefile", "-n", software_name, file_path])

            # Move the generated executable to the desktop folder
            desktop_path = os.path.expanduser("~/Desktop")
            shutil.move(os.path.join("dist", software_name), os.path.join(desktop_path, software_name))

            messagebox.showinfo("Success", "Executable created!\nSaved to the Desktop.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            progress_bar.stop()
            cleanup()

    # Create a new thread for executing the subprocess
    thread = threading.Thread(target=create_executable_thread)
    thread.start()

def cleanup():
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    if os.path.exists("build"):
        shutil.rmtree("build")

    temp_dir = os.path.join(os.path.dirname(__file__), "pyinstaller_temp")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

def select_logo():
    logo_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if logo_path:
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((200, 200))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label.config(image=logo_photo)
        logo_label.image = logo_photo

# Create the main window
window = tk.Tk()
window.title("Odecode")
window.geometry("500x500")

# Create the logo label
logo = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(window, image=logo)
logo_label.pack(pady=10)

# Create the software name label and entry
software_name_label = tk.Label(window, text="Enter the software name:", font=("Arial", 12))
software_name_label.pack()
software_name_entry = tk.Entry(window, width=40, font=("Arial", 12))
software_name_entry.pack(pady=5)

# Create the file path label and entry
file_path_label = tk.Label(window, text="Select a Python file:", font=("Arial", 12))
file_path_label.pack()

file_frame = tk.Frame(window)
file_frame.pack(pady=5)

entry = tk.Entry(file_frame, width=30, font=("Arial", 12))
entry.pack(side=tk.LEFT)

browse_button = tk.Button(file_frame, text="Browse", command=browse_file, font=("Arial", 12))
browse_button.pack(side=tk.LEFT, padx=5)

# Create the button to select the software logo
logo_button = tk.Button(window, text="Select Logo", command=select_logo, font=("Arial", 12))
logo_button.pack(pady=5)

# Create the button to create the executable
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

create_button = tk.Button(button_frame, text="Create Executable", command=create_executable, font=("Arial", 12))
create_button.pack()

# Create a separator line
separator = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=10)

# Create the logo preview label
logo_preview_label = tk.Label(window, text="Software Logo Preview:", font=("Arial", 12))
logo_preview_label.pack()

logo_preview_frame = tk.Frame(window)
logo_preview_frame.pack(pady=5)

default_logo = Image.open("default_logo.png")
default_logo = default_logo.resize((200, 200))
default_photo = ImageTk.PhotoImage(default_logo)

logo_label = tk.Label(logo_preview_frame, image=default_photo)
logo_label.pack()

# Create the progress bar
progress_frame = tk.Frame(window)
progress_frame.pack(pady=5)

progress_label = tk.Label(progress_frame, text="Creating Executable:", font=("Arial", 12))
progress_label.pack()

progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
progress_bar.pack()

# Create the footer label
footer_label = tk.Label(window, text="© 2023 Odecode Software. All rights reserved.", font=("Arial", 10))
footer_label.pack()

# Start the Tkinter event loop
window.mainloop()
