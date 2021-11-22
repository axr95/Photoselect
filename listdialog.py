import tkinter as tk
from tkinter.simpledialog import Dialog


class ListDialog(Dialog):
    """A simple OK/Cancel dialog that shows a scrollable list of entries."""

    def __init__(self, parent, title: str, message: str, list_content: list):
        """
        :param parent: The tkinter parent of this dialog
        :param title:  The title of this dialog
        :param message: The message that should be displayed above the list box
        :param list_content: A list of strings that should be displayed in the list box
        """
        self.message = message
        self.listContent = list_content
        Dialog.__init__(self, parent, title)

    def body(self, master):
        """Creates dialog body. Overrides method from Dialog"""
        tk.Label(master, text=self.message).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(master, yscrollcommand=scrollbar.set)
        listbox.insert(tk.END, *self.listContent)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=listbox.yview)

        return listbox

    def apply(self):
        """Sets the result of this dialog to true. Overrides method from Dialog, is called when user clicks "OK"."""
        self.result = True
