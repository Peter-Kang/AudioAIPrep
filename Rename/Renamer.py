import uuid
from pathlib import Path
import os, errno

class Renamer:

    def __init__(self, path:str):
        self.path = path

    def removeSpace(self):
        files = os.listdir(self.path)
        for filename in files:
            if ' ' in filename:
                newName = filename.replace(' ', '_')
                newFilePath = Path(self.path+'//'+newName)
                #check if name exsits
                if newFilePath.is_file():
                    newName = newName+str(uuid.uuid5())
                try:
                     os.rename(Path(self.path+'//'+filename), newFilePath)
                except OSError as e:
                        raise
        print("Spaces removed")