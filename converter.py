from pydub import AudioSegment
import os


def convert_audio(
    input_files, output_format, output_dir, quality=192, progress_callback=None
):
    for index, file_path in enumerate(input_files):
        try:
            audio = AudioSegment.from_file(file_path)
            output_file = os.path.join(
                output_dir,
                os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}",
            )

            # Set bitrate based on quality argument, applicable for certain formats
            bitrate = f"{quality}k" if output_format in ["mp3", "ogg", "aac"] else None

            audio.export(output_file, format=output_format, bitrate=bitrate)

            if progress_callback:
                progress_callback(index + 1, len(input_files))

        except Exception as e:
            return False, str(e)

    return True, "All files converted successfully."


from pydub import AudioSegment


def get_audio_metadata(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = round(len(audio) / 1000, 2)  # in seconds
    channels = audio.channels
    sample_rate = audio.frame_rate
    return {"duration": duration, "channels": channels, "sample_rate": sample_rate}
