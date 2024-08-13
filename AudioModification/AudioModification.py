import os, errno
from typing import Final

from SilenceSplit import SilenceSplitter
from TimeSplit import TimeSplitter

class AudioModification:
    SPLIT_PATH:Final[str] = "\Split"

    def __init__(self, path:str):
        self.full_path:str = os.path.join(path, self.SPLIT_PATH)
        self.local_path_name:str = path

    def SplitDefault(self):
        try:
            if not os.path.exists(self.full_path):
                os.mkdir(self.full_path)

            TimeSplitter(self.local_path_name, self.full_path).split()
            SilenceSplitter(self.local_path_name, self.full_path).split()

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise