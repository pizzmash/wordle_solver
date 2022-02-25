import tkinter

from app import App


def main():
    words_file = "./data/pokemon.txt"
    with open(words_file, encoding="utf-8") as f:
        words = f.read().split("\n")

    App(words).run()


if __name__ == "__main__":
    main()
