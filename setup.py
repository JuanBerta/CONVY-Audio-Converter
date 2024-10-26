import os
import sys
import subprocess

# Define dependencies
dependencies = [
    "pydub",
    "ttkbootstrap",
    "mutagen",
]


# Function to check if ffmpeg is installed
def check_ffmpeg_installed():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("ffmpeg is already installed.")
    except FileNotFoundError:
        print("ffmpeg is not installed. Please install ffmpeg to continue.")
        if sys.platform == "win32":
            print("You can download ffmpeg from https://ffmpeg.org/download.html")
        elif sys.platform == "darwin":
            print(
                "On macOS, you can install ffmpeg using Homebrew: brew install ffmpeg"
            )
        elif sys.platform == "linux":
            print(
                "On Linux, you can install ffmpeg using your package manager, e.g., sudo apt install ffmpeg"
            )
        sys.exit(1)


# Function to install Python dependencies
def install_dependencies():
    for dependency in dependencies:
        try:
            __import__(dependency)
        except ImportError:
            print(f"Installing {dependency}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])


# Run the setup
if __name__ == "__main__":
    print("Checking and installing dependencies...")
    install_dependencies()
    check_ffmpeg_installed()
    print("Setup completed. You can now run the program.")
