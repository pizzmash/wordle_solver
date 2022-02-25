import tkinter
import threading

from solver.solver import Solver
from solver.word_model import GrayHint, YellowHint, GreenHint, Hints
from widget.app_frame import AppFrame


class App:
    def __init__(self, all_words):
        self.solver = Solver(all_words)
        words = self.solver.model.words

        root = tkinter.Tk()
        root.title("Wordle Solver")
        self.frame = AppFrame(
            root, applier=self.apply_hint,
            searcher=self.solver.search,
            resetter=self.reset, checker=self.check)

        self.frame.set_candidates(words)

    def run(self):
        self.frame.mainloop()

    def reset(self, event):
        self.frame.set_candidates(self.solver.model.words)
        self.solver.reset()

    def check(self, words):
        return words in self.solver.model.words

    def apply_hint(self, event):
        states = self.frame.cbs.state()
        hint_classes = {0: GrayHint, 1: YellowHint, 2: GreenHint}
        hints = Hints([hint_classes[color](ch, i) for i, (ch, color) in enumerate(states)])
        self.solver.apply(hints)
        self.frame.set_candidates(self.solver.model.candidates_words())
