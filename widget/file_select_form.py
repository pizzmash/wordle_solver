import tkinter
from tkinter import filedialog


class FileSelectForm(tkinter.Frame):
    def __init__(self, master, setupper):
        self.setup = setupper

        super().__init__(master)

        l = tkinter.Label(self, text="Words File：")
        l.grid(row=0, column=0, padx=5, sticky=tkinter.E)

        self.et = tkinter.Entry(self, width=82, state="readonly")
        self.et.grid(row=0, column=1, padx=5)

        self.bt = tkinter.Button(self, text="Browse")
        self.bt.grid(row=0, column=2, padx=5, sticky=tkinter.W)
        self.bt.bind("<Button-1>", self.browse)
    
    def browse(self, event):
        idir = "./data"
        filetype=[("Text", "*.txt")]
        file_path = tkinter.filedialog.askopenfilename(filetype=filetype, initialdir=idir)
        if len(file_path) > 0:
            self.et.configure(state="normal")
            self.et.delete(0, tkinter.END)
            self.et.insert(tkinter.END, file_path)
            self.et.configure(state="readonly")
            self.setup()

