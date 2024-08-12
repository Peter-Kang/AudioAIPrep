from Rename.Renamer import Renamer
from tkinter import Tk
from tkinter.filedialog import askdirectory

def main():
    audioPath:str = askdirectory(title='Select Folder') # shows dialog box and return the path
    renamer:Renamer = Renamer(audioPath)
    renamer.removeSpace()

main()