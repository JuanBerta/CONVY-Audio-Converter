from pydub import AudioSegment
import subprocess
import os


def convert_audio(
    input_paths,
    output_format,
    output_dir,
    bitrate=None,
    sample_rate=None,
    channels=None,
    progress_callback=None,
):
    # Set default sample rate if none is specified, typically 44100 Hz for most formats
    sample_rate = sample_rate if sample_rate is not None else 44100

    total = len(input_paths)
    for current, input_path in enumerate(input_paths, start=1):
        # Check if the input path is valid
        if not input_path or not os.path.isfile(input_path):
            return False, f"Input file does not exist or is invalid: {input_path}"

        # Determine output path
        output_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + f".{output_format}",
        )

        # Construct the FFmpeg command
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            input_path,
            "-b:a",
            f"{bitrate}" if bitrate else None,
            "-ar",
            str(sample_rate) if sample_rate else None,
            "-ac",
            str(channels) if channels else None,
            output_path,
        ]

        # Filter out None values from the command
        ffmpeg_command = [arg for arg in ffmpeg_command if arg is not None]

        # Run the FFmpeg command
        result = run_ffmpeg(ffmpeg_command)

        if not result:  # Handle any errors returned from run_ffmpeg
            return False, "Error occurred during conversion."

        if progress_callback:
            progress_callback(current, total)

    return True, "Conversion successful"


def run_ffmpeg(command):
    try:
        # Run the command without opening a console window and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if result.returncode != 0:
            print(f"Error: {result.stderr.decode()}")
            return False  # Indicate failure
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # Indicate failure

    return True  # Indicate success


def get_audio_metadata(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = round(len(audio) / 1000, 2)  # in seconds
    channels = audio.channels
    sample_rate = audio.frame_rate
    return {"duration": duration, "channels": channels, "sample_rate": sample_rate}
