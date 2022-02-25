import tkinter


class ColorButtons(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.cbs = [ColorButton(self) for _ in range(5)]
        [cb.grid(row=0, column=i) for i, cb in enumerate(self.cbs)]
        [cb.bind("<Button-1>", cb.toggle) for cb in self.cbs]

    def write(self, chs):
        [cb.configure(text=ch) for cb, ch in zip(self.cbs, chs)]

    def state(self):
        return [cb.state() for cb in self.cbs]


class ColorButton(tkinter.Button):
    def __init__(self, master):
        super().__init__(master, height=6, width=10)
        self.color_state = 0
        self.color = ["#C0C0C0", "#FFFF00", "#00FF00"]
        self.set_color()

    def set_color(self):
        self.configure(bg=self.color[self.color_state])

    def toggle(self, event):
        self.color_state = (self.color_state + 1) % 3
        self.set_color()

    def state(self):
        return self.cget("text"), self.color_state
