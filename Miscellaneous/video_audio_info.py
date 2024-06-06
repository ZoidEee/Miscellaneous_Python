import av
import os

def process_file(file_path):
    """
    Process a single video or audio file.

    Args:
        file_path (str): The path to the video or audio file.

    This function opens the specified file using the PyAV library and extracts
    information about the video and audio streams. It then creates a text file
    in the same directory as the input file, with the name "Video-Audio-Information.txt",
    and writes the extracted information to this file.

    If the input file is invalid or cannot be opened, an error message is printed.
    """
    try:
        container = av.open(file_path)
    except av.error.InvalidDataError:
        print(f"Error processing file {file_path}: Invalid data")
        return

    file_dir = os.path.dirname(file_path)
    file_name = "Video-Audio-Information.txt"
    output_file = os.path.join(file_dir, file_name)

    with open(output_file, 'w') as file:
        for stream in container.streams:
            if stream.type == 'video':
                # Process video stream
                file.write("Video Information:\n")
                file.write(f"  Dimensions: {stream.codec_context.width}x{stream.codec_context.height}\n")
                file.write(f"  Codec: {stream.codec_context.name}\n")
                file.write(f"  Frame Rate: {float(stream.average_rate):.2f}\n")
                bit_rate = stream.bit_rate / 1000 if stream.bit_rate is not None else "Unknown"
                file.write(f"  Bit Rate: {bit_rate} kbps\n")

            elif stream.type == 'audio':
                # Process audio stream
                file.write("\nAudio Information:\n")
                file.write(f"  Codec: {stream.codec_context.name}\n")
                file.write(f"  Channels: {stream.codec_context.channels}\n")
                file.write(f"  Sample Rate: {stream.codec_context.sample_rate} Hz\n")
                bit_rate = stream.bit_rate / 1000 if stream.bit_rate is not None else "Unknown"
                file.write(f"  Bit Rate: {bit_rate} kbps\n")

def process_directory(directory):
    """
    Process all video and audio files in a directory and its subdirectories.

    Args:
        directory (str): The path to the directory to process.

    This function recursively walks through the specified directory and its
    subdirectories, and for each video or audio file found (with extensions
    .mp4, .mov, .avi, or .mkv), it calls the `process_file` function to
    process that file.
    """
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith(('.mp4', '.mov', '.avi', '.mkv')):
                process_file(file_path)

if __name__ == "__main__":
    directory = ""
    process_directory(directory)