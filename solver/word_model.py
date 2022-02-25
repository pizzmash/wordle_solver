class WordModel:
    def __init__(self, words):
        self.words = sorted([word for word in words if len(word) == 5])
        self.candidates = {i for i in range(len(self.words))}
        self.tree = {}
        for i, word in enumerate(self.words):
            for j, ch in enumerate(word):
                if ch not in self.tree:
                    self.tree[ch] = [set() for _ in range(5)]
                self.tree[ch][j] |= {i}

    def frequency(self, ch):
        return sum([len(nodes) for nodes in self.tree[ch]])

    def candidates_words(self):
        return sorted([self.words[candidate] for candidate in self.candidates])

    def reset(self):
        self.candidates = {i for i in range(len(self.words))}


class Hint:
    def __init__(self, character, pos):
        self.ch = character
        self.pos = pos


class GrayHint(Hint):
    def matched_nodes(self, model):
        result = model.candidates
        for nodes in model.tree[self.ch]:
            result = result - nodes
        return result


class YellowHint(Hint):
    def matched_nodes(self, model):
        result = set()
        nodes_list = [model.candidates & nodes for i, nodes in enumerate(model.tree[self.ch]) if i != self.pos]
        for nodes in nodes_list:
            result = result | nodes
        return result


class GreenHint(Hint):
    def matched_nodes(self, model):
        return model.candidates & model.tree[self.ch][self.pos]


class Hints:
    def __init__(self, hints=None):
        self.hints = hints if hints is not None else []

    def add(self, hint):
        self.hints.append(hint)

    def matched_nodes(self, model):
        result = model.candidates
        for hint in self.hints:
            result = result & hint.matched_nodes(model)
        return result

    def __add__(self, other):
        return self.__class__(self.hints + other.hints)
