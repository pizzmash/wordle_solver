import tkinter

from widget.color_buttons import ColorButtons
from widget.search_box import SearchBox
from widget.words_box import WordsBox


class AppFrame(tkinter.Frame):
    def __init__(self, master, applier, searcher, resetter, checker=None):
        super().__init__(master)
        self.grid()

        self.cbs = ColorButtons(self)
        self.cbs.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        bt = tkinter.Button(self, text="Apply", width=43, bg="#80FF80")
        bt.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.E)
        bt.bind("<Button-1>", applier)

        bt = tkinter.Button(self, text="Reset", width=10, bg="#FF8080")
        bt.grid(row=1, column=1, padx=5, pady=5, sticky=tkinter.W)
        bt.bind("<Button-1>", resetter)

        self.sb = SearchBox(self, searcher)
        self.sb.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.plb = WordsBox(self, stream=self.cbs.write, checker=checker)
        self.plb.grid(row=0, column=2, rowspan=3, padx=5, pady=5)

    def set_candidates(self, candidates):
        self.plb.set(candidates)
