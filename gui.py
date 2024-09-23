import os
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
from ttkbootstrap import Style
from ttkbootstrap import ttk
from converter import convert_audio
import threading


def normalize_path(path):
    return path.replace("\\", "/")


def open_files(selected_files_var):
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Audio Files", "*.mp3;*.wav;*.flac;*.ogg;*.aac")]
    )
    if file_paths:
        selected_files_var.set("|||".join(file_paths))


def select_output_directory(output_dir_var):
    directory = filedialog.askdirectory()
    if directory:
        output_dir_var.set(directory)


def update_progress_bar(progress_var, current, total):
    progress = int((current / total) * 100)
    progress_var.set(progress)


def open_output_folder(output_dir):
    webbrowser.open(output_dir)


def start_conversion(
    selected_files, output_format, output_dir, progress_var, convert_button
):
    input_paths = selected_files.get().split("|||")

    if input_paths and output_format:
        # Disable the convert button during conversion
        convert_button.config(state="disabled")

        def conversion_thread():
            success, msg = convert_audio(
                input_paths,
                output_format,
                output_dir,
                lambda current, total: update_progress_bar(
                    progress_var, current, total
                ),
            )

            # Re-enable the convert button after conversion
            convert_button.config(state="normal")

            if success:
                messagebox.showinfo("Success", msg)
                if messagebox.askyesno(
                    "Open Folder", "Do you want to open the output folder?"
                ):
                    open_output_folder(output_dir)
            else:
                messagebox.showerror("Error", msg)

        # Start the conversion in a separate thread
        threading.Thread(target=conversion_thread, daemon=True).start()
    else:
        messagebox.showwarning(
            "Warning", "Please select files, an output format, and an output directory"
        )


def create_gui():
    root = tk.Tk()
    root.title("Audio Converter")

    # Set the window icon from the resources folder
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.png")
    if os.path.exists(icon_path):
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon_image)  # Set the icon

    root.geometry("450x350")
    root.minsize(450, 350)

    style = Style(theme="cosmo")

    # Normalize the default output directory path
    default_output_dir = normalize_path(os.path.expanduser("~/Desktop/Converted_Audio"))
    os.makedirs(default_output_dir, exist_ok=True)

    selected_files = tk.StringVar()
    ttk.Label(root, text="Select audio files:", font=("Helvetica", 12)).grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )
    ttk.Entry(root, textvariable=selected_files, width=40).grid(
        row=0, column=1, padx=10, pady=10, sticky="ew"
    )
    ttk.Button(root, text="Browse", command=lambda: open_files(selected_files)).grid(
        row=0, column=2, padx=10, pady=10
    )

    ttk.Label(root, text="Select output format:", font=("Helvetica", 12)).grid(
        row=1, column=0, padx=10, pady=10, sticky="w"
    )
    format_var = tk.StringVar(value="mp3")
    format_menu = ttk.OptionMenu(
        root, format_var, "mp3", "mp3", "wav", "flac", "ogg", "aac"
    )
    format_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    output_dir_var = tk.StringVar(value=default_output_dir)
    ttk.Label(root, text="Select output directory:", font=("Helvetica", 12)).grid(
        row=2, column=0, padx=10, pady=10, sticky="w"
    )
    ttk.Entry(root, textvariable=output_dir_var, width=40).grid(
        row=2, column=1, padx=10, pady=10, sticky="ew"
    )
    ttk.Button(
        root, text="Browse", command=lambda: select_output_directory(output_dir_var)
    ).grid(row=2, column=2, padx=10, pady=10)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(
        root,
        orient="horizontal",
        length=300,
        mode="determinate",
        variable=progress_var,
        value=0,
    )
    progress_bar.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    convert_button = ttk.Button(
        root,
        text="Convert",
        command=lambda: start_conversion(
            selected_files,
            format_var.get(),
            output_dir_var.get(),
            progress_var,
            convert_button,
        ),
    )
    convert_button.grid(row=4, column=1, padx=10, pady=20, sticky="ew")

    root.grid_columnconfigure(1, weight=1)

    root.mainloop()


# Update the select_output_directory function
def select_output_directory(output_dir_var):
    directory = filedialog.askdirectory()
    if directory:
        output_dir_var.set(normalize_path(directory))


if __name__ == "__main__":
    create_gui()
