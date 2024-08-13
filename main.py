from Rename.Renamer import Renamer

from AudioModification.AudioModification import AudioModification
from tkinter import Tk
from tkinter.filedialog import askdirectory

def main():
    audioPath:str = askdirectory(title='Select Folder') # shows dialog box and return the path

    Renamer(audioPath).removeSpace()

    AudioModification(audioPath).SplitDefault()
    
main()