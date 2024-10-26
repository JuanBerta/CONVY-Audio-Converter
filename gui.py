import os
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
from ttkbootstrap import Style
from ttkbootstrap import ttk
from converter import convert_audio
import threading
from mutagen import File  # Import mutagen for metadata


def normalize_path(path):
    """Normalize the path to use forward slashes."""
    return path.replace("\\", "/")


def open_files(
    selected_files_var, metadata_label, bitrate_menu, sample_rate_menu, channels_menu
):
    """Open file dialog to select audio files and display metadata."""
    file_paths = filedialog.askopenfilenames(
        filetypes=[
            ("Audio Files", "*.mp3;*.wav;*.flac;*.ogg;*.aac;*.mp4;*.mkv;*.avi;*.mov")
        ]
    )
    if file_paths:
        selected_files_var.set("|||".join(file_paths))
        display_metadata(
            file_paths[0], metadata_label
        )  # Display metadata for the first file
        update_options(file_paths[0], bitrate_menu, sample_rate_menu, channels_menu)


def update_options(file_path, bitrate_menu, sample_rate_menu, channels_menu):
    """Enable or disable options based on the file type."""
    is_video = file_path.lower().endswith((".mp4", ".mkv", ".avi", ".mov"))
    is_audio = file_path.lower().endswith((".mp3", ".wav", ".flac", ".ogg", ".aac"))

    if is_video:
        # Disable bitrate, sample rate, and channels for video files
        bitrate_menu.config(state="disabled")
        sample_rate_menu.config(state="disabled")
        channels_menu.config(state="disabled")
    elif is_audio:
        # Enable all options for audio files
        bitrate_menu.config(state="normal")
        sample_rate_menu.config(state="normal")
        channels_menu.config(state="normal")
    else:
        # If neither, disable all options (optional handling)
        bitrate_menu.config(state="disabled")
        sample_rate_menu.config(state="disabled")
        channels_menu.config(state="disabled")


def display_metadata(file_path, metadata_label):
    """Display the metadata of the selected audio file."""
    audio_file = File(file_path)

    if audio_file is not None:
        metadata_info = []
        for key, value in audio_file.items():
            metadata_info.append(f"{key}: {value}")

        metadata_text = "\n".join(metadata_info)
        metadata_label.config(text=metadata_text)
    else:
        metadata_label.config(text="No metadata found.")


def update_progress_bar(progress_var, current, total):
    """Update the progress bar during conversion."""
    progress = int((current / total) * 100)
    progress_var.set(progress)


def open_output_folder(output_dir):
    """Open the output folder in the file explorer."""
    webbrowser.open(output_dir)


def start_conversion(
    selected_files,
    output_format,
    output_dir,
    bitrate,
    sample_rate,
    channels,
    progress_var,
    convert_button,
):
    """Start the audio conversion process."""
    input_paths = selected_files.get().split("|||")

    if input_paths and output_format:
        convert_button.config(
            state="disabled"
        )  # Disable the convert button during conversion

        def conversion_thread():
            success, msg = convert_audio(
                input_paths,
                output_format,
                output_dir,
                bitrate,
                sample_rate,
                channels,
                lambda current, total: update_progress_bar(
                    progress_var, current, total
                ),
            )

            convert_button.config(
                state="normal"
            )  # Re-enable the convert button after conversion

            if success:
                messagebox.showinfo("Success", msg)
                if messagebox.askyesno(
                    "Open Folder", "Do you want to open the output folder?"
                ):
                    open_output_folder(output_dir)
            else:
                messagebox.showerror("Error", msg)

        threading.Thread(
            target=conversion_thread, daemon=True
        ).start()  # Start the conversion in a separate thread
    else:
        messagebox.showwarning(
            "Warning", "Please select files, an output format, and an output directory"
        )


def select_output_directory(output_dir_var):
    """Open a dialog to select the output directory."""
    directory = filedialog.askdirectory()
    if directory:
        output_dir_var.set(normalize_path(directory))


def create_gui():
    """Create the main GUI for the audio converter."""
    root = tk.Tk()
    root.title("Audio Converter")

    root.geometry("800x600")
    root.minsize(800, 600)

    style = Style(theme="cosmo")

    # Set default output directory
    default_output_dir = normalize_path(os.path.expanduser("~/Desktop/Converted_Audio"))
    os.makedirs(default_output_dir, exist_ok=True)

    selected_files = tk.StringVar()
    ttk.Label(root, text="Select audio files:", font=("Helvetica", 12)).grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )
    ttk.Entry(root, textvariable=selected_files, width=40).grid(
        row=0, column=1, padx=10, pady=10, sticky="ew"
    )

    # Define the metadata label
    metadata_label = ttk.Label(root, text="", font=("Helvetica", 10), anchor="w")
    metadata_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

    ttk.Button(
        root,
        text="Browse",
        command=lambda: open_files(
            selected_files,
            metadata_label,
            bitrate_menu,
            sample_rate_menu,
            channels_menu,
        ),
    ).grid(row=0, column=2, padx=10, pady=10)

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

    format_var = tk.StringVar(value="mp3")
    ttk.Label(root, text="Select output format:", font=("Helvetica", 12)).grid(
        row=3, column=0, padx=10, pady=10, sticky="w"
    )
    format_menu = ttk.OptionMenu(
        root, format_var, "mp3", "mp3", "wav", "flac", "ogg", "aac"
    )
    format_menu.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    # Bitrate selection
    bitrate_var = tk.StringVar(value="192k")
    ttk.Label(root, text="Select bitrate:", font=("Helvetica", 12)).grid(
        row=4, column=0, padx=10, pady=10, sticky="w"
    )
    bitrate_menu = ttk.OptionMenu(
        root, bitrate_var, "192k", "64k", "128k", "192k", "256k", "320k"
    )
    bitrate_menu.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Sample rate options
    sample_rate_options = [44100, 48000]  # Example of commonly used sample rates
    sample_rate_var = tk.IntVar(value=44100)  # Set default to 44100 Hz

    ttk.Label(root, text="Select sample rate:", font=("Helvetica", 12)).grid(
        row=5, column=0, padx=10, pady=10, sticky="w"
    )
    sample_rate_menu = ttk.OptionMenu(
        root, sample_rate_var, 44100, *sample_rate_options
    )
    sample_rate_menu.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    # Channels selection
    channels_var = tk.StringVar(value="2")
    ttk.Label(root, text="Select channels:", font=("Helvetica", 12)).grid(
        row=6, column=0, padx=10, pady=10, sticky="w"
    )
    channels_menu = ttk.OptionMenu(root, channels_var, "2", "1", "2")
    channels_menu.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(
        root,
        orient="horizontal",
        length=300,
        mode="determinate",
        variable=progress_var,
        value=0,
    )
    progress_bar.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

    convert_button = ttk.Button(
        root,
        text="Convert",
        command=lambda: start_conversion(
            selected_files,
            format_var.get(),
            output_dir_var.get(),
            bitrate_var.get(),
            sample_rate_var.get(),
            channels_var.get(),
            progress_var,
            convert_button,
        ),
    )
    convert_button.grid(row=8, column=1, padx=10, pady=20, sticky="ew")

    root.grid_columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
