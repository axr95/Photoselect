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
First, enter your preferred filename format. You may (and should) include Exif Tag names like so: "<DateTimeOriginal>_<OriginalName><Ext>". OriginalName and Ext are special entries that are not real Exif Tags, but refer to the original Filename and extension.
Then, click on "Vorschau" and preview the results. This, at the same time, is validation - if an error occurs (eg. a used Exif Tag was not found in at least one file), the corresponding new filename is shown in red. Also, if there are conflicts (multiple files would be mapped to the same or to an existing filename), the second name is shown in orange. In these cases, you have to enter another filename format.
Finally, if there are no errors, you can click on OK to perform the rename operation.

## Localization
Currently the program texts are in german; maybe I will add an english version but feel free to contribute.
