import soundfile as sf
import os

class ConvertToWave:
    def __init__(self, inputPath:str, outputPath:str):
        self.inputPath:str = inputPath
        self.outputPath:str = outputPath

    def Convert(self):
        for filename in os.listdir(self.inputPath):
            try:
                data, sampleRate = sf.read(os.path.join(f'{self.inputPath}/{filename}'))
                outputFilePath = os.path.join(self.outputPath, os.path.splittext(filename)[0]+'.wav')
                sf.write(outputFilePath, data, sampleRate)
            except OSError as e:
                print(f"Error reading in {filename}")
                raise
