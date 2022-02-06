from tqdm import tqdm


class Hint:
    def __init__(self, character, positions):
        self.ch = character
        self.poss = positions

    def is_matched(self, name):
        flag = False
        for i, ch in enumerate(name):
            if ch == self.ch:
                flag = True
                if i not in self.poss:
                    return False
        if len(self.poss) > 0 and not flag:
            return False
        else:
            return True


class Hints:
    def __init__(self, hints=None):
        self.hints = hints if hints is not None else []

    def add(self, hint):
        self.hints.append(hint)

    def is_matched(self, name):
        for hint in self.hints:
            if not hint.is_matched(name):
                return False
        return True

    def __add__(self, other):
        return self.__class__(self.hints + other.hints)


class Comparer:
    def __init__(self, name):
        self.name = name

    def compare(self, name):
        hints = Hints()
        for i, c1 in enumerate(name):
            yellow_pos = []
            for j, c2 in enumerate(self.name):
                if c1 == c2:
                    if i == j:
                        # Green Hint
                        hints.add(Hint(c1, [i]))
                        break
                    else:
                        yellow_pos.append(i)
            else:
                if len(yellow_pos) > 0:
                    # Yellow Hint
                    h = Hint(c1, [j for j in range(5) if j not in yellow_pos])
                    hints.add(h)
                else:
                    # Gray Hint
                    hints.add(Hint(c1, []))
        return hints


class Solver:
    def __init__(self, pokemons):
        self.pokemons = [p for p in pokemons if len(p) == 5]
        self.candidates = [p for p in pokemons if len(p) == 5]
        self.freq_score = {}
        for p in pokemons:
            for c in p:
                if c in self.freq_score:
                    self.freq_score[c] += 1
                else:
                    self.freq_score[c] = 1
        self.hints = Hints()

    def search(self):
        k = lambda p: sum([self.freq_score[c] for c in p])
        sorted_pokemons = sorted(self.pokemons, key=lambda p: -1 * k(p))
        sorted_candidates = sorted(self.candidates, key=k)

        result = None
        min_num = len(self.candidates) + 1

        for p1 in tqdm(sorted_pokemons):
            comparer = Comparer(p1)
            max_num = -1
            for p2 in sorted_candidates:
                hints = self.hints + comparer.compare(p2)
                candidates = [p for p in self.candidates if hints.is_matched(p)]
                num = len(candidates)
                if num > max_num:
                    max_candidates = candidates
                    max_num = num
                    if max_num > min_num:
                        break
            else:
                if max_num != 0:
                    result = p1
                    min_candidates = max_candidates
                    min_num = max_num

        return result, min_num

    def apply(self, hints):
        self.hints = self.hints + hints
        self.candidates = [p for p in self.candidates if self.hints.is_matched(p)]
        return len(self.candidates)
