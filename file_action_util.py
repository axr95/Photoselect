import tkinter as tk
from tkinter.simpledialog import Dialog
from tkinter.messagebox import showinfo


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

        listbox = tk.Listbox(master, yscrollcommand=scrollbar.set, width=50)
        listbox.insert(tk.END, *self.listContent)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=listbox.yview)

        return listbox

    def apply(self):
        """Sets the result of this dialog to true. Overrides method from Dialog, is called when user clicks "OK"."""
        self.result = True


def perform_action(action, objects, past_tense: str = "verarbeitet", name_func=str):
    """
    Performs an action on each entry in a list, and afterwards displays a summary of occurred errors
    :param action: A function that takes the objects as single input
    :param objects: A list of objects on which the action should be applied
    :param past_tense: The past tense of the action to be shown in the dialog (currently german)
    :param name_func: A function to map the object that failed to the name that should be mentioned in the failed list
    """
    results = []
    for o in objects:
        try:
            action(o)
        except Exception as e:
            results.append("[ERROR] {}: {}".format(name_func(o), str(e)))

    if results:
        ok_count = len(objects) - len(results)
        showinfo("Vorgang abgeschlossen",
                 ("{0} von {1} Dateien wurden erfolgreich {2}." +
                  "\nEs gab Probleme bei den folgenden Dateien:\n\n{3}")
                 .format(ok_count, len(objects), past_tense, "\n".join(results)))
    else:
        showinfo("Vorgang abgeschlossen", "Alle {0} Dateien wurden erfolgreich {1}.".format(len(objects), past_tense))
