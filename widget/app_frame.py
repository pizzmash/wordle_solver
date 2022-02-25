import tkinter

from widget.file_select_form import FileSelectForm
from widget.color_buttons import ColorButtons
from widget.search_box import SearchBox
from widget.words_box import WordsBox


class AppFrame(tkinter.Frame):
    def __init__(self, master, setupper, applier, resetter, searcher=None, checker=None, is_available=True):
        self.is_available=is_available

        super().__init__(master)
        self.grid()

        self.fsf = FileSelectForm(self, setupper=setupper)
        self.fsf.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.cbs = ColorButtons(self)
        self.cbs.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        bt = tkinter.Button(self, text="Apply", width=43, bg="#80FF80")
        bt.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.E)
        bt.bind("<Button-1>", lambda e: self.is_available and applier(e))

        bt = tkinter.Button(self, text="Reset", width=10, bg="#FF8080")
        bt.grid(row=1, column=1, padx=5, pady=5, sticky=tkinter.W)
        bt.bind("<Button-1>", lambda e: self.is_available and resetter(e))

        self.sb = SearchBox(self, searcher, is_available=is_available)
        self.sb.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.wb = WordsBox(self, stream=self.cbs.write, checker=checker, is_available=is_available)
        self.wb.grid(row=0, column=2, rowspan=3, padx=5, pady=5)

    def set_candidates(self, candidates):
        self.wb.set(candidates)
    
    def set_searcher(self, searcher):
        self.sb.set_searcher(searcher)
    
    def enable(self):
        self.is_available = True
        self.sb.enable()
        self.wb.enable()
    
    def disable(self):
        self.is_available = False
        self.sb.disable()
        self.wb.disable()
