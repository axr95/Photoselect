import tkinter as tk
from os.path import dirname, basename, join
import sys

import PIL
from PIL import ImageTk, Image, ImageOps


class ImageControlsGroup(object):
    """A class that manages the display of an SelectImage, including the selection box, name, and image."""
    SIZES = {"MAIN": (600, 600), "SIDE": (400, 400), "THUMBNAIL": (128, 128)}
    _NOVAR = None

    def __init__(self, base, image_label, name_checkbox, index_offset, size_name, is_thumbnail=False):
        """

        :param base: The SelectWindow instance this group is part of
        :param image_label: The label where the image should be shown on
        :param name_checkbox: The checkbox element where the name and the selected state are shown
        :param index_offset: The offset with respect to the currently centered image of this group
        :param size_name: One of "MAIN", "SIDE" or "THUMBNAIL", standing for the size of the image
        :param is_thumbnail: Indicator if this is a thumbnail. If True, loading the image can be skipped if thumbnails
                             are not shown
        """
        if not SelectImage.PLACEHOLDER_IMAGE:
            SelectImage.PLACEHOLDER_IMAGE = load_static_icon("placeholder.gif")

        if not ImageControlsGroup._NOVAR:
            ImageControlsGroup._NOVAR = tk.BooleanVar()

        self.base = base
        self.lblImage = image_label
        self.chkName = name_checkbox
        self.offset = index_offset
        self.sizeName = size_name
        self.isThumbnail = is_thumbnail

        self._photoImage = None
        self._image = None



    def reload_view(self):
        """Refreshes the appearance of the current image, accounting for new sizes, changed indices, etc."""
        idx = self.base.cur_idx + self.offset
        size = ImageControlsGroup.SIZES[self.sizeName]
        if 0 <= idx < len(self.base.images):
            if self._image != self.base.images[idx]:
                self._image = self.base.images[idx]
                self.chkName.configure(text=self._image.name, wraplength=size[0],
                                       variable=self._image.selected, state=tk.ACTIVE)

            if self.isThumbnail:
                if self.base.showThumbnails.get() == 1:
                    self._photoImage = self.base.images[idx].get_thumbnail()
            else:
                self._photoImage = self.base.images[idx].get_image(size=size)
        else:
            self.chkName.configure(variable=ImageControlsGroup._NOVAR, state=tk.DISABLED)
            # self.chkName.deselect()

            self._photoImage = SelectImage.PLACEHOLDER_IMAGE
            self._image = None
            if idx == -1:
                self.chkName.configure(text="[Anfang]")
            elif idx == len(self.base.images):
                self.chkName.configure(text="[Ende]")
            else:
                self.chkName.configure(text="")

        self.lblImage.configure(image=self._photoImage, width=size[0], height=size[1])


class SelectImage(object):
    """Class to represent a selectable image in a directory, with helper functions to efficiently load them."""
    PLACEHOLDER_IMAGE = None  # can not create PhotoImage at this point

    THUMBNAIL_SIZE = 64, 64

    def __init__(self, path):
        """
        :param path: The path of the image this instance should represent.
        """
        if not SelectImage.PLACEHOLDER_IMAGE:
            SelectImage.PLACEHOLDER_IMAGE = load_static_icon("placeholder.gif")

        self.name = basename(path)
        self.path = path
        self.thumbnail = None
        self.selected = tk.BooleanVar()

        self.prepared = None
        self.preparedSize = None

    def get_thumbnail(self) -> ImageTk.PhotoImage:
        """Loads and returns a thumbnail representation of this image, as PhotoImage"""
        if self.thumbnail:
            return self.thumbnail

        self.thumbnail = self.get_image(SelectImage.THUMBNAIL_SIZE)
        # print("thumbnail created for", self.name)
        return self.thumbnail

    def get_image(self, size=None) -> ImageTk.PhotoImage:
        """Loads the image as PhotoImage, and resizes it if the size argument is given (as a width,height tuple)"""
        if size and self.prepared and self.preparedSize == size:
            return self.prepared
        try:
            with Image.open(self.path) as im:
                if size:
                    # im.draft('RGB', size)
                    im.thumbnail(size)
                res = ImageTk.PhotoImage(ImageOps.exif_transpose(im))
                # print("image_get for", self.name)
                self.prepared = res
                self.preparedSize = size
        except PIL.UnidentifiedImageError:
            res = SelectImage.PLACEHOLDER_IMAGE

        return res

    def __str__(self):
        return self.name


def load_static_icon(filename: str, size:tuple=None) -> ImageTk.PhotoImage:
    """
    Loads a static icon from the icons folder of the application. To be used for GUI-icons like placeholder-icons etc.
    :param filename: The filename of the image file that is located in the icons directory
    :param size: A tuple of ints describing the desired image size in pixels. Defaults to None: no resize
    :return: A PhotoImage that was loaded.
    """
    with Image.open(join(dirname(sys.modules['__main__'].__file__), "icons", filename)) as im:
        if size:
            im.thumbnail(size)
        return ImageTk.PhotoImage(im)
