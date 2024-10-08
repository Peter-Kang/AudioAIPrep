from scipy.io import wavfile
import os

class TimeSplitter:

    def __init__(self, inputPath:str):
        self.InputPath = inputPath

    def split(self):
        self.audioSplitter()
        print("Time Split Done")

    def audioSplitter(self):
        # Ask the user to select the audio file directory using the file explorer
        input_directory = self.InputPath
        # Check if a directory was selected
        if input_directory:
            # Iterate over the files in the directory
            files = os.listdir(self.InputPath)
            for filename in files:
                if filename.endswith(".wav"):
                    file_path = os.path.join(input_directory, filename)
                    self.splitAudioFile(file_path)
        else:
            print("No directory selected.")

    def splitAudioFile(self, file_path, segment_duration=10):
        # Load the audio file
        sample_rate, audio_data = wavfile.read(file_path)

        # Calculate the number of segments
        num_segments = int(len(audio_data) / (sample_rate * segment_duration))
        remainder = len(audio_data) % (sample_rate * segment_duration)
        if remainder > 0:
            num_segments += 1

        # Create the output directory for segments
        output_dir = os.path.dirname(file_path)
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Split the audio file into segments
        for i in range(num_segments):
            start = i * sample_rate * segment_duration
            end = min((i + 1) * sample_rate * segment_duration, len(audio_data))
            segment = audio_data[start:end]

            # Create the output file name
            segment_filename = f"{base_filename}_{i+1}.wav"
            segment_path = os.path.join(output_dir, segment_filename)

            # Save the segment as a new WAV file
            wavfile.write(segment_path, sample_rate, segment)

            print(f"Segment {i+1}/{num_segments} saved: {segment_filename}")

        #os.remove(file_path)