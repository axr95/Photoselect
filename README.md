# Photoselect
Photo-selection application with support for mass-renaming image files

## How to use
There are two main functionalities here:

The main program in main.py opens a window where all pictures in the folder can be scrolled through, selected and acted on.
- Use your arrow keys, click on a preview image, or use the scrollbar to scroll through the images
- Use your spacebar or click on the checkbox left to the filename, to select or unselect an image.
- Right-clicking on the main image in the background shows a context menu with actions to:
  - Select another directory
  - Rename all files (see below)
  - Move, Copy, or Delete all selected files
  - Move, Copy, or Delete the current file
  - Hide or unhide the preview bar (which overlays the image by default)

All file operations will ask for confirmation together with a list of all affected files.

The rename program in rename.py acts on all image files in a directory, to which Exif Tags could be found.
- First, enter your preferred filename format. You may (and should) include Exif Tag names like so: `<DateTimeOriginal>_<OriginalName><Ext>`. OriginalName and Ext are special entries that are not real Exif Tags, but refer to the original Filename and extension.
- Then, click on "Vorschau" and preview the results. This, at the same time, is validation - if an error occurs (eg. a used Exif Tag was not found in at least one file), the corresponding new filename is shown in red. Also, if there are conflicts (multiple files would be mapped to the same or to an existing filename), the second name is shown in orange. In these cases, you have to enter another filename format.
- Finally, if there are no errors, you can click on OK to perform the rename operation.

## Localization
Currently the program texts are in german; maybe I will add an english version but feel free to contribute.

## License
Photoselect, an application to review images in a folder, including a mass-renaming functionality

    Copyright (C) 2021  Alexander Simunics

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
 
The author of the file "icon.ico" is Xiran Dong, (C) 2020.

## Dependencies
This project uses Pillow, licensed as follows:

The Python Imaging Library (PIL) is

    Copyright © 1997-2011 by Secret Labs AB
    Copyright © 1995-2011 by Fredrik Lundh

Pillow is the friendly PIL fork. It is

    Copyright © 2010-2021 by Alex Clark and contributors

Like PIL, Pillow is licensed under the open source HPND License:

By obtaining, using, and/or copying this software and/or its associated
documentation, you agree that you have read, understood, and will comply
with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and its
associated documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appears in all copies, and that
both that copyright notice and this permission notice appear in supporting
documentation, and that the name of Secret Labs AB or the author not be
used in advertising or publicity pertaining to distribution of the software
without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
