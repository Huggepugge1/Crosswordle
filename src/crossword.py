import square
import clue

class Crossword:
    def __init__(self, title: str, author: str, copyright: str, version: str, width: int, height: int, solution: str, user_state: str, clues: list[str]):
        self.title = title
        self.author = author
        self.copyright = copyright
        self.version = version
        self.width = width
        self.height = height
        self.solution = solution
        
        self.clues = clue.assign_clues(clues, solution, width)
        self.user_state = square.make_squares_from_user_state(user_state)
        


