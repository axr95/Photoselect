LICENSE = """Photoselect, an application to review images in a folder, including a mass-renaming functionality
Copyright (C) 2021  Alexander Simunics

This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version.

This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details.

You should have received a copy of the GNU General Public License \
along with this program.  If not, see <https://www.gnu.org/licenses/>.
 
The author of the icon file "icon.ico" is Xiran Dong, (C) 2020."""

import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, askyesno, showinfo

import sys
import os
from os.path import join, isfile
import shutil

from imagehelpers import SelectImage, ImageControlsGroup
from rename import RenameDialog
from file_action_util import perform_action, ListDialog

from time import time


class SelectWindow(object):
    """The main Window where a user can view, select, and perform actions on images in a directory."""

    EMPTY_CHECKBOX_IMG_BASE64_GIF = "R0lGODlhgACAAHAAACH5BAEAAPwALAAAAACAAIAAhwAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAAAj/AAEIHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmypMmTKFOqXMlS5b6XMGPKnEmzps2bOHPq3EkTIs+fQIMKHdrzIdGjSJMe9am0qdOnMplCnUp1qNSqWLPevKq1q1euXsNWBSu2rFOyZtMuNaq2bVK0buPqhCu3bk26dvPCxKs3L9++df8Cjit4cNvChtMiTlx2MeOwjh93jSw5K+XKY9litnt5M9TOns9qDu0WNOm3o08rTq26MevWkF/Dnix7tuXatjM7zO16N+/Yvn/TDi78NvHiuhsi12p6+VbczpE2j170OPWm06/HzK79Jffu37WHWL8+nnr56Oedp1++Hnn74u+Fx/89n3f93Pdt55+9H3b/1v+pFuBpA5JWYGgHepbgZgti1mBlD0oW4WMTMlZhYhcaluFgGwLWYV8f6hWiX9B1B9SInJVoIk9uKAam4opzvQgjTi3KVSNhMs5o042l5ahjdcr9SBSPh/ko5HZGHuldkkoSqZaTq1mnZIxSTkkjk0dCaZaWvQVpJYtYCsmlWGMC5+WXVJ6J5pVVrjlTS3DGKeecdNZp55145qnnnnz26eefgAZqUEAAOw=="
    TICKED_CHECKBOX_IMG_BASE64_GIF = "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"

    CHECKBOX_POPUP_DURATION = 1500

    def __init__(self, start_path=None):
        root = tk.Tk()
        root.title("Bitte Verzeichnis auswählen!")
        self.root = root

        # store placeholder image
        self.placeholder = tk.PhotoImage(data=SelectImage.PLACEHOLDER_IMG_BASE64_GIF)
        self.empty_checkbox_img = tk.PhotoImage(data=SelectWindow.EMPTY_CHECKBOX_IMG_BASE64_GIF)
        self.ticked_checkbox_img = tk.PhotoImage(data=SelectWindow.TICKED_CHECKBOX_IMG_BASE64_GIF)

        self.imageControls = []

        # path of folder
        self.path = tk.StringVar()
        self.path.trace_add("write", self.title_handler)

        # image storage
        self.images = []
        self.cur_idx = 0

        self.showThumbnails = tk.BooleanVar()

        m = tk.Menu(title="Aktionen")
        m.add_command(label="Verzeichnis auswählen ...", command=self.change_directory_handler)
        m.add_command(label="Alle Dateien umbenennen ...", command=self.rename_handler)
        m.add_checkbutton(label="Navigation anzeigen", variable=self.showThumbnails, command=self.reload_view)
        m.add_separator()
        m.add_command(label="Alles markieren/demarkieren", command=self.mark_all_handler)
        m.add_separator()
        m.add_command(label="Einzelbild kopieren", command=self.get_cur_action_handler(self.copy_images))
        m.add_command(label="Einzelbild verschieben", command=self.get_cur_action_handler(self.move_images))
        m.add_command(label="Einzelbild löschen", command=self.get_cur_action_handler(self.delete_images))
        m.add_separator()
        m.add_command(label="Auswahl kopieren", command=self.copy_images)
        m.add_command(label="Auswahl verschieben", command=self.move_images)
        m.add_command(label="Auswahl löschen", command=self.delete_images)
        m.add_separator()
        m.add_command(label="Über ...", command=self.show_about)
        self.menu = m

        # max sizes of images
        self.mainSize = 600, 600

        self.mainImage = tk.Label(root)#, bg="#bbb")
        self.mainImage.pack(side="top")

        self.btn_left = tk.Button(root, text="<", width=8, font=196, height=60, relief=tk.FLAT,
                                  command=self.get_change_cur_handler(-1))
        self.btn_right = tk.Button(root, text=">", width=8, font=196, height=60, relief=tk.FLAT,
                                   command=self.get_change_cur_handler(1))

        self.imageControls.append(ImageControlsGroup(self, self.mainImage, tk.Checkbutton(root), 0, "MAIN", False))

        root.bind("<Button-3>", lambda ev: self.menu.tk_popup(ev.x_root, ev.y_root))

        # Preview (Thumbnails)
        grp_previews = tk.Frame(root)
        grp_previews.pack(side="bottom")

        for idx in range(0, 9):
            lbl_prev = tk.Checkbutton(grp_previews, wraplength=SelectImage.THUMBNAIL_SIZE[0])
            lbl_prev.grid(column=idx, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
            img_prev = tk.Label(grp_previews, image=self.placeholder)
            img_prev.grid(column=idx, row=1, sticky=tk.N+tk.S+tk.E+tk.W)
            img_prev.bind("<Control-Button-1>", self.get_select_handler(idx - 4))
            img_prev.bind("<Button-1>", self.get_change_cur_handler(idx - 4))
            controls_group = ImageControlsGroup(self, img_prev, lbl_prev, idx - 4, "THUMBNAIL", True)
            self.imageControls.append(controls_group)

        self.imageControls[5].lblImage.configure(bg="#04f")

        self.prevScrollbar = tk.Scale(grp_previews, orient=tk.HORIZONTAL, from_=0, to=1, sliderlength=20,
                                      showvalue=False, command=self.scrollbar_handler)
        self.prevScrollbar.grid(column=0, row=2, sticky=tk.S+tk.E+tk.W, columnspan=9)
        self.grpPreviews = grp_previews

        self.checkbox_popups = [tk.Label(image=self.empty_checkbox_img), tk.Label(image=self.ticked_checkbox_img)]

        root.state("zoomed")

        root.bind("<Configure>", self.resize_handler)

        root.bind("<Left>", self.get_change_cur_handler(-1))
        root.bind("<Right>", self.get_change_cur_handler(1))
        root.bind("<space>", self.get_select_handler(0))

        self.oldWidth = None
        self.oldHeight = None
        self.resize_cb_id = None
        self.popup_cb_id = None

        if start_path:
            self.path.set(start_path)
            self.reload_directory()
        else:
            self.root.after_idle(self.change_directory_handler)

        self.root.mainloop()

    def title_handler(self, *_event):
        """Sets the title of the window to the current path"""
        self.root.title(self.path.get())

    def resize_handler(self, event):
        """(Re-)Schedules a resize to be done in 200ms, to provide smoother experience during resizing"""
        if event.widget == self.root and (event.width != self.oldWidth):
            if self.resize_cb_id:
                self.root.after_cancel(self.resize_cb_id)
            self.resize_cb_id = self.root.after(200, self.do_resize, event)

    def do_resize(self, event):
        """Recomputes the needed sizes of all images for new windows size and triggers a refresh"""
        # print("RESIZE")
        self.oldWidth = event.width
        self.oldHeight = event.height
        self.resize_cb_id = None
        size_thumbnail = (event.width - 45) // 9

        ImageControlsGroup.SIZES["MAIN"] = (event.width, event.height)

        SelectImage.THUMBNAIL_SIZE = (size_thumbnail, size_thumbnail * 3 // 4)
        ImageControlsGroup.SIZES["THUMBNAIL"] = SelectImage.THUMBNAIL_SIZE

        if self.images:
            for img in self.images:
                img.thumbnail = None

        self.prevScrollbar.configure(length=event.width)

        self.reload_view()

    def get_change_cur_handler(self, diff):
        """
        Creates a handler-function that shifts the current view by a given amount, when called, and returns it.
        :param diff: The offset the handler should be adding to the currently selected index.
        :return: The handler-function that was created, which sets the selected index and reloads the view
        """
        def change_cur_handler(_event=None):
            self.cur_idx += diff
            if self.cur_idx < 0:
                self.cur_idx = 0
            elif self.cur_idx >= len(self.images):
                self.cur_idx = len(self.images) - 1
            self.prevScrollbar.set(self.cur_idx)
            self.reload_view()
            self.show_checkbox_popup()
        return change_cur_handler

    def get_select_handler(self, offset):
        """
        Creates a handler-function that toggles the "selected"-state of the image with the given offset.
        :param offset: The offset of the image to be toggled, with respect to the currently centered image.
        :return: The handler-function that was created, which toggles the correct selected-state.
        """
        def select_handler(_event):
            if 0 <= self.cur_idx + offset < len(self.images):
                new_state = 1 - self.images[self.cur_idx + offset].selected.get()
                self.images[self.cur_idx + offset].selected.set(new_state)
                if offset == 0:
                    self.show_checkbox_popup()

        return select_handler

    def get_cur_action_handler(self, action):
        """
        Creates a handler that applies the given action to the currently centered SelectImage
        :param action: A function that takes a keyword argument "img" of type SelectImage
        :return: The created handler.
        """
        def cur_action_handler(_event=None):
            if self.images:
                action(img=[self.images[self.cur_idx]])
        return cur_action_handler

    def scrollbar_handler(self, _event):
        """Shifts the view according to the scrollbar"""
        self.cur_idx = self.prevScrollbar.get()
        self.reload_view()

    def ask_directory_action(self) -> bool:
        """
        Asks the user whether the directory can be changed
        :return: The answer of the user (True or False)
        """
        if self.images:
            res = askyesno("Verzeichnis ändern",
                           "Neues Verzeichnis laden? Alle aktuellen Markierungen gehen verloren (falls vorhanden)!")
            if res == tk.NO:
                return False
        return True

    def ask_confirmation(self, title: str, text: str, images: list = None) -> list:
        """
        Asks the user to confirm an action on the given SelectImages
        :param title: The title of the dialog
        :param text:  The message text of the dialog
        :param images: The images that should be listed. If None (default), all currently selected images are taken.
        :return: The images to be processed, if the user confirmed the dialog. Otherwise an empty list.
        """
        if not images:
            if not self.images:
                return []
            else:
                images = [x for x in self.images if x.selected.get()]
        if any(images):
            d = ListDialog(self.root, title, text, [i.name for i in images])
            if d.result:
                return images
        return []

    def delete_images(self, img=None) -> None:
        """
        Deletes the given images after confirmation by the user.
        :param img: A list of SelectImages to be deleted. If None, all selected images are taken.
        """
        img = self.ask_confirmation("Dateien löschen?",
                                    "Alle folgenden Elemente werden unwiderruflich gelöscht. Fortfahren?", img)
        if img:
            perform_action(lambda x: os.remove(x.path), img, "gelöscht")
            i = self.cur_idx
            while i > 0 and self.images[self.cur_idx].selected.get():
                i -= 1
            self.reload_directory(self.images[i].name)

    def copy_images(self, img=None):
        """
        Copies the given images after confirmation by the user, and a destination selection.
        :param img: A list of SelectImages to be copied. If None, all selected images are taken.
        """
        self.move_images(True, img)

    def move_images(self, copy=False, img=None):
        """
        Moves or copies the given images after confirmation by the user, and a destination selection.
        :param copy: If copy evaluates to True, the images also remain in the original location.
        :param img: A list of SelectImages to be moved/copied. If None, all selected images are taken.
        """
        action_name = "kopiert" if copy else "verschoben"
        img = self.ask_confirmation("Dateien {0}?".format("kopieren" if copy else "verschieben"),
                                    "Alle folgenden Elemente werden {0}. Fortfahren?".format(action_name), img)
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

        if copy:
            perform_action(lambda x: shutil.copy2(x.path, destination), img, "kopiert")
        else:
            perform_action(lambda x: shutil.move(x.path, destination), img, "verschoben")

            i = self.cur_idx
            while i > 0 and self.images[self.cur_idx].selected.get():
                i -= 1
            self.reload_directory(self.images[i].name)

    def change_directory_handler(self):
        """Changes the current directory, after asking the user for confirmation (iff a directory is already open)"""
        if self.path.get() != '' and not self.ask_directory_action():
            return
        path = askdirectory(parent=self.root, title="Bitte Ordner auswählen", mustexist=True)
        if path:
            self.path.set(path)
            self.reload_directory()

    def rename_handler(self):
        """Opens the renaming dialog"""
        if self.path.get() == '':
            showerror("Fehler", "Bitte zuerst ein Verzeichnis auswählen!")
        else:
            RenameDialog(self.root, self.path.get())

    def mark_all_handler(self):
        """Marks all the images as selected. If all images are already selected, unselects them."""
        if self.images:
            if all(map(lambda x: x.selected.get(), self.images)):
                for img in self.images:
                    img.selected.set(0)
            else:
                for img in self.images:
                    img.selected.set(1)

    def show_checkbox_popup(self):
        state = self.images[self.cur_idx].selected.get()

        if self.popup_cb_id:
            self.root.after_cancel(self.popup_cb_id)
        self.checkbox_popups[1 - state].place_forget()
        self.checkbox_popups[state].place(x=0, y=0)
        self.popup_cb_id = self.root.after(SelectWindow.CHECKBOX_POPUP_DURATION,
                                           self.checkbox_popups[state].place_forget)

    def reload_directory(self, select_name=None):
        """(Re-)loads the directory of the current path.
        If select_name is set, the image with the given name is selected as current image."""
        starttime = time()
        p = self.path.get()
        filepaths = [join(p, f) for f in os.listdir(p)]
        print("got filepaths in {0:0.3f}s".format(time() - starttime))
        filepaths.sort()
        print("sorted after {0:0.3f}s".format(time() - starttime))
        self.images = [SelectImage(fpath) for fpath in filepaths if isfile(fpath)]
        self.cur_idx = 0
        if select_name:
            for i, img in enumerate(self.images):
                if img.name == select_name:
                    self.cur_idx = i
                    break
        print("prepared SelectImages after {0:0.3f}s".format(time() - starttime))
        self.showThumbnails.set(1)
        self.prevScrollbar.config(to=len(self.images)-1)

        self.reload_view()

    def reload_view(self):
        """Reloads the current view (including refreshing all images, accounting for new sizes and changed index)"""
        starttime = time()
        # assert (0 <= self.cur_idx < len(self.images))
        for group in self.imageControls:
            group.reload_view()

        if self.showThumbnails.get() == 1:
            self.btn_left.place(anchor="w", x=0, y=self.oldHeight // 2 if self.oldHeight else 0)
            self.btn_right.place(anchor="e", x=self.oldWidth, y=self.oldHeight // 2 if self.oldHeight else 0)
            self.grpPreviews.place(anchor="sw", y=self.oldHeight)
        else:
            self.btn_left.place_forget()
            self.btn_right.place_forget()
            self.grpPreviews.place_forget()
        print("reloaded view in {0:0.3f}s".format(time() - starttime))

    def show_about(self):
        showinfo("About", LICENSE)


def main():
    """Main entry point of the application."""
    start_path = None
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    SelectWindow(start_path)


if __name__ == '__main__':
    main()
