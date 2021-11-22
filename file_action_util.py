from tkinter.messagebox import showinfo
import shutil


def perform_action(action, objects: list, past_tense: str = "verarbeitet", name_func=str):
    """
    Performs an action on a list, and afterwards displays a summary of possible errors
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
