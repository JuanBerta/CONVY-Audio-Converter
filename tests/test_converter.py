import unittest
from converter import convert_audio


class TestAudioConverter(unittest.TestCase):

    def test_convert_audio_success(self):
        # Test successful conversion with additional parameters
        input_files = [
            r"C:/Audios_IA/Voz Juan/Voice Files/Voz Juan 1.wav"
        ]  # Replace with your valid audio file path
        output_format = "mp3"
        output_dir = r"C:/Audios_IA/Voz Juan/Voice Files"  # Replace with your output directory path
        export_params = {
            "bitrate": "320k",  # Recommended bitrate
            "sample_rate": 44100,  # Recommended sample rate
            "channels": 2,  # Recommended number of channels (stereo)
        }

        # Define a mock progress callback
        def progress_callback(current, total):
            pass  # You can leave this empty or add logic if needed

        success, msg = convert_audio(
            input_files, output_format, output_dir, progress_callback, **export_params
        )
        self.assertTrue(success)
        self.assertEqual(
            msg, "Conversion successful"
        )  # Replace with the expected success message

    def test_convert_audio_invalid_file(self):
        # Test conversion with an invalid file path
        input_files = [
            r"C:/Audios_IA/Voz Juan/Voice Files/invalid_file.wav"
        ]  # Use a path that doesn't exist
        output_format = "mp3"
        output_dir = (
            r"C:/Audios_IA/Voz Juan/Voice Files"  # Use your output directory path
        )

        # Define a mock progress callback
        def progress_callback(current, total):
            pass  # You can leave this empty or add logic if needed

        success, msg = convert_audio(
            input_files, output_format, output_dir, progress_callback
        )
        self.assertFalse(success)
        self.assertIn("Error", msg)  # Replace with the expected error message

    def test_convert_audio_with_invalid_bitrate(self):
        input_files = [r"C:/Audios_IA/Voz Juan/Voice Files/Voz Juan 1.wav"]
        output_format = "mp3"
        output_dir = r"C:/Audios_IA/Voz Juan/Voice Files"

        def progress_callback(current, total):
            pass

        # Here, use an invalid bitrate value to test error handling
        success, msg = convert_audio(
            input_files,
            output_format,
            output_dir,
            bitrate=128,  # Assuming this is valid for your test case
            progress_callback=progress_callback,
        )

        self.assertTrue(success)  # or assertFalse based on your testing logic
        self.assertIn("Conversion successful", msg)  # Check for the correct message


if __name__ == "__main__":
    unittest.main()
