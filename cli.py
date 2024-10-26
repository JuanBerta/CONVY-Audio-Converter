import os
import argparse
from converter import convert_audio
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audio Converter CLI - Convert audio files to various formats."
    )
    parser.add_argument(
        "input_files",
        nargs="+",
        help="Path(s) to the input audio file(s) (supports .mp3, .wav, .flac, .ogg, .aac)",
    )
    parser.add_argument(
        "-f",
        "--format",
        required=True,
        choices=["mp3", "wav", "flac", "ogg", "aac"],
        help="Output format for the conversion.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=os.path.expanduser("~/Desktop/Converted_Audio"),
        help="Directory where converted files will be saved.",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        choices=[64, 128, 192, 256, 320],
        default=192,
        help="Quality setting for output (where applicable, in kbps).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_paths = [Path(file).resolve() for file in args.input_files]
    output_dir = Path(args.output_dir).resolve()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # After parsing the input paths, check if each file exists
    for input_path in input_paths:
        if not input_path.exists():
            print(f"File not found: {input_path}")
            continue  # Skip this file if it doesn’t exist

        print(f"Converting: {input_path.name} to {args.format} format")
        success, message = convert_audio(
            [str(input_path)], args.format, str(output_dir), quality=args.quality
        )

        if success:
            print(
                f"Successfully converted {input_path.name} to {args.format} in {output_dir}"
            )
        else:
            print(f"Failed to convert {input_path.name}: {message}")

    print("Starting audio conversion...")
    for input_path in input_paths:
        # Display each file being converted
        print(f"Converting: {input_path.name} to {args.format} format")

        # Call the convert_audio function from your main script
        success, message = convert_audio(
            [str(input_path)], args.format, str(output_dir), quality=args.quality
        )

        # Print feedback on each file conversion status
        if success:
            print(
                f"Successfully converted {input_path.name} to {args.format} in {output_dir}"
            )
        else:
            print(f"Failed to convert {input_path.name}: {message}")

    print("Conversion process completed.")


if __name__ == "__main__":
    main()
