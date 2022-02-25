from solver.word_model import WordModel
from solver.word_model import GrayHint, YellowHint, GreenHint, Hints


class Comparer:
    def __init__(self, name):
        self.name = name

    def compare(self, name):
        hints = Hints()
        for i, c1 in enumerate(self.name):
            is_found = False
            for j, c2 in enumerate(name):
                if c1 == c2:
                    if i == j:
                        hints.add(GreenHint(c1, i))
                        is_found = True
                        break
                    else:
                        hints.add(YellowHint(c1, i))
                        is_found = True
            if not is_found:
                hints.add(GrayHint(c1, i))
        return hints


class Solver:
    def __init__(self, words):
        self.model = WordModel(words)
        self.hints = Hints()

    def character_score_dict(self):
        score = {ch: self.model.frequency(ch) for ch in self.model.tree.keys()}
        for hint in self.hints.hints:
            score[hint.ch] = 0
        return score

    def search(self, progress):
        csd = self.character_score_dict()
        score = lambda word: sum([csd[ch] for ch in word])
        sorted_words = sorted(self.model.words, key=lambda word: -1 * score(word))
        sorted_candidates = sorted(self.model.candidates_words(), key=score)

        result = None
        min_num = len(self.model.candidates) + 1

        for w1 in progress(sorted_words):
            comparer = Comparer(w1)
            max_num = -1
            for w2 in sorted_candidates:
                hints = self.hints + comparer.compare(w2)
                candidates = hints.matched_nodes(self.model)
                num = len(candidates)
                if num > max_num:
                    max_num = num
                    if max_num >= min_num:
                        break
            else:
                if max_num != 0:
                    result = w1
                    min_num = max_num

        return result, min_num

    def apply(self, hints):
        self.model.candidates = hints.matched_nodes(self.model)
        return len(self.model.candidates)

    def reset(self):
        self.model.reset()
        self.hints = Hints()
