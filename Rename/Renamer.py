import uuid
from pathlib import Path
import os

class Renamer:

    def __init__(self, path:str):
        self.path = path

    def removeSpace(self):
        for filename in os.listdir(self.path):
            if ' ' in filename:
                newName = filename.replace(' ', '_')
                newFilePath = Path(self.path+'//'+newName)
                #check if name exsits
                if newFilePath.is_file():
                    newName = newName+str(uuid.uuid5())
                os.rename(Path(self.path+'//'+filename), newFilePath)
        print("Spaces removed")