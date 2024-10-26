from pydub import AudioSegment
import os


def convert_audio(input_paths, output_format, output_dir, progress_callback=None):
    """
    Convert a list of audio files to the specified format.
    :param input_paths: List of input file paths.
    :param output_format: Format to convert the files to.
    :param output_dir: Directory where the converted files will be saved.
    :param progress_callback: Optional callback function for progress bar.
    """
    try:
        for i, input_path in enumerate(input_paths):
            input_path = input_path.strip("'\"")
            audio = AudioSegment.from_file(input_path)

            base = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{base}.{output_format}")

            # Handle AAC output format using libvo_aacenc codec
            if output_format == "aac":
                audio.export(output_path, format="adts", codec="libvo_aacenc")
            else:
                audio.export(output_path, format=output_format)

            if progress_callback:
                progress_callback(i + 1, len(input_paths))

        return True, "Files converted successfully!"
    except Exception as e:
        return False, f"Failed to convert: {str(e)}"


from pydub import AudioSegment


def get_audio_metadata(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = round(len(audio) / 1000, 2)  # in seconds
    channels = audio.channels
    sample_rate = audio.frame_rate
    return {"duration": duration, "channels": channels, "sample_rate": sample_rate}
