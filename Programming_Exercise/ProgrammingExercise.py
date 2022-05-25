from distutils import extension
from msilib.schema import Patch
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import *
from tkinter import filedialog
import os
import errno
import pathlib

def on_created(event):
    print("created")
    moveFile(event.src_path)
def on_modified(event):
    print("modified")
    moveFile(event.src_path)
def on_moved(event):
    print("moved")
    moveFile(event.src_path)

# Event Monitor
def watchdog(path):
    event_handler = FileSystemEventHandler()
    #call funtions
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        print("Empezando monitoreo")
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        print("Monitoreo Finalizado")
        observer.join()

def openFile():
    filepath = filedialog.askdirectory()
    createDirectories(filepath)
    watchdog(filepath)

# Event to create main directories
def createDirectories(path):
    directory1 = "Processed"
    directory2 = "Not_Applicable"
    path1 = os.path.join(path, directory1)
    path2 = os.path.join(path, directory2)
    try:
       os.mkdir(path1)
       os.mkdir(path2)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
# Move files
def moveFile(path):
    root,extension = os.path.splitext(path)
    actualPath = pathlib.Path(path)
    
    route1 = "Not_Applicable"
    route2 = "Processed"
    notApplicable = os.path.join(actualPath.parent,route1,actualPath.name)
    processed = os.path.join(actualPath.parent,route2,actualPath.name)
    #print(actualPath)
    if extension == ".xlsx":
        os.rename(actualPath,processed)
    else:
        os.rename(actualPath,notApplicable)
      
    

if __name__ == "__main__":
    root = Tk()
    root .title("Monitoreo de Carpetas")
    root.geometry('250x150')
    root['background']='gray'
    button = Button(text="Carpeta", command=openFile)
    button
    button.pack()
    root.mainloop()