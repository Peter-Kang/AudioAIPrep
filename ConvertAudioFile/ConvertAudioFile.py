import soundfile as sf
import wave

import os

class ConvertToWave:
    def __init__(self, inputPath:str, outputPath:str):
        self.InputPath:str = inputPath
        self.OutputPath:str = outputPath

    def Convert(self):
        files = [f for f in os.listdir(self.InputPath) if os.path.isfile(os.path.join(self.InputPath, f).replace("\\","/"))]
        for filename in files:
            try:
                fullPathToExistingFile = os.path.join(self.InputPath, filename).replace("\\","/")
                outputFilePath = os.path.join(self.OutputPath, os.path.splitext(filename)[0]+'.wav')

                # Read the audio file



            except OSError as e:
                print(f"Error reading in {filename}")
                raise
