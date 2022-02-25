import threading
import tkinter
from tkinter import ttk


class SearchBox(tkinter.Frame):
    def __init__(self, master, searcher=None, is_available=True):
        self.is_available = is_available

        super().__init__(master)

        self.bt = tkinter.Button(self, text="Search")
        self.bt.grid(row=0, column=0, rowspan=2, padx=5)
        self.bt.bind("<Button-1>", lambda e: self.is_available and self.search(e))

        self.pb = ttk.Progressbar(self, length=200, mode="determinate")
        self.pb.grid(row=0, column=1, rowspan=2, padx=5)

        self.sv0 = tkinter.StringVar()
        l = tkinter.Label(self, textvariable=self.sv0, width=10)
        l.grid(row=0, column=2, rowspan=2, padx=5)

        l = tkinter.Label(self, text="最善手：")
        l.grid(row=0, column=3, sticky=tkinter.E, padx=5)

        self.sv1 = tkinter.StringVar()
        l = tkinter.Label(self, textvariable=self.sv1, width=6)
        l.grid(row=0, column=4, sticky=tkinter.W)

        l = tkinter.Label(self, text="最悪候補数：")
        l.grid(row=1, column=3, sticky=tkinter.E, padx=5)

        self.sv2 = tkinter.StringVar()
        l = tkinter.Label(self, textvariable=self.sv2, width=6)
        l.grid(row=1, column=4, sticky=tkinter.W)

        self.searcher = searcher
        self.lock = threading.Lock()

    def set_searcher(self, searcher):
        self.searcher = searcher

    def search(self, event):
        if self.searcher is None or self.lock.locked():
            return
        else:
            def f():
                self.lock.acquire()
                result, num = self.searcher(self.progress)
                self.sv1.set(result)
                self.sv2.set(str(num))
                self.lock.release()
            thread = threading.Thread(target=f)
            thread.setDaemon(True)
            thread.start()

            return

    def progress(self, iter):
        self.pb.configure(maximum=len(iter), value=0)
        self.pb.configure(value=0)
        self.sv0.set("  0 / " + "{}".format(len(iter)).rjust(3))
        for i, elem in enumerate(iter):
            yield elem
            self.pb.configure(value=i)
            self.sv0.set("{}".format(i+1).rjust(3) + " / " + "{}".format(len(iter)).rjust(3))
    
    def enable(self):
        self.is_available = True

    def disable(self):
        self.is_available = False
