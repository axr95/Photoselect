import tkinter as tk
from tkinter.simpledialog import Dialog


class ListDialog(Dialog):
    def __init__(self, parent, title, message, list_content):
        self.message = message
        self.listContent = list_content
        Dialog.__init__(self, parent, title)

    def body(self, master):

        tk.Label(master, text=self.message).pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(master, yscrollcommand=scrollbar.set)
        listbox.insert(tk.END, *self.listContent)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=listbox.yview)

        return listbox

    def apply(self):
        self.result = True
