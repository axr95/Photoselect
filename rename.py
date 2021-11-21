import tkinter as tk
from tkinter.simpledialog import Dialog

import PIL
from PIL import Image, ExifTags

import datetime
import re

import sys
import os
from os.path import join, isfile
import shutil


FORMAT_PATTERN = re.compile("{(.+?)}")


class RenameDialog(Dialog):
    def __init__(self, parent, path):
        self.files = {}
        self.computedNames = None
        self.path = path

        for f in os.listdir(path):
            fullname = join(path, f)
            if isfile(fullname):
                try:
                    with Image.open(fullname) as im:
                        exif_data = im.getexif()
                        # get dictionary by exif tag name: https://stackoverflow.com/a/4765242
                        self.files[f] = {ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS}
                        self.files[f]["OriginalName"], self.files[f]["Ext"] = os.path.splitext(f)
                except PIL.UnidentifiedImageError:
                    pass

        self.listBox = None
        self.okButton = None
        self.statusLabel = None

        self.formatVariable = tk.StringVar()
        self.formatVariable.set("{DateTimeOriginal}_{OriginalName}{Ext}")
        self.dateFormatVar = tk.StringVar()
        self.dateFormatVar.set("%Y%m%d_%H%M%S")
        Dialog.__init__(self, parent, "Dateien umbenennen")

    def body(self, master):
        grpSettings = tk.Frame(master)
        grpSettings.grid_configure(rows=2, columns=3)
        tk.Label(grpSettings, text="Dateiname:").grid(column=0, row=0)
        tk.Entry(grpSettings, textvariable=self.formatVariable, width=50).grid(column=1, row=0)
        tk.Label(grpSettings, text="Datumsformat:").grid(column=0, row=1)
        tk.Entry(grpSettings, textvariable=self.dateFormatVar, width=50).grid(column=1, row=1)
        tk.Button(grpSettings, text="Vorschau", command=self.update_preview).grid(column=2, row=0, rowspan=2)

        grpSettings.pack(side=tk.TOP, fill=tk.X)

        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listBox = tk.Listbox(master, yscrollcommand=scrollbar.set, height=20, activestyle=tk.NONE)
        self.listBox.insert(tk.END, *self.files.keys())
        self.listBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listBox.yview)

        return self.listBox

    def apply(self):
        self.result = True

    def update_preview(self):
        error = False
        date_format = self.dateFormatVar.get()
        self.computedNames = {}

        self.listBox.delete(0, tk.END)

        for f in self.files:
            def repl(matchobj):
                nonlocal error, date_format
                prop = matchobj.group(1)
                val = self.files[f].get(prop, None)
                if not val:
                    error = True
                    return "ERROR"
                else:
                    try:
                        dat = datetime.datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
                        return dat.strftime(date_format)
                    except ValueError:
                        return val

            self.computedNames[f] = FORMAT_PATTERN.sub(repl, self.formatVariable.get())
            self.listBox.insert(tk.END, self.computedNames[f])

        if error:
            self.computedNames = None
            self.okButton.configure(state=tk.DISABLED)
            self.statusLabel.configure(text="Fehler bei mindestens einer Datei!", foreground="red")
        else:
            self.okButton.configure(state=tk.ACTIVE)
            self.statusLabel.configure(text="Keine Fehler! Zum Umbenennen auf OK klicken.", foreground="green")

    def buttonbox(self):
        """Custom button box, to adapt text and make OK button disableable"""

        box = tk.Frame(self)

        self.statusLabel = tk.Label(box, text="Bitte vorher Vorschau überprüfen!", foreground="blue")
        self.statusLabel.pack(side=tk.LEFT, padx=5, pady=5)
        self.okButton = tk.Button(box, text="OK", width=10, command=self.ok, state=tk.DISABLED)
        self.okButton.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Abbrechen", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Escape>", self.cancel)

        box.pack()


def main():
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
        root = tk.Tk()
        root.withdraw()
        RenameDialog(root, start_path)
    else:
        print("Usage:", sys.argv[0], "<path>")


if __name__ == '__main__':
    main()
