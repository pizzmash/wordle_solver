import tkinter


class WordsBox(tkinter.Frame):
    def __init__(self, master, stream, checker=None, is_available=True):
        super().__init__(master)

        l = tkinter.Label(self, text="候補数：")
        l.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.E)

        self.sv = tkinter.StringVar()

        self.et = tkinter.Label(self, textvariable=self.sv, width=5)
        self.et.grid(row=0, column=1, sticky=tkinter.W)

        self.slb = ScrollListBox(self, stream)
        self.slb.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.wf = WordForm(self, stream, checker=checker, is_available=is_available)
        self.wf.grid(row=2, column=0, columnspan=2, padx=5)

    def set(self, words):
        self.sv.set(str(len(words)))
        self.slb.set(words)
    
    def enable(self):
        self.wf.enable()
    
    def disable(self):
        self.wf.disable()


class ScrollListBox(tkinter.Frame):
    def __init__(self, master, stream):
        super().__init__(master)

        self.lb = tkinter.Listbox(self)
        self.lb.grid(row=0, column=0)

        sb = tkinter.Scrollbar(
            self,
            orient=tkinter.VERTICAL,
            command=self.lb.yview
        )
        self.lb['yscrollcommand'] = sb.set
        sb.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))

        self.lb.bind("<<ListboxSelect>>", self.write_to_stream)

        self.stream = stream

    def set(self, l):
        self.lb.delete(0, tkinter.END)
        [self.lb.insert(tkinter.END, e) for e in l]

    def write_to_stream(self, event):
        try:
            word = self.lb.get(self.lb.curselection())
            self.stream(word)
        except tkinter.TclError:
            pass


class WordForm(tkinter.Frame):
    def __init__(self, master, stream, checker=None, is_available=True):
        self.is_available = is_available

        super().__init__(master)

        self.et = tkinter.Entry(self, width=15)
        self.et.grid(row=0, column=0, padx=5)

        self.bt = tkinter.Button(self, text="Enter")
        self.bt.grid(row=0, column=1, padx=5)

        self.bt.bind("<Button-1>", lambda e: self.is_available and self.write_to_stream(e))

        self.stream = stream
        self.checker = checker

    def set_checker(self, checker):
        self.checker = checker

    def write_to_stream(self, event):
        word = self.et.get()
        if self.checker is None or self.checker(word):
            self.stream(word)
            self.et.configure(bg="#FFFFFF")
        else:
            self.et.configure(bg="#FF8080")

    def enable(self):
        self.is_available = True
    
    def disable(self):
        self.is_available = False