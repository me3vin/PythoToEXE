import subprocess
import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog, font

# List of required packages for the Python to .exe conversion app
required_packages = [
    "pyinstaller"
]

def install_packages():
    """Install required packages via pip."""
    try:
        for package in required_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        label_status.config(text="Wszystkie wymagane pakiety zostały zainstalowane.", fg="#16a34a")
    except subprocess.CalledProcessError:
        messagebox.showerror("Błąd", "Instalacja pakietów nie powiodła się.")
        root.destroy()

def select_python_script():
    """Open file dialog to select a Python script."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Pliki Pythona", "*.py")],
        title="Wybierz plik .py do konwersji"
    )
    if file_path:
        entry_script_path.delete(0, tk.END)
        entry_script_path.insert(0, file_path)
        label_status.config(text="")

def select_icon_file():
    """Open file dialog to select an icon file."""
    icon_path = filedialog.askopenfilename(
        filetypes=[("Pliki ikon", "*.ico")],
        title="Wybierz plik .ico"
    )
    if icon_path:
        entry_icon_path.delete(0, tk.END)
        entry_icon_path.insert(0, icon_path)
        label_status.config(text="")

def select_output_folder():
    """Open file dialog to select an output folder."""
    folder_path = filedialog.askdirectory(title="Wybierz folder docelowy")
    if folder_path:
        entry_output_folder.delete(0, tk.END)
        entry_output_folder.insert(0, folder_path)
        label_status.config(text="")

def on_button_hover(e):
    e.widget['background'] = "#111827"
    e.widget['foreground'] = "#f9fafb"

def on_button_leave(e):
    e.widget['background'] = "#1f2937"
    e.widget['foreground'] = "#d1d5db"

def convert_to_exe():
    """Use PyInstaller to convert Python script to .exe."""
    script_path = entry_script_path.get().strip()
    icon_path = entry_icon_path.get().strip()
    output_folder = entry_output_folder.get().strip()

    if not script_path or not os.path.isfile(script_path):
        label_status.config(text="Proszę wybrać poprawny plik .py", fg="#dc2626")
        return

    if not output_folder or not os.path.isdir(output_folder):
        label_status.config(text="Proszę wybrać poprawny folder docelowy", fg="#dc2626")
        return

    # Build PyInstaller command with --windowed to suppress console window
    cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconfirm", "--windowed", "--distpath", output_folder]
    if icon_path and os.path.isfile(icon_path):
        cmd += ["--icon", icon_path]
    cmd.append(script_path)

    label_status.config(text="Trwa konwersja... Proszę czekać.", fg="#2563eb")
    root.update_idletasks()
    try:
        subprocess.check_call(cmd,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)
        label_status.config(text=f"Sukces! Plik .exe został wygenerowany w:\n{output_folder}", fg="#16a34a")
        messagebox.showinfo("Sukces", f"Plik .exe został wygenerowany w:\n{output_folder}")
    except subprocess.CalledProcessError:
        label_status.config(text="Konwersja nie powiodła się.", fg="#dc2626")
        messagebox.showerror("Błąd", "Konwersja nie powiodła się.")

def on_start():
    install_packages()

# ------- UI Setup -------

root = tk.Tk()
root.title("Python → EXE Konwerter")
root.configure(bg="#ffffff")
root.geometry("800x700")
root.resizable(False, False)

# Center window on screen
root.eval('tk::PlaceWindow . center')

# Fonts
font_title = font.Font(family="Segoe UI", size=36, weight="bold")
font_label = font.Font(family="Segoe UI", size=14)
font_entry = font.Font(family="Consolas", size=12)
font_button = font.Font(family="Segoe UI", size=14, weight="bold")
font_status = font.Font(family="Segoe UI", size=11)

# Main container centered, max width 600px
container = tk.Frame(root, bg="#fefefe")
container.pack(expand=True, fill="both", padx=48, pady=32)

# Card with subtle shadow and rounded corners using Canvas
card = tk.Frame(container, bg="#ffffff", bd=0)
card.pack(expand=True, fill="both")

# Add subtle shadow using a separate Canvas behind card (simulate shadow)
shadow_canvas = tk.Canvas(container, bg="#f0f0f0", highlightthickness=0)
shadow_canvas.place(x=6, y=6, relwidth=1, relheight=1)
# lift card on top visually
card.lift()

# Title Label
label_title = tk.Label(card, text="Python → EXE Konwerter", bg="#ffffff", fg="#111827", font=font_title)
label_title.pack(anchor="w", pady=(0, 24), padx=8)

def create_input_section(parent, label_text, browse_command):
    section_frame = tk.Frame(parent, bg="#ffffff")
    section_frame.pack(fill="x", pady=10, padx=12)

    label = tk.Label(section_frame, text=label_text, bg="#ffffff", fg="#6b7280", font=font_label)
    label.pack(anchor="w", pady=(0, 6))

    entry_frame = tk.Frame(section_frame, bg="#ffffff")
    entry_frame.pack(fill="x")

    entry = tk.Entry(entry_frame, font=font_entry, bg="#f9fafb", fg="#111827",
                     bd=1, relief="solid")
    entry.pack(side="left", fill="x", expand=True)

    btn = tk.Button(entry_frame, text="Przeglądaj", font=font_button, bg="#1f2937", fg="#d1d5db",
                    relief="flat", activebackground="#111827", activeforeground="#f9fafb",
                    padx=14, pady=8, command=browse_command, cursor="hand2")
    btn.pack(side="left", padx=(12, 0))

    btn.bind("<Enter>", on_button_hover)
    btn.bind("<Leave>", on_button_leave)

    return entry

# Create inputs & keep widget references as simple variables
entry_script_path = create_input_section(card, "Wybierz plik .py do konwersji:", select_python_script)
entry_icon_path = create_input_section(card, "Wybierz plik ikony (.ico):", select_icon_file)
entry_output_folder = create_input_section(card, "Wybierz folder docelowy:", select_output_folder)

# Convert button
btn_convert = tk.Button(card, text="Konwertuj na .exe", font=font_button,
                        bg="#111827", fg="#f9fafb", relief="flat",
                        padx=30, pady=14, activebackground="#374151",
                        activeforeground="#f9fafb", cursor="hand2", command=convert_to_exe)
btn_convert.pack(pady=(24, 8), fill="x")

btn_convert.bind("<Enter>", on_button_hover)
btn_convert.bind("<Leave>", on_button_leave)

# Status label
label_status = tk.Label(card, text="Przy pierwszym uruchomieniu aplikacja zainstaluje wymagane biblioteki.",
                        bg="#ffffff", fg="#6b7280", font=font_status, wraplength=600, justify="left")
label_status.pack(anchor="w", pady=(4, 0), padx=8)

root.after(100, on_start)

root.mainloop()

