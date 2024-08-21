import os, errno
from typing import Final

from AudioModification.SplitBy.SilenceSplit import SilenceSplitter
from AudioModification.SplitBy.TimeSplit import TimeSplitter
from AudioModification.ConvertAudioFile.ConvertAudioFile import ConvertToWave

class AudioModification:
    SPLIT_PATH:Final[str] = "Split"

    def __init__(self, path:str):
        self.Full_OutputPath:str = os.path.join(path, self.SPLIT_PATH).replace("\\","/")
        self.InputPath:str = path

    def SplitDefault(self):
        try:
            if not os.path.exists(self.Full_OutputPath):
                os.mkdir(self.Full_OutputPath)

            ConvertToWave(self.InputPath, self.Full_OutputPath).Convert()

            #split on silence
            SilenceSplitter(self.Full_OutputPath).split()

            #split for over 10 seconds
            TimeSplitter(self.Full_OutputPath).split()

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise