import tkinter as tk
import subprocess
import sys
import os

# Helper to get python executable
PYTHON = sys.executable

# List of projects
PROJECTS = [
    ("Traffic Light Simulation", "traffic.py"),
    ("Measurement Error System", "thinker.py"),
    ("Interactive Periodic Table", "chemical.py"),
    ("Coin Game", "coin.py"),
]

def launch_script(script):
    # Use absolute path for safety
    script_path = os.path.abspath(script)
    subprocess.Popen([PYTHON, script_path])

root = tk.Tk()
root.title("All Projects Launcher")
root.geometry("350x350")

header = tk.Label(root, text="Select a Project to Launch", font=("Arial", 16, "bold"))
header.pack(pady=20)

for name, script in PROJECTS:
    btn = tk.Button(root, text=name, width=30, height=2, command=lambda s=script: launch_script(s))
    btn.pack(pady=8)

quit_btn = tk.Button(root, text="Quit", width=30, height=2, command=root.quit, fg="red")
quit_btn.pack(pady=20)

root.mainloop() 