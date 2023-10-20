import crossword
import crossword_reader
import GUI

if __name__ == "__main__":
    path = input("Path to your crossword: ")
    GUI.main(crossword_reader(path))
