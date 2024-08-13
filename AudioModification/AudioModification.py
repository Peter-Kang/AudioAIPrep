import os, errno
from typing import Final

from SilenceSplit import SilenceSplitter
from TimeSplit import TimeSplitter
from ConvertAudioFile.ConvertAudioFile import ConvertToWave

class AudioModification:
    SPLIT_PATH:Final[str] = "\Split"

    def __init__(self, path:str):
        self.full_OutputPath:str = os.path.join(path, self.SPLIT_PATH)
        self.inputPath:str = path

    def SplitDefault(self):
        try:
            if not os.path.exists(self.full_OutputPath):
                os.mkdir(self.full_OutputPath)
            #Get Everything into Wav
            ConvertToWave(self.inputPath, self.full_OutputPath).Convert()
            #split on silence
            SilenceSplitter(self.inputPath, self.full_OutputPath).split()
            #split for over 10 seconds
            TimeSplitter(self.inputPath, self.full_OutputPath).split()

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise