import tkinter
import threading

from solver.solver import Solver
from solver.word_model import GrayHint, YellowHint, GreenHint, Hints
from widget.app_frame import AppFrame


class App:
    def __init__(self):
        root = tkinter.Tk()
        root.title("Wordle Solver")
        self.frame = AppFrame(
            root, applier=self.apply_hint,
            setupper=self.setup,
            resetter=self.reset, checker=self.check,
            is_available=False)

    def run(self):
        self.frame.mainloop()
    
    def setup(self):
        words_file_path = self.frame.fsf.et.get()
        with open(words_file_path, encoding="utf-8") as f:
            words = f.read().split("\n")
        
        self.solver = Solver(words)
        self.frame.enable()
        self.frame.set_candidates(self.solver.model.words)
        self.frame.set_searcher(self.solver.search)

    def reset(self, event):
        self.frame.set_candidates(self.solver.model.words)
        self.solver.reset()

    def check(self, words):
        return words in self.solver.model.words

    def apply_hint(self, event):
        states = self.frame.cbs.state()
        hint_classes = {0: GrayHint, 1: YellowHint, 2: GreenHint}
        hints = Hints([hint_classes[color](ch, i) for i, (ch, color) in enumerate(states) if ch != ""])
        self.solver.apply(hints)
        self.frame.set_candidates(self.solver.model.candidates_words())
