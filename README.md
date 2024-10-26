# CONVY-Audio-Converter

## Overview
**CONVY-Audio-Converter** is a user-friendly Python GUI program designed for converting audio files between various formats (MP3, WAV, FLAC, OGG, AAC). It features progress tracking and batch processing to enhance user experience.

### Key Features
- **Supports Multiple Audio Formats**: Convert between MP3, WAV, FLAC, OGG, and AAC.
- **Batch Conversion**: Efficiently convert multiple audio files at once.
- **Progress Bar**: Visualize conversion progress, even for large files.
- **Customizable Output Directory**: Choose where to save converted files, with a default save path to your Desktop.
- **Success Notification**: Receive notifications upon completion, with an option to open the output folder immediately.
- **Responsive GUI**: Built with Tkinter and ttkbootstrap for a modern and clean interface.
- **Custom Icon**: Features a custom icon for the application window.
- **Command Line Interface (CLI)**: Provides a CLI option for advanced users.

## Requirements
To run CONVY-Audio-Converter, you need the following:

- Python 3.x
- [pydub](https://github.com/jiaaro/pydub) (for audio file manipulation)
- [ffmpeg](https://ffmpeg.org/download.html) (for audio processing, must be installed separately)
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/) (for enhanced GUI appearance)

## Installation
1. **Clone the repository**:

```bash
git clone https://github.com/JuanBerta/CONVY-Audio-Converter.git
cd audio-file-converter
```

## Install the required dependencies:
```bash
python setup.py
```

## Make sure ffmpeg is installed and accessible via the command line:

```bash
# Download ffmpeg if it's not already installed.
For macOS, install with Homebrew: brew install ffmpeg.
For Linux, install via package manager: sudo apt install ffmpeg.
```

# Run the program:

```bash
python gui.py
```

## How to Use
1- Launch the program and select the audio files you wish to convert.
2- Choose the desired output format (MP3, WAV, FLAC, OGG, AAC).
3- Specify the output directory or use the default path.
4- Click Convert and watch the progress bar as your files are converted.

## Screenshots
![screenshot program](https://github.com/user-attachments/assets/d9b30b30-d0b4-40b9-b9db-37b656e02520)
![screenshot program video selected](https://github.com/user-attachments/assets/17c1d52c-628d-4aa4-9fdc-cc85db83910c)

![Screenshot Successful conversion](https://github.com/user-attachments/assets/af90e16d-ea5e-47a9-bc71-c69944a30c3e)

![Screenshot Open Folder](https://github.com/user-attachments/assets/f65da6df-4d69-4ec7-8ebb-ff41611ce7d5)


# Disclaimer:
This project, including both the code and the icon, was created with the assistance of AI tools. As such, it may contain elements generated by AI, and the author assumes no responsibility for any errors or issues arising from its use.
