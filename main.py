import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo, askyesno

import sys
import os
from os.path import join, isfile
import shutil

from imagehelpers import SelectImage, ImageControlsGroup
from listdialog import ListDialog

from time import time


class SelectWindow(object):

    def __init__(self, start_path=None):
        root = tk.Tk()
        root.title("Bitte Verzeichnis auswählen!")
        self.root = root

        # store placeholder image
        self.placeholder = tk.PhotoImage(data=SelectImage.PLACEHOLDER_IMG_BASE64_GIF)

        self.imageControls = []

        # path of folder
        self.path = tk.StringVar()
        self.path.trace_add("write", self.title_handler)

        # image storage
        self.images = []
        self.cur_idx = 0

        self.showPreviews = tk.BooleanVar()

        m = tk.Menu(title="Aktionen")
        m.add_command(label="Verzeichnis auswählen ...", command=self.change_directory_handler)
        m.add_separator()
        m.add_command(label="Alles markieren/demarkieren", command=self.mark_all_handler)
        m.add_separator()
        m.add_command(label="Auswahl kopieren", command=self.copy_marked)
        m.add_command(label="Auswahl verschieben", command=self.move_marked)
        m.add_command(label="Auswahl löschen", command=self.delete_marked)
        m.add_separator()
        m.add_checkbutton(label="Navigation anzeigen", variable=self.showPreviews, command=self.reload_view)
        self.menu = m

        # max sizes of images
        self.mainSize = 600, 600

        self.mainImage = tk.Label(root)
        self.mainImage.pack(side="top")

        self.imageControls.append(ImageControlsGroup(self, self.mainImage, tk.Label(root), 0, "MAIN", False))

        root.bind("<Button-3>", lambda ev: self.menu.tk_popup(ev.x_root, ev.y_root))

        # Preview (Thumbnails)
        grpPreviews = tk.Frame(root)
        grpPreviews.pack(side="bottom")

        for idx in range(0, 9):
            lblPrev = tk.Label(grpPreviews, wraplength=SelectImage.THUMBNAIL_SIZE[0])
            lblPrev.grid(column=idx, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
            imgPrev = tk.Label(grpPreviews, image=self.placeholder)
            imgPrev.grid(column=idx, row=1, sticky=tk.N+tk.S+tk.E+tk.W)
            imgPrev.bind("<Button-1>", self.get_select_handler(idx - 4))
            imgPrev.bind("<Double-Button-1>", self.get_change_cur_handler(idx - 4))
            controlsGroup = ImageControlsGroup(self, imgPrev, lblPrev, idx - 4, "THUMBNAIL", True)
            self.imageControls.append(controlsGroup)

        self.prevScrollbar = tk.Scale(grpPreviews, orient=tk.HORIZONTAL, from_=0, to=1, sliderlength=20,
                                      showvalue=False, command=self.scrollbar_handler)
        self.prevScrollbar.grid(column=0, row=2, sticky=tk.S+tk.E+tk.W, columnspan=9)
        self.grpPreviews = grpPreviews

        root.state("zoomed")

        root.bind("<Configure>", self.resize_handler)

        root.bind("<Left>", self.get_change_cur_handler(-1))
        root.bind("<Right>", self.get_change_cur_handler(1))
        root.bind("<space>", self.get_select_handler(0))

        self.oldWidth = None
        self.oldHeight = None
        self.resize_cb_id = None

        if start_path:
            self.path.set(start_path)
            self.reload_directory()
        else:
            self.change_directory_handler()

        self.root.mainloop()

    def title_handler(self, *_event):
        self.root.title(self.path.get())

    def resize_handler(self, event):
        if event.widget == self.root and (event.width != self.oldWidth):
            if self.resize_cb_id:
                self.root.after_cancel(self.resize_cb_id)
            self.resize_cb_id = self.root.after(200, self.do_resize, event)

    def do_resize(self, event):
        # print("RESIZE")
        self.oldWidth = event.width
        self.oldHeight = event.height
        self.resize_cb_id = None
        # width = self.root.winfo_width()
        size_main = event.width
        # size_side = width * 3 // 11
        size_thumbnail = (event.width - 45) // 9

        ImageControlsGroup.SIZES["MAIN"] = (event.width, event.height)
        # ImageControlsGroup.SIZES["SIDE"] = (size_side, size_side * 3 // 4)

        SelectImage.THUMBNAIL_SIZE = (size_thumbnail, size_thumbnail * 3 // 4)
        ImageControlsGroup.SIZES["THUMBNAIL"] = SelectImage.THUMBNAIL_SIZE

        if self.images:
            for img in self.images:
                img.thumbnail = None

        self.reload_view()

    def get_change_cur_handler(self, diff):
        def change_cur_handler(_event):
            self.cur_idx += diff
            if self.cur_idx < 0:
                self.cur_idx = 0
            elif self.cur_idx >= len(self.images):
                self.cur_idx = len(self.images) - 1
            self.prevScrollbar.set(self.cur_idx)
            self.reload_view()
        return change_cur_handler

    def get_select_handler(self, offset):
        def select_handler(_event):
            if 0 <= self.cur_idx + offset < len(self.images):
                new_state = 1 - self.images[self.cur_idx + offset].selected.get()
                self.images[self.cur_idx + offset].selected.set(new_state)

        return select_handler

    def scrollbar_handler(self, _event):
        self.cur_idx = self.prevScrollbar.get()
        self.reload_view()

    def ask_directory_action(self):
        if self.images:
            res = askyesno("Verzeichnis ändern",
                           "Neues Verzeichnis laden? Alle aktuellen Markierungen gehen verloren (falls vorhanden)!")
            if res == tk.NO:
                return False
        return True

    def ask_confirmation(self, title: str, text: str):
        if self.images:
            img = [x for x in self.images if x.selected.get()]
            if any(img):
                d = ListDialog(self.root, title, text, [i.name for i in img])
                if d.result:
                    return img
        return False

    def delete_marked(self):
        img = self.ask_confirmation("Dateien löschen?",
                                    "Alle folgenden Elemente werden unwiderruflich gelöscht. Fortfahren?")
        if not img:
            return
        results = []
        for i in img:
            try:
                os.remove(i.path)
            except OSError as e:
                results.append("[ERROR] {}: {}".format(i.name, str(e)))
        if results:
            ok_count = len(img) - len(results)
            showinfo("Löschen abgeschlossen",
                     ("{0} von {1} Dateien wurden erfolgreich gelöscht." +
                      "\nEs gab Probleme bei den folgenden Dateien:\n\n{2}")
                     .format(ok_count, len(img), "\n".join(results)))
        else:
            showinfo("Löschen abgeschlossen", "Alle {0} Dateien wurden erfolgreich gelöscht.".format(len(img)))

        self.reload_directory()

    def copy_marked(self):
        self.move_marked(True)

    def move_marked(self, copy=False):
        action_name = "kopiert" if copy else "verschoben"
        img = self.ask_confirmation("Dateien {0}?".format("kopieren" if copy else "verschieben"),
                                    "Alle folgenden Elemente werden {0}. Fortfahren?".format(action_name))
        if not img:
            return

        destination = askdirectory(parent=self.root, title="Bitte Zielordner auswählen")
        if not destination:
            return

        if not os.path.isdir(destination):
            try:
                os.makedirs(destination, exist_ok=False)
            except Exception as e:
                showerror("Konnte den Zielordner nicht erstellen:\n" + str(e))
                return

        action = shutil.copy2 if copy else shutil.move
        results = []
        for i in img:
            try:
                action(i.path, destination)
            except Exception as e:
                results.append("[ERROR] {}: {}".format(i.name, str(e)))

        if results:  # if errors were logged
            ok_count = len(img) - len(results)
            showinfo("Vorgang abgeschlossen",
                     "{0} von {1} Dateien wurden erfolgreich {2}.\nEs gab Probleme bei den folgenden Dateien:\n\n{3}"
                     .format(ok_count, len(img), action_name, "\n".join(results)))
        else:
            showinfo("Vorgang abgeschlossen", "Alle {0} Dateien wurden erfolgreich {1}.".format(len(img), action_name))

        if not copy:
            self.reload_directory()

    def change_directory_handler(self):
        if self.path.get() != '' and not self.ask_directory_action():
            return
        path = askdirectory(parent=self.root, title="Bitte Ordner auswählen", mustexist=True)
        if path:
            self.path.set(path)
            self.reload_directory()

    def mark_all_handler(self):
        if self.images:
            if all(map(lambda x: x.selected.get(), self.images)):
                for img in self.images:
                    img.selected.set(0)
            else:
                for img in self.images:
                    img.selected.set(1)

    def reload_directory(self):
        starttime = time()
        p = self.path.get()
        filepaths = [join(p, f) for f in os.listdir(p)]
        print("got filepaths in {0:0.3f}s".format(time() - starttime))
        filepaths.sort()
        print("sorted after {0:0.3f}s".format(time() - starttime))
        self.images = [SelectImage(fpath) for fpath in filepaths if isfile(fpath)]
        self.cur_idx = 0
        print("prepared SelectImages after {0:0.3f}s".format(time() - starttime))
        self.showPreviews.set(1)
        self.prevScrollbar.config(to=len(self.images)-1)

        self.reload_view()

    def reload_view(self):
        starttime = time()
        # assert (0 <= self.cur_idx < len(self.images))
        for group in self.imageControls:
            group.reload_view()

        if self.showPreviews.get() == 1:
            self.grpPreviews.place(anchor="sw", y=self.oldHeight)
        else:
            self.grpPreviews.place_forget()
        print("reloaded view in {0:0.3f}s".format(time() - starttime))


def main():
    start_path = None
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    SelectWindow(start_path)


if __name__ == '__main__':
    main()
