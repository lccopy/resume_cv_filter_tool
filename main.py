import PyPDF2
import shutil
import os
from PyPDF2.errors import PdfReadError
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
import sv_ttk


def validation():
    """'OK' button that launches the main algo function"""
    global word
    word = my_word.get()
    main()


def openfile(entry_box):
    """function working with tkinter to choose directory"""
    global directory
    directory = filedialog.askdirectory()
    entry_box.delete(0, tk.END)
    entry_box.insert(tk.END, directory)


def app():
    """tk init and grids"""
    # tk init
    root = tk.Tk()
    root.title("Resume/CV filter tool")
    width = 600
    height = 500
    root.geometry(f"{width}x{height}")
    frame = ttk.Frame(root)
    frame.grid()
    word_label = ttk.Label(frame, text="Enter keyword")
    global my_word
    my_word = tk.StringVar(frame)
    word_entry = ttk.Entry(frame, width=8, textvariable=my_word)
    word_entry_button = ttk.Button(frame, command=validation, text="OK")
    dir_selector = ttk.Frame(frame)
    dir_entry = ttk.Entry(frame)
    ttk.Button(frame, text="Quit", command=root.destroy).grid(column=0,
                                                              row=0)  # quit
    select_button1 = ttk.Button(dir_selector, text="Browse directory",
                                command=partial(openfile, dir_entry))

    dir_selector.grid(row=2, column=2)
    dir_entry.grid(row=2, column=1)
    word_entry.grid(row=1, column=1)
    select_button1.grid(row=2, column=3)
    word_label.grid(row=1, column=2)
    word_entry_button.grid(row=3, column=1)
    sv_ttk.set_theme("dark")

    root.mainloop()


def main():
    """Create a directory and fill it with the CV/resumes that contains the
    keyword"""
    print(directory)
    dir = directory + "/"
    list_file = os.listdir(dir)
    for file in list_file:
        full_file_name = f"{dir}{file}"
        try:
            reader = PyPDF2.PdfFileReader(f"{full_file_name}")
        except (PdfReadError, IsADirectoryError):
            pass
        count = 0
        for i in range(reader.getNumPages()):
            page = reader.getPage(i)
            print("Page N°" + str(1 + reader.getPageNumber(page)))
            page_content = page.extractText()
            page_content = page_content.lower()
            if word in page_content:
                count = + 1

            if count > 0:
                print("cv ok")
                try:
                    os.mkdir(f"{dir}/cv_is_valid_{word}/")
                except FileExistsError:
                    pass
                shutil.copy(full_file_name, f"{directory}/cv_is_valid_"
                                            f"{word}/{file}")

            else:
                print(f"{word} not found in CV")


if __name__ == "__main__":
    app()

